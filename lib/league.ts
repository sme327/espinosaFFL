import leagueData from "@/app/data/league.json";

export type InterfaceMode = "picture-assisted" | "guided" | "strategy";
export type Manager = {
  id: string; name: string; teamName: string | null; color: string; lightColor: string; emoji: string;
  order: number; active: boolean; clubhouseMember: boolean;
  photoPath: string | null; teamLogoPath: string | null; soundPath: string | null;
  celebration: string | null; interfaceMode: InterfaceMode | null;
};
export type Matchup = { season: number; week: number; teamName: string; opponent: string; result: "Win" | "Loss"; teamScore: number; opponentScore: number };
export type PlayoffGame = { season: number; week: number; round: number; gameType: "semifinal" | "final" | "3rd_place"; seed1: number; team1: string; score1: number; seed2: number; team2: string; score2: number };
export type DraftPick = { season: number; round: number; pickInRound: number; overallPick: number; teamName: string; playerName: string };
export type SeasonNote = { season: number; tagline: string; highlights: string[] };
export type RecentEvent = { icon: string; text: string };
export type LeagueSettings = { season: number; numTeams: number; scoringType: string; draftType: string; rosterSlots: string; divisions: string; waiverType: string; playoffTiebreaker: string };

export const LEAGUE_NAME = leagueData.leagueName;
export const LEAGUE_SUBTITLE = leagueData.leagueSubtitle;
export const FOUNDED = leagueData.founded;
export const CURRENT_SEASON = leagueData.currentSeason;
export const FAMILY_SIZE = leagueData.familySize;

export const managers = leagueData.managers as Manager[];
export const seasonNotes = leagueData.seasons as SeasonNote[];
export const recentEvents = leagueData.recentEvents as RecentEvent[];
export const matchups = leagueData.matchups as Matchup[];
export const playoffGames = leagueData.playoffs as PlayoffGame[];
export const draftPicks = leagueData.draftPicks as DraftPick[];
export const leagueSettings = leagueData.leagueSettings as LeagueSettings[];

export const MANAGER_ORDER: Manager[] = [...managers].filter((manager) => manager.active).sort((a, b) => a.order - b.order);
export const CLUBHOUSE_FAMILY: Manager[] = [...managers].filter((manager) => manager.clubhouseMember).sort((a, b) => a.order - b.order);
export const RIVALRY_PAIRS: [Manager, Manager][] = MANAGER_ORDER.flatMap((a, i) => MANAGER_ORDER.slice(i + 1).map((b): [Manager, Manager] => [a, b]));

/** Rotates through every rivalry pair once per day, like a museum's rotating exhibit. */
export function rivalrySpotlightPair(): [Manager, Manager] {
  const dayIndex = Math.floor(Date.now() / 86400000) % RIVALRY_PAIRS.length;
  return RIVALRY_PAIRS[dayIndex];
}

const managerByTeam = new Map(managers.filter((manager) => manager.teamName).map((manager) => [manager.teamName as string, manager]));
export function managerForTeam(teamName: string): Manager | undefined { return managerByTeam.get(teamName); }
export function managerById(id: string): Manager | undefined { return managers.find((manager) => manager.id === id); }
export function seasonNoteFor(season: number): SeasonNote | undefined { return seasonNotes.find((note) => note.season === season); }

export function regularSeasonMatchups(): Matchup[] { return matchups.filter((matchup) => matchup.week <= 15); }

export type Champion = { season: number; championTeam: string; championManager: Manager | undefined; championScore: number; runnerUpTeam: string; runnerUpManager: Manager | undefined; runnerUpScore: number; margin: number };

export function getChampions(): Champion[] {
  const finals = playoffGames.filter((game) => game.gameType === "final");
  return finals
    .map((game) => {
      const [championTeam, championScore, runnerUpTeam, runnerUpScore] = game.score1 > game.score2
        ? [game.team1, game.score1, game.team2, game.score2]
        : [game.team2, game.score2, game.team1, game.score1];
      return {
        season: game.season,
        championTeam,
        championManager: managerForTeam(championTeam),
        championScore: Math.round(championScore * 10) / 10,
        runnerUpTeam,
        runnerUpManager: managerForTeam(runnerUpTeam),
        runnerUpScore: Math.round(runnerUpScore * 10) / 10,
        margin: Math.round(Math.abs(championScore - runnerUpScore) * 100) / 100,
      };
    })
    .sort((a, b) => a.season - b.season);
}

export type SeasonStanding = { rank: number; teamName: string; manager: Manager | undefined; wins: number; losses: number; pf: number; pa: number; winPct: number };

