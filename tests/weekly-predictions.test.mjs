import assert from "node:assert/strict";
import fs from "node:fs";
import test from "node:test";

const migration = fs.readFileSync(new URL("../drizzle/0002_weekly_predictions.sql", import.meta.url), "utf8");
const route = fs.readFileSync(new URL("../app/api/weekly/[season]/[week]/predictions/route.ts", import.meta.url), "utf8");
const component = fs.readFileSync(new URL("../components/weekly-predictions.tsx", import.meta.url), "utf8");

test("weekly predictions save once per family member and matchup", () => {
  assert.match(migration, /CREATE TABLE IF NOT EXISTS weekly_matchups/);
  assert.match(migration, /CREATE TABLE IF NOT EXISTS weekly_predictions/);
  assert.match(migration, /UNIQUE\(matchup_id, participant_manager_id\)/);
  assert.match(route, /ON CONFLICT\(matchup_id, participant_manager_id\) DO UPDATE/);
  assert.match(route, /CLUBHOUSE_FAMILY/);
});

test("prediction choices are picture-led, use faces, and lock independently", () => {
  assert.match(component, /family\.map/);
  assert.match(component, /Who will win\?/);
  assert.match(component, /🤔/);
  assert.match(component, /🙂/);
  assert.match(component, /🤩/);
  assert.match(component, /openedAt >= Date\.parse\(matchup\.locksAt\)/);
  assert.doesNotMatch(component, /reading level|projection|point spread/i);
});
