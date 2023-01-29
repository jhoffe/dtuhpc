from typing import Optional

from .command import Command


class Showstart(Command):
    base_command = "showstart"

    def run(
        self,
        *job_ids: list[str],
        user: Optional[str] = None,
        queue: Optional[str] = None,
    ):
        args = []

        if user is not None:
            args.append(f"-u {user}")
        if queue is not None:
            args.append(f"-q {queue}")

        args += job_ids

        return super().run(*args)
