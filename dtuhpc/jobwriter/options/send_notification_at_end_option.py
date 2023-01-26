from .option import Option


class SendNotificationAtEndOption(Option):
    send: bool

    def __init__(self, send: bool = True):
        self.send = send
        super().__init__(option="N")
