from .option import Option


class CoreBlockSizeOption(Option):
    block_size: int

    def __init__(self, block_size: int):
        assert block_size > 0
        self.block_size = block_size

        super().__init__(option="R", value=f"span[block={block_size}]")
