import { ClubhouseLink as Link } from "@/components/clubhouse-link";

const rooms = [
  ["/", "Clubhouse", "clubhouse"],
  ["/champions", "Trophy Room", "trophy"],
  ["/seasons", "Scrapbook", "scrapbook"],
  ["/managers", "Locker Room", "locker"],
  ["/rivalries", "Rivalries", "rivalry"],
  ["/draft", "Draft Room", "draft"],
  ["/weekly", "Weekly Fun", "weekly"],
  ["/achievements", "Achievements", "achievements"],
] as const;

export function SiteHeader() {
  return <header className="hq-nav">
    <nav className="hq-nav-inner" aria-label="Clubhouse rooms">
      <Link className="hq-nav-brand" href="/"><span className="hq-nav-crest" aria-hidden="true">E</span><span>Espinosa FFL</span></Link>
      <div className="hq-nav-tabs">
        {rooms.map(([href, label, icon]) => <Link key={href} href={href} className="hq-nav-tab"><img src={`/stadium/icons/${icon}.svg`} alt="" /><span>{label}</span></Link>)}
      </div>
    </nav>
  </header>;
}
