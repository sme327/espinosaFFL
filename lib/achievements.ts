import achievementData from "@/data/config/achievements.json";

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
