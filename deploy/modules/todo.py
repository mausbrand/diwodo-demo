import logging
import base64
import json
from viur.core.prototypes import List
from viur.core import conf, current, utils, exposed, skey, access, tasks
from viur.assistant import CONFIG as ASSISTANT_CONFIG
from viur.core.skeleton import RelSkel as ActionSkel  # TODO: ActionSkel
from viur.core.bones import *


class Todo(List):
    """
    Module for managing todo requests and tasks for
    """
    COLUMNS = (
        "creationdate",
        "lastname",
        "facility",
        "phone",
        "message",
        "summary",
        "user",
    )

    adminInfo = {
        "icon": "file-check-fill",
        "columns": ("status", "category") + COLUMNS,
        "views": [
            {
                "name": "Service - Neu",
                "icon": "hammer",
                "columns": COLUMNS,
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
        '''
        skel = self.skel(
            bones=(
                "category",
                "firstname",
                "lastname",
                "phone",
                "facility",
                "message",
                "attachments",
            )
        )
        '''

        skel = super().addSkel().clone()

        skel.summary = None
        skel.status = None
        skel.proposed_user = None
        skel.proposed_user_why = None
        skel.user = None
        skel.due_date = None

        return skel

    def onAdded(self, skel):
        if skel["attachments"]:
            self._ai_summary(skel["key"])
        else:
            self._ai_propose(skel["key"])

        super().onAdded(skel)

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

    @tasks.CallDeferred
    def _ai_summary(self, key):
        assert (skel := self.skel().read(key))

        content = []

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

        content.append({
            "type": "text",
            "text": (
                f"""
                Du bist ein erfahrener Bausachverständiger.
                Analysiere den folgenden Freitext {"im Zusammenhang mit den Fotos" if content else ""}:

                {skel["message"]}

                Auftrag:
                Verfasse eine fachgerechte Momentaufnahme (Ist-Situation) des gemeldeten Schadens / Mangels.
                Gib ausschließlich objektive Beobachtungen wieder.
                Keine Vermutungen zu Ursachen, Empfehlungen oder Verbesserungsvorschläge.
                Verwende neutrale deutsche Fachsprache; übersetze internationale Fachbegriffe ins Deutsche.
                Lass unklare oder widersprüchliche Angaben unkommentiert;
                Beschreibe nur, was eindeutig erkennbar ist.
                Maximal 200 Wörter, bei zu wenig Eingabe reicht ein Satz.

                Erzeuge HTML als Ausgabe, aber nur <br> für Absatzumbrüche, keine anderen HTML-Tags.
                Bitte mehrere kurze Absätze generieren.
                """
            ),
        })

        answer = conf.main_app.assistant.openai_create_completion(
            model=conf.main_app.assistant.getContents()["openai_model"],
            messages=[{
                "role": "user",
                "content": content,
            }],
        )

        logging.info(f"{answer=}")

        skel.patch({"summary": answer})
        self._ai_propose(key)

    @tasks.CallDeferred
    def _ai_propose(self, key):
        assert (skel := self.skel().read(key))

        # Fetch all field users and their skills
        q = conf.main_app.user.skel().all()
        q.filter("roles", "field")

        user_skills = {}
        for user_skel in q.fetch():
            if skills := user_skel["skills"]:
                user_skills[str(user_skel["key"])] = skills

        answer = conf.main_app.assistant.openai_create_completion(
            model=conf.main_app.assistant.getContents()["openai_model"],
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""
                            Du bist ein intelligenter Matching-Assistent.
                            Zuerst erhältst du eine Liste von Mitarbeitern mit ihren Fähigkeiten:

                            {"\n".join(f"{key}: {",".join(value)}" for key, value in user_skills.items())}

                            Danach folgt eine Freitext-Problembeschreibung:

                            {skel["summary"] or skel["message"]}

                            Jetzt kommt deine Aufgabe:
                            Berücksichtige exakte sowie sinnvolle Teilwort-Übereinstimmungen;
                            Groß-/Kleinschreibung darf nicht ignoriert werden.
                            Ziehe semantische Ähnlichkeiten (Synonyme, Ober-/Unterbegriffe) eigenständig heran;
                            es gibt kein Wörterbuch.
                            Deckt kein Mitarbeiter alle Anforderungen ab, gib denjenigen mit den meisten passenden
                            Teiltreffern zurück; bei Gleichstand wähle den zuerst gelisteten.

                            Antwort JSON-kodiert als Objekt:
                            - Schlüssel "key" mit dem Key als Wert des passenden Mitarbeiters,
                            - Schlüssel "reason" mit einem kurzen Text als Begründung, warum dieser Mitarbeiter
                              (maximal 100 Wörter)

                            Wenn kein passender Mitarbeiter gefunden wird, ein leeres JSON-Objekt ({{}}) liefern.
                        """
                    }
                ],
            }],
        )

        if answer:
            answer = json.loads(answer)
            logging.info(f"{answer=}")

            skel.patch({
                "proposed_user": answer["key"],
                "proposed_user_why": answer["reason"]
            })
        else:
            logging.info("No proposed_user found for this problem!")

    # @exposed
    # def ai_summary(self, key):
    #     self._ai_summary(key)

    # @exposed
    # def ai_propose(self, key):
    #     self._ai_propose(key)


Todo.html = True
Todo.json = True
