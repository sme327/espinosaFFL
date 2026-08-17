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
