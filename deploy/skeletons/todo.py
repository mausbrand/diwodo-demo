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

    facility = RelationalBone(
        descr="Anlage",
        kind="facility",
        required=True,
        type_suffix="select",
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

    attachments = FileBone(
        descr="Fotos",
        multiple=True,
    )

    summary = TextBone(
        descr="Zusammenfassung (KI)",
        readOnly=True,
        indexed=False,
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

    proposed_user = UserBone(
         descr="Vorschlag (KI)",
         readOnly=True,
    )

    proposed_user_why = TextBone(
        descr="Vorschlags-Begründung (KI)",
        readOnly=True,
        indexed=False,
    )

    user = UserBone(
         descr="Zugewiesen an",
    )

    due_date = DateBone(
        descr="Fällig bis",
    )
