from viur.core import skeleton, utils
from viur.core.bones import *


class FacilitySkel(skeleton.Skeleton):
    sortindex = SortIndexBone()

    name = StringBone(
        descr="Bezeichnung",
        required=True,
    )

    descr = TextBone(
        descr="Beschreibung",
        required=True,
    )

    image = ImageBone(
        descr="Bild",
        required=True,
    )

    city = StringBone(
        descr="Ort",
    )
