from fabric.runners import Result

from dtuhpc.outputs.bqueues_output import BQueuesOutput
from dtuhpc.outputs.table import Table

from .command import Command


class BQueues(Command):
    base_command = "bqueues"
    default_args = []

    def _parse_output(self, result: Result) -> (Table, str):
        return BQueuesOutput.parse(result)
