import click

from dtuhpc.cli.cli_context import CLIContext
from dtuhpc.commands import Showstart


@click.command()
@click.option("--user", "-u", default=None, type=str)
@click.option("--queue", "-q", default=None, type=str)
@click.argument("job_ids", nargs=-1)
@click.pass_obj
def showstart(config: CLIContext, user, queue, job_ids):
    """Show start times for jobs."""
    conn = config.connection

    cmd = Showstart(conn)
    cmd.run(*job_ids, user=user, queue=queue)
    conn.close()
