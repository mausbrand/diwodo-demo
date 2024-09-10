from viur.core.render import admin, html, json, vi


def gen_postProcessAppObj(renderer):
    renderer._viur_postProcessAppObj = renderer._postProcessAppObj  # backup

    def _postProcessAppObj(obj):
        obj = renderer._viur_postProcessAppObj(obj)
        obj["getStructure"] = vi.getStructure
        return obj

    return _postProcessAppObj


json._postProcessAppObj = gen_postProcessAppObj(json)
