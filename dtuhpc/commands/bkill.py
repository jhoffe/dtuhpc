from typing import Optional

from .command import Command


class BKill(Command):
    base_command = "bkill"

    def run(  # noqa: C901
        self,
        *job_ids: list[str],
        kill_all: bool = False,
        as_done: bool = False,
        list_signals: bool = False,
        remove_without_waiting: False = True,
        application_profile_name: Optional[str] = None,
        kill_reason: Optional[str] = None,
        group_name: Optional[str] = None,
        job_name: Optional[str] = None,
        host_name: Optional[str] = None,
        queue: Optional[str] = None,
        signal_name: Optional[str] = None,
        status: Optional[str] = None,
        kill_all_satisfying: bool = False,
    ):
        args = []

        if kill_all:
            args.append("-b")
        if as_done:
            args.append("-d")
        if list_signals:
            args.append("-l")
        if remove_without_waiting:
            args.append("-r")
        if application_profile_name is not None:
            args.append(f"-app {application_profile_name}")
        if kill_reason is not None:
            args.append(f"-C {kill_reason}")
        if group_name is not None:
            args.append(f"-g {group_name}")
        if job_name is not None:
            args.append(f"-J {job_name}")
        if host_name is not None:
            args.append(f"-m {host_name}")
        if queue is not None:
            args.append(f"-q {queue}")
        if signal_name is not None:
            args.append(f"-s {signal_name}")
        if status is not None:
            args.append(f"-stat {status}")
        if kill_all_satisfying:
            args.append("0")

        args += job_ids

        return super().run(*args)
