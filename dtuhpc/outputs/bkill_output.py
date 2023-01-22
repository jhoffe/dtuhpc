import re
from dataclasses import dataclass
from typing import Optional

from fabric.runners import Result

from ..console import console
from .output import Output


@dataclass
class BKillOutput(Output):
    cmd_result: Result
    job_id: Optional[int]

    @staticmethod
    def parse(result: Result) -> "BKillOutput":
        if result.failed:
            return BKillOutput(cmd_result=result, job_id=None)

        matches = re.match("[a-zA-Z| ]+<(?P<job_id>[0-9]+)>[a-zA-Z| ]+", result.stdout)

        job_id = int(matches.group("job_id")) if matches else None

        return BKillOutput(cmd_result=result, job_id=job_id)

    def print(self) -> None:
        console.print(f"Killed job: {self.job_id}")
