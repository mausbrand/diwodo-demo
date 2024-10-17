from viur.core.prototypes import List
from viur.core import current, utils, exposed, skey, access
from viur.core.skeleton import RelSkel as ActionSkel  # TODO: ActionSkel
from viur.core.bones import *


class Todo(List):
    adminInfo = {
        "icon": "file-check-fill",
        "columns": (
            "creationdate",
            "lastname",
            "firstname",
            "phone",
            "message",
            "user",
        ),
        "views": [
            {
                "name": "Service - Neu",
                "icon": "hammer",
                "filter": {
                    "category": "service",
                    "status": "new",
                },
                "actions": ["assign"],
                "customActions": {
                    "assign": {
                        "name": "Zuweisen",
                        "access": ["todo-edit", "root"],
                        "icon": "person-plus-fill",
                        "variant": "success",
                        "outline": True,
                        "action": "action",
                        "url": "/{{module}}/assign",
                        "enabled": "True",
                        "show_label": True,
                        "target": "popup",
                    },
                },
            }
        ],
    }

    default_order = {
        "orderby": "creationdate",
        "orderdir": "desc",
    }

    roles = {
        "field": ["edit", "view"],
        "indoor": ["*"],
    }

    addTemplate = "todo_add"
    addSuccessTemplate = "todo_add_success"

    def canAdd(self):
        return True  # everyone can add entries!

    def addSkel(self):
        skel = super().addSkel().clone()
        skel.status = None
        skel.user = None
        return skel

    def listFilter(self, query):
        if query := super().listFilter(query):
            if not utils.string.is_prefix(self.render.kind, "json.vi"):
                cuser = current.user.get()
                query.mergeExternalFilter({
                    "user.dest.key": cuser["key"],
                })

        return query

    @exposed
    @skey(allow_empty=True)
    @access("todo-edit")
    def assign(self, **kwargs):

        # ActionSkel for assigning multiple todos to one user
        class TodoAssignSkel(ActionSkel):
            todo = RelationalBone(
                kind="todo",
                descr="Todos",
                multiple=True,
                required=True,
                format="$(dest.lastname) - $(dest.message)",
                refKeys={
                    "lastname",
                    "message",
                }
            )

            user = UserBone(
                descr="Zuweisen an",
                required=True,
            )

        action_skel = TodoAssignSkel()

        if selected_keys := current.request.get().context.get("viur_selected_keys"):
            if isinstance(selected_keys, str):
                selected_keys = selected_keys,

            for key in selected_keys:
                action_skel.setBoneValue("todo", key, append=True)

        if not kwargs or not action_skel.fromClient(kwargs):
            return self.render.render("assign", action_skel)

        for todo in action_skel["todo"]:
            self.editSkel().patch(
                values={
                    "status": "open",
                    "user": action_skel["user"]["dest"]["key"],
                },
                key=todo["dest"]["key"],
            )

        return self.render.render("assignSuccess", action_skel)


Todo.html = True
Todo.json = True
