import type { CSSProperties } from "react";

export type DraftPlayerIdentity = {
  name: string;
  position: "QB" | "RB" | "WR" | "TE" | "K" | "DEF";
  nflTeam: string;
  imageUrl?: string | null;
};

const POSITION_COLORS: Record<DraftPlayerIdentity["position"], string> = {
  QB: "#C0392B",
  RB: "#1F7A4D",
  WR: "#2563A6",
  TE: "#7B5EA7",
  K: "#B7791F",
  DEF: "#4A5568",
};

function initials(name: string): string {
  return name.split(/\s+/).filter(Boolean).slice(0, 2).map((part) => part[0]).join("").toUpperCase();
}

export function PlayerIdentity({ player, size = "medium", showName = true }: { player: DraftPlayerIdentity; size?: "small" | "medium" | "large"; showName?: boolean }) {
  const style = { "--player-color": POSITION_COLORS[player.position] } as CSSProperties;
  return <span className={`player-identity player-identity-${size}`} style={style}>
    <span className="player-identity-picture" aria-hidden="true">
      {player.imageUrl
        ? <span className="player-identity-photo" style={{ backgroundImage: `url(${player.imageUrl})` }} />
        : <span className="player-identity-initials">{initials(player.name)}</span>}
    </span>
    {showName && <span className="player-identity-copy">
      <strong>{player.name}</strong>
      <span><b>{player.position}</b><i aria-label={`${player.nflTeam} NFL team`}>{player.nflTeam}</i></span>
    </span>}
  </span>;
}
