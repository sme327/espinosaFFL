import type { CSSProperties } from "react";
import type { Manager } from "@/lib/league";

type ManagerIdentityProps = {
  manager: Manager;
  size?: "small" | "medium" | "large";
  showName?: boolean;
  showTeam?: boolean;
  futureLabel?: boolean;
  className?: string;
};

export function ManagerIdentity({
  manager,
  size = "medium",
  showName = false,
  showTeam = false,
  futureLabel = false,
  className = "",
}: ManagerIdentityProps) {
  const style = { "--manager-color": manager.color, "--manager-light": manager.lightColor } as CSSProperties;
  return <div className={`manager-identity manager-identity-${size} ${className}`.trim()} style={style}>
    <span className="manager-identity-avatar" aria-hidden="true">
      {manager.photoPath
        ? <span className="manager-identity-photo" style={{ backgroundImage: `url(${manager.photoPath})` }} />
        : <span className="manager-identity-fallback">{manager.emoji}</span>}
    </span>
    {(showName || showTeam || futureLabel) && <span className="manager-identity-copy">
      {futureLabel && <span className="manager-identity-status">Future Manager</span>}
      {showName && <strong>{manager.name}</strong>}
      {showTeam && <small>{manager.teamName ?? "Clubhouse roster spot reserved"}</small>}
    </span>}
  </div>;
}
