from viur.core import skeleton, utils
from viur.core.bones import *
from viur.assistant.bones.image import ImageBone


class FacilitySkel(skeleton.Skeleton):
    sortindex = SortIndexBone()

    name = StringBone(
        descr="Bezeichnung",
        required=True,
    )

    descr = TextBone(
        descr="Beschreibung",
    )

    image = ImageBone(
        descr="Bild",
        public=True,
    )

    city = StringBone(
        descr="Ort",
    )
