from common.line.classes import TextMessage
from common.line.utilities import reply_message
from config import Config
from loguru import logger
import openai


from ..classes import State

openai.api_key = Config.API_KEY


class Reply(State):
    name = "reply"

    def execute(self, message="", **kwargs):
        response = self.analyze_message(message)

        reply_message(self.reply_token, [TextMessage(response)])

        return "OK"

    def analyze_message(self, message: str):
        messages = [
            {
                "role": "system",
                "content": "You are a general customer service assistant.",
            },
            {
                "role": "user",
                "content": (
                    f"Message: {message}\n"
                    "Provide an concise anwser strait to the point.\n"
                    "Please ensure that the response strictly adheres to a text format."
                ),
            },
        ]

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=300,
            temperature=0.7,
        )
        result = response.choices[0].message.content
        logger.debug(f"result: {result}")
        return result
