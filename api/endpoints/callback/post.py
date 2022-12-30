from typing import List

from common.enums import EnumResponse
from common.line.classes import Event
from connections import REPLY_CACHE, STATE_CACHE
from loguru import logger
from machine import MACHINES
from machine.classes import Machine

# pylint: disable=E0611
from pydantic import BaseModel

# pylint: enable=E0611


DOC = {
    200: EnumResponse.OK.value.doc,
    500: EnumResponse.INTERNAL_SERVER_ERROR.value.doc,
}


class Payload(BaseModel):
    destination: str
    events: List[Event]


def post(payload: Payload):
    for event in payload.events:
        logger.debug(f"{event=}")
        machine: Machine = None
        state: str = ""

        line_id = event.source["userId"]
        reply_token = event.replyToken
        message = ""

        if STATE_CACHE.get(line_id):
            machine = MACHINES[STATE_CACHE.get(line_id)["machine"]]
            state = STATE_CACHE.get(line_id)["state"]

        # Unhandled requests goes to default reply
        else:
            machine = MACHINES["default"]
            state = "reply"

        if event.type == "message" and event.message["type"] == "text":
            message = event.message["text"]
                
            # No session, use pre-defined flow
            if message == "quickreply":
                machine = MACHINES["quickreply"]
                state = "question"

            elif message == "Notification":
                machine = MACHINES["notification"]
                state = "reply"

            elif message == "ChatGPT":
                machine = MACHINES["chatGPT"]
                state = "reply"

            elif message == "Stock":
                machine = MACHINES["Stock"]
                state = "reply"

            elif message == "Weather":
                machine = MACHINES["weather"]
                state = "reply"

        machine.setup(line_id, reply_token)
        logger.debug(f"Line: {line_id}, Machine: {machine.name}, State: {state}")
        machine.execute(message, state, kwargs=event)

    return EnumResponse.OK.value.response
