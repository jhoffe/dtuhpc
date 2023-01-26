from .option import Option


class NameOption(Option):
    name: str

    def __init__(self, name: str):
        self.name = name
        super().__init__(option="J", value=name)
