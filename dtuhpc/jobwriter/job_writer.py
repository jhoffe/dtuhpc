"""This module contains the JobWriter class, which is used to write LSF job scripts."""
from sys import stdout
from typing import Union

from .commands import Command
from .options import Option


class JobWriter:
    """This class is used to write LSF job scripts.

    Attributes:
        options (list[Option]): List of options to add to the job script.
        commands (list[Command]): List of commands to add to the job script.
    """

    options: list[Option] = []
    commands: list[Command] = []

    def __init__(self, opts: list[Option] = [], cmds: list[Command] = []):
        """Initialize the JobWriter with the given options and commands.

        Args:
            opts (list[Option], optional): List of options to add to the job script.
            Defaults to [].
            cmds (list[Command], optional): List of commands to add to the job script.
            Defaults to [].
        """
        self.options = opts
        self.commands = cmds

    def add(self, opt_or_cmd: Union[Option, Command]):
        if isinstance(opt_or_cmd, Option):
            self.add_option(opt_or_cmd)
        if isinstance(opt_or_cmd, Command):
            self.add_command(opt_or_cmd)

        return self

    def add_option(self, option: Option) -> "JobWriter":
        """Add an option to the job script.

        Args:
            option (Option): Option to add to the job script.

        Returns:
            JobWriter: The JobWriter object.
        """
        self.options.append(option)
        return self

    def add_command(self, command: Command) -> "JobWriter":
        """Add a command to the job script.

        Args:
            command (Command): Command to add to the job script.

        Returns:
            JobWriter: The JobWriter object.
        """
        self.commands.append(command)
        return self

    def to_string(self) -> str:
        """Convert the job script to a string.

        Returns:
            str: The job script as a string.
        """

        lines = ["#!/bin/sh", "# LSF Job options"]
        lines += list(map(lambda o: o.get_option_line(), self.options))
        lines.append("# Commands")
        lines += list(map(lambda c: c.get_command(), self.commands))

        return "\n".join(lines)

    def to_stdout(self):
        """Write the job script to stdout.

        Returns:
            JobWriter: The JobWriter object.
        """
        stdout.write(self.to_string())
        return self
