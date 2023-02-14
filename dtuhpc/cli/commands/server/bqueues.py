import click

from dtuhpc.cli.cli_context import CLIContext
from dtuhpc.commands import BQueues


@click.command()
@click.pass_obj
def bqueues(ctx: CLIContext):
    """Show current running jobs."""
    conn = ctx.connection

    cmd = BQueues(conn)
    cmd.run()
    conn.close()
