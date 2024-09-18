from viur.core.render import admin, html, json, vi


def gen_postProcessAppObj(renderer):
    renderer._viur_postProcessAppObj = renderer._postProcessAppObj  # backup

    def _postProcessAppObj(obj):
        obj = renderer._viur_postProcessAppObj(obj)
        obj["getStructure"] = vi.getStructure
        return obj

    return _postProcessAppObj


json._postProcessAppObj = gen_postProcessAppObj(json)


import typing as t
import json as _json
import logging
from viur.core.render.html.utils import jinjaGlobalFunction
@jinjaGlobalFunction
def inject_vite(render, development: bool = False) -> t.Any:
    """build vue imports from manifest"""

    if development:
        return """<script type="module" src="http://localhost:8081/@vite/client"></script>
                  <script type="module" src="http://localhost:8081/main.js"></script>"""

    vite_path = "/static/site"

    try:
        fd = open(f"static/site/.vite/manifest.json", "r")
        manifest = _json.load(fd)
    except:
        raise Exception(
            f"Vite manifest file not found or invalid. Maybe your {vite_path}/.vite/manifest.json file is empty?"
        )
    imports_files = ""
    if "imports" in manifest["index.html"]:
        imports_files = "".join(
            [
                f'<script type="module" src="{vite_path}/{manifest[file]["file"]}"></script>'
                for file in manifest["index.html"]["imports"]
            ]
        )

    return f"""<script type="module" src="{vite_path}/{manifest['index.html']['file']}"></script>
        <link rel="stylesheet" type="text/css" href="{vite_path}/{manifest['index.html']['css'][0]}" />
        {imports_files}"""
