# Lokale Prüfwerkzeuge

Python 3.9+; die Kernlogik nutzt nur die Standardbibliothek. Für benannte Zeitzonen muss eine IANA-Zeitzonendatenbank verfügbar sein (auf Windows gegebenenfalls das Python-Paket `tzdata` installieren). `catalog` braucht ExifTool oder dessen JSON-Ausgabe. `qa` braucht FFmpeg/ffprobe. Die Werkzeuge ändern keine Medien und verweigern vorhandene Ausgabedateien. Neue Version oder neuen Dateinamen wählen.

## Einrichtung vor dem Filmbriefing

Beim erstmaligen Einbinden mit [SETUP.md](../SETUP.md) anfangen: Skill-Auswahl und passende MCPs stehen vor Stilfragen. `python3 tools/manage_skills.py status --target both --project /pfad/zum/projekt` prüft nur lokale Projekt-Skilldateien. `install --dry-run` prüft geplante Kopien ohne Schreiben; wiederholte `--skill NAME` wählen einzelne Skills. Der Installer richtet selbst keine MCPs ein; der Setup-Skill führt die gewählte Konfiguration über den jeweiligen Host aus.

Vor dem Schnitt kann `python3 tools/brief.py local/project-v001/brief.json` Stil, Humorgrad und Format abfragen. Mit `--non-interactive --style serious` lassen sich bekannte Angaben ohne Dialog speichern. Weitere Flags: `--humor`, `--format`, `--duration`, `--media`, `--music`, `--pacing`, `--must-keep`, `--avoid`, `--original-sound`. Details und Skill-Installer: [Skills](../docs/skills.md). Der Assistent rendert nichts und lässt unbekannte Werte offen.

## Inventur

```sh
python3 tools/editing.py catalog /pfad/zu/medien local/project-v001/catalog.json --zone Europe/Berlin
```

`--zone` nur angeben, wenn diese Annahme für die betreffenden Medien passt. Bei Reisen über Zeitzonen Kataloge getrennt erfassen oder Offsets/Overrides pro Medium nachprüfen. Ohne Zone bleiben naive Zeitangaben ungelöst. ExifTool liefert gruppierte Schlüssel mit `-G1 -a -s`. Der Filter umfasst JPG, JPEG, PNG, HEIC/HEIF, WEBP, MOV, MP4 und M4V. Andere Formate erfordern eine bewusste Erweiterung.

Schon vorhandenes JSON verwenden:

```sh
python3 tools/editing.py catalog /pfad/zu/medien local/project-v001/catalog.json --metadata-json local/exiftool.json
```

`SourceFile` muss absolut innerhalb des Medienordners oder relativ zu diesem Ordner liegen. Alle Zeitkandidaten bleiben im Ergebnis erhalten. Gleichnamige Meta-Tags verschiedener Gruppen bleiben getrennt. Exakte Duplikate werden per SHA-256 markiert. Zeitzonen ohne Offset, DST-Konflikte und Abweichungen werden gelistet. Datei-Hashes lesen alle Bytes; die Inventur großer Videos kann dauern. Kein GPS-Export und keine automatische Ortszuordnung in diesem CLI.

## Timeline prüfen

```sh
python3 tools/editing.py validate examples/timeline.json
```

Schema siehe Beispieldatei. Alle Intervalle sind halb offen: `[start_frame, start_frame + duration_frames)`. `fps` darf `30` oder `30000/1001` sein. `shots` ist die lückenlose **Basis-Bildspur**. Effekte liegen zusätzlich darüber. Überlappende Remotion-Quellsequenzen mit Handles müssen für dieses Manifest auf ihre tatsächlichen sichtbaren Basissegmente abgebildet werden; das CLI ist kein Remotion-Parser.

Pflichtfelder: `fps`, `duration_frames`, `shots`; je Shot `id`, `asset`, `start_frame`, `duration_frames`. Optional: `captured_utc`, `role` (`main`, `recap`, `graphic`), `beat_seconds`, `short_shot_reason`, `chronology_override_reason`. `effects` enthalten `start_frame` und `duration_frames`. Der Validator kontrolliert Intervalle, Gesamtdauer, Bildspur-Reihenfolge, relative Pfade, ausgewählte Beatkanten und Effektgrenzen. Ohne `--media-root` wird die Existenz der Assets nicht geprüft. Die musikalische Richtigkeit der ausgewählten Beats bleibt eine eigene Hörprüfung.

## Quellbereiche und fehlende Medien prüfen

```sh
python3 tools/editing.py validate examples/timeline-source.json
python3 tools/editing.py validate local/project-v001/timeline.json --media-root .
```

`--media-root` bezeichnet den Ordner, gegen den die `asset`-Pfade aufgelöst werden (hier das Projekt). Es erkennt fehlende Dateien und Symlinks außerhalb dieses Ordners. Webadressen, absolute Pfade und Traversal werden auch ohne dieses Flag abgelehnt. Die Beispieldateien enthalten absichtlich nur Platzhalterpfade; für sie keine Existenz behaupten.

