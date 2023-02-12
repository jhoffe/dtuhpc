from typing import Optional

from .option import Option


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
        aff: Optional[bool] = None,
        block: Optional[bool] = None,
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
        ]

        if self.aff is not None:
            options.append(f"aff={self.format_bool_as_yes_no(self.aff)}")

        if self.block is not None:
            options.append(f"block={self.format_bool_as_yes_no(self.block)}")

        if self.gpu_model_name is not None:
            options.append(f"gmodel={self.gpu_model_name}")

        if self.memory_size is not None:
            options.append(f"gmem={self.memory_size}G")

        return ":".join(options)
