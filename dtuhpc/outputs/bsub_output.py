import re
from dataclasses import dataclass
from typing import Optional

from fabric.runners import Result

from ..console import console
from .output import Output


@dataclass
class BSubOutput(Output):
    cmd_result: Result
    job_id: Optional[int]
    queue: Optional[str]

    @staticmethod
    def parse(result: Result) -> "BSubOutput":
        if result.failed:
            return BSubOutput(cmd_result=result, job_id=None)

        matches = re.match(
            "[a-zA-Z| ]+<(?P<job_id>[0-9]+)>[a-zA-Z| ]+<(?P<queue>[a-zA-Z]+)>",
            result.stdout,
        )

        job_id = int(matches.group("job_id")) if matches else None
        queue = matches.group("queue") if matches else None

        return BSubOutput(cmd_result=result, job_id=job_id, queue=queue)

    def print(self) -> None:
        console.print(f"Job ID: {self.job_id} on queue {self.queue}")
