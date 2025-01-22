from ..classes import Machine
from .reply import Reply


class AssetAllocationMachine(Machine):
    name = "asset_allocation"
    states = {Reply.name: Reply}
