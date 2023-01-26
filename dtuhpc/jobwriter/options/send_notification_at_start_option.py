from .option import Option


class SendNotificationAtStartOption(Option):
    send: bool

    def __init__(self, send: bool = True):
        self.send = send
        super().__init__(option="B")
