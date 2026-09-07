import { createHash } from "node:crypto";
import { env } from "cloudflare:workers";
import { cookies } from "next/headers";
import { requireDraftDb } from "@/db";

// Trusted-household identity: the family taps a name, no PINs or passwords.
// The session cookie only records who is picking so turn order holds up.
export const DRAFT_SESSION_COOKIE = "espinosa_ffl_draft_session";

export type DraftActor = { id: string; displayName: string; isCommissioner: boolean };

export function sha256(value: string): string {
  return createHash("sha256").update(value).digest("hex");
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
