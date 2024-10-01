# DiWoDo 2024

Dies ist unser DiWoDo-Demo-Projekt, welches wir auf der [Digitalen Woche Dortmund (DiWoDo)](https://www.diwodo.de/) am 26.09.2024 im Rahmen der Keynote ["Open Source: Generative Plattformentwicklung mit ViUR für die Google App Engine"](https://www.diwodo.de/events/open-source-generative-plattformentwicklung-c5b21ddc-8b68-464c-a6f7-1d79b2ae264a/?sourcePath=%2Fevents%2F%3Fq%3Dviur) im Projektspeicher Dortmund abgehalten haben.

Die Keynote wurde auch im Livestream übertragen und kann [bei YouTube angeschaut](https://www.youtube.com/live/-heq-E3APi4?si=kDYfi0D5Tcxs16Ph&t=15939) werden!

## Schnellstart

Dieses Projekt wurde entwickelt und getestet mit:

- Python 3.12.6
- gcloud 494.0.0
  - app-engine-python
  - app-engine-python-extras
- pipenv 2024.0.2
- npm 10.8.3

Projekt bauen und starten:

```sh
$ pipenv install --dev
$ pipenv shell
$ viur build release
$ viur run
```

> [!IMPORTANT]
> Das Google Cloud AppEngine Projekt "diwodo-demo-viur3" ist nicht öffentlich, weshalb ein eigenes Projekt eingerichtet werden muss.
> Welche Schritte dazu nötig sind ist [hier](https://github.com/viur-framework/viur-base?tab=readme-ov-file#requirements) beschrieben.
>

## Lizenz

Copyright © 2024 Mausbrand Informationssysteme GmbH.<br>
Mausbrand und ViUR sind eingetragene Marken der Mausbrand Informationssysteme GmbH.

Lizenziert unter der MIT Lizenz. Siehe LICENSE für weitere Informationen.
