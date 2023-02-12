import click

from dtuhpc.cli.cli_config import CLIConfig


@click.command()
@click.argument("command", nargs=1, type=str, required=True)
@click.pass_obj
def exec(config: CLIConfig, command: str):
    config.load_config()
    """Executes COMMAND on the DTU HPC Server."""
    conn = config.connection()
    conn.run(command)

    conn.close()
