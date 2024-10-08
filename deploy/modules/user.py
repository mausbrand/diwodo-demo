from viur.core.modules.user import User


class User(User):
    """
    Customization of the default user module.
    """

    # Extend default adminInfo to custom adminInfo
    adminInfo = User.adminInfo | {
        "name": "Benutzer",
        "columns": [
            "name",
            "firstname",
            "lastname",
        ],
        "filter": {
            "orderby": "lastname",
        },
    }

    roles = {
        "indoor": ["view"],
    }

    def get_role_defaults(self, role: str) -> set[str]:
        if role in ("field", "indoor", "admin"):
            return {"admin"}

        return set()


User.json = True
