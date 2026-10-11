# Musik und Beatcut

## Ein Peak ist noch kein sinnvoller Schnitt

Im VN-Projekt war „auf erkannten Beatmarken“ zunächst technisch erfüllt, für den Nutzer aber hörbar unbefriedigend. Spätere lokale Prüfberichte verwendeten Bass-Onsets, Tempo-Raster und kurze Problemabschnitte. Daraus folgt kein pauschales Urteil über VN: Material, Markerphase und Songstruktur müssen geprüft werden.

1. Song in Intro, Strophe, Refrain, Bridge und Schluss gliedern. Hook/Drop und starke gemeinsame Aufnahmen zusammenbringen.
2. Tempo, Phase und mögliche Halb-/Doppeltempo-Erkennung prüfen. Drums und Vocals können unterschiedliche Peaks erzeugen. Keine feste BPM über einen variablen Song erzwingen.
3. Aus starken Downbeats/Kicks/Snares eine Auswahl bilden. Ruhig etwa 4–8 Beats pro Einstellung, schnell etwa 1–2 als Ausgangspunkt; diese Zahlen sind keine Pflicht.
4. Jeden gewählten Zeitpunkt **einmal** auf einen ganzzahligen Frame runden: `floor(seconds * fps + 0.5)` für nichtnegative Zeiten. Dauern aus aufeinanderfolgenden Kanten ableiten. Nicht gerundete Einzeldauern aufsummieren.
5. Bei 30 fps beträgt der beste mögliche Rundungsfehler höchstens 16,67 ms. Ein Schwellenwert von 50 ms in einem Onset-Audit beantwortet eine andere Frage und ist kein Beleg für Framegenauigkeit.
6. Zu kurze Shots zusammenfassen oder andere Beatkanten wählen. 0,5 Sekunden war die gewünschte Untergrenze; Akzentläufe brauchen bewusste Ausnahmen.

## Drei getrennte Prüfungen

| Prüfung | Belegt | Belegt nicht |
|---|---|---|
| Frame gegen ausgewählte Marke | Kante wurde korrekt quantisiert | Marke ist musikalisch richtig |
| Onset-/Bass-Energie in Cut-Nähe | Schnitt liegt nahe einem Schallereignis | Downbeat, Groove oder guter Ausdruck |
| Export mit Ton ansehen/anhören | tatsächlicher wahrgenommener Zusammenhang | vollständige automatische Fehlerfreiheit |

Höre Anfang/Mitte/Ende jedes Songs, alle Songwechsel und die schnellsten Läufe. Teile lange Filme in 20–45-Sekunden-Prüfstücke. Ein Klick genau auf Schnittkanten kann helfen; zusätzlich ohne Klick hören. Beatpositionen aus dem **tatsächlich geschnittenen Audiomaster** prüfen, nicht aus einem Song mit anderem Vorlauf. Fades, Stille-Trim, Resampling und Speedänderungen verändern die Zuordnung.

CLI `beat-report` erwartet bereits ausgewählte Marken; es ist absichtlich **kein Beatdetektor**. Markenauswahl und Hörprüfung bleiben eigenständige Arbeitsschritte.

## Audio-Mix

Originalton nur gezielt: Lachen, Tür, Motor, Ankunft, Wind. Sprache vorher verständlich schneiden. Musik bereits vor Sprache absenken, sanft zurückführen. Im Roadtrip waren etwa 16 dB Ducking und kurze Ein-/Ausblendungen brauchbar; nach Gehör anpassen. Bei einem reinen Foto-Recap kann Originalton vollständig stumm bleiben.

Eigene SFX eher kurz und leise, auf die Aktion statt auf jeden Beat. Ein Boing unterstützt einen Sprung; neun konkurrierende Meme-Sounds verdecken Musik und Persönlichkeit. Humor funktioniert häufig mit einem einzigen präzisen Geräusch.

Den vollständigen Mix messen, nicht nur einzelne Stems. Etwa −16 LUFS und genügend True-Peak-Reserve waren ein praktikables privates Filmziel, keine universelle Plattformvorschrift. AAC-Encoding kann Peaks verändern; den MP4-Export erneut messen. Niemals nur Sample-Peaks mit True Peaks gleichsetzen. Schluss musikalisch auflösen, Fade sinnvoll ausklingen lassen; kein harter Abbruch.
