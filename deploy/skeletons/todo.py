from viur.core import skeleton, utils
from viur.core.bones import *


class TodoSkel(skeleton.Skeleton):
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

    reason = SelectBone(descr="Thema", values={
        "billing":"Abrechnung",
        "question":"Anfrage",
        "service":"Service"
    },defaultValue="question")

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
            "pending": "In Bearbeitung",
            "closed": "Geschlossen",
        }
    )

    user = UserBone(
         descr="Zugewiesen an",
    )
