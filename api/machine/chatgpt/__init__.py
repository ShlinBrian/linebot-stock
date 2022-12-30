from ..classes import Machine
from .reply import Reply


class ChatgptMachine(Machine):
    name = "chatgpt"
    states = {Reply.name: Reply}
