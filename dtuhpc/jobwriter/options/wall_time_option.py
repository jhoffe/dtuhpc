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

    @staticmethod
    def time_prefix(time: int) -> str:
        return f"0{time}" if time < 10 else str(time)

    def format_time(self):
        return f"{self.time_prefix(self.hours)}:{self.time_prefix(self.minutes)}"
