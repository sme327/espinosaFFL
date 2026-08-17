import type { Manager } from "@/lib/league";

export function TeamLogo({ manager, size = "medium", className = "" }: { manager: Manager; size?: "small" | "medium" | "large"; className?: string }) {
  return <span className={`team-logo team-logo-${size} ${className}`.trim()} aria-label={`${manager.teamName ?? `${manager.name} future team`} logo`}>
    {manager.teamLogoPath
      ? <img src={manager.teamLogoPath} alt="" />
      : <span aria-hidden="true">{manager.emoji}</span>}
  </span>;
}
