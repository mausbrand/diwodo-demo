from viur.core.prototypes import List
from viur.core import exposed, skey, access
from viur.core.skeleton import RelSkel as ActionSkel  # TODO: ActionSkel
from viur.core.bones import *


class Todo(List):
    adminInfo = {
        "icon": "file-check-fill",
        "columns": (
            "creationdate",
            "lastname",
            "firstname",
            "subject",
        ),
        "actions":["assign"],
        "customActions":{
            "assign": {
                    "name": "Zuweisen",  # button name
                    "access": ["todo-edit", "root"],  # wer darf triggern
                    "icon": "person-plus-fill", # button icon
                    "variant":"success", # button color
                    "outline":True, # button outline style
                    "action": "action",
                    "url": "/todo/assign",  # actionSkel initial url
                    "enabled": 'True',  # regel wann button aktiv "TRUE" === immer
                    "show_label":True, # button ohne label
                    "target":"popup" # popup, tab
                },
        }
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
        # TODO: new skel.sub_skel() feature!
        skel = super().addSkel().clone()
        #skel.status = None
        return skel

    @exposed
    @skey(allow_empty=True)
    @access("root", "todo-edit")
    def assign(self, **kwargs):

        # ActionSkel for assigning multiple todos to one user
        class TodoAssignSkel(ActionSkel):
            todo = RelationalBone(
                kind="todo",
                descr="Todos",
                multiple=True,
                required=True,
            )

            user = UserBone(
                descr="Zuweisen an",
                required=True,
            )

        action_skel = TodoAssignSkel()

        if not kwargs or not action_skel.fromClient(kwargs):
            # TODO: Provide generic render action skel
            return self.render.edit(action_skel, "assign")

        # TODO: Add program logic here
        for todo in action_skel["todo"]:
            skel = self.editSkel()
            skel.fromDB(todo["dest"]["key"])
            skel.setBoneValue("user", action_skel["user"]["dest"]["key"])
            skel.toDB()

        # TODO: Provide generic render action success
        return self.render.editSuccess(action_skel, "assignSuccess")


Todo.html = True
Todo.json = True
