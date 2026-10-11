# Erfahrungen, die wirklich etwas ändern

## Roadtrip: aus einem ruhigen Film wurde bewusst mehr Comedy

Der geprüfte Projektstatus der dritten Version enthält 11.425 Frames bei 30 fps, also 6:20,833; 1920×1080/H.264. Im finalen Messbericht: −16,66 LUFS, −3,07 dBTP, keine erkannten Schwarzintervalle und Decoder-Exitcode 0. Diese Werte gehören zu diesem Film, nicht zur synthetischen Demo im Repo. Manuelles Hören durch das Modell war nicht erfolgt.

Die erste Auswahl bewahrte Etappen und emotionale Ruhe. Nutzerfeedback verlangte mehr Übergänge, Gesichts-Zoom, Scooter-Flammen und später **deutlich mehr** lustige Aktionen. Daraus entstanden 20 zusätzliche Gags mit neun individuellen Freistellern. Lernpunkt: Humor-Dichte ist ein Briefingparameter. „Hochwertig“ bedeutet nicht automatisch „kaum albern“.

Ein generativ erstellter Freisteller veränderte Details und wurde verworfen. Originalpixel-Masken bewahrten die Person. Drei Masken brauchten Korrekturen zwischen den Beinen. Lernpunkt: nicht nur Außenkontur prüfen und nicht „Freistellung erledigt“ melden, bevor die maximalen Bewegungsphasen angesehen wurden.

Ein späterer Renderer-Test entdeckte leere Frames in einem Ausschnitt, nicht im Hauptfilm. Lernpunkt: QA muss den wirklich ausgelieferten Encode prüfen; Hilfsreels können eigene Fehler haben.

## Familien-Beatcut / VN

Im gelesenen Chat forderte der Nutzer die Chronologie erneut zu prüfen, weil bereits nummerierte Medien keine ausreichende Gewissheit geben. Er verlangte einheitliches 16:9, weichgezeichnete Hintergründe, vorsichtigen Zoom und einen kurzen Titel auf einem passenden Foto statt einer langen schwarzen Tafel.

Die erste Aussage „alle Schnitte auf Beatmarken“ wurde vom Nutzer als hörbar ungenügend korrigiert. Lokale Folgeaudits gingen zu Bass-Onsets und kurzen Prüfstücken über. Dabei existieren Berichte mit unterschiedlichen Ergebnissen und Songständen. Keinen davon als zeitloses Qualitätssiegel übernehmen. Künftig Messungen an Timeline-/Audiohash binden und getrennt auflisten: Marker-Abstand, Onset-Nähe, Gehör.

Ein späterer Songwechsel ersetzte einen ursprünglich geplanten Titel. Lernpunkt: aktuelle Dateien und aktuellen Stand lesen; ein älterer Chat-Prompt ist kein verlässlicher endgültiger Schnittplan.

## Übertragbare Entscheidungen

| Beobachtung | Künftige Entscheidung |
|---|---|
| Nutzer will viel mehr Comedy | neue passende Gags über den Film verteilen, ruhiges Finale bewahren |
| Hafen unklar und nicht wichtig | neutrale Formulierung, keine erfundene Route |
| schmaler Portrait-Shot | Person vollständig, Blur-Hintergrund; nicht blind vergrößern |
| Songwechsel klingt daneben | Audiooffset/Trim und Phase am Übergang erneut prüfen |
| kleine QA-Scores sehen gut aus | tatsächlichen Export trotzdem ansehen/anhören |
| Weitergabe an anderes LLM | relative Pfade, manifeste Daten, konkrete offene Punkte, getestete Befehle |
