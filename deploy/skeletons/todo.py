from viur.core import skeleton, utils
from viur.core.bones import *


class TodoSkel(skeleton.Skeleton):

    firstname = StringBone(
        descr="Vorname",
    )

    lastname = StringBone(
        descr="Nachname",
        required=True,
    )

    building = SelectBone(
        descr="Gebäude",
        required=True,
        values=(
            "Kanalhafen 23",
            "Kohlenhafen 13",
            "Petroleumhafen 42",
            "Stadthafen 1a",
            "Stadthafen 1b",
            "Südhafen 9",
        )
    )

    category = SelectBone(
        descr="Thema",
        defaultValue="question",
        required=True,
        values={
            "question": "Anfrage",
            "billing": "Abrechnung",
            "service": "Service",
        },
    )

    phone = PhoneBone(
        default_
    )

    message = TextBone(
        descr="Nachricht",
        required=True,
        validHtml=None,
    )

    status = SelectBone(
        descr="Status",
        required=True,
        defaultValue="new",
        values={
            "new": "Neu",
            "open": "Zugewiesen",
            "pending": "In Bearbeitung",
            "closed": "Geschlossen",
        },
    )

    user = UserBone(
         descr="Zugewiesen an",
    )
