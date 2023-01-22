from dataclasses import dataclass

from fabric.runners import Result

from .table import Table


@dataclass
class ShowstartOutput(Table):
    columns: list[str]
    rows: list[list[str]]

    @staticmethod
    def _split_line(line: str) -> list[str]:
        return [c.strip() for c in line.split("  ") if c != ""]

    @staticmethod
    def parse(result: Result) -> "ShowstartOutput":
        table_str = result.stdout
        lines = table_str.splitlines()
        columns = ShowstartOutput._split_line(lines[0])
        rows = [ShowstartOutput._split_line(line) for line in lines[1:]]

        return ShowstartOutput(columns, rows)
