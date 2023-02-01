"""Console module for outputting to consoleself.

This module defines a class for outputting to the console,
with the capabilities of the rich package.
"""

from rich.console import Console as RichConsole


class Console(RichConsole):
    """Class for providing rich console output with custom methods
    Args:
        RichConsole: Inherits from rich.console.Console
    """

    def primary(self, format: str) -> None:
        """Prints text in blue color. Should be used for primary text output.

        Args:
            format (str): Text to be printed
        """
        self.print(f"[blue]{format}[/blue]")

    def success(self, format: str):
        """Prints text in green. Should be used for success messages.

        Args:
            format (str): Text to be printed
        """
        self.print(f"[green]{format}[/green]")

    def error(self, format: str):
        """Prints text in red color. Should be used for error messages.

        Args:
            format (str): Text to be printed
        """
        self.print(f"[bold red]{format}[/bold red]")

    def prompt_list(self, question: str, options: list[str]) -> int:
        """Prints a list of options, and prompts the user for an answer.
        It will continue to prompt the user until a valid answer is inputted.

        Args:
            question (str): The prompt message.
            options (list[str]): The different options that should be displayed.

        Returns:
            int: Returns the index of the chosen option.
        """
        for i, option in enumerate(options):
            self.print(f"[{i}]: {option}")

        def print_invalid_input():
            return self.error("Invalid input")

        try:
            question_idx = int(self.input(question))
        except ValueError:
            print_invalid_input()
            return self.prompt_list(question, options)

        if question_idx >= len(options) or question_idx < 0:
            print_invalid_input()
            return self.prompt_list(question, options)

        return question_idx


console = Console()
