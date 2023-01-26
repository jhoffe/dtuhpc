from .option import Option


class EmailForNotificationsOption(Option):
    email: str

    def __init__(self, email: str):
        self.email = email
        super().__init__(option="u", value=email)
