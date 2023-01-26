from .option import Option


class CorePTileSizeOption(Option):
    ptile_size: int

    def __init__(self, ptile_size: int):
        assert ptile_size > 0
        self.ptile_size = ptile_size

        super().__init__(option="R", value=f"span[ptile={ptile_size}]")
