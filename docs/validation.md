# Prüfstand

Stand: 11.10.2026. Ergebnisse für den Toolkit-Starter, getrennt vom historischen Roadtrip.

- 45 Python-Tests bestanden: 24 Prüfungen für Metadaten, Timeline und Beatbericht sowie 21 Prüfungen für Stilwahl, Benutzer-Overrides, offene Angaben, Schreibschutz, Installer-Vorprüfung, Symlink-Abweisung, reproduzierbare ZIPs, Standalone-Briefing, selektive Installation, lesenden Status und Dry-Run ohne Schreibzugriffe.
- Beispiel-Timeline ohne Fehler/Warnungen validiert; Beatreport-Smoke-Test bestanden.
- Alle zehn Skill-Frontmatter mit dem Skill-Creator-Validator geprüft. Interne Ressourcen sind ohne Repository verfügbar; Kopien für Codex/Claude und ZIPs stimmen mit ihren Quellen überein. Installation beider Host-Varianten in einem temporären Projekt und identische Wiederholungsinstallation getestet.
- Remotion TypeScript/Lint und Bundle bestanden.
- Frische separate Kopie ohne node_modules: npm ci, Lint und Bundle bestanden (Node 24 / macOS).
- npm-Audit nach gezieltem typescript-eslint-Update: 0 bekannte Schwachstellen am Prüfdatum. Das ist keine Garantie für künftige Versionen.
- Synthetische Demo vollständig exportiert: 810 Frames, 27 Sekunden, 960×540, 30 fps, H.264, yuv420p, BT.709. Vollständiger Decode bestanden, keine Schwarzintervalle erkannt. [Messbericht](demo-qa.json).
- Neun repräsentative Frames des finalen Encodes visuell kontrolliert. Zusätzliche Bewegungsphasen und Grenzen des ersten Testencodes geprüft; drei Kontaktbögen des finalen Encodes liegen unter [assets](assets/). Bewusstes Verlassen der Leinwand bei Rakete/Davonlaufen ist Teil des Effekts.
- Die tatsächliche Demo misst −32,88 LUFS / −18,13 dBTP; sie ist eine leise synthetische Timing-Demonstration, kein fertig gemasterter Musikfilm.
- Die drei zuvor hochgeladenen fremden Songs und ihr Manifest wurden wegen fehlender Weitergaberechte entfernt, einschließlich ihrer Dateien in der veröffentlichten Git-Historie. MP3-Dateien sind ohne Ausnahme von Git ausgeschlossen. Eigene synthetische Demo-Sounds bleiben enthalten.
- Lokale Markdown-Verweise und öffentliche Pfad-Hygiene geprüft. GitHub Actions führt Tests, Timeline-Prüfung, Linkprüfung, Skill-Paketprüfung, Lint und Build bei Push/PR aus.

Die Skill-Erweiterung ändert keine Film-/Demo-Komposition. Dafür wurden Python-Prüfungen, Paketprüfung, TypeScript/Lint und Bundle ausgeführt; die oben dokumentierten Render-/Messwerte gehören weiterhin zur unveränderten Demo. [Verhaltensfälle und Grenzen der Skill-Prüfung](skill-evaluation.md).

## Grenzen

Die Skills wurden strukturell validiert und anhand konkreter Verhaltensfälle redaktionell geprüft. Es wurde kein automatisierter Codex-/Claude-Modellvergleich und kein Import in ein Claude-Konto durchgeführt. Automatische Skill-Auswahl sowie gute kreative Entscheidungen hängen vom eingesetzten Modell und dessen Werkzeugen ab. Die Bildauswahl-Anleitung ist kein neu trainierter Unschärfe-/Ästhetik-Klassifikator.

Die MCP-Auswahl und Beispiele stammen aus den verlinkten aktuellen Herstellerdokumentationen. Beim Erstellen dieses Onboardings wurde kein neuer MCP-Server installiert, kein Login durchgeführt und keine bestehende Host-Konfiguration verändert. Der Setup-Skill soll die künftige Nutzerwahl umsetzen; ein GitHub-Link allein erzwingt keinen Installationsdialog. `status` im Installer prüft nur Projekt-Skilldateien.

ExifTool war auf dem Testrechner nicht installiert; seine Extraktion wurde nicht live getestet. Der Import gruppierter Metadaten, Auswahl von Aufnahmezeitpunkten, Hashing und Konfliktbehandlung sind mit lokalen Fixtures geprüft. Die CLI benennt die fehlende Abhängigkeit ausdrücklich.

Audio wurde technisch gemessen, nicht vom Modell manuell angehört. Die Demo-Sounds sind bewusst leise. Kein Beleg für automatisch richtigen Beatcut bei beliebigen Songs.

Das Lint-Preset nutzt ESLint 9, das npm inzwischen als nicht mehr unterstützt markiert. Für die getestete Remotion-Version blieb diese kompatible Kombination gepinnt; ein späteres Upgrade gemeinsam mit dem Preset prüfen. Keine laufende öffentliche Web-App wird durch dieses Repo bereitgestellt.
