from viur.core.render.html.utils import jinjaGlobalFunction
from viur.core.render import admin, html, json, vi


def gen_postProcessAppObj(renderer):
    renderer._viur_postProcessAppObj = renderer._postProcessAppObj  # backup

    def _postProcessAppObj(obj):
        obj = renderer._viur_postProcessAppObj(obj)
        obj["getStructure"] = vi.getStructure
        return obj

    return _postProcessAppObj


json._postProcessAppObj = gen_postProcessAppObj(json)


@jinjaGlobalFunction
def inject_vite(render, development: bool | None = None, development_server: str = "http://localhost:8081"):
    """build vue imports from manifest"""

    if development is None:
        import logging
        import requests

        try:
            resp = requests.get(development_server, timeout=2)
            development = resp.status_code == 200
        except Exception:
            logging.warning(f"{development_server} isn't active, using prebuilt fallback")
            development = False

    if development:
        return f"""
            <script type="module" src="{development_server}/@vite/client"></script>
            <script type="module" src="{development_server}/main.js"></script>
        """

    import json
    vite_path = "static/site"

    try:
        fd = open(f"{vite_path}/.vite/manifest.json", "r")
        manifest = json.load(fd)
    except Exception as e:
        raise Exception(
            f"Vite manifest file not found or invalid {e=}. Maybe your /{vite_path}/.vite/manifest.json file is empty?"
        )

    return f"""
        <script type="module" src="/{vite_path}/{manifest["index.html"]["file"]}"></script>
        <link rel="stylesheet" type="text/css" href="/{vite_path}/{manifest["index.html"]["css"][0]}" />
    """ + "".join(
        f"""<script type="module" src="/{vite_path}/{manifest[file]["file"]}"></script>"""
        for file in (manifest["index.html"].get("imports") or ())
    )
