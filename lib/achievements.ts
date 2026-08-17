import achievementData from "@/data/config/achievements.json";
import { getChampions, matchups, type Manager } from "@/lib/league";

export type AchievementCategory = "league" | "draft" | "participation" | "family_spirit" | "memory";
export type AwardMethod = "automatic" | "commissioner";
export type ClubhouseEventSource = "league" | "draft" | "weekly" | "commissioner";

export type AchievementDefinition = {
  id: string;
  name: string;
  icon: string;
  category: AchievementCategory;
  description: string;
  awardMethod: AwardMethod;
  ruleKey: string | null;
  repeatable: boolean;
};

export type ClubhouseEvent = {
  id: string;
  season: number;
  eventType: string;
  managerId: string | null;
  occurredAt: string;
  source: ClubhouseEventSource;
  sourceId: string | null;
  title: string;
  story: string | null;
  payload: Record<string, unknown>;
};

export type AchievementAward = {
  id: string;
  achievementId: string;
  managerId: string;
  season: number;
  awardKey: string;
  eventId: string | null;
  awardedByManagerId: string | null;
  awardedAt: string;
  note: string | null;
  photoUrl: string | null;
};

export const achievementCategories = achievementData.categories;
export const achievements = achievementData.achievements as AchievementDefinition[];

export function achievementsForCategory(category: AchievementCategory): AchievementDefinition[] {
  return achievements.filter((achievement) => achievement.category === category);
}

export function automaticAchievements(): AchievementDefinition[] {
  return achievements.filter((achievement) => achievement.awardMethod === "automatic");
}

export function commissionerAchievements(): AchievementDefinition[] {
  return achievements.filter((achievement) => achievement.awardMethod === "commissioner");
}

export type HistoricalAchievement = AchievementDefinition & { count: number; seasons: number[] };

export function historicalAchievementsFor(manager: Manager): HistoricalAchievement[] {
  const earned: HistoricalAchievement[] = [];
  const titles = getChampions().filter((champion) => champion.championManager?.id === manager.id).map((champion) => champion.season);
  if (titles.length) earned.push({ ...achievements.find((item) => item.id === "league_champion")!, count: titles.length, seasons: titles });

  if (manager.teamName) {
    const managerGames = matchups.filter((game) => game.teamName === manager.teamName);
    const highScoreWeeks = managerGames.filter((game) => {
      const weekScores = matchups.filter((row) => row.season === game.season && row.week === game.week).map((row) => row.teamScore);
      return game.teamScore === Math.max(...weekScores);
    });
    if (highScoreWeeks.length) earned.push({
      ...achievements.find((item) => item.id === "weekly_high_score")!,
      count: highScoreWeeks.length,
      seasons: [...new Set(highScoreWeeks.map((game) => game.season))].sort(),
    });
  }
  return earned;
}
