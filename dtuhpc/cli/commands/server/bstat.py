from typing import Optional

import click

from dtuhpc.cli.cli_context import CLIContext
from dtuhpc.commands import BStat


@click.command()
@click.option("--cpu", "-c", default=False, help="Show CPU usage.")
@click.option("--memory", "-m", default=False, help="Show memory usage.")
@click.option("--user", "-u", default=None, type=str)
@click.option("--queue", "-q", default=None, type=str)
@click.argument("job_ids", nargs=-1)
@click.pass_obj
def bstat(
    ctx: CLIContext,
    cpu: bool,
    memory: bool,
    user: Optional[str],
    queue: Optional[str],
    job_ids: list[str],
):
    """Show current running jobs."""
    conn = ctx.connection

    cmd = BStat(conn)
    cmd.run(
        *job_ids,
        cpu_usage=cpu,
        memory_usage=memory,
        user=user,
        queue=queue,
    )
    conn.close()
