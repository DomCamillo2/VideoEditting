# Vom Material zum Film

Bei erstmaliger Übernahme des Toolkits zuerst [SETUP.md](../SETUP.md): Skills auswählen, vorhandene Werkzeuge prüfen und gewünschte MCPs einrichten. Erst danach beginnt dieser Filmablauf. Bereits beantwortete Setup-/Briefingfragen werden übernommen; Zusatzinstallationen können abgelehnt werden.

## Erst die Absicht, dann die Effekte

Für einen Freundschaftsfilm zählen gemeinsame Erlebnisse, kleine Reaktionen und ein fühlbarer Reisebogen. Ein brauchbarer Aufbau: kurzer Auftakt → Aufbruch → wechselnde Erlebnisse → ruhiger Höhepunkt → gemeinsamer Abschluss. 5–8 Sekunden Intro und 2–5 Sekunden Karten waren geeignete Roadtrip-Werte. Bei einem 20-Sekunden-Reel wären sie viel zu lang.

Die Reiseart beeinflusst diesen Bogen: Roadtrip, ein Ort mit Ausflügen, Rundreise, Aktivität oder Mischform. Bei einem City-Aufenthalt vor dem Roadtrip zuerst Stadtleben erzählen und das Fahrzeug erst in der passenden Phase als Motiv aufnehmen. Fahrzeugtyp und Kartenstil aus dem aktuellen Briefing verwenden. [Fragen, Kapitelmodelle und konkrete Roadtrip-Ideen](travel-films.md).

Eine Version nach der anderen:

| Phase | Konkretes Ergebnis | Freigabe zum Weiterarbeiten |
|---|---|---|
| Inventur | Katalog, Duplikate, Kontaktbögen, Zeitkonflikte | Material zugänglich; Unklarheiten sichtbar |
| Story | Etappen, stärkste Momente, Songabschnitte | Chronologie plausibel, kein erfundener Ort |
| Rohschnitt | klare Szeneauswahl, Musik, feste Laufzeit | Film funktioniert ohne Effekte |
| Feinschnitt | Beatkanten, Ausschnitte, Originalton | keine unbeabsichtigten Mini-Clips |
| Comedy | je Moment ein nachvollziehbarer Gag | Personen vorteilhaft; Pointe lesbar |
| Vorschau | kleiner Export + dokumentierte Prüfung | konkrete Fehler behoben |
| Master | gewünschter Codec + vollständige QA | Datei vorhanden und decodierbar |
| Handoff | Projekt, Exporte, offene Punkte | andere Person findet sofort den Einstieg |

Diese Kriterien sind Arbeitskontrollen, keine zusätzlichen Nutzerfreigaben. Vorhandene Autorisierung nutzen; nicht nach jeder Etappe erneut fragen.

## Auswahl statt Vollständigkeitszwang

Exakte Duplikate per Hash markieren. Ähnliche Bilder anhand Kontaktbögen vergleichen, nicht automatisch löschen. Ein leicht unscharfes authentisches Lachen kann wichtiger sein als das zehnte perfekte Gebäude. Schlechte Anfänge/Enden längerer Clips wegtrimmen. Gruppen, Aktivitäten und Landschaften abwechseln; nicht dieselbe Person dauerhaft als Hauptfigur behandeln.

Jeder gewählte Clip braucht einen Zweck: Ort zeigen, Bewegung tragen, Beziehung zeigen, Pointierung oder Pause. Ausschlussgründe knapp dokumentieren: Duplikat, Wiederholung, verwackelt, ungünstiger Ausschnitt, schwacher Moment, nicht ausgewählt. „Nicht verwendet“ bedeutet nicht automatisch „schlecht“.

## Stark verwackelte Clips gezielt stabilisieren

Bei einem wichtigen, deutlich verwackelten Moment zuerst störende Anfänge/Enden kürzen oder eine ruhigere Alternative vergleichen. Bleibt die Stelle wertvoll, mit einem vorhandenen Stabilisator eine neue lokale Vergleichsversion erstellen. Mit geringer Stärke beginnen und nur so weit erhöhen, wie Bewegung und Bildausschnitt davon profitieren. Gewollte Schwenks, lebendige Handkamera und Comedy-Shakes bewusst erhalten.

Original und Korrektur in Bewegung vergleichen: bleiben Köpfe, Hände und Füße vollständig, Gebäude und Gesichter unverzerrt, Ränder sauber und der Zoom ruhig? Starke Bewegungsunschärfe lässt sich durch Stabilisierung nicht einfach scharf machen. Bei schlechtem Ergebnis Stärke reduzieren, eine kürzere Stelle verwenden oder mit dokumentiertem Grund beim Original bleiben. Quellmedien bleiben unverändert.

Stabilisierung erfolgt vor endgültigem Hochformat-Ausschnitt, Gesichtstracking, Freistellern und Effekten. Danach Zeitbezug, Originalton und Beatpositionen prüfen. [Konkreter Ablauf, Werkzeugprüfung und Übergabe](../skills/video-editing/references/stabilization.md). Die Anleitung nutzt vorhandene Editor-/FFmpeg-Funktionen; der JSON-Renderer selbst enthält keinen Stabilisator und erkennt Verwacklung nicht automatisch.

## Nutzerkorrekturen ernst nehmen

„Viel mehr funny“ darf zu deutlich mehr Comedy führen. Erhöhe passende Momente und Variationen, nicht nur die Stärke desselben Zooms. Wenn die genaue letzte Hafenroute dem Nutzer egal ist, keine zusätzliche Recherche zum Blocker machen: neutral beschriften und Unsicherheit dokumentieren. Ein stimmiger Rückblick darf die Chronologie verlassen, wenn er klar als Finale erkennbar ist; Hauptreise und Rückblick getrennt prüfen.

## Assistierter Rohschnitt und Übergabe

Für lange Clips können Szenenerkennung, Kontaktbilder und Aktivitätsanalyse Kandidaten liefern. Prüfe auch die vorgeschlagenen Ausschlüsse, damit Landschaftsruhe, Lachen und Reaktionen erhalten bleiben. [Auswahlhilfe und Werkzeuggrenzen](../skills/video-select-media/references/assisted-selection.md).

Quell-In/Out und Timeline-Start/Dauer getrennt speichern, mit expliziten Bildraten und exklusivem Endframe. Vor langem Render mit `validate --media-root` fehlende/verknüpfte Medien prüfen; für die Übergabe eine `cut-list`-CSV erzeugen. [Befehle und Beispiel](../tools/README.md). Ramps und VFR brauchen eine gesonderte Zeitabbildung.
