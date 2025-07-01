from viur.core.modules.user import UserSkel
from viur.core.bones import *


class UserSkel(UserSkel):

    skills = StringBone(
        descr="Qualifikationen",
        multiple=True,
    )
