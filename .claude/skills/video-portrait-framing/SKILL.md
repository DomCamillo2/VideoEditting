---
name: video-portrait-framing
description: Fit portrait photos or videos into landscape edits, or reframe mixed aspect ratios with a blurred copy of the same media. Use to prevent black borders and cropped faces or bodies; not for privacy anonymization or sharpening a blurry subject.
---

# Preserve the subject, soften the unused canvas

Read target aspect ratio and protected content first. Correct source rotation before computing dimensions. Review each asset individually; one global crop cannot protect every group shot.

1. Place a duplicate of the same source as the background, filling the canvas with `cover`. Enlarge enough that blur sampling and camera motion cannot expose transparent/dark edges. Blur strongly and optionally darken/desaturate gently so the sharp foreground remains dominant. Check bright edges as well as dark ones.
2. Place the foreground with preserved aspect ratio. Start with `contain`: for canvas `W,H` and oriented source `w,h`, scale is `min(W/w, H/h)`. Background cover scale is `max(W/w, H/h)`. Never stretch to fill.
3. Mark protected areas: relevant faces, heads, gestures, feet when full-body action matters, and contextual objects. Increase foreground size only while these remain inside the canvas throughout the shot. Use subject-aware positioning only after visual verification; don't automatically push people away from center.
4. If a full portrait group cannot be larger without losing people, accept the visible blurred side areas. Do not satisfy a 'small border' request by secretly cropping heads. Alternatives such as a deliberate two-photo layout need an editorial reason and coherent timing.
5. Optional gentle motion: around 103–107% relative to the chosen base framing only when there is enough safe margin. Tight portraits can remain still. Check the **maximum** scale and all pan extremes; motion is not required for every photo.
6. For video, keep foreground and background on the identical source time, trim, speed mapping and orientation. Background audio must be muted; use only one intended audio track. Avoid a blurred duplicate visibly lagging behind the subject.
7. Keep captions, location names and effects away from protected regions and destination UI overlays. Check at actual viewing size. Do not use intentional blurred padding to hide unusable foreground focus.

In frame-based renderers derive motion from the current frame. In Remotion use media components with render synchronization; a CSS blur can be static, but wall-clock CSS animation is not a reliable video clock.

Deliver per-shot framing values, protected regions/notes, start/mid/end stills and reviewed moving ranges. Inspect the final encode for clipping, black/transparent edges, background flicker, mismatched frames and stretching. Automated black detection alone cannot prove people are safely framed.
