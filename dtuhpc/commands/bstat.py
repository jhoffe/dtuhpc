from typing import Optional

from .command import Command


class BStat(Command):
    base_command = "bstat"

    def run(
        self,
        *job_ids: list[str],
        cpu_usage: bool = False,
        memory_usage: bool = False,
        user: Optional[str] = None,
        queue: Optional[str] = None,
    ):
        args = []

        if cpu_usage:
            args.append("-C")
        if memory_usage:
            args.append("-M")
        if user is not None:
            args.append(f"-u {user}")
        if queue is not None:
            args.append(f"-q {queue}")

        args += job_ids

        return super().run(*args)
