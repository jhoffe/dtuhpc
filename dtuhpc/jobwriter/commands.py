from typing import Union


class Command:
    command: str

    def __init__(self, command: str):
        self.command = command

    def get_command(self):
        return self.command


class LoadModuleCommand(Command):
    module: str

    def __init__(self, module: str):
        self.module = module

        super().__init__(command=f"module load {module}")


class ActivateCondaEnvironment(Command):
    env: str

    def __init__(self, env: str):
        self.env = env
        super().__init__(command=f"conda activate {env}")


class FitModelWithPython(Command):
    model: str
    config_paths: Union[str, list[str]]
    entry_script_path: str

    def __init__(
        self,
        model: str,
        config_paths: Union[str, list[str]],
        entry_script_path: str = "src/main.py",
    ):
        self.model = model
        self.config_paths = config_paths
        self.entry_script_path = entry_script_path

        config_strings = (
            " ".join([f"--config={cp}" for cp in self.config_paths])
            if type(self.config_paths) == "list"
            else f"--config={self.config_paths}"
        )
        super().__init__(
            command=" ".join(
                [
                    "python",
                    self.entry_script_path,
                    "fit",
                    f"--model={self.model}",
                    config_strings,
                ]
            )
        )
