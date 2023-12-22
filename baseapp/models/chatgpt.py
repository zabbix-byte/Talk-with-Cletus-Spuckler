from pypulse.Model import Model, List


class ChatGpt(Model):
    choices = List()

    class Meta:
        target = "chat/completions"
        method = "post"
        body = None
