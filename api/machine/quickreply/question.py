from common.line.classes import Event, QuickReplyMessage, TextMessage
from common.line.utilities import reply_message
from connections import STATE_CACHE

from ..classes import State


class Question(State):
    name = "question"

    def execute(self, message="", **kwargs):

        # Check the user is in state or not
        if self.from_different_state():
            # First time enter, the user will now keep in this state until further reply
            # Setup the session
            STATE_CACHE.set(
                self.line_id, {"machine": self.machine.name, "state": self.name}
            )
            reply_message(
                self.reply_token,
                [
                    QuickReplyMessage(
                        "What is the result of 1+1 ?", [("2", "2"), ("1", "1")]
                    )
                ],
            )
            return "OK"

        try:
            answer = int(message)
            if answer == 2:
                reply_message(self.reply_token, [TextMessage("Correct answer")])
                STATE_CACHE.delete(self.line_id)
                return "Correct answer"
            else:
                reply_message(self.reply_token, [TextMessage("Incorrect answer")])
                return "Incorrect answer"
        except ValueError:
            reply_message(
                self.reply_token, [TextMessage("Invalid option(must be a number)")]
            )
            return "Invalid option"
