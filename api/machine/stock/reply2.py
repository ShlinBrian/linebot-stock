from common.line.classes import Event, TextMessage
from common.line.utilities import reply_message
from yfinance import Ticker

from ..classes import State


class Reply(State):
    name = "reply"

    def execute(self, message="", **kwargs):
        # Create a ticker object for Google
        ticker = Ticker("GOOG")

        # Get stock info
        info = ticker.info

        # Print the info
        print(info["open"])
        # Get historical market data
        hist = ticker.history(period="5d")

        # Print the open prices
        print(hist["Open"])

        reply_message(self.reply_token, [TextMessage("Invalid option")])
        return "Invalid option"
