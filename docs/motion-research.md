# Was wir von guten Motion-Websites übernehmen können

Recherche am 11.10.2026 anhand offizieller Dokumentation und öffentlich zugänglicher Beispielbeschreibungen. Kein Premium-Quellcode wurde übernommen; keine Behauptung über TikTok-Rankings oder Reichweite. Die Übertragung auf persönliche Filme ist unsere gestalterische Ableitung.

## Motion.dev: Feder statt gleichförmigem Zoom

Motion unterscheidet zeitgesteuerte Tweens und Federn; Dämpfung, Steifigkeit und Masse beeinflussen das Gefühl. Die Dokumentation beschreibt auch `visualDuration`, um den sichtbaren Hauptteil einer Federbewegung zeitlich zu koordinieren. Für einen Cutout heißt das: rasches Einrasten auf dem Akzent, kleiner Nachlauf, dann Ruhe. Ein sanftes Overlay braucht weniger Überschwingen als ein bewusst alberner Sprung. In unserer Demo wird die Bewegung aus Frames berechnet. [Transitions](https://motion.dev/docs/react-transitions).

**Konkretes Beispiel: Bobble hover.** Das Beispiel reagiert auf die Geschwindigkeit des Mauszeigers. Unsere Übertragung ersetzt den interaktiven Trigger durch einen geplanten musikalischen Akzent: stärkerer Akzent → etwas größere, begrenzte Auslenkung → gedämpfte Rückkehr. Keine Mausbewegung steuert den fertigen Film. Der eigene Boing-/Sticker-Code bildet eine ähnliche gestalterische Idee ab, er ist keine Kopie des kostenpflichtigen Beispiels. [Bobble hover](https://motion.dev/examples/react-bobble-hover).

## Motion.dev: Wiedererkennung durch gemeinsame Elemente

`layout` und `layoutId` verbinden Größe und Position von UI-Elementen über Zustände. Für Filme ist die nützliche Idee die visuelle Identität: ein Gesicht, ein Bus oder ein runder Gegenstand führt das Auge über den Schnitt. Unsere `FaceMatch`-Komponente hält zwei separat definierte Gesichtsanker während des Wechsels am selben Leinwandpunkt. Die Layout-API selbst wird dafür nicht benötigt. [Layout-Animationen](https://motion.dev/docs/react-layout-animations), [Shared-layout-Beispiel](https://motion.dev/examples/js-shared-layout-animation).

## Motion.dev: Masken statt wahlloser Blenden

Das Clip-path-Beispiel zeigt einen Zustandswechsel über eine Maske. Übertragung: Brille, Rad oder Hafenfenster als motivierte Öffnung in den nächsten Shot. Die Form braucht einen Bezug zum Bild und muss den relevanten Bildinhalt im richtigen Moment zeigen. Ein Vollbild-Wipe ohne motivischen Anschluss wird dadurch nicht automatisch besser. [Clip-path-Beispiel](https://motion.dev/examples/vue-animate-view-clip-path), [Beispielübersicht](https://motion.dev/examples).

## GSAP: Choreografie auf einer kontrollierten Zeitachse

GSAP-Timelines können auf eine bestimmte Zeit gesucht werden. Seit Remotion 4.0.517 ist außerdem `@remotion/gsap` dokumentiert: Es baut eine pausierte Timeline und bindet deren Position an den aktuellen Remotion-Frame. Nutze den offiziellen Adapter, wenn eine komplexere GSAP-Choreografie sinnvoll ist; unsere kleinen Beispiele bleiben bei Remotion-Funktionen. Nicht gleichzeitig einen autonomen GSAP-Ticker und Remotion-Frames als zwei Zeitquellen betreiben. [GSAP seek](https://gsap.com/docs/v3/GSAP/Timeline/seek()/), [Remotion-Adapter](https://www.remotion.dev/docs/gsap), [useGsapTimeline](https://www.remotion.dev/docs/gsap/use-gsap-timeline).

## Remotion: Effekt und Zeitplan getrennt denken

Die API unterscheidet überlappende Transitions und zeitneutrale Overlays. Das ist entscheidend, wenn ein bereits guter Beatcut neue Effekte bekommt. `spring()`/`interpolate()` liefern framebezogene Bewegungen; jeder Renderframe soll denselben Zustand ergeben, unabhängig davon, wie er angefahren wird. [TransitionSeries](https://www.remotion.dev/docs/transitions/transitionseries), [Animation](https://www.remotion.dev/docs/animating-properties), [spring](https://www.remotion.dev/docs/spring).

## Adobe, CapCut und VN: Schnittlogik bleibt entscheidend

Adobe beschreibt den Match Cut als Verbindung über passende visuelle oder akustische Eigenschaften. Daraus folgt für uns: Bewegung und Anker auswählen, bevor ein Zoom-Preset gewählt wird. [Match Cut](https://www.adobe.com/in/creativecloud/video/discover/match-cut.html).

CapCut beschreibt Geschwindigkeitskurven für wechselndes Tempo innerhalb eines Clips. Unsere Ableitung: geeignete Fahrt-/Bewegungsaufnahmen wählen, Beschleunigung an den Akzent legen und den ruhigen Teil als lesbaren Moment erhalten. Das ist kein Nachweis, dass ein bestimmter Effekt gerade viral ist. [Velocity](https://www.capcut.com/resource/how-to-do-velocity-on-capcut).

VN beschreibt BeatsClips als Verbindung von Beatmarken und Vorlagen. Unser Projekt zeigte zusätzlich: vorhandene Marken und ein musikalisch überzeugender Film sind unterschiedliche Prüfziele. UI-Namen/Funktionsumfang immer in der installierten Version bestätigen, statt aus einer Website blind Klickanleitungen abzuleiten. [BeatsClips](https://www.vlognow.me/blog/features/beats-clips/).

## Praktische Übersetzung

| Web-Prinzip | Film-Anwendung | Umsetzung / Grenze |
|---|---|---|
| Spring / Nachlauf | Sticker-Pop, Label, Boing | framebasierte Feder, begrenzte Amplitude |
| Shared element | Gesichts-/Objekt-Match-Cut | zwei Bildanker, gemeinsame Zielposition |
| Clip reveal | motivischer Übergang | Maske mit kontrolliertem Fortschritt |
| Stagger | Team-Kombo, wenige Textwörter | feste Frame-Offsets, kein Laufzeit-Zufall |
| Scroll progress | Kartenfahrt / Kamerazoom | Fortschritt aus Filmframe statt Scrollposition |
| Loading UI | „Mensch wird geladen“ | begrenzte Comedy-Sequenz mit echter Auflösung |

Die Demo zeigt einen Teil davon ausführbar. Karten, automatische Segmentierung, echte 3D-Rigs und automatische Beat-Erkennung sind bewusst **keine** eingebauten Features dieses kleinen Starters; dazu gibt es Arbeitsrezepte und Erweiterungspunkte.
