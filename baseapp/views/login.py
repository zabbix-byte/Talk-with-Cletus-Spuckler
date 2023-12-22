import json

from pypulse.View import view
from pypulse.Template import RenderTemplate, Redirect
from pypulse.Controller import set_manual_bearer, authenticated


@view(name="login", path_trigger="/login")
def login(request):
    with open("meta.json", "r") as meta:
        meta = json.loads(meta.read())

    token = meta.get("token")

    if token:
        set_manual_bearer(token)
        if authenticated():
            return Redirect("/")

    if request.get("method") == "POST":
        body = request.get("body")
        if body:
            token = body.get("apiKey")
        if token:
            set_manual_bearer(token)

    if token and not authenticated():
        return RenderTemplate(
            "login.html",
            {"error": "Invalid API Key. Please try again."},
        )

    if token:
        with open("meta.json", "w") as meta_to_write:
            meta["token"] = token
            meta_to_write.write(json.dumps(meta))

        return Redirect("/")

    return RenderTemplate("login.html", {"error": False})
