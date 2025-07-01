from viur.core.prototypes import List
from viur.core import current, utils, exposed, skey, access
from viur.core.skeleton import RelSkel as ActionSkel  # TODO: ActionSkel
from viur.core.bones import *


class Facility(List):
    adminInfo = {
        "name": "Anlage",
        "icon": "houses",
    }

    default_order = {
        "orderby": "sortindex",
    }

    roles = {
        "*": ["view"],
        "indoor": ["*"],
    }

    def listFilter(self, query):
        return query  # public access!


Facility.html = True
Facility.json = True
