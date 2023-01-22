from dataclasses import dataclass

from fabric.runners import Result
from rich.table import Table as RichTable

from dtuhpc.console import console

from .output import Output


@dataclass
class Table(Output):
    columns: list[str]
    rows: list[list[str]]

    @staticmethod
    def _split_line(line: str) -> list[str]:
        raise NotImplementedError()

    @staticmethod
    def parse(result: Result) -> "Table":
        table_str = result.stdout
        lines = table_str.splitlines()
        columns = Table._split_line(lines[0])
        rows = [Table._split_line(line) for line in lines[1:]]

        return Table(columns, rows)

    def print(self) -> None:
        table = RichTable(*self.columns)
        for row in self.rows:
            table.add_row(*row)
        console.print(table)
