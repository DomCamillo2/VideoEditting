# Musikbibliothek

Die drei bereitgestellten Roadtrip-Songs liegen in `tracks/`; [tracks.json](tracks.json) enthält Namen, Pfade, Größen und SHA-256-Hashes. Der Repository-Eigentümer hat am 11.10.2026 ausdrücklich bestätigt, dass die öffentliche Weitergabe erlaubt ist. Ein separates Lizenzdokument wurde nicht vorgelegt. Die Dateien stehen **nicht unter der MIT-Lizenz** dieses Repos; weitergehende Nutzungsrechte werden damit nicht zugesichert.

| Datei | Titel |
|---|---|
| [norden-remix.mp3](tracks/norden-remix.mp3) | Verschwommen x Von hier an blind Remix |
| [team.mp3](tracks/team.mp3) | Ohne mein Team |
| [real.mp3](tracks/real.mp3) | Bist Du real (feat. Moé) |

Für ein eigenes Projekt gewünschte Dateien nach `studio/public/local/music/` kopieren. Trims, Songreihenfolge, Timeline-Start und erlaubten Verwendungszweck im privaten Manifest festhalten. Neue fremde Songs nicht automatisch committen. Remixe und unterschiedliche Vorläufe brauchen eine neue Beatprüfung.

`python3 tools/synth_audio.py` erzeugt zusätzlich einen kurzen synthetischen Rhythmus und Boing/Zap/Blip/Chime/Swish ohne Samples fremder Songs. Diese eigenen Demo-WAVs sind unter MIT nutzbar.
