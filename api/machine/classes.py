from __future__ import annotations

from typing import Any, Dict, Type
from connections import STATE_CACHE
from loguru import logger


# pylint:disable=R0201
class State:
    """
    State base class

    Attributes:
        name (str): State name, use to match which state in cache
        machine (Machine): State machine instance
            used to reference back to the machine itself
    """

    name: str = ""
    machine: Machine
    reply_token: str = ""
    line_id: str = ""

    def __init__(self, machine, line_id="", reply_token="", message=""):
        self.machine = machine
        self.line_id = line_id
        self.reply_token = reply_token
        self.message = message

    def from_different_state(self) -> bool:
        """Check if the state if from different state

        Args:
            line_id (str): User Line ID

        Returns:
            bool: Result
        """
        if (
            STATE_CACHE.get(self.line_id) is None
            or STATE_CACHE.get(self.line_id)["machine"] != self.machine.name
            or STATE_CACHE.get(self.line_id)["state"] != self.name
        ):
            return True
        return False

    def execute(self, message="", **kwargs) -> Any:
        """
        Function execute, write your business logic here in subclasses

        Args:
            user_id (str): User ID. Default to ""
            payload (Any, optional): Message payload. Defaults to None.

        Raises:
            Exception: Raised when called directly

        Returns:
            Any: Any data depends on subclass implenation
                Can return status code for further debugging and API responses
        """
        raise Exception("This function should be implemented in subclass!")


class Machine:
    """
    State machine base class

    Attributes:
        name (str): Machine name, use to match which machine in cache
        states (Dict[str, State]): Dictionary pair of state classes
            Use state name as key and State subclass as value
            State subclasses will be initialized to instance in __init__ function
    """

    name: str = ""
    states: Dict[str, Type[State]]
    line_id: str = ""
    reply_token: str = ""

    def setup(self, line_id, reply_token=""):
        self.line_id = line_id
        self.reply_token = reply_token

    def execute(self, message="", state="", **kwargs) -> Any:
        """
        Execute state function directly

        Args:
            state (str, optional): State name. Defaults to "".
            user_id
            payload (str, optional): Line payload. Defaults to "".

        Returns:
            Any: Any data depends on state implenation
                Can return status code for further debugging and API responses
        """
        # Init state object in runtime
        state: State = self.states[state](self, self.line_id, self.reply_token, message)

        return state.execute(message=message, **kwargs)
