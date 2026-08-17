# Achievement and Memory System

The Achievement Wall celebrates winning without making winning the only way to belong. Every season includes five equal paths: league performance, draft day, participation, family spirit, and memories.

## Permanent records

- `clubhouse_events` is the shared family timeline. Draft picks, weekly activities, final results, and commissioner-added memories all use the same event shape.
- `achievement_definitions` is the reusable badge catalog.
- `achievement_awards` records who earned an achievement, when, why, and any associated story or photo.
- Photos remain optional. A future image store can hold the files while `photo_url` keeps the connection to the award.

## Award methods

Automatic awards use a named, testable `ruleKey`. They cover objective events such as winning the championship, completing predictions, making a first pick, or filling a roster.

Commissioner awards capture judgment and family context: kindness, helping someone, a hilarious moment, a bold prediction, or a meaningful story. These require a manager, season, date, and short note. They never silently award themselves.

## Fairness rules

- Participation and family-spirit achievements do not require winning a matchup.
- Wyatt may collect family-spirit and memory achievements before becoming an active Yahoo manager.
- Repeatable badges use an event or week `award_key`; one-time seasonal badges use the season as their key. This prevents accidental duplicates without blocking repeat awards.
- An award can be revoked without deleting its history.
- The commissioner can add missing historical memories, but automated league facts remain tied to their source event.
