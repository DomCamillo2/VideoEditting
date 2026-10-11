# Stabilize useful shaky footage

Use when distracting camera shake compromises a selected clip or the user requests stabilization. This is an editing workflow using available stabilization tools, not a built-in Remotion filter or an automatic shake detector. No new installation is required merely to read this reference.

## Decide what needs treatment

Watch the candidate span at playback speed. Separate unwanted camera jolts from intentional pans, subject movement, handheld energy and an added comedy shake. Inspect a stationary background when possible; moving people alone do not establish camera shake. Automatic motion scores are only candidates and can confuse scene changes, occlusion or action with bad camera movement.

First trim accidental recording starts/stops or choose a cleaner nearby take. For a valuable moment with persistent distracting shake, create a short stabilized comparison including the worst movement and a representative quiet portion. Use sufficient handles; split at actual scene changes instead of estimating motion across a cut. Start with modest smoothing and increase only if the result improves. Preserve intended camera movement. A unique reaction can remain slightly shaky if stronger correction damages it.

## Process a separate source version

- Keep the original unchanged. Write a new local derivative, such as `shots/clip-017-stable-v001.mp4`, with a source hash, exact source interval, tool/version and settings.
- Prefer an available editor's stabilizer. For a scripted local alternative, first check `ffmpeg -hide_banner -filters`: the optional `vidstabdetect` and `vidstabtransform` filters form an analysis pass and a correction pass and require a build with libvidstab. Check the installed filter help before choosing parameters. Both passes must see exactly the same frames, order, orientation and preprocessing; isolate transform files per source version. [Official FFmpeg documentation](https://ffmpeg.org/ffmpeg-filters.html#vidstabdetect).
- Choose smoothing and crop/zoom per shot; no universal strong-shake preset. Check faces and body parts at the worst movement, not just the center frame. Reject stretching, stale/mirrored edge fills or unstable auto-zoom that make the result distracting.
- Stabilize the source before final portrait framing, creative zooms, face anchors, tracking, masks, text and stickers. Recompute existing tracking after replacing the source. A portrait's foreground and blurred background should use the same corrected source and time mapping.
- Preserve duration, intended frame rate, color handling and audio sync. VFR material needs an explicit timestamp/CFR mapping; do not silently change timing to simplify stabilization. Spatial stabilization cannot reliably restore detail lost to exposure-time motion blur or severe rolling-shutter distortion.

Use the derivative's actual frame coordinates in the timeline. If it contains a trimmed excerpt, its frame zero differs from the original: retain that offset in the handoff. Recheck beat positions, source bounds and original sound. Never reuse transform data for a differently trimmed or resized clip.

## Accept only a visible improvement

Compare original and corrected clips at the same playback speed and useful resolution. Review the beginning, end and worst jolts, including continuous playback. Check reduced distracting motion, natural pans, stable faces/buildings/horizons, preserved heads/hands/feet, sufficient detail, edge coverage, zoom pumping and synchronized audio. A contact sheet or successful render alone cannot confirm stable motion.

If correction needs excessive crop or produces wobbling geometry, reduce strength, use a shorter span, choose another take or keep the original with a reason. Do not stack repeated stabilizations or force a locked-off look on every shot.

Record the decision (`use stabilized`, `keep original`, `shorter span`, `alternate take`, `exclude from edit`, or `pending`), original/derivative paths and hashes, source-time mapping, settings, crop impact and reviewed intervals. If no suitable tool is available, record the missing capability and use the best existing editorial option; do not claim that stabilization was applied.
