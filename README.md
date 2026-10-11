# VideoEditting — Filme mit Gefühl, Rhythmus und Quatsch

Ein deutschsprachiger Werkzeugkasten für LLM-gestützte Roadtrip-Filme, Freundschafts-Recaps und kurze Reels. Aus echten Schnittkorrekturen entstanden: Metadaten statt Dateisortierung, hörbare Beats statt beliebiger Peaks, vollständige Gesichter statt automatischer Crops und gezielte Comedy statt beliebiger Effekte.

**Hier anfangen:** [START_HERE.md](START_HERE.md). Das Repo liefert Arbeitswissen, Vorlagen, Prüfprogramme und einen ausführbaren Remotion-Effektbaukasten. Die kreative Auswahl und die Sicht-/Hörkontrolle bleiben notwendig; ein Prompt garantiert keinen perfekten Film.

## An dein LLM weitergeben

Repo klonen oder ZIP herunterladen und zusammen mit den eigenen Medien lokal öffnen. Diesen Auftrag einsetzen:

> Lies START_HERE.md und AGENTS.md. Nutze dieses Repository als Arbeitsgrundlage. Meine Medien liegen in [lokaler Ordner], mein Ziel ist [Film/Reel, Länge, Format, Stimmung]. Prüfe den vorhandenen Projektstand, sammle Aufnahmezeiten mit Herkunft und Unsicherheiten, plane Geschichte und Musik und erstelle eine neue bearbeitbare Version mit Vorschau. Nutze passende Comedy-Rezepte. Prüfe Änderungen am tatsächlichen Export. Berichte ehrlich, welche Sicht- und Hörkontrollen erfolgt sind. Private Medien bleiben lokal. Beachte meine aktuellen Wünsche vor den Beispielvorgaben dieses Repos.

Ein Chat ohne Dateizugriff kann daraus einen Schnittplan erstellen; zum Bauen braucht das LLM eine lokale Arbeitsumgebung oder einen passenden Editor. Ein GitHub-Link allein gibt ihm keinen Zugriff auf deine Fotos.

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
| Chronologie und unsichere Route | [Metadaten und Karten](docs/metadata-routes.md) |
| Musik, Beats, Originalton | [Musik und Beatcut](docs/music-beats.md) |
| Mehr lustige Dinge | [Comedy-Kochbuch](docs/comedy.md), [ausführbarer Baukasten](studio/README.md) |
| Übergänge wie in schnellen Edits | [Übergänge](docs/transitions.md), [Motion-Recherche](docs/motion-research.md) |
| Hochformat und Reels | [Framing](docs/framing.md), [Reels](docs/reels.md) |
| Vorschau und fertiger Export | [QA und Rendering](docs/qa-render.md), [Werkzeuge](tools/README.md) |
| Erfahrungen und bekannte Fehler | [Fallstudien](docs/learnings.md), [Provenienz](docs/provenance.md) |
| An anderes LLM übergeben | [Handoff](templates/handoff.md), [Agent-Skill](skills/video-editing/SKILL.md) |
| Songs lokal nutzen | [Musikverzeichnis](music/README.md) |

## Was geteilt wird

Code, allgemeine Erkenntnisse, synthetische Beispiele und Referenzlinks. Die drei vom Eigentümer zur öffentlichen Weitergabe freigegebenen Songs sind im Musikverzeichnis enthalten. Private Fotos, Rohvideos, Chatprotokolle und GPS-Kataloge gehören in `local/` bzw. `studio/public/local/` und sind von Git ausgeschlossen. [Rechte und Abhängigkeiten](NOTICE.md).

Stand der Recherche: **11. Oktober 2026**. Der Starter pinnt Remotion 4.0.534; Web-Dokumentation kann inzwischen andere APIs zeigen. [Prüfstand](docs/validation.md).
