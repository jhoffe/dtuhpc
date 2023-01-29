import os
from typing import Optional

import click

from dtuhpc.cli.cli_config import CLIConfig
from dtuhpc.cli.server_commands_cli import server_command
from dtuhpc.console import console, prompt_list


@click.group()
@click.option(
    "--hide/--no-hide",
    default=False,
    show_default=True,
    help="hide output from the server.",
)
@click.option(
    "--config", default=None, type=click.Path(exists=True), help="path to config file."
)
@click.option(
    "--cwd",
    default=None,
    type=str,
    help="default working directory for executing commands.",
)
@click.pass_context
def cli(ctx, hide, config, cwd):
    ctx.obj = CLIConfig(config_path=config, hide=hide, cwd=cwd)


@cli.command()
def init():
    """Initiates the current project on DTU's HPC server."""
    pass


@cli.command()
@click.option("--pr", "-p", type=Optional[int], default=None)
@click.option("--branch", "-b", type=Optional[str], default=None)
@click.pass_obj
def deploy(config: CLIConfig, pr: Optional[int], branch: Optional[str]):
    """Deploy a job."""
    gh = config.github()

    repo = config.git_repo()
    repo_remote = repo.remote("origin")
    repo_url = repo_remote.url
    repo.close()

    repo_id = (
        repo_url.replace("git@github.com:", "")
        .replace("https://github.com/", "")
        .replace(".git", "")
    )

    gh_repo = gh.get_repo(repo_id)

    pull_requests = gh_repo.get_pulls(state="open", sort="created")

    options = [f"#{pr.number}: {pr.title}" for pr in pull_requests]

    if len(options) == 0:
        console.print("[bold red]No open pull requests.[/bold red]")
        os.sys.exit(1)

    option = prompt_list("Pick a PR:", options)

    print(option)


@cli.command()
@click.argument("command", nargs=1, type=str, required=True)
@click.pass_obj
def exec(config: CLIConfig, command: str):
    """Executes COMMAND on the DTU HPC Server."""
    conn = config.connection()
    conn.run(command)


@cli.command()
@click.pass_obj
def ssh(config: CLIConfig):
    """SSH into DTU's server."""
    conn = config.connection()
    conn.open_shell()


if __name__ == "__main__":
    cli.add_command(server_command)

    cli()
