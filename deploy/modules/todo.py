from viur.core.prototypes import List


class Todo(List):
    adminInfo = {
        "icon": "file-check-fill",
        "columns": (
            "creationdate",
            "lastname",
            "firstname",
            "subject",
        )
    }

    default_order = {
        "orderby": "creationdate",
        "orderdir": "desc",
    }

    addTemplate = "todo_add"
    addSuccessTemplate = "todo_add_success"

    def canAdd(self):
        return True  # everyone can add entries!


Todo.html = True
Todo.json = True
