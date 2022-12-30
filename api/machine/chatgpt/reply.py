from common.line.classes import Event, TextMessage, Flex
from common.line.utilities import reply_message
from utils.pyChatGPT import ChatGPT
from connections import STATE_CACHE, REPLY_CACHE

from ..classes import State


class Reply(State):
    name = "reply"

    def execute(self, message="", **kwargs):
        reply_message(self.reply_token, [TextMessage("Invalid option")])
        if self.from_different_state() or message == "成員資料":
            STATE_CACHE.set(
                self.line_id, {"machine": self.machine.name, "state": self.name}
            )

            if not line or not members:
                reply_message(
                    self.reply_token,
                    [FlexMessage(jsonformat=MemberInfoJson(), altText="您尚未註冊")],
                )
            else:
                for member in members:
                    update_member_from_form(db, member)
                reply_message(
                    self.reply_token,
                    [FlexMessage(jsonformat=ManageMemberJson(members), altText="成員資料")],
                )

            return "OK"

        # Go to New state
        if message == "前往註冊" or message == "新增成員":
            self.machine.execute(db, message, "new_hcard", **kwargs)
            return "OK"

        reply: dict = {"target": target}
        REPLY_CACHE.set(self.line_id, reply)

        self.machine.execute(db, message, KeywordState[keyword], **kwargs)

        reply_message(
            self.reply_token, [TextMessage("請點選卡片按鈕，若要使用其他服務，可以點選圖文選單跳出流程，謝謝～")]
        )

        return "OK"
