from .option import Option


class NCPUCoresOption(Option):
    cores: int

    def __init__(self, cores: int):
        self.cores = cores
        super().__init__(option="n", value=cores)