export function getSeasonStandings(season: number): SeasonStanding[] {
  const rows = regularSeasonMatchups().filter((matchup) => matchup.season === season);
  const teams = [...new Set(rows.map((row) => row.teamName))];
  const records = teams.map((teamName) => {
    const games = rows.filter((row) => row.teamName === teamName);
    const wins = games.filter((game) => game.result === "Win").length;
    const losses = games.filter((game) => game.result === "Loss").length;
    const pf = Math.round(games.reduce((total, game) => total + game.teamScore, 0) * 10) / 10;
    const pa = Math.round(games.reduce((total, game) => total + game.opponentScore, 0) * 10) / 10;
    return { teamName, manager: managerForTeam(teamName), wins, losses, pf, pa, winPct: Math.round((wins / Math.max(wins + losses, 1)) * 1000) / 1000 };
  });
  return records
    .sort((a, b) => b.wins - a.wins || b.pf - a.pf)
    .map((record, index) => ({ rank: index + 1, ...record }));
}

export type AllTimeStanding = { manager: Manager; team: string; wins: number; losses: number; pf: number; winPct: number; championships: number };

export function getAllTimeStandings(): AllTimeStanding[] {
  const rs = regularSeasonMatchups();
  const champs = getChampions();
  const records = MANAGER_ORDER.map((manager) => {
    const team = manager.teamName ?? "";
    const games = rs.filter((row) => row.teamName === team);
    const wins = games.filter((game) => game.result === "Win").length;
    const losses = games.filter((game) => game.result === "Loss").length;
    const pf = Math.round(games.reduce((total, game) => total + game.teamScore, 0) * 10) / 10;
    const championships = champs.filter((champ) => champ.championManager?.id === manager.id).length;
    return { manager, team, wins, losses, pf, winPct: Math.round((wins / Math.max(wins + losses, 1)) * 1000) / 1000, championships };
  });
  return records.sort((a, b) => b.championships - a.championships || b.wins - a.wins);
}

export type ManagerCareerStats = {
  manager: Manager; team: string; totalWins: number; totalLosses: number; winPct: number; totalPf: number; avgPpg: number;
  seasons: { season: number; wins: number; losses: number; pf: number; ppg: number }[];
  championships: number[]; runnerUps: number[]; championshipCount: number;
  bestWeek: { season: number; week: number; teamScore: number; opponent: string } | null;
};

export function getManagerCareerStats(managerId: string): ManagerCareerStats | null {
  const manager = managerById(managerId);
  if (!manager || !manager.teamName) return null;
  const team = manager.teamName;
  const rs = regularSeasonMatchups();
  const games = rs.filter((row) => row.teamName === team);
  if (games.length === 0) return null;

  const totalWins = games.filter((game) => game.result === "Win").length;
  const totalLosses = games.filter((game) => game.result === "Loss").length;
  const totalPf = Math.round(games.reduce((total, game) => total + game.teamScore, 0) * 10) / 10;
  const avgPpg = Math.round((games.reduce((total, game) => total + game.teamScore, 0) / games.length) * 100) / 100;

  const seasonNumbers = [...new Set(games.map((game) => game.season))].sort((a, b) => a - b);
  const seasons = seasonNumbers.map((season) => {
    const seasonGames = games.filter((game) => game.season === season);
    return {
      season,
      wins: seasonGames.filter((game) => game.result === "Win").length,
      losses: seasonGames.filter((game) => game.result === "Loss").length,
      pf: Math.round(seasonGames.reduce((total, game) => total + game.teamScore, 0) * 10) / 10,
      ppg: Math.round((seasonGames.reduce((total, game) => total + game.teamScore, 0) / seasonGames.length) * 10) / 10,
    };
  });

  const champs = getChampions();
  const championships = champs.filter((champ) => champ.championManager?.id === managerId).map((champ) => champ.season);
  const runnerUps = champs.filter((champ) => champ.runnerUpManager?.id === managerId).map((champ) => champ.season);

  const best = games.reduce((best, game) => (!best || game.teamScore > best.teamScore ? game : best), null as Matchup | null);
  const bestWeek = best ? { season: best.season, week: best.week, teamScore: best.teamScore, opponent: best.opponent } : null;

  return { manager, team, totalWins, totalLosses, winPct: Math.round((totalWins / Math.max(totalWins + totalLosses, 1)) * 1000) / 1000, totalPf, avgPpg, seasons, championships, runnerUps, championshipCount: championships.length, bestWeek };
}

export type RivalryStats = {
  managerA: Manager; managerB: Manager;
  rsAWins: number; rsBWins: number; poAWins: number; poBWins: number; totalAWins: number; totalBWins: number;
  poMeetings: { season: number; round: string; scoreA: number; scoreB: number; winnerScore: number; loserScore: number; winner: Manager | undefined }[];
  biggestAWin: { scoreA: number; scoreB: number; week: number; season: number } | null;
  biggestBWin: { scoreA: number; scoreB: number; week: number; season: number } | null;
  closestGame: { scoreA: number; scoreB: number; week: number; season: number } | null;
  streakHolder: Manager | null; streakCount: number;
};

