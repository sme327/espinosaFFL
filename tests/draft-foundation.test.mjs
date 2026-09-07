import assert from "node:assert/strict";
import fs from "node:fs";
import test from "node:test";

const config = JSON.parse(fs.readFileSync(new URL("../data/config/draft-seasons.json", import.meta.url), "utf8"));
const migration = fs.readFileSync(new URL("../drizzle/0000_family_draft.sql", import.meta.url), "utf8");
const playerPool = JSON.parse(fs.readFileSync(new URL("../data/draft/players-2026.json", import.meta.url), "utf8"));

test("2026 draft planning reserves exactly one of five family spots for Wyatt", () => {
  assert.equal(config.familySize, 5);
  const draft = config.drafts.find((item) => item.season === 2026);
  assert.ok(draft);
  assert.equal(draft.status, "planning");
  assert.deepEqual(draft.activeManagerIds, ["shawn", "jennifer", "daphne", "elliot"]);
  assert.deepEqual(draft.reservedManagerIds, ["wyatt"]);
  assert.equal(new Set([...draft.activeManagerIds, ...draft.reservedManagerIds]).size, 5);
  assert.equal(draft.rounds, draft.rosterSlots.length);
  assert.equal(draft.draftOrder.length, 0, "draft order should not be invented before the family sets it");
});

test("draft migration contains durable history, sessions, snapshots, and concurrency guards", () => {
  for (const table of ["draft_managers", "draft_seasons", "draft_teams", "draft_players", "draft_slots", "draft_picks_live", "draft_events", "draft_snapshots", "draft_transitions", "draft_sessions", "draft_login_limits"]) {
    assert.match(migration, new RegExp(`CREATE TABLE IF NOT EXISTS ${table}`));
  }
  assert.match(migration, /family_size INTEGER NOT NULL CHECK \(family_size = 5\)/);
  assert.match(migration, /idx_draft_picks_active_slot/);
  assert.match(migration, /idx_draft_picks_active_player/);
  assert.match(migration, /UNIQUE\(draft_id, from_version\)/);
  assert.match(migration, /token_hash TEXT NOT NULL UNIQUE/);
  assert.match(migration, /failed_count INTEGER NOT NULL DEFAULT 0/);
});

test("trusted-household sessions skip PINs but keep turn and concurrency checks server-side", () => {
  const auth = fs.readFileSync(new URL("../lib/server/draft-auth.ts", import.meta.url), "utf8");
  const session = fs.readFileSync(new URL("../app/api/draft/session/route.ts", import.meta.url), "utf8");
  const picks = fs.readFileSync(new URL("../app/api/draft/[draftId]/picks/route.ts", import.meta.url), "utf8");
  assert.doesNotMatch(auth, /pin_hash|pinDigest|verifyDraftPin|PIN_PATTERN/, "the family asked for no PINs — identity is tap-your-name only");
  assert.doesNotMatch(session, /pin_hash|\bpin\b|PIN_PATTERN|failed_count/);
  assert.match(session, /httpOnly: true/);
  assert.match(session, /active = 1/, "only active family managers can hold a draft seat");
  assert.match(picks, /Only the current manager/);
  assert.match(picks, /draft_transitions/);
  assert.match(picks, /idempotencyKey/);
  assert.match(picks, /commissioner_proxy/);
});

test("the live draft room and pick views are wired to the shared state", () => {
  const room = fs.readFileSync(new URL("../components/draft-room-live.tsx", import.meta.url), "utf8");
  const pick = fs.readFileSync(new URL("../components/draft-pick-live.tsx", import.meta.url), "utf8");
  const roomPage = fs.readFileSync(new URL("../app/draft/room/page.tsx", import.meta.url), "utf8");
  const pickPage = fs.readFileSync(new URL("../app/draft/pick/page.tsx", import.meta.url), "utf8");
  for (const view of [room, pick]) assert.match(view, /useFamilyDraftState/);
  assert.match(room, /draft-board/);
  assert.match(pick, /Who&rsquo;s holding this device\?/);
  assert.match(pick, /idempotencyKey/);
  assert.match(pick, /overrideReason/);
  assert.match(roomPage, /familyDraftId\(CURRENT_FAMILY_DRAFT_SEASON\)/);
  assert.match(pickPage, /familyDraftId\(CURRENT_FAMILY_DRAFT_SEASON\)/);
  assert.doesNotMatch(room + pick, /countdown|deadline|timer/i);
});

