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
        # LIVE (3)
        "views": [
            {
                "icon": "chat-dots-fill",  # LIVE (4)
                "name": "Service - Neu",
                "filter": {
                    "category": "service",
                    "status": "new",
                },
                "actions": ["assign"],
                "customActions": {  # LIVE(5)
                    "assign": {
                        "name": "Zuweisen",  # button name
                        "access": ["todo-edit", "root"],  # Who may trigger?
                        "icon": "person-plus-fill",  # button icon
                        "variant": "success",  # button color
                        "outline": True,  # button outline style
                        "action": "action",  # ActionSkel
                        "url": "/{{module}}/assign",  # actionSkel initial url
                        "enabled": 'True',  # regel wann button aktiv "TRUE" === immer
                        "show_label": True,  # button ohne label
                        "target": "popup",  # popup, tab
                    },
                },
            }
        ]
    }

    default_order = {
        "orderby": "creationdate",
        "orderdir": "desc",
    }

    addTemplate = "todo_add"
    addSuccessTemplate = "todo_add_success"

    def canAdd(self):
        return True  # everyone can add entries!

    def addSkel(self):
        # skel = self._resolveSkelCls().subskel(("subject", "message", "*stname"))
        # skel = self._resolveSkelCls().subskel("add")
        # skel = self._resolveSkelCls().subskel(("message", ), "add")
        # return skel

        skel = super().addSkel().clone()
        skel.status = None
        skel.user = None
        return skel

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
                    "subject",
                }
            )

            user = UserBone(
                descr="Zuweisen an",
                required=True,
            )

        action_skel = TodoAssignSkel()

        if selected_keys := current.request.get().context.get("viur_selected_keys"):
            for key in selected_keys:
                action_skel.setBoneValue("todo", key, append=True)

        if not kwargs or not action_skel.fromClient(kwargs):
            # TODO: Provide generic render action skel
            return self.render.edit(action_skel, "assign")

        # TODO: Add program logic here
        # TODO: Create skel.update() function for transactional in-place update
        for todo in action_skel["todo"]:
            skel = self.editSkel()
            skel.fromDB(todo["dest"]["key"])
            skel["status"] = "open"
            skel.setBoneValue("user", action_skel["user"]["dest"]["key"])
            skel.toDB()

        # TODO: Provide generic render action success
        return self.render.editSuccess(action_skel, "assignSuccess")

    def listFilter(self, query):
        if query := super().listFilter(query):
            if not utils.string.is_prefix(self.render.kind, "json.vi"):
                cuser = current.user.get()
                query.mergeExternalFilter({
                    "user.dest.key": cuser["key"],
                })

        return query


Todo.html = True
Todo.json = True
