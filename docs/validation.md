# Prüfstand

Stand: 11.10.2026. Ergebnisse für den Toolkit-Starter, getrennt vom historischen Roadtrip.

- 93 Python-Tests bestanden, mit den optionalen Pillow-/NumPy-Abhängigkeiten: 69 bestehende Prüfungen für Metadaten, Timeline, Beatbericht, Quellbereiche, Handoff, Veröffentlichung und Skill-Installation; 24 neue Prüfungen für Orientierung, Schärfevergleich, Fokusregionen, stabile Medien-IDs, Duplikate, Ähnlichkeitsgruppen, Onsets, Renderdaten, rationale Tempo-/Audioangaben, tatsächliche Quellstreams, Browser-Retry und Überschreibschutz. Ohne Analysepakete werden die betreffenden Tests ausdrücklich übersprungen.
- Beide Beispiel-Timelines ohne Fehler/Warnungen validiert; CLI-Smoke-Tests für CSV-Schnittliste und Beatreport bestanden. Quell-In/Out und Timeline-Grenzen im CSV kontrolliert.
- Alle zehn Skill-Frontmatter mit dem Skill-Creator-Validator geprüft. Interne Ressourcen sind ohne Repository verfügbar; Kopien für Codex/Claude und ZIPs stimmen mit ihren Quellen überein. Installation beider Host-Varianten in einem temporären Projekt und identische Wiederholungsinstallation getestet.
- Remotion TypeScript/Lint und Bundle bestanden.
- Frische separate Kopie ohne node_modules: npm ci, Lint und Bundle bestanden (Node 24 / macOS).
- npm-Audit nach gezieltem typescript-eslint-Update: 0 bekannte Schwachstellen am Prüfdatum. Das ist keine Garantie für künftige Versionen.
- Bisherige EffectsLab-Demo vollständig exportiert: 810 Frames, 27 Sekunden, 960×540, 30 fps, H.264, yuv420p, BT.709. Vollständiger Decode bestanden, keine Schwarzintervalle erkannt. [Messbericht](demo-qa.json).
- Neun repräsentative Frames des finalen Encodes visuell kontrolliert. Zusätzliche Bewegungsphasen und Grenzen des ersten Testencodes geprüft; drei Kontaktbögen des finalen Encodes liegen unter [assets](assets/). Bewusstes Verlassen der Leinwand bei Rakete/Davonlaufen ist Teil des Effekts.
- Die EffectsLab-Demo misst −32,88 LUFS / −18,13 dBTP; sie ist eine leise synthetische Timing-Demonstration, kein fertig gemasterter Musikfilm.
- Die drei zuvor hochgeladenen fremden Songs und ihr Manifest wurden wegen fehlender Weitergaberechte entfernt, einschließlich ihrer Dateien in der veröffentlichten Git-Historie. MP3-Dateien sind ohne Ausnahme von Git ausgeschlossen. Eigene synthetische Demo-Sounds bleiben enthalten.
- Lokale Markdown-Verweise, öffentliche Pfad-Hygiene und 16 eigene Demo-Assets gegen Herkunfts-/Hash-Verzeichnis geprüft. GitHub Actions führt zusätzlich zur bisherigen Prüfung jetzt die synthetische Medienanalyse, Onset-Ermittlung und einen vollständigen 540-Frame-Testexport aus; Vorschau und Prüfbilder werden sieben Tage als CI-Artefakt aufbewahrt.

## Neuer vollständiger Workflow

Der [Schnellstart](end-to-end.md) wurde mit Python 3.9, Node 24 und lokalem Chrome/ANGLE auf macOS ausgeführt. Er erzeugt eigene Medien, sichtet sie und rendert die JSON-Timeline über `ManifestFilm`.

