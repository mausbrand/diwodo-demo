
# 1) Phone

```py
    phone = PhoneBone(
        descr="Telefon",
        default_country_code="+49",
        params={
            "visibleIf": """ category == "service" """,
        },
    )
```

# 2) Admin

```py
conf.admin.login_logo = "/static/site/images/logo.svg"
conf.admin.login_background = "/static/site/images/stage.jpg"
conf.admin.color_primary = "#970000"
conf.admin.color_secondary = "#ffffff"
```

# 3) View

```py
        "views": [
            {
                "name": "Service - Neu",
                "icon": "hammer",
                "filter": {
                    "category": "service",
                    "status": "new",
                },
            }
        ],
```

# 4) Assign

```py
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


    # ---

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
            self.editSkel().update(
                values={
                    "status": "open",
                    "user": action_skel["user"]["dest"]["key"],
                },
                key=todo["dest"]["key"],
            )

        return self.render.render("assignSuccess", action_skel)


```
