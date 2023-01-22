from fabric.runners import Result

from dtuhpc.outputs.bsub_output import BSubOutput

from .command import Command


class BSub(Command):
    base_command = "bsub"
    default_args = []

    def _parse_output(self, result: Result) -> BSubOutput:
        return BSubOutput.parse(result)
