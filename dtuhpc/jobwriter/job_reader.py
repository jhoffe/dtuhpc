from pathlib import Path

import tomli

from dtuhpc.jobwriter.commands import Command, LoadModuleCommand
from dtuhpc.jobwriter.job_writer import JobWriter
from dtuhpc.jobwriter.options import (
    CoreBlockSizeOption,
    CorePTileSizeOption,
    EmailForNotificationsOption,
    ErrorOutputFilePathOption,
    MemoryPerCoreKillLimitOption,
    MemoryPerCoreOption,
    NameOption,
    NCPUCoresOption,
    Option,
    QueueOption,
    SendNotificationAtEndOption,
    SendNotificationAtStartOption,
    SingleHostOption,
    StandardOutputFilePathOption,
    UseGPUOption,
    WallTimeOption,
)

MAPPING = {
    "core_block_size": CoreBlockSizeOption,
    "core_p_tile_size": CorePTileSizeOption,
    "email": EmailForNotificationsOption,
    "error_output": ErrorOutputFilePathOption,
    "memory_kill_limit": MemoryPerCoreKillLimitOption,
    "memory": MemoryPerCoreOption,
    "cpu": NCPUCoresOption,
    "name": NameOption,
    "queue": QueueOption,
    "single_host": SingleHostOption,
    "standard_output_file_path": StandardOutputFilePathOption,
    "notification_start": SendNotificationAtStartOption,
    "notification_end": SendNotificationAtEndOption,
    "walltime": WallTimeOption,
    "use_gpu": UseGPUOption,
    "option": Option,
    "module": LoadModuleCommand,
    "commands": Command,
}


class JobReader:
    job_file_path: Path
    config: dict
    job_writer: JobWriter

    def __init__(self, job_file_path: str):
        self.job_file_path = Path(job_file_path)
        self.job_writer = JobWriter()
        self.load_job(job_file_path)

    def load_job(self, job_file_path: str):
        with open(job_file_path, "rb") as f:
            self.config = tomli.load(f)

        return self

    def parse(self):
        for key, value in self.config.items():
            if key in MAPPING:
                option = MAPPING[key]

                if type(value) is dict:
                    print(value)
                    self.job_writer.add(option(**value))
                elif type(value) is list:
                    for item in value:
                        self.job_writer.add(
                            option(**item) if type(item) is dict else option(item)
                        )
                else:
                    self.job_writer.add(option(value))
            else:
                raise ValueError(f"Unknown option: {key}")
        return self

    def to_str(self):
        return self.job_writer.to_string()
