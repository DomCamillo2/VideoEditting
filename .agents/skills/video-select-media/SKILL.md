---
name: video-select-media
description: Cull and rank photos or video excerpts, remove repetitive selections, and compare blurry versus sharp takes. Use for bursts, near-duplicates, contact sheets and best-moment selection; never delete source media or judge focus only from a blurred background.
---

# Select distinct, readable moments

Inputs: media folder/catalog, film purpose, target length, must-keep/avoid preferences. Outputs: contact sheets, selection manifest and concise exclusion reasons. Keep all originals unchanged; rejection means exclusion from this edit.

## Group before ranking

1. Decode and orient thumbnails correctly (including EXIF rotation); preserve links to original-resolution media. Flag unreadable files separately, not as unattractive images.
2. Hash files for exact duplicates. Group near-identical bursts using capture-time proximity plus visual similarity; neither filename proximity nor perceptual hash proves the same moment. Review visually, including mirrored/cropped/edited variants. Treat Live Photo still/video pairs as related coverage, not automatically redundant files.
3. Produce a labeled contact sheet per event/burst with stable asset IDs. Inspect finalists at useful source resolution, especially important faces and action. Do not infer sharpness from a tiny thumbnail alone.

## Assess the subject and story

- **Focus:** compare eyes/face or the intended subject. Separate subject softness, camera shake, intentional motion blur and shallow depth of field. A sharp textured background must not outrank an out-of-focus person. A blurred background alone is not a rejection reason.
- **Metrics:** Laplacian variance, perceptual hashes and exposure statistics may flag candidates. Resolution, resizing, noise, sharpening, contrast and texture change these scores; there is no universal blur threshold. Compare like-for-like crops and visually verify. If uncertain, mark `review` instead of inventing a score.
- **Exposure/color:** check recoverable shadow detail, clipped faces, mixed white balance and compression. Do not reject a purposeful silhouette or night scene just for a dark histogram.
- **Expression/framing:** compare natural expressions, occlusion and cut-off heads/hands. Closed eyes during laughter can be the best moment. Choose a flattering group take without optimizing only one person. Do not identify people by name or infer attributes from faces.
- **Story:** prefer a distinct activity, reaction or relationship. A technically softer but unique meaningful moment can stay with an explicit reason. Do not select embarrassing moments merely because the brief says funny.
- **Videos:** watch candidate spans, not only their first frame. Trim shake/recording starts and dead endings; record source in/out points, useful original sound and mid-clip focus loss or obstruction. Keep clean handles if a transition needs them.

## Make a deliberate choice per cluster

Choose one hero per near-identical moment by default. A second selection needs a distinct contribution (e.g. setup then reaction, wide then detail), not just a slightly different head angle. Example: five similar group photos with two soft faces → compare all five, keep the clearest natural group moment; retain a second only if it adds new meaning. Never enforce a rigid one-photo rule across an entire event.

Review the timeline for repeated compositions across adjacent clusters, balanced people/activities/landscapes and chapter coverage. Do not force numerical equality or include weak photos to meet a quota. Put a soft unique favorite in reserve rather than destroying it.

## Manifest

Use stable IDs and fields: `asset_id`, `cluster_id`, `exact_duplicate_of`, `decision` (`keep`, `reserve`, `exclude`, `review`), `reason`, `subject_focus`, `expression`, `story_value`, `source_in`, `source_out`, `chapter`, `second_selection_reason`, `review_resolution`, `review_status`. Use qualitative labels or `unknown`, not fabricated precision. Summarize counts, remaining review items and why several versions of one scene were retained.

## Optional automation and handoff

For long clips, speech-heavy rough cuts, proxy relinking or another editor, read [assisted selection](references/assisted-selection.md). It explains when scene detection, activity-based cuts and segment tools help, what needs review, and how to preserve source timing. Do not install those tools just to read this skill.

When the VideoEditting checkout is available, `tools/analyze_media.py` creates paginated contact sheets, exact-duplicate links, conservative similarity groups and optional subject-ROI focus metrics. Read its `--help` and the repo end-to-end guide. Output is review candidates, never an automatic keep/delete verdict. Without the checkout, use equivalent available tools.
