from fabric.runners import Result

from ..outputs.bkill_output import BKillOutput
from .command import Command


class BKill(Command):
    base_command = "bkill"
    default_args = []

    def _parse_output(self, result: Result) -> BKillOutput:
        return BKillOutput.parse(result)
