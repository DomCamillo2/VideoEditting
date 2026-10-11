# Repository-Audit und Vergleich mit Schnittwerkzeugen

Stand: 11.10.2026. Geprüft wurden Einstieg/Skills, CLI und Tests, Medienveröffentlichung, Handoff sowie der Remotion-Starter. Dies ist ein technisches und redaktionelles Audit, kein neuer Praxistest aller Skills in mehreren LLM-Produkten.

## Gefundene Lücken und umgesetzte Änderungen

| Befund | Auswirkung | Änderung |
|---|---|---|
| Ein Shot mit `id: []` brachte `validate()` zum Absturz; ein ungültiger Beatwert wurde nicht als Timeline-Fehler gesammelt | Ein Agent bekam keine brauchbare Fehlerliste | Struktur-, Typ- und Werteprüfung mit Regressionstests |
| `https://…` und Windows-Pfadformen konnten als lokale Assets durchgehen | Eine vermeintlich portable Timeline verwies auf falsche oder externe Medien | Einheitliche relative Pfade; optional `--media-root` für Existenz und Symlink-Grenzen |
| Quelltrims und Quellbildrate fehlten im prüfbaren Manifest | Ein anderer Editor/Agent konnte denselben Ausschnitt nicht zuverlässig nachbauen | Optionale `source`-Bereiche, exklusive Endframes, Dauerprüfung bei unterschiedlichen fps und konstantem Tempo |
| Beatquantisierung rechnete intern mit Floats; eine leere Schnittliste galt als vollständig ausgerichtet | Grenzfälle konnten falsch gerundet bzw. als bestanden gewertet werden | Rationale Rechnung bis zur Framegrenze; keine Erfolgsbehauptung bei null geprüften Schnitten |
| Keine herauslösbare Übersicht der tatsächlichen Schnittentscheidungen | Der Handoff hing am Lesen des gesamten JSON | Neuer `cut-list`-Befehl für eine prüfbare CSV mit Quell- und Timeline-Frames |
| `.gitignore` allein verhindert kein `git add -f` | Entfernte Songs oder andere private Medien könnten wieder in Git landen | `public-assets.json` mit Herkunft/Lizenz/Hash; CI kontrolliert getrackte Medien und private Arbeitsordner |
| Automatik-Werkzeuge wurden kaum nach Aufgabe und Grenzen eingeordnet | Szenenwechsel, Lautstärke oder ein Score könnten als Qualitätsurteil missverstanden werden | Eigenständige Skill-Referenz zu assistierter Auswahl, Proxy-Zuordnung und Rohschnittprüfung |

Das neue Quellbereichs-Beispiel ist [timeline-source.json](../examples/timeline-source.json). Die CSV ist eine menschlich lesbare Schnittliste, kein fertiger OTIO-/Resolve-/Premiere-Importer. Effekte, Audio und Ramps bleiben im Projekt/Manifest; nichts wird still als übertragbar ausgegeben.

## Was andere Repositories gut lösen

