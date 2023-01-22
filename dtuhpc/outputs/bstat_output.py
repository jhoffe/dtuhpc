from dataclasses import dataclass

from fabric.runners import Result

from .table import Table


@dataclass
class BStatOutput(Table):
    columns: list[str]
    rows: list[list[str]]

    @staticmethod
    def _split_line(line: str) -> list[str]:
        return [c.strip() for c in line.split(" ") if c != ""]

    @staticmethod
    def parse(result: Result) -> "BStatOutput":
        table_str = result.stdout

        if table_str == "":
            return BStatOutput([], [])

        lines = table_str.splitlines()
        columns = BStatOutput._split_line(lines[0])
        rows = [BStatOutput._split_line(line) for line in lines[1:]]

        return BStatOutput(columns, rows)