Ein Video-Shot kann zusätzlich enthalten:

```json
"source": {"fps": "24/1", "in_frame": 48, "out_frame": 72, "total_frames": 240, "playback_rate": 1}
```

Das sind Quellframes `[48, 72)`, also eine Sekunde. Auf einer 30-fps-Timeline muss der Shot deshalb 30 Frames lang sein. `total_frames` wird gegen den gewählten Bereich geprüft; ohne diese Angabe bleibt die Obergrenze als Warnung offen. Das Werkzeug misst die Quellframezahl nicht selbst. Fehlende `source`-Angaben bei Videos erzeugen eine Warnung; Standbilder brauchen keinen Video-Quellbereich. `playback_rate` ist optional und standardmäßig 1. Konstante Geschwindigkeit und rationale fps sind unterstützt; VFR-Quellen/Speed-Ramps brauchen eine gesonderte Zeitabbildung. Unbekannte Schema-Versionen werden abgelehnt.

## Schnittliste für Review und Handoff

```sh
python3 tools/editing.py cut-list examples/timeline-source.json local/cut-list-v001.csv
```

Optional ebenfalls `--media-root`. Der Export validiert die Timeline zuerst und verweigert eine vorhandene Ausgabe. Er enthält IDs, relative Assets, Timeline-Start/Ende/Dauer, Quell-In/Out und beide Bildraten. Endframes sind exklusiv. Leere Quellfelder bleiben leer. Textfelder, die Tabellenformeln auslösen könnten, erhalten ein führendes Apostroph; JSON bleibt die unveränderte maschinenlesbare Referenz.

Die CSV ist eine **Review-Schnittliste**, kein Importversprechen für LosslessCut, OTIO, Resolve oder Premiere. Effekte, Tonspuren, Masken und Ramps werden nicht exportiert. Die Erfahrungen aus diesen Projekten und sinnvolle optionale Werkzeuge stehen im [Repo-Audit](../docs/repository-audit.md).

## Ausgewählte Beats prüfen

```sh
python3 tools/editing.py beat-report examples/beats.json local/beat-report-v001.json
```

Eingabe: `fps`, `beats_seconds`, `cuts_frames`. Ausgabe: nächste gewählte Marke, signierter Abstand in Millisekunden, passender gerundeter Frame. Ein positives Vorzeichen bedeutet Schnitt nach der Marke. Eine leere Schnittliste gilt nicht als erfolgreich geprüft. Die Ausgabe bewahrt die rationale Bildrate zusätzlich als `fps_rational`. Das Programm schätzt weder BPM noch Downbeats. Es darf nicht als unabhängige musikalische Prüfung derselben automatisch erzeugten Marken missverstanden werden.

## Tatsächlichen Export prüfen

```sh
python3 tools/editing.py qa local/film-v001.mp4 local/qa-v001.json --expected-frames 11425
```

Die Framezahl im Beispiel ist die historische Roadtrip-Länge: bei eigenen Filmen anpassen. FFprobe zählt decodierte Frames; FFmpeg decodiert vollständig, markiert schwarze Intervalle ab 0,1 s und analysiert die erste Audiospur mit `loudnorm`. Schwarzschwellen: 98% Bildfläche, 5% Luma. Dunkle Szenen/absichtliche Blenden manuell einordnen. Mehrere Audiospuren erfordern eine zusätzliche Mix-/Spurprüfung.

Exitcode 0 bedeutet bei `qa`: Decode erfolgreich und ggf. Framezahl passend. Das ist **keine** automatische Freigabe für Schwarzintervalle, Loudness oder Bildgestaltung. Diese Ergebnisse stehen im JSON; Sicht- und Hörstatus bleiben `pending`. Exitcode 1: Validierungs-/Decode-/Framezahlfehler. Exitcode 2: Eingabe, Abhängigkeit oder Dateizugriff fehlgeschlagen.

## Eigene Demo-Sounds

`python3 tools/synth_audio.py` erzeugt WAVs reproduzierbar aus festen Seeds. Bereits mitgelieferte WAVs werden nicht überschrieben. Vor absichtlicher Neugenerierung sichern/verschieben. Keine Fremdsamples erforderlich.

## Öffentliche Medien vor einem Push

```sh
python3 tools/check_repo.py
```

Prüft lokale Markdown-Verweise, private Benutzerpfade und [public-assets.json](../public-assets.json). Jede getrackte Audio-/Video-/Bilddatei braucht einen eigenen Herkunfts-/Lizenz-/Hash-Eintrag. Neue unbestätigte Medien, abweichende Inhalte, verwaiste Einträge und getrackte Dateien aus den privaten Arbeitsordnern führen zu einem Fehler, auch bei `git add -f`. ZIP-Kopien ohne eigenes Git werden anhand ihrer auslieferbaren Dateien geprüft. Der Befehl löscht keine Medien und erteilt keine Lizenz; Änderungen am Verzeichnis erfordern eine tatsächliche Inhalts-/Rechteprüfung.
