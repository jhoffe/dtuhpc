class Command:
    command: str

    def __init__(self, command: str):
        self.command = command

    def get_command(self):
        return self.command
