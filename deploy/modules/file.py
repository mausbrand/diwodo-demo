from viur.core import i18n, current
from viur.core.modules.file import File


class File(File):
    roles = {
        "indoor": "*",
        "admin": "*",
    }

    adminInfo = File.adminInfo | {
        "name": "Dateien"
    }

    def getAvailableRootNodes(self, *args, **kwargs):
        # Any user who is logged in can see the root-node.
        if current.user.get():
            repository = self.ensureOwnModuleRootNode()

            return [{
                "name": i18n.translate("Files"),
                "key": repository.key
            }]

        return []

    def canAdd(self, skel_type, node):
        if skel_type == "leaf" and not node:
            return True

        return super().canAdd(skel_type)


File.html = True
File.json = True
