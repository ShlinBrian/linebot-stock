from common.line.classes import Event, TextMessage
from common.line.utilities import reply_message

from ..classes import State


class Reply(State):
    name = "reply"

    def execute(self, message="", **kwargs):
        reply_message(self.reply_token, [TextMessage("Invalid option")])
        return "Invalid option"
