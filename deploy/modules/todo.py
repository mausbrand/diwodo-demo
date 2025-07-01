import base64
from viur.core.prototypes import List
from viur.core import conf, current, utils, exposed, skey, access, tasks
from viur.assistant import CONFIG as ASSISTANT_CONFIG
from viur.core.skeleton import RelSkel as ActionSkel  # TODO: ActionSkel
from viur.core.bones import *


class Todo(List):
    adminInfo = {
        "icon": "file-check-fill",
        "columns": (
            "creationdate",
            "lastname",
            "firstname",
            "facility",
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
        "admin": ["*"],
    }

    addTemplate = "todo_add"
    addSuccessTemplate = "todo_add_success"

    def canAdd(self):
        return True  # everyone can add entries!

    def addSkel(self):
        skel = super().addSkel().clone()

        skel.summary = None
        skel.status = None
        skel.user = None
        skel.due_date = None

        return skel

    def onAdded(self, skel):
        if skel["attachments"]:
            self._enrich_with_image_contents(skel["key"])

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

    # @tasks.CallDeferred
    @exposed
    def enrich_with_image_contents(self, key):
        assert (skel := self.skel().read(key))

        content = [
            {
                "type": "text",
                "text": (
                    "Erstelle zu folgenden Bildern eine fachmännische Beschreibung."
                    "Die Beschreibung soll nicht auf einzelne Bilder hinweisen sondern das Gesamtbild beschreiben."
                    "Vermeide es, auf Ursachen hinzuweisen, sondern beschreibe möglichst genau die Situation und Komponenten."
                    "Farben sind dabei nicht relevant, es geht um Zustand und Bezeichnung."
                    "Die Beschreibung soll bereits maßgeschneidert für einen Fachmann sein."
                    f"Hier die Anfrage: {skel["message"]}"
                ),
            },
        ]

        for image in skel["attachments"]:
            if image["dest"]["mimetype"].startswith("image/"):
                file_key = image["dest"]["key"]

                blob, mime = conf.main_app.file.read(key=file_key)
                if not blob:
                    raise errors.NotFound(f"File not found with {file_key=!r}")

                resized_image_bytes = conf.main_app.assistant._get_resized_image_bytes(
                    image=blob,
                    target_pixel_count=ASSISTANT_CONFIG.describe_image_pixel_default,
                    jpeg_quality=ASSISTANT_CONFIG.describe_image_jpeg_quality_default,
                )
                base64_image = base64.b64encode(resized_image_bytes).decode("utf-8")

                content.append(
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "low",
                        },
                    }
                )

        answer = conf.main_app.assistant.openai_create_completion(
            model=conf.main_app.assistant.getContents()["openai_model"],
            messages=[{
                "role": "user",
                "content": content,
            }],
        )

        skel.patch({"summary": answer})


Todo.html = True
Todo.json = True
