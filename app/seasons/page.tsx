import { redirect } from "next/navigation";
import { latestCompletedSeason } from "@/lib/league";

export default function SeasonsIndex() {
  const latest = latestCompletedSeason();
  redirect(latest ? `/seasons/${latest}` : "/");
}
