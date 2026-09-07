import weeklyCycleData from "@/data/config/weekly-cycle.json";

export type WeeklyStageId = "tuesday_recap" | "new_week_picks" | "game_of_week" | "weekend_fun" | "commissioner_finalize";

export type WeeklyStage = {
  id: WeeklyStageId;
  label: string;
  day: string;
  icon: string;
  headline: string;
  description: string;
  primaryAction: string;
  optional: boolean;
  commissionerOnly?: boolean;
  locks: string[];
};

export type ConfidenceChoice = {
  id: "unsure" | "confident" | "super";
  label: string;
  icon: string;
};

export const weeklyCycle = {
  ...weeklyCycleData,
  stages: weeklyCycleData.stages as WeeklyStage[],
  confidenceChoices: weeklyCycleData.confidenceChoices as ConfidenceChoice[],
};

export function weeklyStage(id: WeeklyStageId): WeeklyStage {
  const stage = weeklyCycle.stages.find((candidate) => candidate.id === id);
  if (!stage) throw new Error(`Unknown weekly stage: ${id}`);
  return stage;
}

const WEEK_MS = 7 * 24 * 60 * 60 * 1000;
const FINAL_FAMILY_WEEK = 17;

/**
 * The Tuesday-to-Tuesday family week, from the season's first Tuesday
 * (midnight in the family timezone, approximated as fixed UTC-5).
 */
export function currentFamilyWeek(season: number, now: Date = new Date()): number {
  const startTuesday = (weeklyCycleData.seasonStartTuesdays as Record<string, string>)[String(season)];
  if (!startTuesday) return 1;
  const week = Math.floor((now.getTime() - Date.parse(`${startTuesday}T00:00:00-05:00`)) / WEEK_MS) + 1;
  return Math.min(Math.max(week, 1), FINAL_FAMILY_WEEK);
}
