from viur.core import skeleton
from viur.core.bones import *


class TodoSkel(skeleton.Skeleton):
    firstname = StringBone(
        descr="Vorname",
    )

    lastname = StringBone(
        descr="Nachname",
        required=True
    )

    subject = StringBone(
        descr="Anliegen",
        required=True,
    )

    message = TextBone(
        descr="Nachricht",
        required=True,
        validHtml=None,
        params={"visibleIf":"""lastname!='Brose'"""}
    )

    file = FileBone(descr="Datei")

    status = SelectBone(
        descr="Status",
        required=True,
        defaultValue="open",
        values={
            "open": "Offen",
            "pending": "In Bearbeitung",
            "closed": "Geschlossen",
        }
    )

    # user = UserBone(
    #     descr="Zugewiesen an",
    # )
