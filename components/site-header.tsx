import { ClubhouseLink as Link } from "@/components/clubhouse-link";

const rooms = [
  ["/", "🏠 Clubhouse"],
  ["/champions", "🏆 Trophy Room"],
  ["/seasons", "📖 Scrapbook"],
  ["/managers", "👥 Locker Room"],
  ["/rivalries", "🥊 Rivalry Arena"],
  ["/draft", "🗂️ Draft Room"],
  ["/weekly", "🔮 Weekly Fun"],
  ["/achievements", "🎯 Achievements"],
] as const;

export function SiteHeader() {
  return <header className="hq-nav">
    <nav className="hq-nav-inner" aria-label="Clubhouse rooms">
      <Link className="hq-nav-brand" href="/">🏈 Espinosa FFL</Link>
      <div className="hq-nav-tabs">
        {rooms.map(([href, label]) => <Link key={href} href={href} className="hq-nav-tab">{label}</Link>)}
      </div>
    </nav>
  </header>;
}
