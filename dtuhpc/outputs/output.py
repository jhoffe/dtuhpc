from abc import ABC, abstractmethod

from fabric.runners import Result


class Output(ABC):
    """Base class for all output types."""

    cmd_result: Result

    @abstractmethod
    def print(self) -> None:
        raise NotImplementedError("OutputType.print() not implemented")

    @staticmethod
    @abstractmethod
    def parse(result: Result) -> "Output":
        raise NotImplementedError("OutputType.parse() not implemented")
