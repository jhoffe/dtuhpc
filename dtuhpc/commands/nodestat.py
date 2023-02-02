from .command import Command


class Nodestat(Command):
    base_command = "nodestat"

    def run(  # noqa: C901
        self,
        *queues: list[str],
        cpu: bool = False,
        features: bool = False,
        gpu: bool = False,
        gpu_model: bool = False,
        jobs: bool = False,
        queue_jobs: bool = False,
        load_utilization: bool = False,
        visual_load_utilization: bool = False,
        memory: bool = False,
        reserved_slots: bool = False,
    ):
        args = []

        if cpu:
            args.append("-f")
        if features:
            args.append("-F")
        if gpu:
            args.append("-g")
        if gpu_model:
            args.append("-G")
        if jobs:
            args.append("-j")
        if queue_jobs:
            args.append("-J")
        if load_utilization:
            args.append("-l")
        if visual_load_utilization:
            args.append("-L")
        if memory:
            args.append("-m")
        if reserved_slots:
            args.append("-r")

        args += queues

        return super().run(*args)
