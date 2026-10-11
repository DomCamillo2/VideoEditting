# VideoEditting — Filme mit Gefühl, Rhythmus und Quatsch

Ein deutschsprachiger Werkzeugkasten für LLM-gestützte Roadtrip-Filme, Freundschafts-Recaps und kurze Reels. Aus echten Schnittkorrekturen entstanden: Metadaten statt Dateisortierung, hörbare Beats statt beliebiger Peaks, vollständige Gesichter statt automatischer Crops und gezielte Comedy statt beliebiger Effekte.

**Hier anfangen:** [START_HERE.md](START_HERE.md). Das Repo liefert Arbeitswissen, Vorlagen, Prüfprogramme und einen ausführbaren Remotion-Effektbaukasten. Die kreative Auswahl und die Sicht-/Hörkontrolle bleiben notwendig; ein Prompt garantiert keinen perfekten Film.

## An dein LLM weitergeben

Repo klonen oder ZIP herunterladen und zusammen mit den eigenen Medien lokal öffnen. Diesen Auftrag einsetzen:

> Lies START_HERE.md und AGENTS.md. Nutze dieses Repository als Arbeitsgrundlage. Meine Medien liegen in [lokaler Ordner], mein Ziel ist [Film/Reel, Länge, Format]. Falls noch offen, lass mich zuerst zwischen seriös ohne Gags, emotional mit etwas Humor und deutlich lustig wählen. Übernimm bereits genannte Wünsche. Prüfe den Projektstand und Aufnahmezeiten, vergleiche ähnliche Bilder und wähle die stärksten unterschiedlichen Momente. Plane Geschichte und Musik und erstelle eine neue bearbeitbare Version mit Vorschau. Comedy nur passend zum gewählten Humorgrad. Prüfe den tatsächlichen Export und berichte ehrlich über Sicht- und Hörkontrollen. Private Medien bleiben lokal.

Ein Chat ohne Dateizugriff kann daraus einen Schnittplan erstellen; zum Bauen braucht das LLM eine lokale Arbeitsumgebung oder einen passenden Editor. Ein GitHub-Link allein gibt ihm keinen Zugriff auf deine Fotos.

## Skills für Codex und Claude

**Neun eigenständig nutzbare Skills** sind fertig eingerichtet: Filmschnitt, Erstbriefing, Beatcut, Bildauswahl, Hochformat/Blur, Comedy, Tonmischung, Chronologie und Exportkontrolle. Codex findet die Projektkopien unter `.agents/skills/`, Claude Code unter `.claude/skills/`. Öffne das geklonte Repo als Arbeitsprojekt. Einstieg in Codex CLI/IDE: `$video-editing`; in Claude Code: `/video-editing`. [Installationsdetails und offizielle Quellen](docs/skills.md).

Für Claude mit Skill-Upload gibt es [einzelne ZIP-Pakete](dist/skills/). Für ein anderes lokales Projekt:

```sh
python3 tools/manage_skills.py install --target both --project /pfad/zum/videoprojekt
```

Der Installer lässt abweichende vorhandene Skills stehen. Im ersten Austausch wählen Nutzer Stil und Humor; alternativ startet `python3 tools/brief.py local/project-v001/brief.json` den Terminal-Assistenten. Alle unbekannten Angaben bleiben sichtbar offen.

## Ausführbare Beispiele

Voraussetzungen: Node.js 22 oder 24, npm; Python 3.9+ für die Prüfwerkzeuge. FFmpeg/ffprobe für Exportanalyse, ExifTool für die echte Medieninventur.

```sh
git clone https://github.com/DomCamillo2/VideoEditting.git
cd VideoEditting
python3 -m unittest discover -s tests -v
python3 tools/editing.py validate examples/timeline.json
cd studio
npm ci
npm run lint
npm run dev -- --no-open
```

Öffne die vom Studio ausgegebene lokale URL. **EffectsLab** zeigt Freisteller-Spins, Download, Davonlaufen, Schweben, Raketenstart, Sprungfeder, Gesichts-Zoom, Flammen und einen Wischübergang. **PortraitFraming** demonstriert einen vollständigen Vordergrund mit demselben Motiv als weichem Hintergrund. Alle Demo-Motive sind eigens erstellte SVGs; echte Personen müssen individuell freigestellt werden.

[Demo ohne Installation ansehen/herunterladen](examples/effects-lab.mp4) · [visuelle Übersicht](docs/assets/effects-overview.jpg)

![Neun Szenen aus dem Effektbaukasten](docs/assets/effects-overview.jpg)

## Wegweiser

| Ziel | Einstieg |
|---|---|
| Neuer Film oder bestehender Schnitt | [Workflow](docs/workflow.md), [Briefing](templates/brief.md) |
| Codex-/Claude-Skills installieren | [Skills und Stilwahl](docs/skills.md) |
| Gute Bilder statt fünf ähnlicher | [Medienauswahl](docs/media-selection.md), [Auswahl-Skill](skills/video-select-media/SKILL.md) |
| Chronologie und unsichere Route | [Metadaten und Karten](docs/metadata-routes.md) |
| Musik, Beats, Originalton | [Musik und Beatcut](docs/music-beats.md) |
| Mehr lustige Dinge | [Comedy-Kochbuch](docs/comedy.md), [ausführbarer Baukasten](studio/README.md) |
| Übergänge wie in schnellen Edits | [Übergänge](docs/transitions.md), [Motion-Recherche](docs/motion-research.md) |
| Hochformat und Reels | [Framing](docs/framing.md), [Reels](docs/reels.md) |
| Vorschau und fertiger Export | [QA und Rendering](docs/qa-render.md), [Werkzeuge](tools/README.md) |
| Erfahrungen und bekannte Fehler | [Fallstudien](docs/learnings.md), [Provenienz](docs/provenance.md) |
| Weitere wichtige Schnittentscheidungen | [Recherche: Auswahl, Ton und Qualität](docs/editing-research.md) |
| An anderes LLM übergeben | [Handoff](templates/handoff.md), [Agent-Skill](skills/video-editing/SKILL.md) |
| Songs lokal nutzen | [Musikverzeichnis](music/README.md) |

## Was geteilt wird

Code, allgemeine Erkenntnisse, synthetische Beispiele und Referenzlinks. Die drei vom Eigentümer zur öffentlichen Weitergabe freigegebenen Songs sind im Musikverzeichnis enthalten. Private Fotos, Rohvideos, Chatprotokolle und GPS-Kataloge gehören in `local/` bzw. `studio/public/local/` und sind von Git ausgeschlossen. [Rechte und Abhängigkeiten](NOTICE.md).

Stand der Recherche: **11. Oktober 2026**. Der Starter pinnt Remotion 4.0.534; Web-Dokumentation kann inzwischen andere APIs zeigen. [Prüfstand](docs/validation.md).
