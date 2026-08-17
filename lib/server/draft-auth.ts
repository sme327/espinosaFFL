import { createHash, timingSafeEqual } from "node:crypto";
import { env } from "cloudflare:workers";
import { cookies } from "next/headers";
import { requireDraftDb } from "@/db";

export const DRAFT_SESSION_COOKIE = "espinosa_ffl_draft_session";
export const DRAFT_PIN_PATTERN = /^\d{4}$/;

export type DraftActor = { id: string; displayName: string; isCommissioner: boolean };

export function sha256(value: string): string {
  return createHash("sha256").update(value).digest("hex");
}

export function draftPinDigest(managerId: string, pin: string): string {
  return `sha256:${sha256(`${managerId}:${pin}`)}`;
}

export function verifyDraftPin(managerId: string, pin: string, storedDigest: string): boolean {
  const candidate = Buffer.from(draftPinDigest(managerId, pin));
  const expected = Buffer.from(storedDigest);
  return candidate.length === expected.length && timingSafeEqual(candidate, expected);
}

export async function currentDraftActor(): Promise<DraftActor | null> {
  const token = (await cookies()).get(DRAFT_SESSION_COOKIE)?.value;
  if (!token) return null;
  const db = requireDraftDb(env);
  const row = await db.prepare(
    `SELECT m.id, m.display_name AS displayName, m.is_commissioner AS isCommissioner
       FROM draft_sessions s JOIN draft_managers m ON m.id = s.manager_id
      WHERE s.token_hash = ? AND s.revoked_at IS NULL AND s.expires_at > CURRENT_TIMESTAMP AND m.active = 1`,
  ).bind(sha256(token)).first<{ id: string; displayName: string; isCommissioner: number }>();
  return row ? { id: row.id, displayName: row.displayName, isCommissioner: Boolean(row.isCommissioner) } : null;
}
