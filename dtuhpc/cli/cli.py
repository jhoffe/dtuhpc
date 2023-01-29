import click

from dtuhpc.cli.cli_config import CLIConfig
from dtuhpc.cli.server_commands_cli import server_command


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
def deploy():
    """Deploy a job."""
    pass


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
