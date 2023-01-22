from fabric.runners import Result

from dtuhpc.outputs.bstat_output import BStatOutput

from .command import Command


class BStat(Command):
    base_command = "bstat"
    default_args = []

    def _parse_output(self, result: Result) -> BStatOutput:
        return BStatOutput.parse(result)
