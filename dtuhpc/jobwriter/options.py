from typing import Optional, Union


class Option:
    option: str
    value: Optional[Union[str, int]]
    config_name: str

    def __init__(self, option: str, value: Optional[Union[str, int]] = None):
        self.option = option
        self.value = value

    def _get_option_value(self):
        return (
            '"' + str(self.value) + '"'
            if isinstance(self.value, str)
            else str(self.value)
        )

    def get_option_line(self):
        return (
            f"#BSUB -{self.option} {self._get_option_value()}"
            if self.value is not None
            else f"#BSUB -{self.option}"
        )


class CoreBlockSizeOption(Option):
    block_size: int

    def __init__(self, block_size: int):
        assert block_size > 0
        self.block_size = block_size

        super().__init__(option="R", value=f"span[block={block_size}]")


class CorePTileSizeOption(Option):
    ptile_size: int

    def __init__(self, ptile_size: int):
        assert ptile_size > 0
        self.ptile_size = ptile_size

        super().__init__(option="R", value=f"span[ptile={ptile_size}]")


class EmailForNotificationsOption(Option):
    email: str

    def __init__(self, email: str):
        self.email = email
        super().__init__(option="u", value=email)


class ErrorOutputFilePathOption(Option):
    name: str
    suffix_job_id: bool
    overwrite: bool

    def __init__(self, name: str, suffix_job_id: bool = True, overwrite: bool = False):
        self.name = name
        self.suffix_job_id = suffix_job_id
        self.overwrite = overwrite

        super().__init__(option=self.get_option(), value=self.get_job_name())

    def get_option(self):
        return "e" if not self.overwrite else "eo"

    def get_job_name(self):
        return self.name if self.suffix_job_id else f"{self.name}_%J"


class MemoryPerCoreKillLimitOption(Option):
    memory_in_gb_per_core: int

    def __init__(self, memory_per_core_in_gb: int):
        self.memory_in_gb_per_core = memory_per_core_in_gb
        super().__init__(option="M", value=self.format_ram_option())

    def format_ram_option(self):
        return f"rusage[mem={self.memory_in_gb_per_core}GB]"


class MemoryPerCoreOption(Option):
    memory_in_gb_per_core: int

    def __init__(self, memory_per_core_in_gb: int):
        self.memory_in_gb_per_core = memory_per_core_in_gb
        super().__init__(option="R", value=self.format_ram_option())

    def format_ram_option(self):
        return f"rusage[mem={self.memory_in_gb_per_core}G]"


class NCPUCoresOption(Option):
    cores: int

    def __init__(self, cores: int):
        self.cores = cores
        super().__init__(option="n", value=cores)


class NameOption(Option):
    name: str

    def __init__(self, name: str):
        self.name = name
        super().__init__(option="J", value=name)


class QueueOption(Option):
    queue: str

    def __init__(self, queue: str):
        self.queue = queue
        super().__init__(option="q", value=queue)


class SendNotificationAtEndOption(Option):
    send: bool

    def __init__(self, send: bool = True):
        self.send = send
        super().__init__(option="N")


class SendNotificationAtStartOption(Option):
    send: bool

    def __init__(self, send: bool = True):
        self.send = send
        super().__init__(option="B")


class SingleHostOption(Option):
    def __init__(self):
        super().__init__(option="R", value="span[hosts=1]")


class StandardOutputFilePathOption(Option):
    name: str
    suffix_job_id: bool
    overwrite: bool

    def __init__(self, name: str, suffix_job_id: bool = True, overwrite: bool = False):
        self.name = name
        self.suffix_job_id = suffix_job_id
        self.overwrite = overwrite

        super().__init__(option=self.get_option(), value=self.get_job_name())

    def get_option(self):
        return "o" if not self.overwrite else "oo"

    def get_job_name(self):
        return self.name if self.suffix_job_id else f"{self.name}_%J"


class UseGPUOption(Option):
    num_of_gpus: int
    per_task: bool
    mode: str
    aff: bool
    block: bool
    gpu_model_name: Optional[str]
    memory_size: Optional[int]

    def __init__(
        self,
        num_of_gpus: int = 1,
        per_task: bool = False,
        mode: str = "exclusive_process",
        aff: bool = True,
        block: bool = False,
        gpu_model_name: Optional[str] = None,
        memory_size: Optional[int] = None,
    ):
        self.num_of_gpus = num_of_gpus
        self.per_task = per_task
        self.mode = mode
        self.aff = aff
        self.block = block
        self.gpu_model_name = gpu_model_name
        self.memory_size = memory_size

        super().__init__(option="gpu", value=self.format_value())

    @staticmethod
    def format_bool_as_yes_no(boolvar):
        return "yes" if boolvar else "no"

    def format_value(self):
        options = [
            f"num={self.num_of_gpus}"
            if self.per_task is False
            else f"num={self.num_of_gpus}/task",
            f"mode={self.mode}",
            f"aff={self.format_bool_as_yes_no(self.aff)}",
            f"block={self.format_bool_as_yes_no(self.block)}",
        ]

        if self.gpu_model_name is not None:
            options.append(f"gmodel={self.gpu_model_name}")

        if self.memory_size is not None:
            options.append(f"gmem={self.memory_size}G")

        return "[" + ":".join(options) + "]"


class WallTimeOption(Option):
    hours: int
    minutes: int

    def __init__(self, hours: int = 0, minutes: int = 0):
        assert hours >= 0 and minutes >= 0
        assert hours > 0 or minutes > 0

        self.hours = hours
        self.minutes = minutes

        super().__init__(option="W", value=self.format_time())

    def format_time(self):
        return f"{self.hours}:{self.minutes}"
