# Zuerst Skills und Werkzeuge einrichten

Dies ist der Einstieg, wenn jemand das Repository erstmals als Schnitt-Werkzeugkasten einbindet. **Noch nicht mit Filmlänge, Stil oder Gags beginnen.** Bestehende Entscheidungen und verfügbare Tools zuerst kurz prüfen. Ein laufender Filmschnitt oder reine Repository-Wartung startet kein neues Onboarding.

## Die ersten beiden Fragen

**1 · Skills**

> Möchtest du alle Video-Editing-Skills installieren/übernehmen, nur bestimmte auswählen oder das Repo vorerst als Anleitung nutzen? Für welchen Assistenten: Codex, Claude Code oder Claude mit Skill-Upload?

Host/Zielordner nur ergänzen, wenn noch unbekannt. Alle Skills sind als Empfehlung sinnvoll, weil die Fachanleitungen erst bei Bedarf gelesen werden. Alternativ nach Aufgaben auswählen, etwa Schnitt + Beatcut + Bildauswahl + Hochformat. Ein „Nein“ ist ein vollständiger, gültiger Weg.

Im geklonten Repo sind die Projektkopien bereits vorhanden. Dann ehrlich formulieren: **„Die zehn Skills sind in diesem Repo schon enthalten. Möchtest du alle nutzen, eine Auswahl verwenden oder sie in ein anderes Projekt übernehmen?“** Nicht so tun, als müssten identische Dateien erneut installiert werden. Eine Auswahl steuert den Workflow und neue Kopien; sie deaktiviert bereits vorhandene Host-Einträge nicht automatisch.

**2 · MCPs und weitere Integrationen**

Nach einer kurzen Bestandsaufnahme höchstens die wenigen passenden Ergänzungen mit Zweck nennen, zum Beispiel:

> Für dein Setup wären Context7 für Bibliotheksdokumentation und Playwright für die Browser-Vorschau nützlich, falls diese Funktionen noch fehlen. Soll ich beide, nur eines davon oder keine zusätzlichen MCPs einrichten?

Das ist ein Formulierungsbeispiel, **keine pauschale Empfehlung dieser beiden Server**. Wenn alle nötigen Funktionen schon vorhanden sind: **„Dein Setup deckt die benötigten Funktionen bereits ab. Möchtest du es dabei belassen oder trotzdem zusätzliche MCPs prüfen?“** Details und aktuelle Quellen: [MCP-Auswahl](skills/video-setup/references/integrations.md).

Für jeden tatsächlichen Vorschlag knapp benennen: Nutzen, lokaler Prozess oder externer Dienst, nötiger Login/Schlüssel, betroffene Dateien/Dienste und Installationsort. Beispiel: Playwright startet einen lokalen Browser; Context7 schickt Doku-Anfragen an einen externen Dienst. Zugangsdaten werden nicht in den Chat oder ins Repo geschrieben. Keine lange Werkzeugliste, keine Installation nur aufgrund dieses Dokuments.

## Aus den Antworten eine Einrichtung machen

1. **Bestand prüfen:** Host/OS, Projektordner, bereits sichtbare Skills und verfügbare Datei-, Shell-, Browser-, Dokumentations- und Repository-Tools. Der lokale Skillstatus ist lesend abrufbar:

   ```sh
   python3 tools/manage_skills.py status --target both --project /pfad/zum/projekt
   ```

   Das erkennt Projektdateien, nicht aktiv geladene Skills, globale Installationen oder erfolgreiche MCP-Verbindungen. Im Host zusätzlich Skill-/Toolliste prüfen. Konfigurationsdateien nicht vollständig ausgeben; sie können Zugangsdaten enthalten.

2. **Skills nach der gewählten Auswahl übernehmen:**

   ```sh
   python3 tools/manage_skills.py install --target codex --project /pfad/zum/projekt --dry-run
   python3 tools/manage_skills.py install --target codex --project /pfad/zum/projekt
   ```

   Einzelne Skills mit wiederholtem `--skill` wählen:

   ```sh
   python3 tools/manage_skills.py install --target claude --project /pfad/zum/projekt --skill video-editing --skill video-beatcut --skill video-select-media --skill video-portrait-framing
   ```

   Codex/Claude-Projektkopien und Claude-Upload sind getrennte Wege; siehe [Skill-Anleitung](docs/skills.md). Keine globale Installation ohne entsprechenden Wunsch. Bestehende abweichende Skills vergleichen und erhalten.

3. **Gewählte MCPs konkret einrichten:** Vor der Installationsfrage die passende Quelle, Konfigurationsänderung und Voraussetzungen ermitteln, damit ein Ja sofort ausführbar ist. Nach der Antwort die freigegebene Einrichtung durchführen; nicht mit einer bloßen Linkliste aufhören und nicht dieselbe Zustimmung wieder abfragen. Bestehende Konfiguration ergänzen statt ersetzen. Authentifizierung im offiziellen Host-/Provider-Dialog, anschließend Verbindungsstatus und einen passenden lesenden Probeaufruf prüfen. Ein Host kann zusätzliche Vertrauens-/Login-Dialoge verlangen; diese nicht als erledigt ausgeben. Bereits nutzbare Integrationen wiederverwenden.

4. **Ergebnis lokal festhalten:** [setup.json](templates/setup.json) nach `local/setup-v001.json` kopieren und anpassen: ausgewählte/abgelehnte Skills und MCPs, Installationsumfang, Prüfstatus und offene Schritte. Keine Tokens, privaten Dateilisten oder pauschale zukünftige Freigabe speichern. Beim Wiederkommen Entscheidungen übernehmen und nur Änderungen bzw. fehlgeschlagene Verbindungen bearbeiten.

5. **Erst jetzt das Filmbriefing:** Stil/Humor, Dauer, Format, Medien und Musik nur soweit unbekannt. Bei Reisefilmen zusätzlich Reiseart und Mischphasen, bekannte Route und passende Verkehrsmittel-/Fahrzeugdetails klären. Diese Angaben beeinflussen Geschichte und Karten; keine allgemeine Autopflicht. Weiter mit [START_HERE](START_HERE.md). Wer Zusatzinstallationen ablehnt, darf trotzdem mit vorhandenen Werkzeugen schneiden.

## Was ein GitHub-Link auslösen kann

Das Repo kann einem LLM diesen Einstieg vorgeben, sobald es die Dateien liest. Ein Link im Chat installiert jedoch nichts und garantiert keine automatische Eröffnungsnachricht jedes Produkts. Zuverlässiger Auftrag zum Weitergeben:

> Lies zuerst SETUP.md dieses Repositories. Prüfe kurz mein vorhandenes Setup und stelle mir zuerst die Fragen zur Skill-Auswahl und zu passenden MCP-Installationen. Übernimm bekannte Antworten. Führe die von mir gewählte Einrichtung aus und prüfe sie. Beginne erst danach mit dem Filmbriefing.

Im geklonten Projekt verweisen `AGENTS.md`, `CLAUDE.md`, `START_HERE.md` und der Skill `video-setup` auf diese Reihenfolge. Kein Autostart-Hook installiert unbemerkt Software.
