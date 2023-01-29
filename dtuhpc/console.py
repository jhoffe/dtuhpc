from rich.console import Console

console = Console()


def prompt_list(question: str, options: list[str]) -> int:
    for i, option in enumerate(options):
        console.print(f"[{i}]: {option}")

    def print_invalid_input():
        return console.print("[bold red]Invalid input[/bold red]")

    try:
        question_idx = int(console.input(question))
    except ValueError:
        print_invalid_input()
        return prompt_list(question, options)

    if question_idx >= len(options) or question_idx < 0:
        print_invalid_input()
        return prompt_list(question, options)

    return question_idx
