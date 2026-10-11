# Menschen vorteilhaft zeigen

## Einheitliche Leinwand

Breitformat und Hochformat nicht pro Clip wechseln. Für den Roadtrip: 1920×1080, 16:9. Für ein vertikales Reel: eigene 1080×1920-Komposition, jedes Motiv neu prüfen. Ein 16:9-Film automatisch in die Mitte eines 9:16-Fensters zu croppen ist keine vollständige Reel-Adaption.

Für Portraitmedien in 16:9:

1. EXIF-Ausrichtung und Video-Rotation anwenden, dann Abmessungen bestimmen.
2. Dasselbe Motiv als Hintergrund auf `cover`, deutlich weichzeichnen und leicht abdunkeln. Etwas über die Leinwand hinaus skalieren, damit der Blur keine transparenten Kanten erzeugt.
3. Vordergrund zunächst vollständig auf `contain`. Wichtige Gesichter, Köpfe, Hände, Füße und Ereignisdetails als geschützte Bereiche prüfen.
4. Nur freie Ränder wegnehmen. Zoom etwa 1,03→1,07 war passend, wenn genügend Freiraum vorhanden war. Bei engem Portrait **1,0 ohne zusätzlichen Zoom**.
5. Anfang, Mitte und Ende ansehen: Der sichere Startausschnitt kann am Ende unsicher werden. Motivposition bewusst wählen, nicht alle Menschen automatisch zentrieren.

Geometrische Grenze: Ein schmales Ganzkörperportrait füllt 16:9 nicht randlos, ohne oben/unten Inhalt zu verlieren. Priorität haben vollständige Personen; der Hintergrund darf dann sichtbar bleiben. Nicht durch verzerrtes Strecken „lösen“.

## Freisteller

PNG/WebP mit Alpha oder SVG-Maske der Originalpixel. Haare, Hände, Schuhe und **Lücken zwischen Armen/Beinen** prüfen. Ein bloßes Polygon um die äußere Kontur enthält sonst Treppen oder Pflaster zwischen den Beinen. Schatten/Outline auf die maskierte Silhouette anwenden. Bezugspunkt aus tatsächlicher Personenkontur statt aus der ganzen Foto-Leinwand bestimmen.

Ein aus einem Foto generierter neuer Mensch kann Gesicht/Kleidung verändern. Falls Identität bewahrt werden soll, Segmentierung/Maskierung verwenden. Generative Freistellungen nur nach visueller Prüfung als geeignet bewerten. Ein animierter Foto-Sticker ist keine echte neue Gehbewegung; für letztere braucht es getrennte Körperteile/Rigging oder einen passenden Originalclip.
