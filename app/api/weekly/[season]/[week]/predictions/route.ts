import { randomUUID } from "node:crypto";
import { env } from "cloudflare:workers";
import { NextResponse } from "next/server";
import { requireDraftDb } from "@/db";
import { CLUBHOUSE_FAMILY } from "@/lib/league";

type RouteContext = { params: Promise<{ season: string; week: string }> };
const CONFIDENCE = new Set(["unsure", "confident", "super"]);

function numbers(seasonValue: string, weekValue: string): [number, number] | null {
  const season = Number(seasonValue);
  const week = Number(weekValue);
  return Number.isInteger(season) && Number.isInteger(week) && season >= 2023 && week >= 1 && week <= 18 ? [season, week] : null;
}

export async function GET(_request: Request, context: RouteContext) {
  const params = await context.params;
  const parsed = numbers(params.season, params.week);
  if (!parsed) return NextResponse.json({ error: "Invalid season or week." }, { status: 400 });
  const [season, week] = parsed;
  const db = requireDraftDb(env);
  const [matchups, predictions] = await Promise.all([
    db.prepare("SELECT id, manager_a_id AS managerAId, manager_b_id AS managerBId, locks_at AS locksAt, featured FROM weekly_matchups WHERE season = ? AND week = ? ORDER BY featured DESC, id").bind(season, week).all(),
    db.prepare("SELECT p.matchup_id AS matchupId, p.participant_manager_id AS participantManagerId, p.predicted_manager_id AS predictedManagerId, p.confidence FROM weekly_predictions p JOIN weekly_matchups m ON m.id = p.matchup_id WHERE m.season = ? AND m.week = ?").bind(season, week).all(),
  ]);
  const response = NextResponse.json({ season, week, matchups: matchups.results, predictions: predictions.results });
  response.headers.set("Cache-Control", "no-store");
  return response;
}

export async function POST(request: Request, context: RouteContext) {
  const params = await context.params;
  const parsed = numbers(params.season, params.week);
  if (!parsed) return NextResponse.json({ error: "Invalid season or week." }, { status: 400 });
  const [season, week] = parsed;
  const body = await request.json().catch(() => null) as { matchupId?: string; participantManagerId?: string; predictedManagerId?: string; confidence?: string } | null;
  if (!body?.matchupId || !body.participantManagerId || !body.predictedManagerId || !body.confidence) return NextResponse.json({ error: "Choose a family member, winner, and confidence face." }, { status: 400 });
  if (!CLUBHOUSE_FAMILY.some((manager) => manager.id === body.participantManagerId) || !CONFIDENCE.has(body.confidence)) return NextResponse.json({ error: "That family choice is not available." }, { status: 400 });

  const db = requireDraftDb(env);
  const matchup = await db.prepare("SELECT manager_a_id AS managerAId, manager_b_id AS managerBId, locks_at AS locksAt FROM weekly_matchups WHERE id = ? AND season = ? AND week = ?").bind(body.matchupId, season, week).first<{ managerAId: string; managerBId: string; locksAt: string }>();
  if (!matchup) return NextResponse.json({ error: "Matchup not found." }, { status: 404 });
  if (![matchup.managerAId, matchup.managerBId].includes(body.predictedManagerId)) return NextResponse.json({ error: "Pick one of the two managers in this matchup." }, { status: 400 });
  if (Date.now() >= Date.parse(matchup.locksAt)) return NextResponse.json({ error: "This matchup has already started." }, { status: 409 });

  await db.prepare(`INSERT INTO weekly_predictions (id, matchup_id, participant_manager_id, predicted_manager_id, confidence)
    VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(matchup_id, participant_manager_id) DO UPDATE SET predicted_manager_id = excluded.predicted_manager_id, confidence = excluded.confidence, updated_at = CURRENT_TIMESTAMP`)
    .bind(randomUUID(), body.matchupId, body.participantManagerId, body.predictedManagerId, body.confidence).run();
  return NextResponse.json({ saved: true });
}
