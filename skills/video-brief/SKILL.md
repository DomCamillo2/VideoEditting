---
name: video-brief
description: Establish the style and practical brief before a new film or reel, especially serious versus funny edits and gag intensity. Use when these choices are missing or the user changes direction; skip for a small revision with an established brief.
---

# Choose the film before cutting

Read current user instructions and any saved brief. Reuse known answers. Do not import a previous user's roadtrip duration, format or comedy preference.

## First exchange

In the user's language, offer three directions in one short question:

1. **Seriös / cinematisch:** no inserted gags; deliberate cuts and restrained graphics.
2. **Emotional mit etwas Humor:** relationships and atmosphere, with occasional fitting jokes.
3. **Deutlich lustig:** playful cutouts, reactions and surprising transitions, with pauses so each joke reads.

Ask for length and destination/aspect ratio in the same exchange if missing. Permit free text and combinations. Serious can be fast; funny can have quiet chapters. A funny style is not blanket permission for embarrassing edits or a meme on every shot. If only humor changes, preserve the established format, music and story unless they need adjustment.

Then resolve remaining material questions in a compact bundle: media/project location, music, original sound, must-keep/avoid moments and next deliverable. Ask only what affects the next step. For a plan-only request, do not render. For delegated choices, state reasonable assumptions and proceed. While waiting on a meaningful choice, perform independent inventory work.

## Save a usable brief

Record tone, humor (`none`, `light`, `high`), pacing, film/reel/roadtrip mode, audience, duration, aspect ratio, resolution/fps policy, original-sound policy, music sources, chronology/recap permission, must-include, avoid, publishing restrictions and current project version. Mark unknown fields as unknown; do not silently fill a default trip.

The optional [briefing script](scripts/brief.py) runs with Python 3.9+ and no packages:

```sh
python3 scripts/brief.py brief-v001.json
python3 scripts/brief.py brief-v002.json --style serious --humor none --format 16:9 --duration "3 minutes" --non-interactive
```

Commands are relative to this skill folder. The first starts a short terminal wizard. The second records supplied values and leaves other fields unresolved. This is a convenience, not a required terminal step when the user has already answered in chat. The script never overwrites a brief. [Profiles](assets/profiles.json) are editable starting points, not an editorial verdict.

## Apply, do not merely record

- `none`: no unrequested comedy overlays, meme sounds or person distortion. Authentic laughter may still belong in the story.
- `light`: a few moments with clear setup/payoff; allow entire chapters without gags.
- `high`: more frequent, varied gags where suitable material exists; protect quiet emotional passages and avoid repetitive targeting.
- User overrides win. Note the resulting choices in the edit plan so culling, music and effects follow them.

Output a versioned brief plus the next concrete editing step. Do not claim that this choice alone generates a finished film.
