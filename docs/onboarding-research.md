# Wie vergleichbare Repositories den Einstieg gestalten

Recherche vom 11.10.2026, ausschließlich Hersteller-/Maintainer-Quellen. Betrachtet wurden Einstieg, Installation, Auswahl und Trennung zwischen Anweisungen und Werkzeugzugriff. Keine fremden Skills oder Installationsskripte wurden übernommen oder ausgeführt.

| Repository | Beobachtung | Übernahme in VideoEditting |
|---|---|---|
| [Anthropic Skills](https://github.com/anthropics/skills) | Eigenständige Skillordner und getrennte Wege für Claude Code, Claude im Chat und API; in Claude Code lassen sich Skill-Sets über einen Marketplace auswählen. | Host zuerst erkennen; ganze Sets und einzelne Skills anbieten; ZIP-Upload nicht als lokalen MCP-Installer darstellen. |
| [Vercel Skills CLI](https://github.com/vercel-labs/skills) | Unterstützt Auflisten vor Installation, Auswahl bestimmter Skills/Agenten sowie Projekt- und globale Installation. | Eigener kleiner Installer mit `status`, `--skill` und `--dry-run`; Projekt als normaler Umfang, bestehende Dateien erhalten. |
| [Remotion Skills](https://github.com/remotion-dev/skills) | Zeigt einen direkten Installationsweg; Skills werden auch beim Erstellen eines Remotion-Projekts angeboten. | Einrichtung früh anbieten und danach zum Film übergehen; zusätzliche Renderer-Skills nur bei Bedarf und noch fehlendem Bestand. |
| [OpenAI Plugins](https://github.com/openai/plugins) | Jedes Plugin trennt Manifest und optionale Skills, MCP-Konfiguration, Assets und andere Bestandteile. | Anleitungen, lokale Abhängigkeiten und MCP-Verbindungen in der Benutzerentscheidung getrennt halten. Unser Repo bleibt ein Skill-Toolkit, kein behaupteter Marketplace-Eintrag. |

Das alte [OpenAI-Skills-Repository](https://github.com/openai/skills) verweist inzwischen auf Plugins und ist als veraltet markiert. Für lokale Projekt-Skills ist die [aktuelle OpenAI-Skill-Dokumentation](https://learn.chatgpt.com/docs/build-skills) maßgeblich. Wir übernehmen deshalb keine alten Installationspfade ungeprüft aus einem populären README.

## Eigene Entscheidung für dieses Repo

Die geprüften Repositories liefern Installationsmuster. **Die verbindliche Reihenfolge der ersten Fragen ist unser Design aus dem Nutzerwunsch**, nicht die Behauptung, alle Vergleichsrepos hätten denselben Chatdialog:

1. Bereits verfügbaren Host und Bestand lesen, dann alle/ausgewählte/keine zusätzlichen Skills anbieten.
2. Aus tatsächlichen Fähigkeitslücken wenige sinnvolle MCPs ableiten, Zweck und Zugriff nennen und nach der gewünschten Einrichtung fragen.
3. Gewählte Einrichtung ausführen und überprüfen; Antworten lokal merken, ohne daraus pauschale künftige Befugnisse abzuleiten.
4. Erst danach Filmstil und Humor klären.

Ein geklontes Repo enthält seine Skilldateien bereits. Das wird offen benannt, anstatt einen künstlichen Installationsschritt zu erzeugen. Ein normaler GitHub-Link allein kann keinen Host zum Ausführen oder zu einer bestimmten ersten Antwort zwingen; [SETUP.md](../SETUP.md) enthält deshalb einen kurzen verlässlichen Einbindungsauftrag.

## MCPs nach Nutzen auswählen

Die [MCP-Matrix samt Installationswegen](../skills/video-setup/references/integrations.md) unterscheidet Dokumentation, Browser, GitHub und lokalen Dateizugriff. Der alte Remotion-Dokumentations-MCP wird ausdrücklich **nicht** neu empfohlen: [Remotion markiert ihn als deprecated und verweist auf Skills](https://www.remotion.dev/docs/ai/mcp).

Native Tools oder bereits verbundene Apps können die gleiche Aufgabe abdecken. Das Installieren aller Skills bedeutet deshalb nicht automatisch das Installieren aller MCPs. Eine Konfigurationsdatei beweist weder erfolgreiche Authentifizierung noch einen funktionierenden Toolaufruf.
