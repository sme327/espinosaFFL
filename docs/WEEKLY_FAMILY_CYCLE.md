# Tuesday-to-Tuesday Family Cycle

The clubhouse adds one small layer of family fun around Yahoo; it does not try to become a second fantasy platform. A family member can complete the meaningful weekly activity in one short visit.

## The rhythm

1. **Tuesday Trophy Time:** The previous week closes with official results, earned achievements, and a favorite memory.
2. **Pick the Winners:** From Tuesday until each matchup begins, everyone chooses a family manager by picture and a confidence face.
3. **Game of the Week:** One matchup gets the spotlight, using a rivalry or season story instead of statistics-heavy analysis.
4. **Weekend Fun:** Kids' MVP, a small challenge, and friendly reactions are available but optional.
5. **Make It Official:** On Tuesday, the commissioner confirms Yahoo results and publishes the recap.

## Guardrails

- No streaks that punish a missed week.
- No open chat or public comments.
- No prizes that depend on reading skill.
- No live-score promise until Yahoo freshness has been tested later.
- Wyatt can participate in predictions, MVP picks, challenges, reactions, and family achievements before managing a Yahoo team.
- A matchup locks independently when its relevant NFL games begin; an early Thursday game does not close every family activity.
- Commissioner corrections preserve history instead of silently replacing it.

## Commissioner setup each week

The current week is computed from `seasonStartTuesdays` in `data/config/weekly-cycle.json` (Tuesday to Tuesday, Chicago time). Matchups mirror the real Yahoo pairings and are created by the commissioner in one command:

```
python3 scripts/seed_weekly_matchups.py --pairs shawn:jennifer,daphne:elliot --featured shawn:jennifer --apply
```

Every matchup locks at noon Sunday by default; a `--lock pair=ISO` override handles Thursday games so one early game never closes the whole week. Re-running updates locks and the featured game without touching saved predictions.

## What appears on the weekly home

The page leads with one clear action based on the current stage. Below it are the Game of the Week, each person's participation status, optional fun, and the previous recap. The interface should never present all administration and family choices at once.
