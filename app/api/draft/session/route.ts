import { randomBytes, randomUUID } from "node:crypto";
import { env } from "cloudflare:workers";
import { cookies } from "next/headers";
import { NextResponse } from "next/server";
import { requireDraftDb } from "@/db";
import { DRAFT_PIN_PATTERN, DRAFT_SESSION_COOKIE, sha256, verifyDraftPin } from "@/lib/server/draft-auth";

const ATTEMPT_WINDOW_MS = 15 * 60 * 1000;
const MAX_FAILED_ATTEMPTS = 6;

export async function POST(request: Request) {
  const body = await request.json().catch(() => null) as { managerId?: string; pin?: string } | null;
  if (!body || typeof body.managerId !== "string" || body.managerId.length > 40 || typeof body.pin !== "string" || !DRAFT_PIN_PATTERN.test(body.pin)) {
    return NextResponse.json({ error: "Choose a manager and enter a four-digit PIN." }, { status: 400 });
  }

  const db = requireDraftDb(env);
  const address = request.headers.get("cf-connecting-ip") || request.headers.get("x-forwarded-for")?.split(",")[0]?.trim() || "local";
  const rateKey = sha256(`${body.managerId}:${address}`);
  const now = new Date();
  const limit = await db.prepare("SELECT failed_count AS failedCount, window_started_at AS windowStartedAt, blocked_until AS blockedUntil FROM draft_login_limits WHERE key = ?")
    .bind(rateKey).first<{ failedCount: number; windowStartedAt: string; blockedUntil: string | null }>();
  if (limit?.blockedUntil && new Date(limit.blockedUntil) > now) {
    return NextResponse.json({ error: "Too many unsuccessful attempts. Wait 15 minutes and try again." }, { status: 429 });
  }

  const manager = await db.prepare(
    "SELECT id, display_name AS displayName, pin_hash AS pinHash, is_commissioner AS isCommissioner FROM draft_managers WHERE id = ? AND active = 1",
  ).bind(body.managerId).first<{ id: string; displayName: string; pinHash: string; isCommissioner: number }>();

  if (!manager || !verifyDraftPin(manager.id, body.pin, manager.pinHash)) {
    const inWindow = limit && now.getTime() - new Date(limit.windowStartedAt).getTime() < ATTEMPT_WINDOW_MS;
    const failedCount = inWindow ? limit.failedCount + 1 : 1;
    const windowStartedAt = inWindow ? limit.windowStartedAt : now.toISOString();
    const blockedUntil = failedCount >= MAX_FAILED_ATTEMPTS ? new Date(now.getTime() + ATTEMPT_WINDOW_MS).toISOString() : null;
    await db.prepare(
      `INSERT INTO draft_login_limits (key, failed_count, window_started_at, blocked_until, updated_at) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
       ON CONFLICT(key) DO UPDATE SET failed_count = excluded.failed_count, window_started_at = excluded.window_started_at, blocked_until = excluded.blocked_until, updated_at = CURRENT_TIMESTAMP`,
    ).bind(rateKey, failedCount, windowStartedAt, blockedUntil).run();
    return NextResponse.json({ error: "That manager and PIN were not recognized." }, { status: 401 });
  }

  await db.prepare("DELETE FROM draft_login_limits WHERE key = ?").bind(rateKey).run();
  const token = randomBytes(32).toString("base64url");
  const expires = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000);
  await db.prepare("INSERT INTO draft_sessions (id, manager_id, token_hash, expires_at) VALUES (?, ?, ?, ?)")
    .bind(randomUUID(), manager.id, sha256(token), expires.toISOString()).run();

  const response = NextResponse.json({ manager: { id: manager.id, displayName: manager.displayName, isCommissioner: Boolean(manager.isCommissioner) } });
  response.cookies.set(DRAFT_SESSION_COOKIE, token, { httpOnly: true, secure: new URL(request.url).protocol === "https:", sameSite: "lax", path: "/", expires });
  return response;
}

export async function DELETE(request: Request) {
  const db = requireDraftDb(env);
  const token = (await cookies()).get(DRAFT_SESSION_COOKIE)?.value;
  if (token) await db.prepare("UPDATE draft_sessions SET revoked_at = CURRENT_TIMESTAMP WHERE token_hash = ? AND revoked_at IS NULL").bind(sha256(token)).run();
  const response = NextResponse.json({ ok: true });
  response.cookies.set(DRAFT_SESSION_COOKIE, "", { httpOnly: true, secure: new URL(request.url).protocol === "https:", sameSite: "lax", path: "/", maxAge: 0 });
  return response;
}
