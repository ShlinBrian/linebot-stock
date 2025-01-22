from common.line.classes import Event, TextMessage, dataframe_to_flex_message
from common.line.utilities import reply_message
from common.line.utilities import reply_message
from connections import STATE_CACHE
from utils.util import stock_list
from loguru import logger
import requests
import pandas as pd
from ..classes import State
import yfinance as yf
from ..classes import State


class Reply(State):
    name = "reply"

    def execute(self, message="", **kwargs):
        if self.from_different_state():
            STATE_CACHE.set(
                self.line_id, {"machine": self.machine.name, "state": self.name}
            )
            reply_message(
                self.reply_token,
                [TextMessage("Please enter your asset in Taiwan Dollar (TWD).")],
            )
            return "OK"

        if message.isdigit():
            asset = int(message)
            df = allocate_money(asset, "TWD", "USD")
            reply_message(
                self.reply_token,
                [TextMessage(df.to_string(index=False, justify="center"))],
            )
            # reply_message(self.reply_token, [dataframe_to_flex_message(df=df)])
            STATE_CACHE.delete(self.line_id)
            return "OK"
        else:
            reply_message(self.reply_token, [TextMessage("Please enter a number.")])
            return "Incorrect imput. Please enter a number."


def format_number(num):
    """
    Format a number into K, M, or B format.
    Args:
        num (float): The number to format.
    Returns:
        str: The formatted number.
    """
    if abs(num) >= 1_000_000_000:
        return f"{num / 1_000_000_000:.1f}B"
    elif abs(num) >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif abs(num) >= 1_000:
        return f"{num / 1_000:.1f}K"
    else:
        return f"{num:.2f}"


def get_exchange_rate(base_currency: str, target_currency: str) -> float:
    """
    Fetches the real-time exchange rate between two currencies using a free API.

    Args:
        base_currency (str): The base currency (e.g., "TWD").
        target_currency (str): The target currency (e.g., "USD").

    Returns:
        float: The exchange rate from base_currency to target_currency.
    """
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
        response = requests.get(url)
        response.raise_for_status()
        rates = response.json().get("rates", {})
        return rates.get(target_currency, 1.0)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rate: {e}")
        return 1.0


def get_real_time_closing_prices(compositions: dict) -> dict:
    """
    Fetches real-time closing prices for assets using Yahoo Finance.

    Args:
        compositions (dict): The compositions dictionary containing asset tickers.

    Returns:
        dict: A dictionary of assets and their closing prices.
    """
    try:
        # Extract unique tickers from compositions
        tickers = set()
        for subcategories in compositions.values():
            tickers.update(subcategories.keys())

        # Map cryptocurrency tickers to Yahoo Finance format
        tickers = [ticker for ticker in tickers]

        data = yf.download(tickers, period="1d", interval="1d", progress=False)
        closing_prices = data["Adj Close"].iloc[-1].to_dict()

        return closing_prices
    except Exception as e:
        print(f"Error fetching closing prices: {e}")
        return {}


def allocate_money(
    amount: float, source_currency: str = "TWD", target_currency: str = "USD"
) -> pd.DataFrame:
    """
    Allocate money into categories and subcategories with real-time currency conversion.

    Args:
        amount (float): The amount of money to allocate (in the source currency).
        source_currency (str): The currency of the input money (default is "USD").
        target_currency (str): The currency to allocate money in (default is "USD").

    Returns:
        pd.DataFrame: A dataframe summarizing the allocation.
    """
    # Fetch the exchange rate
    exchange_rate = get_exchange_rate(source_currency, target_currency)
    amount_in_target = amount * exchange_rate
    print(
        f"\nAmount: ${amount:,} ({source_currency}) \nAmount: ${amount_in_target:,} ({target_currency}) \nExchange Rate: {exchange_rate}"
    )

    # Allocation percentages
    categories = {"ETF": 0.55, "STOCK": 0.10, "DEBT": 0.30, "CRYPTO": 0.05}

    # Subcategory compositions
    compositions = {
        "ETF": {"QQQ": 0.80, "SPY": 0.20},
        "STOCK": {"TSM": 0.20, "NVDA": 0.20, "TSLA": 0.60},
        "DEBT": {"TLT": 1.0},
        "CRYPTO": {"BTC-USD": 0.8, "DOGE-USD": 0.2},
    }

    # Fetch real-time closing prices
    closing_prices = get_real_time_closing_prices(compositions)

    # Data for the dataframe
    data = []

    for category, category_percentage in categories.items():
        allocated_amount = amount_in_target * category_percentage

        # Add subcategory rows
        for subcategory, sub_percentage in compositions[category].items():
            sub_amount = allocated_amount * sub_percentage
            sub_amount_in_source = sub_amount / exchange_rate

            # Get closing price and calculate units
            closing_price = closing_prices.get(subcategory, 1.0)
            units = sub_amount_in_source / closing_price

            data.append(
                {
                    # "Category": category.capitalize(),
                    "Subject": subcategory,
                    "Percentage (%)": round(
                        category_percentage * sub_percentage * 100, 2
                    ),
                    f"Amount ({source_currency})": f"{round(sub_amount_in_source, 2):,}",
                    f"Amount ({target_currency})": f"{round(sub_amount, 2):,}",
                    "Closing Price": round(closing_price, 2),
                    "Units": round(units, 4),
                }
            )

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Apply number formatting
    df[f"Amount ({source_currency})"] = df[f"Amount ({source_currency})"].apply(
        lambda x: format_number(float(x.replace(",", "")))
    )
    df[f"Amount ({target_currency})"] = df[f"Amount ({target_currency})"].apply(
        lambda x: format_number(float(x.replace(",", "")))
    )
    df["Closing Price"] = df["Closing Price"].apply(lambda x: format_number(x))
    df["Units"] = df["Units"].apply(lambda x: format_number(x))

    return df
