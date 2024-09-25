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
            "Kanalhafen",
            "Kohlenhafen",
            "Petroleumhafen",
            "Stadthafen",
            "Südhafen",
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
        descr="Telefon",
        default_country_code="+49",
        params={
            "visibleIf": """ category == "service" """,
        },
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
