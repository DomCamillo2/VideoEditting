# Skill-Prüffälle

Stand 11.10.2026. Die folgenden Fälle wurden gegen die Anweisungen gelesen und ihre erwarteten Handlungen überprüft. Das ist eine redaktionelle Prüfung der Regeln, **kein** protokollierter Lauf eines separaten Codex-/Claude-Modells. Die ausführbaren Tests prüfen Installer, Paketgrenzen und Briefing-Logik; sie beweisen keine kreative Schnittqualität.

| Fall | Erwartetes Verhalten | Zuständiger Skill |
|---|---|---|
| „Ich binde dieses GitHub erstmals ein“ | Zuerst alle/ausgewählte/keine Skills, dann sinnvolle MCPs mit Installation; noch keine Stilfrage | video-setup |
| Vollständiger Klon, alle Projekt-Skills vorhanden | Vorhandene Kopien benennen; Nutzung/Übernahme statt fingierter Neuinstallation anbieten | video-setup |
| Browser, Doku, Dateizugriff bereits nutzbar | Keine redundanten MCPs nötig; Beibehalten als gültige Auswahl anbieten | video-setup |
| „Nur Beatcut und Bildauswahl, keine MCPs“ | Nur gewählte Skillkopien installieren; Ablehnung merken, anschließend Filmbriefing | video-setup |
| Nutzer stimmt konkretem MCP und Projektumfang zu | Bestehende Konfiguration ergänzen, Login/Verbindung prüfen; nicht dieselbe Zustimmung erneut fragen | video-setup |
| „Mach aus meinem Urlaub einen Film“, Setup steht, Stil fehlt | Drei Stilrichtungen anbieten; Format/Länge knapp klären, Inventur parallel möglich | video-editing, video-brief |
| „Seriös, schnell, 90 Sekunden, 9:16, keine Gags“ | Vorgaben übernehmen, nicht noch einmal Stil abfragen; schneller Schnitt ohne Comedy | video-brief, video-editing |
| „Bei der bestehenden lustigen Version nur mehr Gags“ | Bestehendes Briefing nutzen, neue Effekte dosiert hinzufügen, Timing danach prüfen | video-comedy |
| „Nur die README korrigieren“ | Kein Filmbriefing, keine Medienanalyse, keine Comedy | Kein Video-Skill nötig |
| Fünf ähnliche Fotos, zwei mit weichen Gesichtern | Cluster vergleichen, bestes natürliches Gruppenfoto wählen; zweite Wahl nur mit neuem Inhalt | video-select-media |
| Scharfes Gesicht vor starkem Bokeh | Nicht wegen niedrigem Gesamtschärfewert aussortieren | video-select-media |
| Ein weicher, aber einzigartiger emotionaler Moment | Gegen Bedeutung abwägen, begründet behalten oder in Reserve statt löschen | video-select-media |
| Enge Hochformat-Gruppe soll Breitbild werden | Gleiches Medium als Blur-Hintergrund, Köpfe erhalten, auf zusätzlichen Zoom verzichten | video-portrait-framing |
| Bewegtes Portraitvideo mit Blur-Kopie | Beide Ebenen auf identischen Quellframes; keine doppelte Tonspur | video-portrait-framing |
| Alle Marker sitzen rechnerisch, Song klingt versetzt | Audio-Trims, Phase und Halb-/Doppeltempo prüfen; Hörkontrolle nicht durch Zahlen ersetzen | video-beatcut |
| Eine überlappende Transition wird eingefügt | Gesamtdauer und nachfolgende Beatgrenzen neu berechnen | video-beatcut, video-comedy |
| Cutout soll über die Leinwand rennen | Originalpixel-Maske prüfen, Stickerbewegung als solche behandeln, Gesicht nicht generativ ändern | video-comedy |
| Hafen der Rückfahrt unklar, Nutzer sagt egal | Neutral beschriften und Unsicherheit dokumentieren; keine Fähre erfinden | video-chronology |
| Musik überdeckt kurze Aussage | Nur relevante Originaltonstelle nutzen, Musik passend absenken und Mix anhören | video-audio-mix |
| Build bestanden, Export noch nicht angesehen | Tatsächliche Datei prüfen; Sicht-/Hörstatus offen lassen bis durchgeführt | video-export-qa |

## Reproduzierbare Prüfungen

`python3 -m unittest discover -s tests -v` enthält 21 Skill-/Briefingtests: Profilvorgaben, unabhängige Humor-/Tempowahl, ungültige Werte, kein Überschreiben, nicht-interaktiver Ablauf, fehlende Stilwahl, Dialog samt Fehleingabe, Abbruch ohne Datei, interne Paketressourcen, deterministische ZIPs, beide Installationsziele, Konflikt ohne Teilinstallation, Symlinks, Drift in Kopien, das ausgepackte Standalone-Skript sowie sechs Prüfungen für Skill-Teilauswahl, Dry-Run, unbekannte Auswahl, Zielvalidierung und lesenden Status.

Für einen zukünftigen echten Host-Test: in einem neuen Projekt die jeweilige Skill-Auswahl öffnen, die Fälle oben mit synthetischen oder freigegebenen Medien ausführen und tatsächlich geladenen Skill, Host-/Modellversion, Ergebnisdateien und Abweichungen protokollieren. Nicht nur das Vorhandensein eines Skillnamens als erfolgreichen Schnitt werten. Keine privaten Medien für eine Evaluation hochladen, wenn nur lokale Nutzung autorisiert ist.
