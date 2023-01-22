from fabric.runners import Result

from dtuhpc.outputs.nodestat_output import NodestatOutput

from .command import Command


class Nodestat(Command):
    base_command = "nodestat"
    default_args = []

    def _parse_output(self, result: Result) -> NodestatOutput:
        return NodestatOutput.parse(result)
