from sys import stdout

from .commands import Command
from .options import Option


class JobWriter:
    options: list[Option] = []
    commands: list[Command] = []

    def __init__(self, opts: list[Option] = [], cmds: list[Command] = []):
        self.options = opts
        self.commands = cmds

    def add_option(self, option: Option):
        self.options.append(option)
        return self

    def add_command(self, command: Command):
        self.commands.append(command)
        return self

    def to_string(self):
        lines = ["#!/bin/sh", "# LSF Job options"]
        lines += list(map(lambda o: o.get_option_line(), self.options))
        lines.append("# Commands")
        lines += list(map(lambda c: c.get_command(), self.commands))

        return "\n".join(lines)

    def to_stdout(self):
        stdout.write(self.to_string())
        return self
