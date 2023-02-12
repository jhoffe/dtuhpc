import re
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
    "standard_output": StandardOutputFilePathOption,
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

    def __init__(self, job_file_path: str, variables: dict = None):
        self.job_file_path = Path(job_file_path)
        self.job_writer = JobWriter()
        self.load_job(job_file_path, variables)

    def load_job(self, job_file_path: str, variables: dict = None) -> "JobReader":
        with open(job_file_path, "r") as f:
            contents = self.replace_variables(f.read(), variables or {})
            self.config = tomli.loads(contents)

        return self

    @staticmethod
    def replace_variables(string: str, variables: dict) -> str:
        regex = re.compile(r"\${{\s*(?P<var_name>[a-zA-Z_]+[0-9]*)\s*}}")

        for match in regex.finditer(string):
            var_name = match.group("var_name")
            if var_name in variables:
                string = string.replace(match.group(0), variables[var_name])
            else:
                raise ValueError(f"Variable {var_name} not found in job file")

        return string

    def parse(self) -> "JobReader":
        for key, value in self.config.items():
            if key in MAPPING:
                option = MAPPING[key]

                if type(value) is dict:
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
