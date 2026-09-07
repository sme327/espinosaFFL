import type { D1DatabaseLike } from "@/db";
import { achievements, type HistoricalAchievement } from "@/lib/achievements";

export type WallAchievement = HistoricalAchievement & { notes: string[] };

type AwardRow = { achievementId: string; managerId: string; season: number; note: string | null };

/**
 * Live commissioner awards from D1, grouped per manager and merged onto the
 * badge catalog. Returns an empty map when the database is unavailable —
 * the import is dynamic because tests render the worker under plain Node,
 * where the cloudflare: scheme (and the DB binding) does not exist.
 */
export async function liveAwardsByManager(): Promise<Map<string, WallAchievement[]>> {
  try {
    const { env } = await import("cloudflare:workers");
    const db = (env as { DB?: D1DatabaseLike }).DB;
    if (!db) return new Map();
    const rows = await db.prepare(
      "SELECT achievement_id AS achievementId, manager_id AS managerId, season, note FROM achievement_awards WHERE revoked_at IS NULL ORDER BY awarded_at",
    ).all<AwardRow>();
    const byManager = new Map<string, WallAchievement[]>();
    for (const row of rows.results) {
      const definition = achievements.find((item) => item.id === row.achievementId);
      if (!definition) continue;
      const wall = byManager.get(row.managerId) ?? [];
      let entry = wall.find((item) => item.id === definition.id);
      if (!entry) {
        entry = { ...definition, count: 0, seasons: [], notes: [] };
        wall.push(entry);
      }
      entry.count += 1;
      if (!entry.seasons.includes(row.season)) entry.seasons.push(row.season);
      if (row.note) entry.notes.push(row.note);
      byManager.set(row.managerId, wall);
    }
    return byManager;
  } catch {
    return new Map();
  }
}

/** Merge computed history with live awards; same badge combines counts and seasons. */
export function mergeWallAchievements(historical: HistoricalAchievement[], live: WallAchievement[]): WallAchievement[] {
  const merged: WallAchievement[] = historical.map((item) => ({ ...item, notes: [] }));
  for (const award of live) {
    const existing = merged.find((item) => item.id === award.id);
    if (existing) {
      existing.count += award.count;
      existing.seasons = [...new Set([...existing.seasons, ...award.seasons])].sort();
      existing.notes.push(...award.notes);
    } else {
      merged.push(award);
    }
  }
  return merged;
}
