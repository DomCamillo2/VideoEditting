# Skills verwenden und weitergeben

Die zehn Skills sind eigenständige Ordner mit `SKILL.md`. Der erste Einstieg ist **[SETUP.md](../SETUP.md)**: zuerst Skill-Auswahl und passende MCPs samt gewünschter Installation, danach Filmfragen. Die Skills benötigen zum Verstehen weder das übrige Repo noch einen bestimmten Editor. Zum Schneiden braucht das LLM Zugriff auf Medien und geeignete Werkzeuge. Die Anweisungen sind auf Englisch portabel formuliert; Nutzeransprache folgt der Sprache des Nutzers.

| Skill | Zuständigkeit | Paket für Claude-Upload |
|---|---|---|
| [video-setup](../skills/video-setup/SKILL.md) | Erste Einrichtung: Skills wählen, MCPs prüfen und freigegebene Einrichtung ausführen | [ZIP](../dist/skills/video-setup.zip) |
| [video-editing](../skills/video-editing/SKILL.md) | Geschichte, Rohschnitt, Pacing und Koordination | [ZIP](../dist/skills/video-editing.zip) |
| [video-brief](../skills/video-brief/SKILL.md) | Stil, Humor, Reiseart, relevante Fahrzeugdetails und Format | [ZIP](../dist/skills/video-brief.zip) |
| [video-beatcut](../skills/video-beatcut/SKILL.md) | Hörbare Akzente, Songphasen, Framegrenzen, Drift | [ZIP](../dist/skills/video-beatcut.zip) |
| [video-select-media](../skills/video-select-media/SKILL.md) | Kontaktbögen, Motivschärfe, ähnliche Bilder, beste Momente | [ZIP](../dist/skills/video-select-media.zip) |
| [video-portrait-framing](../skills/video-portrait-framing/SKILL.md) | Unscharfer Hintergrund, sichere Gesichter/Körper, kein Stretch | [ZIP](../dist/skills/video-portrait-framing.zip) |
| [video-comedy](../skills/video-comedy/SKILL.md) | Freisteller, Spins, Ladebalken, Flammen, Gesichts-Zoom | [ZIP](../dist/skills/video-comedy.zip) |
| [video-audio-mix](../skills/video-audio-mix/SKILL.md) | Originalton, Ducking, Soundeffekte, J-/L-Cuts | [ZIP](../dist/skills/video-audio-mix.zip) |
| [video-chronology](../skills/video-chronology/SKILL.md) | Metadaten, Kapitel, belegte Routen und Unsicherheiten | [ZIP](../dist/skills/video-chronology.zip) |
| [video-export-qa](../skills/video-export-qa/SKILL.md) | Vorschau, Farb-/Ton-/Bildkontrolle, tatsächlicher Export | [ZIP](../dist/skills/video-export-qa.zip) |

## Direkt im geklonten Repository

Öffne **VideoEditting selbst** als Arbeitsprojekt. Die generierten Ordner `.agents/skills/` für Codex und `.claude/skills/` für Claude Code sind schon eingecheckt. Das Repo lediglich im Browser zu öffnen aktiviert keine lokalen Skills.