| Primärquelle | Beobachtung | Für dieses Repo übernommen |
|---|---|---|
| [Auto-Editor](https://github.com/WyattBlue/auto-editor) | Audio-/Bewegungskriterien, Schnittabstände und Export in Editoren machen einen automatischen Rohschnitt nachbearbeitbar | Automatik als Vorschlag; Atempausen, Reaktionen und absichtliche Ruhe vor dem Entfernen prüfen. Detektorparameter und Originalbereiche dokumentieren |
| [LosslessCut](https://github.com/mifi/lossless-cut) | Markierte Segmente, Labels, CSV-Austausch und Vorschau erleichtern die Materialauswahl | Quellbereiche explizit speichern und als Schnittliste ausgeben. Tatsächliche Grenzen eines verlustfreien Schnitts vor Beatcut prüfen |
| [PySceneDetect](https://github.com/Breakthrough/PySceneDetect), [CLI](https://www.scenedetect.com/docs/latest/cli.html) | Szenenlisten plus Anfang-/Mitte-/Endbilder helfen beim Sichten; adaptive Erkennung berücksichtigt lokale Änderungen bei Kamerabewegung | Szenenerkennung für lange Aufnahmen als optionaler Sichtungsschritt; Detektorgrenze nicht mit Beat oder bestem Moment verwechseln |
| [OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO) | Austausch von Schnittstruktur, Zeitbereichen und externen Medienreferenzen; Medien sind nicht Teil der Timeline | Source- und Timeline-Zeit getrennt, Bildraten explizit, Medienprüfung vor Handoff. Ein echter OTIO-Adapter wäre ein eigener späterer Schritt mit Roundtrip-Tests |
| [Remotion Agent Skills](https://github.com/remotion-dev/skills) | Eigene Fachskills für Markup, Vorschau, Export, Karten und Multimedia statt einer einzigen großen Anleitung | Vorhandene Routerstruktur beibehalten; Spezialwissen zur Auswahl erst bei Bedarf laden und zusammen mit dem Standalone-Skill paketieren |

Die Tabelle ist eine eigene Ableitung aus den verlinkten Projektbeschreibungen und Dokumentationen. Es wurde kein fremder Code, keine Musik und kein fremdes Demo-Asset übernommen. Werkzeuge wurden nicht allein aufgrund dieser Recherche installiert. Auto-Editor, LosslessCut, PySceneDetect und OTIO wurden hier nicht als Anwendungen ausgeführt; ihre beschriebenen Integrationen sind optional, nicht als getestet markiert.

## Öffentliche Assets

[public-assets.json](../public-assets.json) verzeichnet ausschließlich die eigenen Demo-Grafiken, synthetischen Sounds, den Demo-Film und daraus erzeugte Prüfbilder. `tools/check_repo.py` prüft Git-Dateien auch dann, wenn sie mit `-f` entgegen `.gitignore` hinzugefügt wurden. Eine heruntergeladene ZIP ohne eigenes Git-Verzeichnis wird anhand der auslieferbaren Dateien geprüft; lokale Arbeitsordner bleiben dort außen vor.

Bei einer beabsichtigten Änderung eines öffentlichen Assets zuerst Herkunft/Nutzungsrechte und Inhalt prüfen, dann Hash und Herkunftseintrag aktualisieren. Ein passender Hash ist ein Nachweis der geprüften Dateiversion, keine rechtliche Lizenzprüfung. Diese Kontrolle löscht keine alten GitHub-Caches und verhindert keinen direkten Push, wenn vorgeschriebene CI-Prüfungen auf dem Server nicht erzwungen werden.

## Bewusst offene Grenzen

Nachtrag zum ursprünglichen Audit: Der [durchgängige Workflow](end-to-end.md) ergänzt inzwischen Kontaktbögen, Ähnlichkeitsgruppen, Onset-Kandidaten und einen echten JSON-zu-MP4-Renderer. [Prüfstand](validation.md) trennt diesen neuen Test von der früheren EffectsLab-Demo.

- Keine automatische objektive Bewertung von Humor, Attraktivität oder Bildästhetik. Automatische Auswahl bleibt überprüfbar.
- Die einfache Medienprüfung in `editing.py validate` bestätigt Existenz und Pfadgrenzen; `total_frames` bleibt eine deklarierte Angabe. Der neue `film.py`-Renderer misst zusätzlich Quellstreams, Framezahl, Bildrate und Audiolänge. Visuelle Eignung bleibt eine Sichtentscheidung.
- Quellframe-Mapping unterstützt konstante Bildrate und konstante Geschwindigkeit. VFR-Originale benötigen eine geprüfte Zeitstempel-/Proxy-Zuordnung; Speed-Ramps eine eigene Abbildung.
- Kein getesteter Austausch kompletter Remotion-Effekte mit anderen Editoren. CSV-Formelschutz kann Textfelder mit einem führenden Apostroph versehen; JSON bleibt die maschinenlesbare Quelle.
- Die bestehende EffectsLab-Demo blieb unverändert. Der neue ManifestFilm wurde separat in Vorschau- und Masterauflösung gerendert; die Berichte sind getrennt.

Aktueller ausführbarer Prüfstand: [validation.md](validation.md).
