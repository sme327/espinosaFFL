import draftConfig from "@/data/config/draft-seasons.json";

export type DraftOrderType = "snake" | "linear";
export type DraftStatus = "planning" | "ready" | "live" | "complete" | "closed";

export type FamilyDraftConfig = {
  season: number;
  status: DraftStatus;
  activeManagerIds: string[];
  reservedManagerIds: string[];
  commissionerManagerId: string;
  draftOrder: string[];
  orderType: DraftOrderType;
  rounds: number;
  rosterSlots: string[];
};

export type FamilyDraftSlot = {
  overall: number;
  round: number;
  pickInRound: number;
  managerId: string;
  rosterSlot: string;
};

export const FAMILY_DRAFT_CAPACITY = draftConfig.familySize;
export const familyDrafts = draftConfig.drafts as FamilyDraftConfig[];
export const CURRENT_FAMILY_DRAFT_SEASON = Math.max(...familyDrafts.map((draft) => draft.season));

/** The stable D1 row ID for a season's draft; the seed script uses the same shape. */
export function familyDraftId(season: number): string {
  return `family-${season}`;
}

export function familyDraftForSeason(season: number): FamilyDraftConfig | undefined {
  return familyDrafts.find((draft) => draft.season === season);
}

export function validateFamilyDraftConfig(config: FamilyDraftConfig): string[] {
  const issues: string[] = [];
  const active = new Set(config.activeManagerIds);
  const reserved = new Set(config.reservedManagerIds);

  if (active.size !== config.activeManagerIds.length) issues.push("Active managers must be unique.");
  if (reserved.size !== config.reservedManagerIds.length) issues.push("Reserved managers must be unique.");
  if (config.activeManagerIds.length < 4 || config.activeManagerIds.length > FAMILY_DRAFT_CAPACITY) issues.push("A draft must have four or five active managers.");
  if ([...active].some((managerId) => reserved.has(managerId))) issues.push("A manager cannot be both active and reserved.");
  if (active.size + reserved.size !== FAMILY_DRAFT_CAPACITY) issues.push("Every one of the five family members must be active or reserved.");
  if (!active.has(config.commissionerManagerId)) issues.push("The commissioner must be an active manager.");
  if (config.rounds < 1 || config.rosterSlots.length !== config.rounds) issues.push("Draft rounds must match the season's roster slots.");

  if (config.status === "planning") {
    if (config.draftOrder.length !== 0 && config.draftOrder.length !== active.size) issues.push("A planning draft order must be empty or complete.");
  } else if (config.draftOrder.length !== active.size) {
    issues.push("A non-planning draft requires a complete draft order.");
  }
  if (config.draftOrder.length > 0) {
    if (new Set(config.draftOrder).size !== config.draftOrder.length) issues.push("Draft-order managers must be unique.");
    if (config.draftOrder.some((managerId) => !active.has(managerId))) issues.push("Draft order can contain only active managers.");
    if ([...active].some((managerId) => !config.draftOrder.includes(managerId))) issues.push("Draft order must contain every active manager.");
  }
  return issues;
}

export function buildFamilyDraftSchedule(config: FamilyDraftConfig): FamilyDraftSlot[] {
  const issues = validateFamilyDraftConfig(config);
  if (issues.length) throw new Error(issues.join(" "));
  if (config.draftOrder.length === 0) throw new Error("Draft order has not been finalized.");

  const slots: FamilyDraftSlot[] = [];
  for (let round = 1; round <= config.rounds; round += 1) {
    const order = config.orderType === "snake" && round % 2 === 0
      ? [...config.draftOrder].reverse()
      : config.draftOrder;
    order.forEach((managerId, index) => slots.push({
      overall: slots.length + 1,
      round,
      pickInRound: index + 1,
      managerId,
      rosterSlot: config.rosterSlots[round - 1],
    }));
  }
  return slots;
}
