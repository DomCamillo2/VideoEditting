# Comedy-Kochbuch

Eine Person oder Situation erkennen → kurze Erwartung → überraschende Aktion → zurück zur Reise. Die meisten Gags brauchen 1–3 Sekunden. Ein Effekt sollte auf einen konkreten Moment reagieren. Kein Gag muss auf Kosten einer Person gehen.

## Freisteller-Rezepte

Alle Rezepte verwenden Originalpixel bzw. eine geprüfte Maske. Im Baukasten dient eine eigens gezeichnete Figur als austauschbarer Platzhalter.

| Gag | Aufbau | Animation | Ton / Stolperfalle |
|---|---|---|---|
| Pirouette | Körper gut sichtbar, Foto kurz halten | 0→360°, währenddessen auf ca. 72–85% verkleinern | leiser Swish; Rotationsbox und Füße prüfen |
| Mensch wird heruntergeladen | Person bleibt Mittelpunkt | kleiner/gedreht starten, auf 100% wachsen, Fortschrittsbalken endet | Blip auf Fertig; Text nicht vor Gesicht |
| Lädt … 99% | irritierter oder wartender Moment | Bewegung kurz einfrieren, Ring stockt, Pointe beim Weitergehen | 99% bewusst kurz halten; keine erfundene Aussage |
| Davonlaufen | klare Silhouette und freie Austrittsseite | x nach außen, kleiner rhythmischer Hopser, ±8° Neigung | Foto-Sticker, kein behauptetes echtes Laufvideo |
| Raketenstart | dynamische Pose | kurz rückwärts/squash, dann diagonal herausbeschleunigen | Zap + Flammen unter Füßen; nur hier Exit beabsichtigt |
| Sprungfeder | Standpose | kleine Kompression, Aufwärtssprung, sanft landen | Boing auf Abheben/Landen; Gesicht kaum verzerren |
| Schweben | entspannte Situation | sanfter Bogen, kleine Rotation, Schatten bleibt am Boden | Chime; nicht jede Landschaft überladen |
| Drehscheibe | Pose frontal | horizontale Skalierung `cos(phase)` für 2,5D-Flip | wird kurz schmal; keine anatomische 3D-Behauptung |
| Teleport | zwei plausible Positionen | Energie-Ring, sehr kurze Abblendung, andere Position | kein langer Leerframe; Hintergrund braucht Basisbild |
| Seebrise | Wind bereits sichtbar | kleine seitliche Schwingung, wenige Windlinien | geringe Amplitude; kein hektisches Vollbildzittern |

## Gags ohne Freistellung

| Idee | Guter Kontext | Gestaltung |
|---|---|---|
| Scooter-Turbo | echte E-Scooter-Fahrt | Flammen am Deck, kurze Geschwindigkeitslinien, Label im freien Rand |
| Snack-Level | Essen/Picknick | kleiner Zähler +1 oder Ladebalken, einmaliger Pop |
| Team-Kombo | mehrere Freunde in Aktion | kurze Verbindung/Combo-Zahl, keine Namensidentifikation nötig |
| Akku laden | Pause/Schlafen | Batteriesymbol abseits des Gesichts, ruhiger Fortschritt |
| Orientierung gesucht | Karte/Planlosigkeit | kleiner Radar, keine falsche geografische Aussage |
| Konfetti | Ankunft/Feiern | kurzer gerichteter Ausstoß mit fixiertem Zufallsseed |
| Helm-Sterne | Helm-/Scooter-Moment | Sterne darüber, Gesicht bleibt frei |
| Fokus gefunden | Fotograf fotografiert | Fokusrahmen auf Kamera/Objekt, kurzer Einrastmoment |
| Windstärke Urlaub | Haare/Jacke im Wind | kurze Beschriftung, Foto weiter atmen lassen |
| Fünftes Bandmitglied | Pose neben Musiker/Statue | dezentes Bühnenlicht oder Stern, respektvoll bleiben |

## Scooter-Flammen richtig platzieren

Mindestens Start, Kurve/Bewegungswechsel und Ende tracken. Koordinaten in das tatsächlich gecroppte/rotierte Video transformieren. Zwischen Keyframes interpolieren. Flammenrichtung entgegen Fahrt, im Verhältnis zum Scooter skalieren. Effekt vor Kamerazoom/Occlusion ausblenden, wenn das Tracking sonst unplausibel wird. Maske bei Vordergrundobjekten. Echte Trackingdaten können nicht durch Zufallsbewegung ersetzt werden.

## Dichte und Rhythmus

Im 6:21-Roadtrip kamen in einer späteren Version 20 zusätzliche Gags, neun Freisteller und neun kurze Soundakzente hinzu. Das war eine ausdrückliche Nutzerpräferenz, kein Standard für jeden Film. Plane Gags als eigene Liste mit Startframe, Dauer, Quelle, Maskenstatus, Beatakzent und Prüfstatus. In ruhigen Landschaften und im emotionalen Finale Luft lassen. Dasselbe Foto im Rückblick ohne wiederholten Gag zeigen.

## Qualitätskontrolle

Original, erste Aktion, maximale Rotation/Skalierung und Rückkehr ansehen. Achte auf Maskenreste zwischen Beinen, abgeschnittene Hände, hartes Auftauchen, doppelte Person auf dem Hintergrund, Texte über Gesichtern und laute SFX. Der geisterhafte Originalkörper im Basisfoto lässt sich mit einer sauberen Hintergrundplatte vermeiden; sonst bewusst dimmen/blurrieren und als Papier-Sticker gestalten. Eine ruhige Rahmenvariante ist besser als eine auffällige schlechte Maske.
