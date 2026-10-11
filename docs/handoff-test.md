# Übergabetest mit frischem Agentenkontext

Durchgeführt am 11.10.2026. Ein separater Agent ohne unseren Chatverlauf erhielt eine isolierte Kopie des Repository-Stands, die Aufgabe, den dokumentierten Einstieg auszuführen, und bereits beantwortete Setup-Fragen: vorhandene Projekt-Skills nutzen, keine neuen MCPs, lustiges synthetisches 16:9-Beispiel, Vorschau erlaubt. Er sollte anhand von README, SETUP, AGENTS und den verlinkten Anleitungen bis zu einem echten Film kommen. Private Reisemedien standen ihm nicht zur Verfügung.

Das war ein Kontext- und Handoff-Test in derselben Werkzeugumgebung, kein Vergleich verschiedener Modelle, kein Test eines fremden Rechners und kein Import in ein Claude-Konto.

## Ergebnis

- Frische Kopie ohne installierte Node-Abhängigkeiten; `npm ci` und Installation der optionalen Analysepakete ausgeführt.
- Alle zehn Codex-/Claude-Skillkopien identisch vorgefunden; Setup und Fachskills führten zum vollständigen Beispiel.
- Medien erzeugt, Kontaktbogen und Kandidatenanalyse erstellt, Timeline und Schnittliste geprüft.
- Tatsächliche Vorschau: 960×540, 30 fps, 540 Frames / 18 Sekunden, SHA-256 `5726028c93bfc6bba78769b93e6cabf9305ebc31f5458d307d78e392afbf07ce`.
- Tatsächlicher Master: 1920×1080, 30 fps, 540 Frames, SHA-256 `fa9bc650246ff49fe4bcafdcd0c5deb69d3664040e55dd938ce65739712f12dd`.
- Beide Exporte vollständig decodiert, keine Schwarzintervalle erkannt. 18 Vorschauframes und zusätzliche Masterbilder visuell angesehen: vollständige Hochformatfiguren, Spin und Wisch sichtbar.
- `ManifestFilm` im Studio geladen. Audio nur technisch gemessen, nicht als angehört bestätigt.

Die Hashes binden den Bericht an die Exporte dieses Testlaufs. Encoder-, Browser- und Plattformunterschiede können andere MP4-Hashes erzeugen; Bytegleichheit zwischen Rechnern ist kein Abnahmekriterium.

## Gefundene Reibungen und Korrekturen

1. **Browser und Sandbox:** Der automatische Browserdownload war in der eingeschränkten Umgebung blockiert. Vorhandener Chrome mit `--gl angle` und erlaubtem Hostzugriff funktionierte. Der Schnellstart erklärt den vorhandenen Browser als Fallback; zusätzliche Berechtigungen bleiben eine Entscheidung der ausführenden Umgebung.
2. **Erneuter Render-Versuch:** Nach gescheitertem Browserstart blieben Props zurück und blockierten denselben Exportnamen. Der Renderer verwendet jetzt neue `attempt-002`-Hilfsdateien, solange kein MP4/QA-Bericht existiert. Bestehende Dateien bleiben erhalten. Der Agent hat den Fix mit einem absichtlich ungültigen Browserpfad und anschließend demselben MP4-Ziel praktisch nachgeprüft: 30 Frames, Decode erfolgreich. Ein dritter Versuch mit vorhandenem MP4 wurde zurückgewiesen; dessen Hash blieb unverändert.
3. **Studio-Inspector:** Bei CLI-Props zeigte der Inspector weiterhin Defaultwerte. Die Anleitung erklärt jetzt, dass die vorbereitete JSON und tatsächliche Timeline maßgeblich sind und Änderungen in der Quell-JSON erfolgen.
4. **Beat-Zeitbezug:** Der erste Beispielbefehl übernahm den Musik-Quellstart von 0,5 Sekunden nicht. Anleitung und CI verwenden jetzt `--source-in 0.5`; der Kandidatenlauf mit diesem Mapping wurde erneut erfolgreich ausgeführt. Periodische Testmusik hatte den Unterschied verdeckt.

Der unveränderte Erstlauf und der Nachtest der Korrektur werden getrennt betrachtet. Der Agent übernahm für den Retry-Nachtest ausschließlich den korrigierten Renderer und die Anleitung in seine Kopie; er änderte keine Quelldateien des Hauptprojekts.

## Weiterhin nötig

Ein echter Film braucht eine Sichtung an Originalauflösung, bestätigte Aufnahmezeiten und Orte, ausgewogene Personenauswahl sowie einen Hörtest von Musik, Sprache und Übergängen. Synthetische Duplikate und gezeichnete Figuren belegen die technische Pipeline, nicht automatisch gute Entscheidungen über reale Freunde, schwierige Unschärfe, Hauttöne oder Humor.
