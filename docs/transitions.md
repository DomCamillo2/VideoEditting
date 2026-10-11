# Übergänge mit einem Grund

Harte Schnitte tragen die meisten Szenen. Ein besonderer Übergang funktioniert, wenn Bewegung, Motiv oder Musik ihn vorbereitet. Nicht jeden Clip mit einem Preset dekorieren.

| Technik | Geeigneter Anlass | Startwert bei 30 fps | Wichtigste Kontrolle |
|---|---|---:|---|
| Whip | Busfahrt, Schwenk, schnelle Stadtmontage | 10–16 Frames | Richtung beider Bilder konsistent, keine leeren Ränder |
| Push/Punch | Refrain, betonte Reaktion | 8–14 | Motiv bleibt sichtbar, Zoom nicht am Bildrand |
| Gesichts-Match-Zoom | ähnliche Pose/Blickrichtung in zwei Bildern | 14–22 | beide Gesichter zum selben Anker führen |
| Warmes Licht | Sonne, Meer, ruhiger Kapitelwechsel | 18–26 | Highlights/Gesichter nicht ausbrennen |
| Foto-Snap | Gruppenfoto oder Erinnerungsmoment | 6–10 | kein dauerndes weißes Stroboskop |
| Shape/Iris reveal | Brille, Rad, Hafenfenster | 12–20 | Form entsteht aus dem tatsächlichen Motiv |
| Überblendung | Zeit vergehen lassen, ruhiger Abschluss | 20–35 | keine versehentlichen Doppelgesichter |

Die Werte sind Rezepte, keine Regel. Bei anderer fps Sekunden erhalten.

## Gesichts-Zoom präzise bauen

Im Ausgangs- und Zielbild jeweils den Gesichtsanker in normierten Koordinaten festlegen. Bild um diesen Anker skalieren und zum selben Leinwandpunkt verschieben. Am musikalischen Akzent wechseln. Zweite Hälfte vom Zielgesicht wieder herauszoomen. Die Beispielkomponente `FaceMatch` nimmt dafür zwei getrennte Anker. Keine Gesichtserkennung notwendig, wenn wenige Übergänge sorgfältig von Hand platziert werden. Den größten Zoom auf Auflösung, Gesichtsausschnitt und Comedy-Wirkung prüfen.

## Überlappung verändert die Zeit

Bei `TransitionSeries.Transition` gilt: Gesamtdauer = Summe der Szenen minus Summe der Überlappungen. `TransitionSeries.Overlay` verändert die Dauer nicht. Das ist eine dokumentierte Remotion-Eigenschaft, keine Versionspanne. [API](https://www.remotion.dev/docs/transitions/transitionseries).

Beispiel: zwei 60-Frame-Szenen mit 12-Frame-Transition ergeben 108 Frames. Soll ein vorhandener Beatcut bei Frame 60 bleiben, müssen Ein-/Ausgangshandles und Transition-Phase bewusst platziert werden oder ein Overlay über den unveränderten Schnitt gelegt werden. Nur die Gesamtdauer zu korrigieren reicht nicht: auch den wahrgenommenen Umschlagpunkt kontrollieren.

## Speed-Ramp

Für jeden Output-Frame den monoton steigenden Source-Zeitpunkt berechnen. Rampen integrieren: Source-Zeit ist die Summe/Integration der Geschwindigkeit, nicht `frame * aktuelleGeschwindigkeit`. Anfang/Ende müssen im Originalclip liegen. Originalfps, VFR und Rotation berücksichtigen. Bei 30-fps-Material erzeugt verlangsamtes 30-fps-Output ohne Zwischenbildverfahren wiederholte Frames; kein echtes Slow Motion behaupten. Optischen Fluss auf Räder, Gliedmaßen und Kanten prüfen.

Im Roadtrip funktionierte ein kurzer Brücken-Clip mit ungefähr 2,8×→1×→2,8×. Nicht jedem Fahrschnipsel dieselbe Kurve geben. Passende Musik und Bewegung sind wichtiger als die Anzahl der Rampen.
