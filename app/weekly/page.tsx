import type { Metadata } from "next";
import { WeeklyPredictions } from "@/components/weekly-predictions";
import { CLUBHOUSE_FAMILY, CURRENT_SEASON } from "@/lib/league";
import { RoomHero } from "@/components/room-hero";

export const metadata: Metadata = { title: "Weekly Fun" };

export default function WeeklyPage() {
  return <main className="page-wrap inner-page">
    <RoomHero room="weekly" label="Tuesday to Tuesday" title="Family Picks">Tap a picture. Pick a face. Cheer for everybody.</RoomHero>
    <section className="hq-section"><WeeklyPredictions season={CURRENT_SEASON} week={1} family={CLUBHOUSE_FAMILY} /></section>
  </main>;
}
