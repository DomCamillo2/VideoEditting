# Prüfstand

Stand: 11.10.2026. Ergebnisse für den Toolkit-Starter, getrennt vom historischen Roadtrip.

- 24 Python-Tests bestanden: Offsets, DST-Fälle, Konflikte, Duplikate, Pfade, Framequantisierung, Basis-Timeline, Recap-Ausnahme und Schreibschutz.
- Beispiel-Timeline ohne Fehler/Warnungen validiert; Beatreport-Smoke-Test bestanden.
- Skill-Frontmatter mit dem Skill-Creator-Validator geprüft.
- Remotion TypeScript/Lint und Bundle bestanden.
- Frische separate Kopie ohne node_modules: npm ci, Lint und Bundle bestanden (Node 24 / macOS).
- npm-Audit nach gezieltem typescript-eslint-Update: 0 bekannte Schwachstellen am Prüfdatum. Das ist keine Garantie für künftige Versionen.
- Synthetische Demo vollständig exportiert: 810 Frames, 27 Sekunden, 960×540, 30 fps, H.264, yuv420p, BT.709. Vollständiger Decode bestanden, keine Schwarzintervalle erkannt. [Messbericht](demo-qa.json).
- Neun repräsentative Frames des finalen Encodes visuell kontrolliert. Zusätzliche Bewegungsphasen und Grenzen des ersten Testencodes geprüft; drei Kontaktbögen des finalen Encodes liegen unter [assets](assets/). Bewusstes Verlassen der Leinwand bei Rakete/Davonlaufen ist Teil des Effekts.
- Die tatsächliche Demo misst −32,88 LUFS / −18,13 dBTP; sie ist eine leise synthetische Timing-Demonstration, kein fertig gemasterter Musikfilm.
- Musikdateien vor der Veröffentlichung gegen die drei im Manifest gespeicherten SHA-256-Hashes geprüft.
- Lokale Markdown-Verweise und öffentliche Pfad-Hygiene geprüft. GitHub Actions führt Tests, Timeline-Prüfung, Linkprüfung, Lint und Build bei Push/PR aus.

## Grenzen

ExifTool war auf dem Testrechner nicht installiert; seine Extraktion wurde nicht live getestet. Der Import gruppierter Metadaten, Auswahl von Aufnahmezeitpunkten, Hashing und Konfliktbehandlung sind mit lokalen Fixtures geprüft. Die CLI benennt die fehlende Abhängigkeit ausdrücklich.

Audio wurde technisch gemessen, nicht vom Modell manuell angehört. Die Demo-Sounds sind bewusst leise. Kein Beleg für automatisch richtigen Beatcut bei beliebigen Songs.

Das Lint-Preset nutzt ESLint 9, das npm inzwischen als nicht mehr unterstützt markiert. Für die getestete Remotion-Version blieb diese kompatible Kombination gepinnt; ein späteres Upgrade gemeinsam mit dem Preset prüfen. Keine laufende öffentliche Web-App wird durch dieses Repo bereitgestellt.
