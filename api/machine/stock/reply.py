from common.line.utilities import reply_message
from yfinance import Ticker
from common.line.classes import Event, QuickReplyMessage, dataframe_to_flex_message
from common.line.utilities import reply_message
from connections import STATE_CACHE
from utils.util import stock_list
from loguru import logger

from ..classes import State

from ..classes import State


class Reply(State):
    name = "reply"

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
                        "Which stock you wanna check?",
                        [(i, i) for i in stock_list],
                    )
                ],
            )
            return "OK"

        if message in stock_list:
            # Get stock info
            ticker = Ticker(message)

            info = ticker.info

            # Get historical market data
            hist = ticker.history()

            # Rename the index from timestamp to date
            hist.index = hist.index.strftime("%m/%d")

            # hist.index become a new column
            hist.reset_index(inplace=True)

            # # Round each row from float to 2 decimal places
            hist = hist.round(2)

            hist = hist[["Date", "Close", "Volume"]]

            hist["Volume"] = (hist["Volume"] / 1000000).round(2)

            # # Get each day price change in percentage
            hist["Change"] = (hist["Close"].pct_change() * 100).round(2)

            # make 'Volume' and 'Change' to be round to 2 decimal places format, eg. 1.6 -> 1.60
            hist["Close"] = hist["Close"].apply(lambda x: f"{x:.2f}")
            hist["Volume"] = hist["Volume"].apply(lambda x: f"{x:.2f}")
            hist["Change"] = hist["Change"].apply(
                lambda x: f"+{x:.2f}" if x != "nan" and x >= 0 else f"{x:.2f}"
            )

            hist.columns = ["Date", "Close", "Vol(M)", "Chg(%)"]

            STATE_CACHE.delete(self.line_id)
            # reply_message(self.reply_token, [TextMessage(f"{hist.tail(14)}")])
            reply_message(self.reply_token, [dataframe_to_flex_message(df=hist)])

            return "OK"
        else:
            reply_message(
                self.reply_token,
                [
                    QuickReplyMessage(
                        "Incorrect option, please try again.",
                        [(i, i) for i in stock_list],
                    )
                ],
            )
            return "Incorrect option, please try again."
