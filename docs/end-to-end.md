# Vom Material bis zum abspielbaren Film

Dieser Weg baut einen echten, bearbeitbaren 18-Sekunden-Beispielfilm aus eigenen synthetischen Bildern, einem Video und selbst erzeugtem Audio. Er benötigt keine privaten Fotos, keine Musikdownloads und keinen API-Schlüssel. Das Beispiel demonstriert die Pipeline; es ersetzt keinen Test der kreativen Auswahl an realen Urlaubsfotos.

## Voraussetzungen einmal prüfen

Python 3.9+, Node 22/24, npm, FFmpeg/ffprobe und ein von Remotion unterstützter Chromium-Browser. Die vorhandene Setup-Auswahl aus [SETUP](../SETUP.md) übernehmen; keine neue MCP-Installation ist für diesen Weg nötig.

```sh
python3 tools/film.py doctor
python3 -m venv .venv
```

Danach die virtuelle Umgebung aktivieren (`source .venv/bin/activate` auf macOS/Linux, `.venv\Scripts\Activate.ps1` in Windows PowerShell) und:

```sh
python -m pip install -r requirements-analysis.txt
npm --prefix studio ci
```

`doctor` prüft nur Verfügbarkeit. Es installiert nichts und bestätigt keinen funktionierenden Browser. Die Analysepakete sind optional für das Handbuch und die bisherigen Prüfwerkzeuge, aber nötig für Kontaktbögen, Beat-Kandidaten und den Beispieldatensatz.

## Das Beispiel vollständig ausführen

Alle folgenden Befehle laufen vom Repository-Hauptordner aus. `local/demo-v001` muss neu sein. Bei einer Wiederholung `v002` verwenden, damit frühere Ergebnisse erhalten bleiben.

```sh
python tools/demo_project.py local/demo-v001
python tools/analyze_media.py local/demo-v001/media local/demo-v001/review
python tools/beat_candidates.py local/demo-v001/media/original-rhythm.wav local/demo-v001/beat-candidates.json --fps 30 --source-in 0.5
python tools/editing.py validate local/demo-v001/timeline.json --media-root local/demo-v001
python tools/editing.py cut-list local/demo-v001/timeline.json local/demo-v001/cuts.csv --media-root local/demo-v001
python tools/editing.py beat-report local/demo-v001/selected-beats.json local/demo-v001/beat-report.json
python tools/film.py render local/demo-v001/timeline.json local/demo-v001/preview.mp4 --media-root local/demo-v001 --scale 0.5
```

Ergebnis: `preview.mp4`, `preview.qa.json`, `preview.props.json`, `preview.props.assets.json`, Kontaktbögen und bearbeitbare `timeline.json`. Der Renderer kopiert nur die referenzierten Medien in einen eigenen ignorierten Ordner unter `studio/public/local/`; Originale bleiben unverändert. Der Export wird vollständig decodiert und auf Framezahl geprüft. Sicht- und Hörstatus bleiben zunächst offen.

`--source-in 0.5` entspricht dem Musikausschnitt der Beispiel-Timeline. Bei eigener Musik Quellstart, Timeline-Start und gegebenenfalls konstantes Tempo aus dem tatsächlich geschnittenen Audiobereich übernehmen; sonst liegen die Kandidaten im falschen Zeitbezug.

Bei Problemen mit Remotions gebündeltem Browser einen **vorhandenen** Chrome mit `--browser-executable /pfad/zu/chrome` angeben; `--gl angle` war ein funktionierender Mac-Fallback. Pfad selbst ermitteln, nicht einen fremden Benutzerpfad übernehmen. Ein gesperrter Browser-/Port-Start kann eine Host-Berechtigung benötigen; er ist kein Beweis eines Timeline-Fehlers.

Solange nach einem Fehlschlag noch kein MP4 existiert, lässt sich derselbe Exportname mit dem Browser-Fallback erneut versuchen. Vorhandene Props und Asset-Berichte bleiben erhalten; der nächste Versuch bekommt `attempt-002` usw. als Hilfsdateinamen. Existiert bereits ein teilweise geschriebener Film oder QA-Bericht, einen neuen Exportnamen wählen. Es wird nichts überschrieben.

Nach der Vorschaukorrektur einen neuen Master exportieren:

```sh
python tools/film.py render local/demo-v001/timeline.json local/demo-v001/master-v001.mp4 --media-root local/demo-v001 --scale 1
```

## Eigene Medien verwenden

1. Kontaktbögen mit `analyze_media.py MEDIENORDNER NEUER_REVIEWORDNER` erzeugen. Der Reviewordner liegt außerhalb des Medienordners. `review.json` enthält Hashes, exakte Duplikate, Ähnlichkeitsgruppen und technische Indizien; jede Entscheidung beginnt als `review`. Videos erhalten drei zeitlich beschriftete Stichproben. Mehrere Kontaktseiten entstehen automatisch.
2. Kandidaten anhand Originalauflösung und Kontext auswählen. Die Analyse löscht nichts und wählt keine Person als besonders schön oder wichtig aus. `--roi-json local/focus.json` kann pro relativem Dateipfad eine geprüfte Fokusregion `[links, oben, rechts, unten]` zwischen 0 und 1 vorgeben. Ohne Region wird das gesamte Bild gemessen. Vergleichbare Schärfewerte brauchen vergleichbare Ausschnitte und Größen. HEIC muss mit einem vorhandenen lokalen Werkzeug konvertiert oder ein passender Decoder ergänzt werden.
3. Musik lokal mit passenden Rechten bereitstellen. `beat_candidates.py` liefert spektrale Onsets und Tempo-Hypothesen, **keine bestätigten Downbeats**. `--source-in`, `--timeline-start`, `--playback-rate` bilden den gewählten Ausschnitt ab. Analyse standardmäßig maximal zehn Minuten; längere Abschnitte ausdrücklich mit `--max-seconds` wählen oder passend kürzen. Gute Akzente anhören und erst danach in das `beats_seconds`-Format für `beat-report` übernehmen.
4. `timeline.json` mit relativen Medienpfaden, bewusst gewählten Shots und festem Timing füllen. Mit `film.py prepare` oder `render` prüfen. Das Tool schlägt keine Geschichte allein aus Scores vor.

