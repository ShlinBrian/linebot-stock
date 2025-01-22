from typing import Dict

from .classes import Machine
from .stock import StockMachine
from .asset_allocation import AssetAllocationMachine
from .inspiration_quote import InspirationQuoteMachine
from .default import DefaultMachine
from .quickreply import QuickReplyMachine

MACHINES: Dict[str, Machine] = {
    DefaultMachine.name: DefaultMachine(),
    QuickReplyMachine.name: QuickReplyMachine(),
    StockMachine.name: StockMachine(),
    AssetAllocationMachine.name: AssetAllocationMachine(),
    InspirationQuoteMachine.name: InspirationQuoteMachine(),
}
