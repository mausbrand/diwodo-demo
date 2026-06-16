from viur.core.modules.user import User


class User(User):
    """
    Customization of the default user module.
    """

    roles = {
        "indoor": ["view"],
    }

    # Extend default adminInfo to custom adminInfo
    def adminInfo(self):
        return super().adminInfo() | {
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

    def get_role_defaults(self, role: str) -> set[str]:
        if role in ("field", "indoor", "admin"):
            return {"admin"}

        return set()


User.json = True
