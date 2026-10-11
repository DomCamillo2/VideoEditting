# Aufnahmezeiten, Reihenfolge und Karten

## Zeit ist ein Datensatz, kein einzelnes Feld

Bewahre Originaldateiname, Hash, alle relevanten Rohzeiten, ausgewählte Quelle, Offset, normalisierte UTC-Zeit und Begründung auf. Bevorzuge bei Fotos EXIF `DateTimeOriginal` + `OffsetTimeOriginal`; bei Apple-Videos das ursprüngliche `com.apple.quicktime.creationdate`/ExifTool `Keys:CreationDate`. Vergleiche QuickTime `CreateDate`, Medien-/Trackzeiten und ffprobe `creation_time`. Containerzeiten können einen Export beschreiben. Metadaten sind Hinweise, keine unfehlbare Wahrheit.

ExifTool behandelt QuickTime-Zeitfelder und Zeitzonen je nach Tag/Option unterschiedlich. Nicht blind UTC auf jedes Feld anwenden. Der CLI dieses Repos lässt naive Zeitangaben ohne ausdrücklich angegebene Zeitzone ungelöst. Ein eingetragener Projekt-Zeitzonenname ist eine dokumentierte Annahme, keine nachträglich entdeckte Metadateninformation.

- Explizite Offsets korrekt berücksichtigen, auch `-03:30` oder `+05:45`.
- Naive Ortszeit nur mit belegter Reisezone normalisieren; Sommerzeit beachten.
- Bei DST-Rückstellung kann dieselbe Ortszeit zweimal vorkommen. Bei DST-Vorstellung gibt es nicht existente Uhrzeiten. Unser CLI meldet beide Fälle zur Klärung.
- Ungültige/Nullzeiten erhalten einen Fehlerhinweis. Ein anderer Kandidat kann verwendet werden; der kaputte Rohwert bleibt sichtbar.
- Dateinamen nur als gekennzeichneten Ersatz nutzen. Kein stilles Sortieren nach mtime.
- Live Photo: Standbild + zugehöriges MOV als ein Ereignis markieren; gleiche Uhrzeit allein beweist keine Paarung.
- Identische Hashes sind echte Duplikate. Perceptual Hashes nur zur Vorauswahl ähnlicher Motive einsetzen.
- Zeitgleiche Dateien stabil sortieren, ohne behauptete interne Reihenfolge. Unbekannte Zeiten separat führen; nicht kommentarlos ans Filmende kleben.

Der CLI erzeugt eine **Arbeitsreihenfolge**, keine abschließend geprüfte Chronologie. Kontaktbögen, Clipinhalt und Nutzerkorrekturen gehören zur Prüfung. Ein dokumentierter manueller Override soll Rohdaten nie löschen.

## Orts- und Routenbelege

GPS → sichtbare Schilder/Sehenswürdigkeiten → zeitlich benachbarte belegte Medien → Reisebeschreibung. Für jeden Abschnitt `evidence`, `confidence` und `transport` speichern. Ein historischer Fahrplan belegt, dass eine Verbindung existierte; er belegt nicht, dass die Gruppe sie nahm.

Im Roadtrip änderte GPS den angenommenen Oslo-Abfahrtshafen: Hamburg war der vorherige Stadtstopp, Kiel der Hafen. Die letzte Überfahrt blieb unklar. Dafür war „Auf See · Richtung Heimat“ ehrlicher als eine konkrete erfundene Verbindung.

## Moderne Karten

Zurückhaltende Landflächen, klare Ortslabels und eine gut lesbare Route. Farbe und Fahrzeug folgen dem aktuellen Briefing: Limousine, SUV, Camper, Zug, Fähre usw. nach tatsächlicher Etappe; der blaue Camper war nur die Gestaltung des ursprünglichen Roadtrips. Unbekannte Modelle/Farben nicht erfinden, einen passenden neutralen Fahrzeugtyp verwenden. Straßenlinie etwa durchgezogen, Wasserlinie gestrichelt. Bei belegter Überfahrt am Hafen erkennbar zum Schiff wechseln. Die Form des Fahrzeugs muss zur Bewegung passen; bei Symbolrotation Blickrichtung und SVG-Ausrichtung berücksichtigen.

Bei einem Urlaub an einem Ort genügen gegebenenfalls eine Übersicht und dezente Ortsnamen. Bei Mischformen Stadtaufenthalt und Fahrstrecke unterschiedlich behandeln. Kein Auto auf einer Stadt-/Flugetappe darstellen, nur weil später ein Mietwagen vorkommt. Eine grobe Ost-West-Reisebeschreibung belegt keine bestimmte Fernstraße, Anzahl gefahrener Meilen oder besuchten Nationalparks. [Reisebriefing und Kartenideen](travel-films.md).

Eine Karte ist kein Straßenrouter. Direkte Linien dürfen als schematisch gekennzeichnet sein; keine Linie quer über Land als vermeintliche Fähre zeigen. Bei echter Straßenführung Routingdaten nutzen und deren Lizenz/Attribution mitführen. GeoJSON verwendet gewöhnlich `[longitude, latitude]`, nicht die umgekehrte Reihenfolge. Projektion, Kamerafahrt, Marker und Route müssen dieselbe Transformation verwenden. Vorwärts/Endpunkt/Rückfahrt in drei Phasen prüfen. Karten mit unbekanntem Ziel lieber weglassen oder nur einen belegten Ankunftspunkt zeigen.
