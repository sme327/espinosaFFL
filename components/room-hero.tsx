export type StadiumRoom = "trophy" | "scrapbook" | "locker" | "rivalry" | "draft" | "weekly" | "achievements";

export function RoomHero({ room, label, title, children, status }: { room: StadiumRoom; label: string; title: string; children: React.ReactNode; status?: string }) {
  return <header className={`room-hero room-hero-${room}`}>
    <img className="room-hero-icon" src={`/stadium/icons/${room}.svg`} alt="" />
    <div className="room-hero-copy"><p className="eyebrow">{label}</p><h1>{title}</h1><p>{children}</p></div>
    {status && <span className="room-hero-status">{status}</span>}
  </header>;
}