export function getRivalryStats(managerA: Manager, managerB: Manager): RivalryStats {
  const teamA = managerA.teamName ?? "";
  const teamB = managerB.teamName ?? "";
  const rs = regularSeasonMatchups();
  const games = rs.filter((row) => row.teamName === teamA && row.opponent === teamB);

  const rsAWins = games.filter((game) => game.result === "Win").length;
  const rsBWins = games.filter((game) => game.result === "Loss").length;

  const poMeetings: RivalryStats["poMeetings"] = [];
  let poAWins = 0;
  let poBWins = 0;
  for (const game of playoffGames) {
    if (!((game.team1 === teamA && game.team2 === teamB) || (game.team1 === teamB && game.team2 === teamA))) continue;
    const winnerTeam = game.score1 > game.score2 ? game.team1 : game.team2;
    const winnerManager = managerForTeam(winnerTeam);
    const scoreA = game.team1 === teamA ? game.score1 : game.score2;
    const scoreB = game.team1 === teamA ? game.score2 : game.score1;
    poMeetings.push({
      season: game.season,
      round: game.gameType,
      scoreA: Math.round(scoreA * 10) / 10,
      scoreB: Math.round(scoreB * 10) / 10,
      winnerScore: Math.round(Math.max(scoreA, scoreB) * 10) / 10,
      loserScore: Math.round(Math.min(scoreA, scoreB) * 10) / 10,
      winner: winnerManager,
    });
    if (winnerManager?.id === managerA.id) poAWins += 1; else poBWins += 1;
  }

  let biggestAWin: RivalryStats["biggestAWin"] = null;
  let biggestBWin: RivalryStats["biggestBWin"] = null;
  let closestGame: RivalryStats["closestGame"] = null;
  if (games.length > 0) {
    const withMargin = games.map((game) => ({ ...game, margin: game.teamScore - game.opponentScore }));
    const aWins = withMargin.filter((game) => game.result === "Win");
    if (aWins.length) {
      const best = aWins.reduce((best, game) => (game.margin > best.margin ? game : best));
      biggestAWin = { scoreA: best.teamScore, scoreB: best.opponentScore, week: best.week, season: best.season };
    }
    const bWins = withMargin.filter((game) => game.result === "Loss");
    if (bWins.length) {
      const best = bWins.reduce((best, game) => (game.margin < best.margin ? game : best));
      biggestBWin = { scoreA: best.teamScore, scoreB: best.opponentScore, week: best.week, season: best.season };
    }
    const closest = withMargin.reduce((closest, game) => (Math.abs(game.margin) < Math.abs(closest.margin) ? game : closest));
    closestGame = { scoreA: closest.teamScore, scoreB: closest.opponentScore, week: closest.week, season: closest.season };
  }

  let streakHolder: Manager | null = null;
  let streakCount = 0;
  if (games.length > 0) {
    const sorted = [...games].sort((a, b) => a.season - b.season || a.week - b.week);
    const last = sorted[sorted.length - 1];
    streakHolder = last.result === "Win" ? managerA : managerB;
    for (let i = sorted.length - 1; i >= 0; i -= 1) {
      const winner = sorted[i].result === "Win" ? managerA : managerB;
      if (winner.id === streakHolder.id) streakCount += 1; else break;
    }
  }

  return {
    managerA, managerB, rsAWins, rsBWins, poAWins, poBWins,
    totalAWins: rsAWins + poAWins, totalBWins: rsBWins + poBWins,
    poMeetings, biggestAWin, biggestBWin, closestGame, streakHolder, streakCount,
  };
}

export function getAllRivalries(): RivalryStats[] { return RIVALRY_PAIRS.map(([a, b]) => getRivalryStats(a, b)); }

export type SeasonPlayoffGame = PlayoffGame & { winnerTeam: string; winnerManager: Manager | undefined; loserTeam: string };

export function getSeasonPlayoffs(season: number): SeasonPlayoffGame[] {
  return playoffGames
    .filter((game) => game.season === season)
    .map((game) => {
      const winnerTeam = game.score1 > game.score2 ? game.team1 : game.team2;
      const loserTeam = game.score1 > game.score2 ? game.team2 : game.team1;
      return { ...game, winnerTeam, winnerManager: managerForTeam(winnerTeam), loserTeam };
    });
}

export function seasonList(): number[] {
  const years = new Set(matchups.map((matchup) => matchup.season));
  return [...years].sort((a, b) => a - b);
}

export function latestCompletedSeason(): number | null {
  const completed = getChampions().map((champion) => champion.season);
  return completed.length ? Math.max(...completed) : null;
}