test("family draft deliberately has no timer or pause-resume machinery", () => {
  const engine = fs.readFileSync(new URL("../lib/family-draft.ts", import.meta.url), "utf8");
  const schema = fs.readFileSync(new URL("../db/schema.ts", import.meta.url), "utf8");
  assert.doesNotMatch(engine, /"paused"/);
  assert.doesNotMatch(schema, /paused_reason/);
  assert.doesNotMatch(schema, /countdown|pick_deadline|timer/i);
});

test("commissioner correction only undoes the latest pick and preserves history", () => {
  const control = fs.readFileSync(new URL("../app/api/draft/[draftId]/control/route.ts", import.meta.url), "utf8");
  assert.match(control, /Only the commissioner can do that/);
  assert.match(control, /'draft\.started'/);
  assert.match(control, /action !== "undo-latest"/);
  assert.match(control, /ORDER BY s\.overall DESC LIMIT 1/);
  assert.match(control, /reversed_at = CURRENT_TIMESTAMP/);
  assert.match(control, /'pick\.undone'/);
  assert.doesNotMatch(control, /pause|resume|timer/i);
});

test("shared draft state refreshes simply and recovers after device focus", () => {
  const stateRoute = fs.readFileSync(new URL("../app/api/draft/[draftId]/state/route.ts", import.meta.url), "utf8");
  const hook = fs.readFileSync(new URL("../lib/use-family-draft-state.ts", import.meta.url), "utf8");
  assert.match(stateRoute, /Cache-Control", "no-store/);
  assert.match(hook, /setInterval/);
  assert.match(hook, /visibilitychange/);
  assert.match(hook, /window\.addEventListener\("focus"/);
  assert.match(hook, /reconnecting/);
  assert.doesNotMatch(hook, /countdown|deadline|pause|resume/i);
});

test("family player pool is ranked, unique, and large enough for the small draft", () => {
  assert.equal(playerPool.season, 2026);
  assert.equal(playerPool.playerCount, playerPool.players.length);
  assert.ok(playerPool.players.length >= 100);
  assert.equal(new Set(playerPool.players.map((player) => player.id)).size, playerPool.players.length);
  assert.deepEqual([...playerPool.players].sort((a, b) => a.overallRank - b.overallRank), playerPool.players);
  for (const player of playerPool.players) {
    assert.ok(["QB", "RB", "WR", "TE", "K", "DEF"].includes(player.position));
    assert.ok(player.name && player.nflTeam && Number.isInteger(player.overallRank));
  }
});

test("player identity keeps picture and NFL-team fallbacks", () => {
  const component = fs.readFileSync(new URL("../components/player-identity.tsx", import.meta.url), "utf8");
  assert.match(component, /player\.imageUrl/);
  assert.match(component, /player-identity-initials/);
  assert.match(component, /aria-label={`\$\{player\.nflTeam\} NFL team`}/);
});

test("the shared 2026 Draft Room is visible and has no clock", () => {
  const page = fs.readFileSync(new URL("../app/draft/page.tsx", import.meta.url), "utf8");
  const home = fs.readFileSync(new URL("../app/page.tsx", import.meta.url), "utf8");
  const header = fs.readFileSync(new URL("../components/site-header.tsx", import.meta.url), "utf8");
  assert.match(page, /2026 Draft Room/);
  assert.match(page, /No clock\. No rushing/);
  assert.match(page, /playerPool\.players\.slice/);
  assert.match(home, /href: "\/draft"/);
  assert.match(header, /\["\/draft", "Draft Room", "draft"\]/);
  assert.doesNotMatch(header, /🏠|🏆|📖|👥|🥊|🗂️|🔮|🎯/);
  assert.doesNotMatch(page, /countdown|pauseDraft|resumeDraft/i);
});
