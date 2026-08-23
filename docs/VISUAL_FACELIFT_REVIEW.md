# Visual Facelift Review

Status: Direction approved; implementation in progress.

## Executive finding

The current Stadium Club checkpoint established the right Seahawks-inspired palette and removed much of the bright rounded-card styling. It still reads primarily as a recolored information dashboard because the old page structures, emoji illustrations, mixed material language, and duplicated CSS remain underneath the new palette.

## Counted evidence

- The homepage source contains roughly 40 emoji instances across decoration, room art, labels, activity, and trophies.
- The site currently relies on seven three-emoji room illustrations rather than a durable icon or image system.
- The stylesheet contains more than 70 border-radius declarations, more than 50 shadows, and roughly 20 gradients from multiple visual eras.
- The stylesheet includes 140+ literal color values instead of one fully authoritative palette.
- Five full team crests exist, but the current data change temporarily disconnects them from the interface.
- Only two family portraits exist, so portraits cannot yet be the consistent identity system.

## Layer review

### Environment

The dark navy direction is correct, but most pages still sit on a flat gray grid. They need stadium depth: dark structural bands, directional light, field or concourse geometry, and room-specific hero treatments.

### Surfaces and materials

The Stadium Club override squares many cards, but old warm paper, museum gold, wood, and pastel rules remain in the stylesheet. The result is fragile and inconsistent. The new system should use four materials only: painted stadium steel, dark scoreboard glass, concrete, and turf/action green.

### Typography

Fredoka remains visible in places where the identity calls for broadcast or stadium typography. Display text should become condensed and uppercase; Nunito can remain for comfortable family-readable body copy.

### Iconography

Emoji do too much work and vary by platform. Room wayfinding needs a coherent set of bold stadium pictograms. Until those are delivered, CSS and text-based wayfinding should hold the layout without emoji dependence.

### Family identity

The five crests are the strongest existing personality assets. They should be shown whole, never circularly cropped, and used as manager/team identity throughout the site until the family photo set is complete.

### Layout rhythm

Repeated boxes make every section feel equally important. Pages need a clear sequence: room entrance, primary event or story, supporting information, then onward navigation.

## Phased remediation

1. Consolidate the palette and stadium primitives; preserve existing behavior and data work.
2. Replace the global header and homepage with the Real Stadium entrance/concourse system.
3. Apply room-specific entrances and signage to the seven interior destinations.
4. Create and QA the stadium asset set.
5. Wire assets, then inspect every route at desktop and phone widths.
6. Validate accessibility, performance, fallbacks, and the live deployment.

## Acceptance checks

- No page uses white, cream, or pale gray as its main background.
- All five family members can appear with a full, uncropped crest.
- Primary room navigation is understandable with icons/images plus labels; emoji are not required.
- No more than one decorative gradient and one dominant illustrated/photo asset appear above the fold.
- No more than two bounded surface styles are visible in one viewport.
- Action green occupies less than approximately 15% of any page and consistently signals action or emphasis.
- Every route has a room name, room identity, and clear path back to the Clubhouse.
- At 360px wide, all navigation, crest labels, major headings, and actions remain readable without horizontal page scrolling.
- Every interactive control has a visible focus state and at least a 44px touch target where practical.
- Decorative imagery has empty alt text; meaningful imagery has concise alt text.
- Initial page assets stay within the size ceilings in the production brief.
