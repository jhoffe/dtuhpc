import click

from dtuhpc.cli.cli_config import CLIConfig


@click.command()
@click.argument("command", nargs=1, type=str, required=True)
@click.pass_obj
def exec(config: CLIConfig, command: str):
    """Executes COMMAND on the DTU HPC Server."""
    config.load_config()
    conn = config.connection()
    conn.run(command)

    conn.close()
