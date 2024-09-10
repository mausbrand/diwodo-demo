from viur.core import skeleton
from viur.core.bones import *


class TodoSkel(skeleton.Skeleton):
    firstname = StringBone(
        descr="Vorname",
    )

    lastname = StringBone(
        descr="Nachname",
        required=True,
    )

    subject = StringBone(
        descr="Anliegen",
        required=True,
    )

    message = TextBone(
        descr="Nachricht",
        required=True,
        validHtml=None,
    )
    status = SelectBone(
        descr="Status",
        required=True,
        defaultValue="open",
        values={
            "open": "Offen",
            "closed": "Geschlossen"
        }
    )
