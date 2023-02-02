import click

from dtuhpc.cli.cli_config import CLIConfig
from dtuhpc.commands import BQueues


@click.command()
@click.pass_obj
def bqueues(config: CLIConfig):
    """Show current running jobs."""
    conn = config.connection()

    cmd = BQueues(conn)
    cmd.run()
    conn.close()
