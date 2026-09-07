import { randomBytes, randomUUID } from "node:crypto";
import { env } from "cloudflare:workers";
import { cookies } from "next/headers";
import { NextResponse } from "next/server";
import { requireDraftDb } from "@/db";
import { DRAFT_SESSION_COOKIE, currentDraftActor, sha256 } from "@/lib/server/draft-auth";

const SESSION_DAYS = 30;

export async function GET() {
  const actor = await currentDraftActor();
  return NextResponse.json({ actor });
}

export async function POST(request: Request) {
  const body = await request.json().catch(() => null) as { managerId?: string } | null;
  if (!body || typeof body.managerId !== "string" || body.managerId.length > 40) {
    return NextResponse.json({ error: "Tap your name first." }, { status: 400 });
  }

  const db = requireDraftDb(env);
  const manager = await db.prepare(
    "SELECT id, display_name AS displayName, is_commissioner AS isCommissioner FROM draft_managers WHERE id = ? AND active = 1",
  ).bind(body.managerId).first<{ id: string; displayName: string; isCommissioner: number }>();
  if (!manager) return NextResponse.json({ error: "That name is not part of the family draft." }, { status: 404 });

  const token = randomBytes(32).toString("base64url");
  const expires = new Date(Date.now() + SESSION_DAYS * 24 * 60 * 60 * 1000);
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
