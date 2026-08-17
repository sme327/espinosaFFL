import assert from "node:assert/strict";
import fs from "node:fs";
import test from "node:test";

const catalog = JSON.parse(fs.readFileSync(new URL("../data/config/achievements.json", import.meta.url), "utf8"));
const migration = fs.readFileSync(new URL("../drizzle/0001_clubhouse_achievements.sql", import.meta.url), "utf8");

test("achievement catalog offers every family member more than a winning path", () => {
  const ids = catalog.achievements.map((achievement) => achievement.id);
  assert.equal(ids.length, new Set(ids).size);
  assert.deepEqual(new Set(catalog.categories.map((category) => category.id)), new Set(["league", "draft", "participation", "family_spirit", "memory"]));
  for (const category of catalog.categories) {
    assert.ok(catalog.achievements.filter((achievement) => achievement.category === category.id).length >= 4);
  }
  assert.ok(catalog.achievements.some((achievement) => achievement.awardMethod === "automatic"));
  assert.ok(catalog.achievements.some((achievement) => achievement.awardMethod === "commissioner"));
  for (const achievement of catalog.achievements.filter((item) => item.awardMethod === "automatic")) assert.ok(achievement.ruleKey);
});

test("achievement storage preserves events, awards, stories, and corrections", () => {
  for (const table of ["clubhouse_events", "achievement_definitions", "achievement_awards"]) {
    assert.match(migration, new RegExp(`CREATE TABLE IF NOT EXISTS ${table}`));
  }
  assert.match(migration, /payload_json TEXT NOT NULL/);
  assert.match(migration, /event_id TEXT REFERENCES clubhouse_events/);
  assert.match(migration, /photo_url TEXT/);
  assert.match(migration, /revoked_at TEXT/);
  assert.match(migration, /award_key TEXT NOT NULL/);
  assert.match(migration, /idx_achievement_awards_manager_season/);
});
