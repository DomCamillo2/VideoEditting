# Lokale Prüfwerkzeuge

Python 3.9+; die Kernlogik nutzt nur die Standardbibliothek. Für benannte Zeitzonen muss eine IANA-Zeitzonendatenbank verfügbar sein (auf Windows gegebenenfalls das Python-Paket `tzdata` installieren). `catalog` braucht ExifTool oder dessen JSON-Ausgabe. `qa` braucht FFmpeg/ffprobe. Die Werkzeuge ändern keine Medien und verweigern vorhandene Ausgabedateien. Neue Version oder neuen Dateinamen wählen.

## Inventur

Vor dem Schnitt kann `python3 tools/brief.py local/project-v001/brief.json` Stil, Humorgrad und Format abfragen. Mit `--non-interactive --style serious` lassen sich bekannte Angaben ohne Dialog speichern. Weitere Flags: `--humor`, `--format`, `--duration`, `--media`, `--music`, `--pacing`, `--must-keep`, `--avoid`, `--original-sound`. Details und Skill-Installer: [Skills](../docs/skills.md). Der Assistent rendert nichts und lässt unbekannte Werte offen.

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

Pflichtfelder: `fps`, `duration_frames`, `shots`; je Shot `id`, `asset`, `start_frame`, `duration_frames`. Optional: `captured_utc`, `role` (`main`, `recap`, `graphic`), `beat_seconds`, `short_shot_reason`, `chronology_override_reason`. `effects` enthalten `start_frame` und `duration_frames`. Der Validator kontrolliert Intervalle, Gesamtdauer, Bildspur-Reihenfolge, relative Pfade, ausgewählte Beatkanten und Effektgrenzen. Er prüft nicht, ob Assets bereits existieren oder die ausgewählte Musik richtig ist.

## Ausgewählte Beats prüfen

```sh
python3 tools/editing.py beat-report examples/beats.json local/beat-report-v001.json
```

Eingabe: `fps`, `beats_seconds`, `cuts_frames`. Ausgabe: nächste gewählte Marke, signierter Abstand in Millisekunden, passender gerundeter Frame. Ein positives Vorzeichen bedeutet Schnitt nach der Marke. Das Programm schätzt weder BPM noch Downbeats. Es darf nicht als unabhängige musikalische Prüfung derselben automatisch erzeugten Marken missverstanden werden.

## Tatsächlichen Export prüfen

```sh
python3 tools/editing.py qa local/film-v001.mp4 local/qa-v001.json --expected-frames 11425
```

Die Framezahl im Beispiel ist die historische Roadtrip-Länge: bei eigenen Filmen anpassen. FFprobe zählt decodierte Frames; FFmpeg decodiert vollständig, markiert schwarze Intervalle ab 0,1 s und analysiert die erste Audiospur mit `loudnorm`. Schwarzschwellen: 98% Bildfläche, 5% Luma. Dunkle Szenen/absichtliche Blenden manuell einordnen. Mehrere Audiospuren erfordern eine zusätzliche Mix-/Spurprüfung.

Exitcode 0 bedeutet bei `qa`: Decode erfolgreich und ggf. Framezahl passend. Das ist **keine** automatische Freigabe für Schwarzintervalle, Loudness oder Bildgestaltung. Diese Ergebnisse stehen im JSON; Sicht- und Hörstatus bleiben `pending`. Exitcode 1: Validierungs-/Decode-/Framezahlfehler. Exitcode 2: Eingabe, Abhängigkeit oder Dateizugriff fehlgeschlagen.

## Eigene Demo-Sounds

`python3 tools/synth_audio.py` erzeugt WAVs reproduzierbar aus festen Seeds. Bereits mitgelieferte WAVs werden nicht überschrieben. Vor absichtlicher Neugenerierung sichern/verschieben. Keine Fremdsamples erforderlich.
