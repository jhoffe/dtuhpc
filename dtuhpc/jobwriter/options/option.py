from typing import Optional, Union


class Option:
    option: Optional[str]
    value: Optional[Union[str, int]]
    config_name: str

    def __init__(
        self, option: Optional[str] = None, value: Optional[Union[str, int]] = None
    ):
        self.option = option
        self.value = value

    def _get_option_value(self):
        return (
            '"' + str(self.value) + '"'
            if isinstance(self.value, str)
            else str(self.value)
        )

    def get_option_line(self) -> str:
        if self.option is None:
            return ""

        return (
            f"#BSUB -{self.option} {self._get_option_value()}"
            if self.value is not None
            else f"#BSUB -{self.option}"
        )
