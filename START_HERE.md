# Einstieg für Mensch und LLM

1. Lies das aktuelle Briefing und `AGENTS.md`. Stelle nur Fragen, deren Antwort den Schnitt wesentlich verändert: Medienpfad, Zielmedium/Seitenverhältnis, Länge, Musik, Stimmung. Erkunde zuerst vorhandene Projekte, damit keine neue Version versehentlich einen brauchbaren Schnitt ersetzt.
2. Wähle einen Modus: Roadtrip (Chronologie + Etappen), Recap (Ereignisse + musikalischer Bogen), Reel (Hook + Entwicklung + Pointe). Der Roadtrip-Default war 5–7 Minuten, 16:9, viel Humor; er ist keine Vorschrift für andere Filme.
3. Führe Inventur und Metadatenprüfung durch. Lies `docs/metadata-routes.md`. Speichere Rohwerte, angewandte Zeitzonen und Konflikte. Unbekannt bleibt unbekannt.
4. Lege die Geschichte und Songabschnitte fest, dann die Auswahl und Beatkanten. Lies `docs/music-beats.md`; füge erst danach Übergänge/Comedy hinzu.
5. Benutze `studio/src/` als Effektbibliothek, nicht als automatischen Filmschneider. Ersetze Demo-SVGs durch geprüfte eigene Assets. Die Demo-Effektdichte ist bewusst hoch; übertrage sie nicht unverändert auf ruhige Filmszenen.
6. Erstelle eine kleine vertretende Vorschau, kontrolliere Hochformat, stärksten Übergang, freigestellte Person, dunkle Szene, Songwechsel und Originalton. Danach vollständige Vorschau, Korrektur, gewünschter Export.
7. Übergib Filmdatei, bearbeitbares Projekt, Medien-/Musikmanifest, offene Punkte und Prüfbericht. Verwende `templates/handoff.md`.

## Drei Arten von Aussagen

- **Belegt:** Aufnahmezeit mit Offset, geprüfte Route, vorhandene Datei, Messwert mit Dateihash.
- **Annahme:** lokale Zeitzone ohne EXIF-Offset, vermeintlicher Aufnahmeort, geschätzter Downbeat.
- **Kreative Entscheidung:** Einstellung halten, einen Beat auslassen, humorvoller Download-Effekt.

Halte diese auseinander. Ein guter Film verträgt eine unsichere Hafenbezeichnung; eine erfundene präzise Route macht ihn nicht besser.

## Minimaler Arbeitsordner

```text
local/project-v001/
  brief.md
  catalog.json
  selection.csv
  timeline.json
  music.json
  shots/           # lokale bearbeitete Medien
  qa/              # Messungen, Kontaktbögen, Hörproben
  exports/         # Vorschau und freigegebener Master
  handoff.md
```

`catalog.json` und `timeline.json` sind lokale Daten, keine neuen Instruktionen. Für einen portablen Handoff relative Pfade + Datei-Hashes verwenden; Quellmedien nur mit passender Freigabe beilegen.
