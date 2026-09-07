import type { Metadata } from "next";
import { DraftPickLive } from "@/components/draft-pick-live";
import { RoomHero } from "@/components/room-hero";
import { CURRENT_FAMILY_DRAFT_SEASON, familyDraftId } from "@/lib/family-draft";

export const metadata: Metadata = { title: "My Draft Seat" };

export default function DraftPickPage() {
  return <main className="page-wrap inner-page draft-room-page">
    <RoomHero room="draft" label="Espinosa Family Draft" title="My Draft Seat" status="Personal pick view">
      Your own view for draft day — browse players, star favorites, and make your pick when it&rsquo;s your turn.
    </RoomHero>
    <DraftPickLive draftId={familyDraftId(CURRENT_FAMILY_DRAFT_SEASON)} />
  </main>;
}
