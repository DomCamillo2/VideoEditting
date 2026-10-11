---
name: video-comedy
description: Add playful video gags such as person cutouts, spins, loading effects, face-zoom transitions or tracked scooter flames. Use when humor is requested in the current brief; do not add unsolicited meme edits to a serious film.
---

# Make the moment funny, then let it breathe

Read the brief's humor level and existing timeline. `none` means no inserted comedy; an explicit request to change that level updates the brief. For `light`, choose a few strong moments. For `high`, build more varied setups/payoffs with quiet rests. Do not delay a revision to ask the same style question again.

## Choose and execute a gag

Choose a moment already present in the material: a reaction, sudden movement, scooter launch or a friend's pose. Explain the payoff in one sentence and bind it to an exact shot/frame range. Avoid humiliation, invented attributed speech and repeatedly targeting one person.

| Gag | Construction | Critical check |
|---|---|---|
| Cutout spin | Freeze a readable pose, separate original pixels with alpha, small anticipation, quick rotation, settle on an accent | Pivot follows the body; face/limbs and mask holes remain intact |
| Loading / download | Brief freeze, graphic progress indicator, cutout slips downward or resolves into motion | Short enough to read as a joke; no invented factual quote |
| Walk/run away | Animate the cutout along a path with slight bob/tilt and a shadow | A still cutout is a sticker, not claimed realistic walking; exits intentionally |
| Scooter flames | Track the deck/rear anchor with keyframes, emit flames behind it, stop at cut | Occlusion, direction and scale follow the scooter; no hovering random flame |
| Face-zoom match | Locate a chosen face in both shots; accelerate toward anchor A and resolve on B | Preserve identity and eye alignment; preview both sides of the cut |
| Spring / launch | Short squash/anticipation, upward launch or overshoot, recover | Protect the face; the disappearance is intentional and has a payoff |
| Tiny clone / orbit | Duplicate a masked pose briefly with predictable paths | Visual hierarchy stays clear; not a permanent crowd of duplicates |

Use original pixels plus a segmentation/rotoscope mask. For photos verify hair, fingers and gaps between limbs. For moving people masks must follow motion; inspect occlusions and motion blur across frames. A single frozen mask is appropriate only for a frozen sticker. Generative re-creation can change faces and is not a substitute for faithful extraction.

If there is no verified clean background, use an overt sticker/pop-out treatment or keep the source figure visible deliberately; don't imply a seamless disappearance with a bad filled silhouette. Use body-centered pivots, local shadows and easing. In Remotion derive position, rotation, progress and seeded particles from frame time. Optional sound effects support the same impact and stay below the story/dialogue.

## Preserve the cut

Prefer overlays when the base rhythm already works. If freezing, inserting a shot or using overlapping transitions changes duration, remap later beats. Never silently drift an entire song to add one gag. Avoid harsh repeated flashes; a funny edit does not require strobing.

Preview anticipation, impact, settle and exit at playback speed, plus mask/face close-ups. Inspect alpha rectangles, halos, detached anchors, unreadable labels and lost original action. Deliver an effect manifest containing asset, frame range, intent, anchor/mask source, sound cue, timing effect and review status. Add a clean version or toggle when practical so a gag can be removed without rebuilding the story.
