from abc import ABC, abstractmethod
from typing import Optional, Union

from fabric.runners import Result

from dtuhpc.connector import HPCConnection
from dtuhpc.outputs.output import Output


class Command(ABC):
    """Base class for all commands."""

    base_command: str
    default_args: list[str]
    connection: HPCConnection

    def __init__(
        self, connection: HPCConnection, *default_args: Union[str, int, float]
    ):
        self.connection = connection
        self.default_args = list(default_args)

    def run(self, *args: Union[str, int, float]) -> Optional[Output]:
        parsed_default_args = " ".join([str(arg) for arg in self.default_args])
        parsed_args = " ".join([str(arg) for arg in args])

        command = self.base_command + " " + parsed_default_args + " " + parsed_args
        cmd = self.connection.run(command, hide=True)
        return self._parse_output(cmd)

    @abstractmethod
    def _parse_output(self, result: Result) -> Optional[Output]:
        raise NotImplementedError("Command._parse_output() not implemented")
