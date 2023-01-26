from .option import Option


class QueueOption(Option):
    queue: str

    def __init__(self, queue: str):
        self.queue = queue
        super().__init__(option="q", value=queue)