- Sieben Medien, vier Ähnlichkeitsgruppen, keine Lesefehler. Exaktes Duplikat erkannt; weiche Variante zusammen mit ihrem vergleichbaren Motiv gruppiert. [Kontaktbogen](assets/pipeline-selection.jpg). Alle Auswahlentscheidungen bleiben überprüfbar; der Datensatz hat absichtlich bekannte Varianten.
- 39 Onset-Kandidaten, stärkste Tempo-Hypothese 120 BPM; auch 60 BPM erscheint. Die Analyse wird mit dem tatsächlichen Audio-Quellstart von 0,5 Sekunden abgebildet. Das zeigt die Mehrdeutigkeit, nicht automatisch richtige Downbeats.
- Vorschau 960×540 und lokaler Master 1920×1080: jeweils 540 Frames / 18 Sekunden, 30 fps, H.264/BT.709, vollständiger Decode und keine erkannten Schwarzintervalle. [Vorschau](../examples/pipeline-preview.mp4), [hashgebundener Bericht](pipeline-qa.json).
- Neun Frames des fertigen Vorschau-Encodes visuell kontrolliert: volle Hochformatfiguren, derselbe Inhalt im unscharfen Hintergrund, Video, Spin und Wisch. [Prüfbilder](assets/pipeline-frames.jpg).
- Quelltrim zusätzlich an Pixeln kontrolliert: Timeline-Frame 216 entspricht dem Quellvideo um Frame 28 bei 24 fps; es zeigt den gewählten Ausschnitt ab Sekunde 1. Dies ist ein Stichprobentest, keine allgemeine VFR-Zertifizierung.
- Audio technisch gemessen: −24,72 LUFS / −10,19 dBTP; Kanal-Amplitudenfaktor 0,7492 bei Vorgabe 0,75. Wegen der periodischen Quelle beweist die Korrelation allein keinen Versatz um 0,5 Sekunden. Ein Hörtest bleibt offen. `loudnorm output_*` im Rohbericht ist verworfene Filterausgabe, keine angewandte Normalisierung.
- [Unabhängiger Übergabetest](handoff-test.md): Ein Agent mit frischem Kontext konnte anhand einer separaten Repository-Kopie Vorschau, Master und Studio erzeugen. Gefundene Probleme beim Browser-Retry und missverständliche Studio-Anzeigen wurden behoben bzw. erklärt.

[Verhaltensfälle und Grenzen der Skill-Prüfung](skill-evaluation.md).

## Grenzen

Die Skills wurden strukturell validiert und anhand konkreter Verhaltensfälle redaktionell geprüft. Es wurde kein automatisierter Codex-/Claude-Modellvergleich und kein Import in ein Claude-Konto durchgeführt. Automatische Skill-Auswahl sowie gute kreative Entscheidungen hängen vom eingesetzten Modell und dessen Werkzeugen ab. Die Bildauswahl-Anleitung ist kein neu trainierter Unschärfe-/Ästhetik-Klassifikator.

Die MCP-Auswahl und Beispiele stammen aus den verlinkten aktuellen Herstellerdokumentationen. Beim Erstellen dieses Onboardings wurde kein neuer MCP-Server installiert, kein Login durchgeführt und keine bestehende Host-Konfiguration verändert. Der Setup-Skill soll die künftige Nutzerwahl umsetzen; ein GitHub-Link allein erzwingt keinen Installationsdialog. `status` im Installer prüft nur Projekt-Skilldateien.

ExifTool war auf dem Testrechner nicht installiert; seine Extraktion wurde nicht live getestet. Der Import gruppierter Metadaten, Auswahl von Aufnahmezeitpunkten, Hashing und Konfliktbehandlung sind mit lokalen Fixtures geprüft. Die CLI benennt die fehlende Abhängigkeit ausdrücklich.

Audio wurde technisch gemessen, nicht vom Modell manuell angehört. Die Demo-Sounds sind bewusst leise. Kein Beleg für automatisch richtigen Beatcut bei beliebigen Songs.

Das Lint-Preset nutzt ESLint 9, das npm inzwischen als nicht mehr unterstützt markiert. Für die getestete Remotion-Version blieb diese kompatible Kombination gepinnt; ein späteres Upgrade gemeinsam mit dem Preset prüfen. Keine laufende öffentliche Web-App wird durch dieses Repo bereitgestellt.

[Auditbefunde, Vergleich mit fünf Schnitt-Repositories und bekannte Grenzen](repository-audit.md). Die externen Vergleichswerkzeuge wurden recherchiert, nicht als Anwendungen getestet.
