# Effect Lab

Ein kleiner, unabhängiger Remotion-Starter mit **27 Sekunden Demo**, keine automatische Vollfilm-Pipeline. Alle Assets liegen im Repo. Keine Symlinks auf das ursprüngliche Roadtrip-Projekt, keine privaten Fotos und keine Fonts/API-Keys aus dem Netz nötig.

```sh
npm ci
npm run lint
npm run dev -- --no-open
```

## Komponenten

| Datei / Export | Verwendung |
|---|---|
| `src/effects.tsx` → `Sticker` | geprüfter transparenter Freisteller; spin/download/walkoff/float/launch/boing |
| `FaceMatch` | zwei bereits gerahmte Bilder und zwei getrennte normierte Gesichtsanker |
| `TrackedFlame` | mindestens zwei zeitlich aufsteigende Keyframes, x/y normiert auf Output nach Crop |
| `PortraitFrame` | contain-Vordergrund + cover/blur-Hintergrund, standardmäßig kein Crop/Zoom |
| `WhipAccent` | kurzer Vordergrund-Wisch über unveränderte Schnittkante; kein echter Kameraschwenk |
| `PopLabel` | kurze, framegesteuerte Federbewegung |
| `src/Composition.tsx` | neun separat editierbare Szenen + synthetischer Rhythmus |

Die Figur hat ein festes Demo-Seitenverhältnis von 400:720. Für andere Freisteller die Abmessungen/Transform-Origin im `Sticker` anpassen; nicht einfach fremde Bilder verzerren. Für echte Personen bevorzugt individuelle Kontur-Boundingbox verwenden. `FaceMatch`-Anker gehören zum angezeigten Bild, nicht ungeprüft zu den Rohpixeln vor Rotation/Crop. `TrackedFlame` interpoliert vorbereitete Daten, es betreibt kein automatisches Tracking.

Titel/Layouts der Demo sind für 1920×1080 entworfen. Eine vertikale Komposition muss neu gesetzt werden; es wird keine automatische Responsive-Video-Gestaltung behauptet. Die Effekte selbst lesen fps und Leinwandgröße aus Remotion. Die Demo-Registrierung ist bewusst auf 30 fps gesetzt.

## Export bei Bedarf

```sh
npx remotion render src/index.ts EffectsLab out/effects-v001.mp4 --codec=h264 --scale=0.5
```

Vorhandene Outputs werden nicht automatisch überschrieben. Bei einem neuen Export neuen Versionsnamen wählen. Nach vollständigem Encode mit `../tools/editing.py qa` prüfen. Bei Problemen mit dem gebündelten Browser kann ein lokal vorhandener Chrome über `--browser-executable` verwendet werden; Pfad pro Rechner ermitteln. Im ursprünglichen Mac-Test half zusätzlich `--gl=angle`.

## Abhängigkeiten

Alle Remotion-Pakete exakt 4.0.534, Lockfile mitliefern. `typescript-eslint` ist auf 8.71.1 überschrieben, weil die vom Remotion-Lint-Preset gepinnte ältere Version eine gemeldete transitive Abhängigkeit mitbrachte; Lint/TypeScript werden gegen die aktualisierte Variante geprüft. Keine beliebige `npm audit fix --force`-Aktualisierung über API-Hauptversionen hinweg.

Die eigenen Demografiken und synthetischen Sounds sind unter MIT nutzbar. Die Demo verwendet ausschließlich diese selbst erzeugten Sounds. Fremde Songs werden nicht mitgeliefert; Musik für eigene Projekte bleibt im ignorierten Ordner `public/local/music/`.
