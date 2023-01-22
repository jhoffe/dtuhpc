from fabric.runners import Result

from ..outputs.showstart_output import ShowstartOutput
from .command import Command


class Showstart(Command):
    base_command = "showstart"
    default_args = []

    def _parse_output(self, result: Result) -> ShowstartOutput:
        return ShowstartOutput.parse(result)
