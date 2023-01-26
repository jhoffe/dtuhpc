from .option import Option


class SingleHostOption(Option):
    def __init__(self):
        super().__init__(option="R", value="span[hosts=1]")
