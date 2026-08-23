# Real Stadium Production Asset Brief

Status: Core production set delivered and accepted. The painted-steel texture and concourse-divider raster were intentionally superseded by lighter CSS treatments after the room scenes established sufficient material depth.

## Source of truth

Match the production palette in `app/globals.css`: stadium navy `#002244`, deep navy `#00182C`, steel blue `#003B5C`, teal `#005F70`, action green `#69BE28`, and cool silver `#A5ACAF`.

No asset may introduce an additional dominant brand color.

## Global conventions

- Raster delivery: WebP, sRGB, no embedded text unless explicitly requested.
- Transparent illustrations must contain a real alpha channel and clean edges at 1×.
- Avoid NFL, Seahawks, Yahoo, or other third-party trademarks and uniform designs.
- Do not bake navigation labels into imagery.
- No emoji-style rendering, glossy app icons, cartoon mascots, or rounded-card backgrounds.
- Each asset receives mechanical inspection, source inspection where applicable, and visual inspection before use.

## Wave 1 — Stadium foundation

### Clubhouse entrance hero

- Purpose: Establish the homepage as the family’s stadium entrance.
- Look: Night stadium concourse opening toward a lit field; dramatic but welcoming; no people, logos, text, or NFL branding.
- Format: 2400×900 WebP.
- Ceiling: 320 KB.
- Filename: `public/stadium/clubhouse-entrance.webp`.
- QA: Dark left-side text-safe area; lights do not blow out to white; field remains secondary; readable crop at 360px.

### Stadium atmosphere texture

- Purpose: Add restrained depth to large navy fields without a visible repeating pattern.
- Look: Fine painted-steel grain with faint stadium haze.
- Format: 512×512 seamless WebP.
- Ceiling: 45 KB.
- Filename: `public/stadium/painted-steel.webp`.
- QA: Seamless at 4×4; subtle at 100%; no scratches that resemble text.

### Concourse divider

- Purpose: Separate major homepage zones with stadium architecture rather than empty lines or emoji.
- Look: Dark structural beam with a narrow action-green wayfinding strip.
- Format: 1600×80 transparent WebP.
- Ceiling: 35 KB.
- Filename: `public/stadium/concourse-divider.webp`.
- QA: True alpha; clean at both 1600px and 360px; no baked shadow halo.

## Wave 2 — Room wayfinding

Create eight bold, consistent pictograms: Clubhouse entrance, trophy display, season program, locker/tunnel, rivalry lights, draft podium, prediction board, and ring of honor.

- Purpose: Replace emoji as the visual language for navigation.
- Look: Stadium signage pictograms; single-color action-green mark plus optional silver detail; strong silhouette for pre-readers.
- Format: SVG with a 64×64 viewBox.
- Ceiling: 8 KB each.
- Path: `public/stadium/icons/{clubhouse,trophy,scrapbook,locker,rivalry,draft,weekly,achievements}.svg`.
- QA: No `<text>`, `font-family`, scripts, external references, `currentColor`, empty groups, or duplicate IDs; recognizable at 24px; accessible name supplied by surrounding HTML.

## Wave 3 — Interior room heroes

Create seven 1800×520 WebP scenes using the same stadium, lighting, and camera language:

- `trophy-room.webp`: championship cases and hanging banners; no engraved names.
- `season-archive.webp`: stadium program archive and season boards.
- `locker-tunnel.webp`: five locker bays leading toward field light.
- `rivalry-night.webp`: opposing tunnel lights and primetime energy.
- `draft-stage.webp`: family-sized draft stage with five crest positions and a large empty board.
- `weekly-desk.webp`: game-day prediction desk facing the field.
- `ring-of-honor.webp`: stadium fascia with empty achievement positions.

Each file ceiling: 220 KB. Every scene requires a dark text-safe area, mobile-safe central subject, no people, no words, no logos, and no white-dominant lighting.

## Existing family crests

Use the five current `*-v2.png` files as full crests during this phase. Do not redraw, crop, mask into circles, or place them inside new generated artwork. A later crest-production pass may create transparent, optimized master files once the family approves the identities.

## Delivery checklist

- [ ] Exact filenames and dimensions.
- [ ] Every raster is below its ceiling.
- [ ] Required alpha channels verified.
- [ ] SVG source checks pass.
- [ ] Desktop and mobile crops reviewed.
- [ ] Images match the approved Real Stadium contract.
- [ ] Asset manifest updated with acceptance or rejection verdicts.
