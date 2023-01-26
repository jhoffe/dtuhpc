from .option import Option


class ErrorOutputFilePathOption(Option):
    name: str
    suffix_job_id: bool
    overwrite: bool

    def __init__(self, name: str, suffix_job_id: bool = True, overwrite: bool = False):
        self.name = name
        self.suffix_job_id = suffix_job_id
        self.overwrite = overwrite

        super().__init__(option=self.get_option(), value=self.get_job_name())

    def get_option(self):
        return "e" if not self.overwrite else "eo"

    def get_job_name(self):
        return self.name if self.suffix_job_id else f"{self.name}_%J"
