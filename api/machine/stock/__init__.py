from ..classes import Machine
from .reply import Reply


class StockMachine(Machine):
    name = "stock"
    states = {Reply.name: Reply}
