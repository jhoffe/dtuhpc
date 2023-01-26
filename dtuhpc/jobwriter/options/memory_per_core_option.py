from .option import Option


class MemoryPerCoreOption(Option):
    memory_in_gb_per_core: int

    def __init__(self, memory_per_core_in_gb: int):
        self.memory_in_gb_per_core = memory_per_core_in_gb
        super().__init__(option="R", value=self.format_ram_option())

    def format_ram_option(self):
        return f"rusage[mem={self.memory_in_gb_per_core}G]"
