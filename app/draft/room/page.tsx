import type { Metadata } from "next";
import { DraftRoomLive } from "@/components/draft-room-live";
import { RoomHero } from "@/components/room-hero";
import { CURRENT_FAMILY_DRAFT_SEASON, familyDraftId } from "@/lib/family-draft";

export const metadata: Metadata = { title: "Draft Big Board" };

export default function DraftRoomBoardPage() {
  return <main className="page-wrap inner-page draft-room-page">
    <RoomHero room="draft" label="Espinosa Family Draft" title="The Big Board" status="Shared family view">
      Put this screen on the TV — every pick shows up here for the whole family.
    </RoomHero>
    <DraftRoomLive draftId={familyDraftId(CURRENT_FAMILY_DRAFT_SEASON)} />
  </main>;
}