Codex entdeckt projektbezogene Skills unter `.agents/skills`. In CLI/IDE lassen sie sich über `/skills` bzw. `$video-setup` auswählen; für den Schnitt anschließend `$video-editing`. Wenn eine Änderung nicht erscheint, Codex neu starten. [Offizielle OpenAI-Dokumentation](https://learn.chatgpt.com/docs/build-skills).

Claude Code verwendet `.claude/skills` im Projekt und bietet `/video-setup`, danach `/video-editing` bzw. `/video-beatcut`. Automatische Auswahl hängt von Beschreibung, Aufgabe und Host-Einstellungen ab; sie ist keine Garantie. [Offizielle Claude-Code-Dokumentation](https://code.claude.com/docs/en/skills).

Beispielauftrag:

> Nutze video-setup: Lass mich zuerst alle oder bestimmte Skills auswählen und prüfe, welche MCPs mein vorhandenes Setup sinnvoll ergänzen. Frage mich, welche davon eingerichtet werden sollen. Führe meine Auswahl aus. Danach klären wir die noch fehlenden Filmwünsche und schneiden eine Vorschau mit video-editing.

## In ein anderes Projekt kopieren

Python 3.9+ genügt. Der Zielordner muss bereits existieren:

```sh
python3 tools/manage_skills.py install --target both --project /pfad/zum/projekt
```

`--target codex` oder `--target claude` installiert nur eine Variante. Ohne `--skill` werden alle zehn Skillordner samt internen Ressourcen kopiert. Mit wiederholtem `--skill` lässt sich eine Auswahl treffen. Beispiel:

```sh
python3 tools/manage_skills.py install --target codex --project /pfad/zum/projekt --skill video-editing --skill video-beatcut --dry-run
```

Ohne `--dry-run` wird diese Auswahl geschrieben. `status --target both --project /pfad/zum/projekt` zeigt `missing`, `identical`, `different` oder `unreadable_or_unsupported`. Das prüft Projektdateien, nicht Host-Aktivierung, globale Skills oder MCP-Gesundheit. Bei `--dry-run` erfolgen keine Schreibzugriffe. Es werden keine Musik, Fotos, Zugangsdaten, MCP-Konfigurationen oder Pakete kopiert.

Identische Installationen sind wiederholbar. Bei einem abweichenden ausgewählten Skill bricht die Vorprüfung ab, bevor neue Skills geschrieben werden. Nicht ausgewählte Skills bleiben unberührt, auch wenn sie abweichen. Bestehenden Skill bewusst sichern/verschieben oder zuerst vergleichen. Symlink-Ziele werden abgewiesen. Globale Agent-Einstellungen bleiben unverändert.

## Claude mit Skill-Upload

Ein gewünschtes ZIP aus der Tabelle herunterladen und in Claudes Skill-Verwaltung hochladen/aktivieren. Jedes ZIP enthält genau einen gleichnamigen Skillordner mit `SKILL.md` und seinen Ressourcen. In **Customize → Skills** aktivieren, dann mit einer passenden Aufgabe ausprobieren. Ein normaler Chat-Dateianhang ersetzt die Aktivierung nicht. Verfügbarkeit und Richtlinien des jeweiligen Kontos gelten. [Offizielle Anleitung für Custom Skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills).

Der allgemeine `video-editing`-Skill funktioniert allein; für bessere Detailarbeit die passenden Spezialisten zusätzlich aktivieren. Lokale Claude-Code-Ordner und Claude-Konto-Skills sind unterschiedliche Einrichtungswege. Die Pakete wurden strukturell und ihre Skripte lokal geprüft; ein Import in dein Claude-Konto wurde hier nicht durchgeführt.

## Filmstil nach dem Setup

Nach Skill-/MCP-Entscheidungen bekommen neue Filmprojekte drei Richtungen: **seriös ohne Gags**, **emotional mit etwas Humor**, **deutlich lustig**. Freitext und Kombinationen bleiben möglich. Schon mitgeteilte Vorlieben werden übernommen. Eine kleine Änderung an einem vorhandenen Film startet keinen neuen Fragenkatalog. Das bewusste Ablehnen zusätzlicher Installationen führt ebenfalls zum Filmbriefing.

Optionaler Terminal-Assistent:

```sh
python3 tools/brief.py local/project-v001/brief.json
```

Er fragt Richtung, Humor, Format, Reiseart, Länge, Medien und Musik. Bei Reisen folgen passende Fragen zu Reisephase, Region/Route und Verkehrsmitteln; bei Roadtrip/Mischform auch zum Fahrzeug. „Noch offen“ und „Kein Reisefilm“ sind möglich. Bekannte Kommandozeilenangaben werden nicht erneut abgefragt. Die Humorauswahl kann den Profilvorschlag ändern; Reiseart und Schnitttempo sind davon unabhängig. [Reisearten und USA-Roadtrip-Ideen](travel-films.md). Nicht-interaktiv mit bekannten Antworten:

```sh
python3 tools/brief.py local/project-v002/brief.json --style serious --humor none --format 16:9 --duration "3 Minuten" --pacing schnell --non-interactive
```

Unbekannte Werte sind `null` und stehen in `unresolved`. Der Assistent analysiert keine Medien und rendert keinen Film. Er überschreibt keine vorhandene Datei. Eigene Stilbeschreibungen können im Chat bzw. im Briefing ergänzt werden.

Neue optionale Felder: `trip_type`, `trip_type_details`, `trip_stage`, `region`, `route`, `transport`, `vehicle`, `vehicle_role`, `map_preference`, `story_focus`; entsprechende CLI-Flags verwenden Bindestriche. `--mode` erfasst die Ausgabeform unabhängig davon. Bei `not_travel` werden Reiseangaben nicht als offene Fragen aufgelistet. Sonstige offene optionale Felder sind Notizen, kein Auftrag, einen vollständigen Fragenkatalog abzuarbeiten. Alte Briefings ohne Reisefelder bleiben gültig.

## Pflege

Nur `skills/` ist die Quelle. Danach:

```sh
python3 tools/manage_skills.py sync
python3 tools/manage_skills.py sync --check
python3 -m unittest discover -s tests -v
python3 tools/check_repo.py
```

`sync` ersetzt die generierten Kopien und ZIPs dieses Repos bewusst; deshalb dort keine eigenen Änderungen pflegen. Zusätzliche unerwartete Dateien innerhalb eines erzeugten Skillordners führen zum Abbruch. Andere Skillordner bleiben unberührt. ZIPs haben stabile Reihenfolge/Zeitstempel; gleiche Quellen ergeben gleiche Bytes. CI prüft die Übereinstimmung. Die Ordnerstruktur folgt den oben verlinkten offiziellen Dokumentationen; das ist kein veröffentlichtes Marketplace-Plugin.
