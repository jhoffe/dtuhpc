from .command import Command


class LoadModuleCommand(Command):
    module: str

    def __init__(self, module: str):
        self.module = module

        super().__init__(command=f"module load {module}")
