# Vorschau, Export und ehrliche Kontrolle

## Vor dem langen Render

Eine repräsentative Passage prüfen: Portrait, zwei Gesichtsanker, freigestellte Füße/Hände, Tracking, schnelle Transition, dunkles Video, Songwechsel und Originalton. Danach die komplette kleine Vorschau. Kontaktbögen für alle Shot-Mitten ergänzen, aber bewegte Fehler an mehreren Phasen und in kurzen Clips ansehen.

Animationen nur aus `useCurrentFrame()` und `fps` ableiten. Asset-Ladevorgänge render-sicher behandeln. Gleicher Frame muss beim Vorwärts-, Rückwärts- und Direktsprung gleich aussehen. CSS-Keyframes, `Date.now()` und ungesetztes `Math.random()` sind dafür ungeeignet. Für GSAP gibt es inzwischen einen offiziellen framegesteuerten Adapter; [Recherche](motion-research.md).

## Was „fertig“ bedeutet

1. Renderer und Encoder erfolgreich beendet, nicht nur „letztes Bild gerendert“.
2. Ausgabedatei vorhanden, gewünschte Bildgröße/fps/Codec/Farbraum und Framezahl per ffprobe geprüft.
3. Vollständig decodiert. Schwarzintervalle gemessen und visuell bewertet; dunkle Nachtbilder nicht blind verwerfen.
4. Finalen Audio-Mix im tatsächlichen MP4 messen. Loudness/True Peaks und Sprache/Musik-Verhältnis getrennt beurteilen.
5. Kritische Übergänge, Masken und Ränder visuell prüfen. Beatcut mit Ton kontrollieren oder den Hörstatus ausdrücklich offenlassen.
   Stabilisierte Clips zusätzlich in Bewegung mit dem Original vergleichen: schlimmste Ruckler, Beschnitt, Gesichts-/Gebäudeverformungen, Ränder, pumpender Zoom und Ton-Synchronität. Nach neuem Beschnitt oder Stabilisierung vorhandene Trackingpunkte erneut prüfen.
6. Dateihash + Prüfdatum + Codeversion + Ausgabeparameter speichern. Verschiedene Versionen niemals mit demselben Prüfbericht versehen.

`tools/editing.py qa` automatisiert Probe, Decode, Blackdetect und Loudness. Es erkennt **keine** falsch zugeordneten Orte, schlechten Gesichtscrops, unlustigen Gags oder musikalisch falschen Beatmarken. „Technisch bestanden“ ist deshalb nicht „kreativ freigegeben“.

## Bewährtes Ausgabeprofil

Für überwiegend 1080p/30-SDR-Material: 1920×1080, 30 fps, H.264, yuv420p, AAC 48 kHz, MP4 Faststart. Auflösung/fps am Projekt festmachen. VFR-Quellen anhand Zeitstempeln behandeln. HDR nicht einfach als SDR taggen: Farbtransfer, Primaries und Tonemapping korrekt verarbeiten oder konsistentes SDR-Material vorbereiten.

Keine vorhandene Version überschreiben. Vorschau etwa 540p; finaler Encode erst nach Korrekturen bzw. gemäß Auftrag. Dateien in Git zu versionieren ersetzt keine lokale Original-/Export-Sicherung.

## Konkrete technische Erfahrungen

- Bei einem maskierten Whip erzeugte `CanvasImage` Streifen am unteren Rand; `Img` behob es in diesem Projekt/Browser. Keine pauschale Behauptung, CanvasImage sei defekt. Ändert sich Renderer/Chrome, repräsentative Frames erneut prüfen.
- Eine isolierte Gag-Testsequenz mit negativem Timing/Freeze verlor zehn Frames eines vorherigen Shots. Die vollständige Komposition war dort korrekt. Testausschnitte brauchen denselben zeitlichen Kontext; Patch nur im exakt geprüften Bereich einsetzen.
- Bei langen Patch-Reels kann ein großes FFmpeg `split`/`trim`-Netz viele Frames puffern. Getrennt geseekte Eingänge waren speicherschonender. Bildgenauigkeit per Exportframe-Vergleich prüfen, nicht allein aus `-ss` ableiten.
- Die lokale gebündelte Chromium-Ausführung hing; System-Chrome mit `--gl=angle` funktionierte. Das ist ein getesteter Fallback für diesen Mac, kein universeller Installationspfad.

Browser- oder Sandboxfehler von Codefehlern trennen. Keine Sicherheitsumgebung dauerhaft abschalten. Versionen, verwendetes Chrome und konkrete Fehlermeldung dokumentieren.
