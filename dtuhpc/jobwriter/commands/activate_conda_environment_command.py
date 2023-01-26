from .command import Command


class ActivateCondaEnvironment(Command):
    env: str

    def __init__(self, env: str):
        self.env = env
        super().__init__(command=f"conda activate {env}")
