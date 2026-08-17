import { ClubhouseLink as Link } from "@/components/clubhouse-link";

export default function NotFound() {
  return <main className="page-wrap inner-page not-found-page">
    <p className="eyebrow">404</p>
    <h1>That room isn&rsquo;t in the Clubhouse.</h1>
    <p>Try one of the rooms below.</p>
    <nav>
      <Link href="/">Clubhouse</Link>
      <Link href="/champions">Trophy Room</Link>
      <Link href="/seasons">Scrapbook</Link>
      <Link href="/managers">Locker Room</Link>
      <Link href="/rivalries">Rivalry Arena</Link>
    </nav>
  </main>;
}
