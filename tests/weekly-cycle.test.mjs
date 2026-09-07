import assert from "node:assert/strict";
import fs from "node:fs";
import test from "node:test";

const cycle = JSON.parse(fs.readFileSync(new URL("../data/config/weekly-cycle.json", import.meta.url), "utf8"));

test("weekly family rhythm is short, optional, and Tuesday-to-Tuesday", () => {
  assert.equal(cycle.timezone, "America/Chicago");
  assert.equal(cycle.officialResultsSource, "yahoo");
  assert.deepEqual(cycle.stages.map((stage) => stage.id), ["tuesday_recap", "new_week_picks", "game_of_week", "weekend_fun", "commissioner_finalize"]);
  assert.equal(cycle.stages[0].day, "Tuesday");
  assert.equal(cycle.stages.at(-1).day, "Tuesday");
  assert.equal(cycle.participationRules.missedWeekPenalty, false);
  assert.equal(cycle.participationRules.futureManagerCanParticipate, true);
  assert.deepEqual(cycle.participationRules.requiredForWeeklyCompletion, ["family matchup predictions"]);
});

test("confidence picks work with faces and matchup locks do not close the whole week", () => {
  assert.deepEqual(cycle.confidenceChoices.map((choice) => choice.icon), ["🤔", "🙂", "🤩"]);
  const picks = cycle.stages.find((stage) => stage.id === "new_week_picks");
  assert.ok(picks.description.includes("manager picture"));
  assert.ok(picks.locks.some((rule) => rule.includes("Each matchup locks")));
  const commissioner = cycle.stages.find((stage) => stage.id === "commissioner_finalize");
  assert.equal(commissioner.commissionerOnly, true);
  assert.ok(commissioner.description.includes("Yahoo"));
});

test("the family week comes from the configured season start and stays in bounds", () => {
  const lib = fs.readFileSync(new URL("../lib/weekly-cycle.ts", import.meta.url), "utf8");
  const page = fs.readFileSync(new URL("../app/weekly/page.tsx", import.meta.url), "utf8");
  assert.equal(cycle.seasonStartTuesdays["2026"], "2026-09-08");
  assert.match(lib, /currentFamilyWeek/);
  assert.match(lib, /Math\.min\(Math\.max\(week, 1\), FINAL_FAMILY_WEEK\)/);
  assert.match(page, /currentFamilyWeek\(CURRENT_SEASON\)/);
  assert.doesNotMatch(page, /week=\{1\}/, "the weekly page must not pin week 1 forever");
});

test("commissioner weekly seeding mirrors Yahoo pairings with independent locks", () => {
  const script = fs.readFileSync(new URL("../scripts/seed_weekly_matchups.py", import.meta.url), "utf8");
  assert.match(script, /ON CONFLICT\(season, week, manager_a_id, manager_b_id\)/, "re-seeding must update, not duplicate");
  assert.match(script, /--lock/.source ? /A manager can only appear in one matchup per week/ : /x/);
  assert.match(script, /locks: dict/);
  assert.doesNotMatch(script, /DELETE FROM weekly_predictions/, "saved predictions are never touched");
});
