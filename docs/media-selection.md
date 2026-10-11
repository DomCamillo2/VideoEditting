# Gute Auswahl beginnt vor dem Beatcut

Fünf fast gleiche Bilder sind keine fünf verschiedenen Momente. Zuerst nach Ereignis und ähnlicher Komposition gruppieren, dann innerhalb der Gruppe vergleichen. Die vorhandene `catalog`-CLI erkennt **exakte** Duplikate per Hash; ähnliche Bilder, Blickrichtung, Gesichtsschärfe und schöne Momente beurteilt der [Auswahl-Skill](../skills/video-select-media/SKILL.md) mit Sichtkontrolle. Es gibt hier keinen vorgetäuschten automatischen Ästhetik-Detektor.

## Ein konkreter Vergleich

| Aufnahme eines Gruppenmoments | Befund nach Sichtung | Entscheidung |
|---|---|---|
| A | Gesicht der vorderen Person weich, Hintergrund scharf | Nicht auswählen, falls bessere Variante vorhanden |
| B | Alle relevanten Gesichter scharf, natürliche Reaktion | Hauptaufnahme |
| C | Fast identisch zu B, ungünstigerer Gesichtsausdruck | Reserve oder aussortiert aus dem Schnitt |
| D | Verwackelt, keine zusätzliche Handlung | Aussortiert aus dem Schnitt |
| E | Neue gemeinsame Reaktion mit leichtem Bewegungsunschärfeanteil | Optional behalten, wenn sie eine eigene Pointe erzählt |

Das ist ein erklärendes Beispiel, keine durchgeführte Analyse echter Fotos. Originale bleiben erhalten. Ein gewolltes Bokeh, eine Silhouette, geschlossene Augen beim Lachen oder ein einzigartiger weicher Erinnerungsmoment sind nicht automatisch Ausschuss.

## Praktischer Ablauf

1. Bilder korrekt drehen und pro ähnlichem Moment einen Kontaktbogen mit IDs erstellen.
2. Kandidaten im Original bzw. bei brauchbarer Auflösung vergleichen; relevante Gesichter/Motive vergrößern. Automatische Schärfe- oder Ähnlichkeitswerte nur als Hinweise verwenden.
3. Pro engem Cluster normalerweise ein starkes Bild auswählen. Weitere Bilder brauchen eine neue Handlung, Perspektive oder Reaktion. Ein ganzes Ereignis darf natürlich mehrere unterschiedliche Bilder bekommen.
4. Bei Videos geeignete **Zeitabschnitte** sichten: nicht nur Anfangsframe, sondern Bewegung, Ton, Fokusverlust, Verwacklung und saubere Schnittpunkte.
   Einen wichtigen Moment bei anhaltendem Kamerawackeln vor dem Aussortieren mit einer vorsichtig stabilisierten Version vergleichen; Beschnitt und Verformungen mitprüfen. [Stabilisierung im Workflow](workflow.md#stark-verwackelte-clips-gezielt-stabilisieren).
5. Entscheidung und Grund in [culling.csv](../templates/culling.csv) festhalten; technische Unsicherheit als `review` markieren. Die bestehende [Schnittauswahl](../templates/selection.csv) ergänzt anschließend Quellbereiche, Framing und Kapitel.
6. Im Rohschnitt Wiederholungen zwischen benachbarten Clustern und eine faire Mischung aus Personen, Tätigkeiten und Landschaft prüfen. Keine starre Personenquote, keine einzelne Person ständig als Gag-Ziel.

Motiv- und Augenschärfe getrennt zu betrachten ist auch in Adobes Culling-Werkzeugen vorgesehen; dort bleiben manuelle Auswahlkorrekturen möglich. Unser Workflow übernimmt diese Unterscheidung als Sichtungsprinzip, nicht Adobes Modell oder Scores. [Adobe: Assisted Culling](https://helpx.adobe.com/ie/lightroom/desktop/organize-photos/assisted-culling.html).
