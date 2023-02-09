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

OPTION_MAPPING = {
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
}

COMMAND_MAPPING = {"module": LoadModuleCommand, "command": Command}


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

    def add_options(self):
        for key, value in self.config["opts"].items():
            if key in OPTION_MAPPING:
                if type(value) is dict:
                    self.job_writer.add_option(OPTION_MAPPING[key](**value))
                elif type(value) is list:
                    for item in value:
                        self.job_writer.add_option(OPTION_MAPPING[key](**item))
            else:
                raise ValueError(f"Unknown option: {key}")
        return self

    def add_commands(self):
        if "cmds" not in self.config.keys():
            raise ValueError("No commands found in job file")
        for key, value in self.config["cmds"].items():
            if key in COMMAND_MAPPING:
                if type(value) is dict:
                    self.job_writer.add_command(COMMAND_MAPPING[key](**value))
                elif type(value) is list:
                    for item in value:
                        self.job_writer.add_command(COMMAND_MAPPING[key](**item))
            else:
                raise ValueError(f"Unknown command: {key}")
        return self

    def to_str(self):
        return self.job_writer.to_string()


job = JobReader("test.toml").add_options().add_commands().to_str()

print(job)
