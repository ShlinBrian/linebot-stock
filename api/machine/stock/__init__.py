from ..classes import Machine
from .reply import Reply


class StockMachine(Machine):
    name = "stock_price"
    states = {Reply.name: Reply}