## Renderfähiges Manifest

Die Basisfelder bleiben wie in [tools/README](../tools/README.md). Zusätzlich braucht ein renderfähiger Film `width`, `height`, `style` und je Shot `kind` (`image`/`video`). Medienpfade beziehen sich auf `--media-root`.

- `fit: "contain-blur"` erhält das vollständige Motiv vor einer unscharfen Kopie desselben Mediums; `cover` füllt die Fläche und muss auf Beschnitt geprüft werden. Default ist `contain-blur`. Hintergrundvideos sind stumm und zeitlich mit dem Vordergrund gekoppelt.
- `zoom` ist optional, standardmäßig 1. Nur nach individueller Motivprüfung erhöhen (maximal 1,15). Keine automatische Gesichtsverschiebung. Kurze `label` erscheinen oben links; bei Gesichtern dort das Label entfernen/anders gestalten.
- Video-`source` enthält eigene fps, `in_frame`, exklusives `out_frame` und optional konstantes `playback_rate`. Das Tool prüft tatsächliche Quellframes und Bildrate per ffprobe. Auffällige fps-Abweichungen erfordern einen geprüften CFR-Proxy. Ein Vergleich von Durchschnitts-/Nominalrate erkennt nicht jede VFR-Abweichung; anspruchsvolle VFR-/Retime-Projekte brauchen eine Zeitstempelabbildung.
- Originalton eines Videos ist standardmäßig stumm. `volume: 0.4` aktiviert bewusst die gewählte Stelle. In `audio` stehen separate Musik-/Soundspuren mit `asset`, `start_frame`, `duration_frames`, `volume`, optional `source_in_seconds`, `fade_in_frames`, `fade_out_frames`.
- `duck` einer Audiospur enthält Intervalle mit absoluten Timeline-`start_frame`, exklusivem `end_frame`, `volume`. Die Musik fährt über sechs Frames herunter/hoch; der Mix muss angehört werden. Werte sind Amplitudenfaktoren, keine LUFS-Ziele.
- `effects` unterstützt `whip` und `sticker` mit transparentem `asset` sowie `gag`: `spin`, `download`, `walkoff`, `float`, `launch`, `boing`. Sticker brauchen ausdrücklich `style: "funny"`. Nicht unterstützte Effekte werden zurückgewiesen.

`ManifestFilm` ist absichtlich eine JSON-gesteuerte Vorlage. Einzelne Shots in der JSON ändern; die generierten Reihen sind keine unabhängig in JSX gespeicherten Studio-Clips. Für komplexe Gesichtsmatches, Karten und Tracking den bestehenden Effektbaukasten in eine eigene Komposition übernehmen.

## Sichtbar im Studio bearbeiten

```sh
python tools/film.py prepare local/demo-v001/timeline.json local/demo-v001/studio-props.json --media-root local/demo-v001
npm --prefix studio run dev -- --no-open --props=../local/demo-v001/studio-props.json
```

In der ausgegebenen lokalen URL `ManifestFilm` öffnen. Nach Änderungen am ursprünglichen Manifest neue Props mit neuem Versionsnamen vorbereiten. Die unabhängigen `EffectsLab`- und `PortraitFraming`-Demos bleiben verfügbar.

Bei `--props` kann der Studio-Inspector weiterhin Defaultwerte wie `360` Frames und `serious` zeigen und darauf hinweisen, dass CLI-Props Vorrang haben. Maßgeblich sind die vorbereitete JSON-Datei und die tatsächliche Timeline (beim Beispiel `540` Frames und `funny`). Änderungen im Inspector lassen sich in diesem Modus nicht als Quellmanifest speichern; dafür die JSON-Datei bearbeiten und Studio mit neuen Props starten.

## Abnahmekriterien

- Kontaktbogen zeigt das Duplikat, die weiche Variante, Hochformat und Videostichproben nachvollziehbar.
- 24-fps-Quellvideo wird ab Sekunde 1 für 3 Sekunden in der 30-fps-Timeline gezeigt.
- 540 Frames / 18 Sekunden; vollständiger Decode; keine unbeabsichtigten Schwarzintervalle.
- Hochformatpersonen bleiben vollständig; Spin und Wisch sind im lustigen Beispiel sichtbar.
- Anfang/Ende der Musik sowie gegebenenfalls Ducking tatsächlich anhören. Eine rechnerisch passende Markerliste ist kein Hörtest.
- Prüfbericht zum tatsächlichen Exporthash speichern; Bericht eines alten Exports nicht übernehmen.
