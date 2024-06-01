from common.line.classes import TextMessage, FlexMessage
from common.line.utilities import reply_message
from connections import STATE_CACHE, REPLY_CACHE
from config import Config
from openai import OpenAI
from loguru import logger


from ..classes import State


class Reply(State):
    name = "reply"

    def execute(self, message="", **kwargs):
        client = OpenAI(api_key=Config.API_KEY)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message},
            ],
        )

        print(response)
        print(response["choices"][0]["message"]["content"])

        reply_message(self.reply_token, [TextMessage(response)])

        return "OK"
