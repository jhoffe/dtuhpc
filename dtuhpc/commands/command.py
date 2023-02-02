from typing import Union

from fabric.runners import Result

from dtuhpc.connector import HPCConnection


class Command:
    """Base class for all commands."""

    base_command: str
    connection: HPCConnection

    def __init__(self, connection: HPCConnection):
        self.connection = connection

    def run(self, *args: Union[str, int, float]) -> Result:
        parsed_args = " ".join([str(arg) for arg in args])

        command = self.base_command + " " + parsed_args
        cmd = self.connection.run(command)
        return cmd
