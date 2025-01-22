from ..classes import Machine
from .reply import Reply


class InspirationQuoteMachine(Machine):
    name = "inspiration_quote"
    states = {Reply.name: Reply}
