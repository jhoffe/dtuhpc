from .option import Option


class WallTimeOption(Option):
    hours: int
    minutes: int

    def __init__(self, hours: int = 0, minutes: int = 0):
        assert hours >= 0 and minutes >= 0
        assert hours > 0 or minutes > 0

        self.hours = hours
        self.minutes = minutes

        super().__init__(option="W", value=self.format_time())

    def format_time(self):
        return f"{self.hours}:{self.minutes}"
