# Assisted selection without losing the story

Use these options for long clips, large collections or an explicit automation request. No extra package is required for a small manual selection. Check current provider instructions and existing tools before offering installation.

| Need | Candidate | What the result actually means |
|---|---|---|
| Locate changes inside a long recording or existing montage | [PySceneDetect](https://github.com/Breakthrough/PySceneDetect) | Candidate shot boundaries, not best moments or beat positions |
| Propose trims in speech-heavy material | [Auto-Editor](https://github.com/WyattBlue/auto-editor) | Activity-based rough cut; review breaths, laughter, pauses and sentence ends |
| Mark reusable source ranges without a full render | [LosslessCut](https://github.com/mifi/lossless-cut) | Labeled selections; check actual keyframe cut boundaries before musical use |
| Hand editorial decisions to another application | [OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO) | Editorial structure and media references; effects/retiming depend on the receiving adapter |

For scene detection, compare start/middle/end frames, then watch promising spans with handles. Fast pans, flashes, camera bumps and lighting changes can look like cuts. PySceneDetect's adaptive detector can reduce camera-motion false positives, but does not remove the need to review. Official [CLI examples](https://www.scenedetect.com/docs/latest/cli.html) support a scene CSV plus extracted images. Write into a new local directory; detection tools may overwrite their own outputs.

Auto-Editor can use audio and motion criteria. Silence is not automatically expendable in a roadtrip: a landscape hold, shared look or comedic pause may carry the scene. Compare proposed keeps **and proposed removals** around protected moments. Record handles before/after speech and reactions. Never overwrite the original or infer that a loud clip is the funniest.

Record each suggestion separately from the final decision: source hash, tool/version, parameters, source time/frame basis, proposed range, reason, review status and reviewer decision. Low confidence means review, not deletion. A detected scene boundary, a duplicate cluster and a beat are three different kinds of evidence.

For proxies, preserve a mapping to the original asset/hash and source timing. Rotation, crop, variable frame rate and transcoding can invalidate frame numbers or tracking coordinates. Recheck face framing and sync against the original before final export. Do not promise exact beat cuts from packet-copy trimming: verify the produced boundaries or render the final edit at the chosen frame rate.

When handing off, separate source in/out from timeline start/end, make the exclusive end explicit and store both frame rates. Constant speed needs its own ratio; a speed ramp needs a mapping. Never silently replace a missing source range with zero. Keep unknowns visible.

These tools are optional research references, not bundled implementations or guaranteed host integrations. Verify versions and format support for the actual project.
