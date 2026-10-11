---
name: video-export-qa
description: Prepare a reviewable preview, verify the final encoded video and hand off a versioned editing project. Use before export or when diagnosing black borders, crop errors, missing assets, drift, color or audio problems; do not claim creative QA from a successful build alone.
---

# Verify the file the user will watch

Read the brief and intended deliverable. A small fix needs checks proportional to the change, not a compulsory new approval ceremony. Preserve earlier versions and original media.

## Before the long render

- Check source dimensions, rotation, fps/time bases, variable-frame-rate behavior and audio synchronization. Choose target fps from the brief/material; don't impose 30 fps on every project. Relink proxies to correct originals and inspect source in/out points.
- Confirm aspect ratio, resolution, codec and color pipeline. Mixed HDR/SDR needs explicit handling and test encodes; keep skin/highlights stable across cuts. Do not label an SDR export HDR. Compare adjacent exposure and white balance before applying a heavy look.
- Validate media references against the project root before rendering: files must exist and symlinks must not escape the intended media scope. Keep explicit source in/out (exclusive end), source fps, timeline fps and constant playback rate; compare mapped duration to the chosen shot length. Unknown source ranges stay unknown. A file-existence check does not measure available frames or certify decode quality.
- Render a small representative sample including a portrait/group, fast action, dark scene, transition, gag if selected, song change, speech and ending. Inspect actual frames and movement. A web player or TypeScript build alone is not an encoded-video test.

## Full preview and master

1. Review chronology/chapter labels, repeated shots, emotional pacing, unwanted gags and ending. Check no fabricated route or embarrassing selection slipped in. Keep key people/gestures clear of text and effects.
2. Review protected portrait crops at start/middle/end and motion extremes; look for black/transparent edges, stretching, desynchronized blurred backgrounds and cutout halos. Check anchors through movement and occlusion.
3. Review audible beat accents and dialogue ducking. Count marker alignment separately from actual listening. Check source-to-timeline offsets after transitions and speed changes.
4. If captions are requested, verify words/timing, readable duration, contrast, line breaks and placement against faces and destination UI. Review strong flashes or excessive shake and soften unnecessary ones.
5. Render a new version and fully decode the actual file. Inspect codec, resolution, fps, duration/frame count, audio streams and missing-media indications. Measure black intervals, silence, loudness and true peaks if tools are available; classify intentional darkness/silence manually.
6. Bind QA to version, file hash and time. Inspect representative frames **from that final encode**, plus changed risky ranges. Don't reuse an old preview's passed label after a new render. Run a full re-review only when changed scope or unresolved concerns require it.

## Handoff

Provide the actual playable export path, editable project, relative media/music manifest, selection/exclusion reasons, routes if used, beat/effect cue lists and remaining issues. Distinguish preview from final and state missing dependencies. Use clear statuses: `measured`, `visually reviewed`, `listened`, `not checked`; never claim viewing/hearing you did not perform. Publishing private source material needs current user authorization, not this skill.
