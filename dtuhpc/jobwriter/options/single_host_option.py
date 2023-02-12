from .option import Option


class SingleHostOption(Option):
    def __init__(self, single_host: bool = True):
        if single_host:
            super().__init__(option="R", value="span[hosts=1]")
        else:
            super().__init__()
