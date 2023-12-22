import json
import random

from pypulse.View import view
from pypulse.Template import RenderTemplate, Redirect
from pypulse.Controller import authenticated
from baseapp.models.chatgpt import ChatGpt
from baseapp.random_cletus_images import CLETUS


@view(name="index", path_trigger="/")
def index(request):
    if not authenticated():
        return Redirect("/login")

    with open("meta.json", "r") as meta:
        meta = json.loads(meta.read())

    user_conversation = meta.get("user_conversation")
    ia_conversation = meta.get("ia_conversation")

    generate_full_conversation = {}

    if not user_conversation:
        user_conversation = []
    if not ia_conversation:
        ia_conversation = []

    for i in range(len(user_conversation)):
        if i > len(ia_conversation) - 1:
            ia = None
        else:
            ia = ia_conversation[i]
        generate_full_conversation[i] = [user_conversation[i], ia]

    params = {"ia": {}, "user": {}, "config": {}}

    params["config"]["model"] = "gpt-3.5-turbo"

    params["ia"]["role"] = "system"
    params["ia"][
        "content"
    ] = "You are Cletus, a good ol' boy from the illustrious town of Springfield in the Simpsons universe, sarcastic, funny and very stupid"

    if request.get("method") == "POST":
        body = request.get("body")
        if not body:
            return RenderTemplate(
                "index.html",
                {"error": False, "full_conversation": generate_full_conversation},
            )
        params["user"]["role"] = "user"
        params["user"]["content"] = body.get("user_input")

        query = {
            "model": params["config"]["model"],
            "messages": [params["ia"], params["user"]],
        }

        action = ChatGpt.body(query)
        action = action.view.all()

        if type(action) is int:
            if action == 429:
                return RenderTemplate(
                    "index.html",
                    {
                        "error": "You exceeded your current quota, please check your plan and billing details."
                    },
                )

        if len(action) == 1:
            action = action[0]

        action = action.get("choices")

        if action:
            if len(action) > 0:
                action = action[0]

        if action:
            action = action.get("message")

        if action:
            action = action.get("content")

        index = len(generate_full_conversation)
        generate_full_conversation[index] = [body.get("user_input"), action]

        user_conversation.append(body.get("user_input"))
        ia_conversation.append(action)

        with open("meta.json", "w") as meta_to_write:
            meta["user_conversation"] = user_conversation
            meta["ia_conversation"] = ia_conversation
            meta_to_write.write(json.dumps(meta))

    random_images = {}

    n = 0
    for i in generate_full_conversation:
        if n > len(CLETUS) - 1:
            n = 0 
        random_images[i] = CLETUS[n]
        n+=1

    return RenderTemplate(
        "index.html",
        {
            "error": False,
            "full_conversation": generate_full_conversation,
            "random_images": random_images,
        },
    )
