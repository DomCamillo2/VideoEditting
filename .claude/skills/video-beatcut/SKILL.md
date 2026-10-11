---
name: video-beatcut
description: Cut photos or video on audible musical beats, downbeats and phrase changes, or diagnose an edit that feels off beat. Use for music-led timing and transitions; do not equate waveform peaks or automatic markers with verified musical accents.
---

# Cut on the intended beat

Inputs: actual audio file, chosen excerpt(s), target fps, current edit and desired energy. If audio cannot be heard with available tools, analyze provisionally and explicitly leave listening validation open.

1. Identify intro, verse, chorus/drop, breakdown and ending. Estimate tempo and phase, then check strong kicks/snares and downbeats near the beginning, middle and end. Watch half/double tempo, pickup notes, syncopation and changing tempo. An onset detector finds transients, not necessarily beats or bar starts.
2. Build a **selected** marker list, not a cut on every peak. Record source seconds, timeline seconds, accent type, confidence and whether actually listened to. Favor phrase changes for chapter/song changes and the strongest images for musical peaks.
3. Map trimmed audio correctly. At normal speed: `timeline_seconds = audio_start + source_seconds - source_in`. With constant playback rate `r`, divide the source offset by `r`. For ramps, use the actual time mapping, not a single BPM. Include source trims, repeats and song crossfades.
4. Quantize each absolute boundary once: for nonnegative times, `frame = floor(seconds * fps + 0.5)`. Preserve rational rates such as `30000/1001`. Shot length is the next boundary minus the current boundary; do not repeatedly round incremental beat lengths. Store fps and integer frame boundaries.
5. Vary holds by story and energy: several beats for atmosphere, shorter phrases for action. Prefer a readable moment over mechanically cutting on every beat. Treat clips below 0.5 seconds as deliberate exceptions to explain, not a default montage strategy.
6. Set transitions so their perceptual impact lands on the intended accent. A cut, flash peak, mask reveal or landing may have different anchor frames. Overlapping transitions shorten total duration; recompute downstream boundaries. An overlay does not inherently shorten the base track.
7. Preview the actual encoded segment with music, including a few seconds before and after key cuts. Listen for phase errors, song edits, speed ramps and effects obscuring the accent. Check again at the end of a long section to catch drift. Do not call numerical alignment an independent listening test.

## Evidence to deliver

Save a beat table with `song_id`, `source_seconds`, `timeline_seconds`, `target_frame`, `accent_type`, `confidence`, `listening_status`; a cut table with `cut_frame`, `matched_marker`, `delta_ms`, `intentional_offset_reason`; and representative review ranges.

Separate **frame alignment** (nearest frame; theoretical quantization error up to half a frame) from **musical correctness** (the chosen sound is the intended accent) and **editorial quality** (the shot holds long enough). A marker-perfect cut can still feel wrong. Finish songs with a phrase ending, intentional tail/fade or suitable authentic sound.
