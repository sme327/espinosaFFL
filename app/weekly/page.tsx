import type { Metadata } from "next";
import { WeeklyPredictions } from "@/components/weekly-predictions";
import { CLUBHOUSE_FAMILY, CURRENT_SEASON } from "@/lib/league";

export const metadata: Metadata = { title: "Weekly Fun" };

export default function WeeklyPage() {
  return <main className="page-wrap inner-page">
    <header className="page-intro weekly-intro"><p className="eyebrow">🔮 Tuesday-to-Tuesday</p><h1>Family Picks</h1><p>Tap a picture. Pick a face. Cheer for everybody.</p></header>
    <section className="hq-section"><WeeklyPredictions season={CURRENT_SEASON} week={1} family={CLUBHOUSE_FAMILY} /></section>
  </main>;
}
