from typing import Dict

from .classes import Machine
from .default import DefaultMachine
from .quickreply import QuickReplyMachine
from .chatgpt import ChatgptMachine
from .stock import StockMachine

MACHINES: Dict[str, Machine] = {
    DefaultMachine.name: DefaultMachine(),
    QuickReplyMachine.name: QuickReplyMachine(),
    ChatgptMachine.name: ChatgptMachine(),
    StockMachine.name: StockMachine(),
}
