# DiWoDo 2026

Dies ist unser DiWoDo-Demo-Projekt, welches wir auf der [Digitalen Woche Dortmund (DiWoDo)](https://www.diwodo.de/) am 26.09.2024 im Rahmen der Keynote ["Open Source: Generative Plattformentwicklung mit ViUR für die Google App Engine"](https://www.diwodo.de/events/open-source-generative-plattformentwicklung-c5b21ddc-8b68-464c-a6f7-1d79b2ae264a/?sourcePath=%2Fevents%2F%3Fq%3Dviur) im Projektspeicher Dortmund abgehalten haben.

Die Keynote wurde auch im Livestream übertragen und kann [bei YouTube angeschaut](https://www.youtube.com/live/-heq-E3APi4?si=kDYfi0D5Tcxs16Ph&t=15939) werden!

Das Projekt wurde im Rahmen des [Digiday 2025 der SIHK zu Hagen](https://www.ihk.de/hagen/digitalisierung/events-netzwerke/digiday) um AI-Demo-Funktionalitäten erweitert und dort präsentiert.

## Schnellstart

Dieses Projekt benutzt uv als Build-Umgebung:

```sh
$ uv sync --dev
$ uv run viur build release
```

## Lokal starten

```sh
$ uv run viur run
```

## Deployment

```sh
$ uv run viur build release
$ uv run viur cloud deploy app
```

> [!IMPORTANT]
> Das Google Cloud AppEngine Projekt "diwodo-demo-viur3" ist nicht öffentlich, weshalb ein eigenes Projekt eingerichtet werden muss.
> Welche Schritte dazu nötig sind ist [hier](https://github.com/viur-framework/viur-base?tab=readme-ov-file#requirements) beschrieben.
>

## Lizenz

Copyright © 2026 Mausbrand Informationssysteme GmbH.<br>
Mausbrand und ViUR sind eingetragene Marken der Mausbrand Informationssysteme GmbH.

Lizenziert unter der MIT Lizenz. Siehe LICENSE für weitere Informationen.
