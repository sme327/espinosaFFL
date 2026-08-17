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
