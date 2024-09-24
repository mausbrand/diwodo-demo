from viur.core import skeleton, utils
from viur.core.bones import *


class TodoSkel(skeleton.Skeleton):
    subSkels = {
        "*": ("*name", ),
        "add": ["subject"],
    }

    # FIXME: viur-core
    creationdate = DateBone(
        descr="Erstellt am",
        readOnly=True,
        visible=False,
        indexed=True,
        compute=Compute(fn=utils.utcNow, interval=ComputeInterval(ComputeMethod.Once)),
    )

    firstname = StringBone(
        descr="Vorname",
    )

    lastname = StringBone(
        descr="Nachname",
        required=True,
    )

    category = SelectBone(
        descr="Thema",
        defaultValue="question",
        required=True,
        values={
            "question": "Frage",
            "billing": "Abrechnung",
            "service": "Service",
        },
    )

    # LIVE (1)
    phone = PhoneBone(
        descr="Telefon",
        default_country_code="+49",
        params={
            "visibleIf": """ category == "service" """  # LIVE(2)
        }
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
