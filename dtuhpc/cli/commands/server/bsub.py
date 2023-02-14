import click

from dtuhpc.cli.cli_context import CLIContext
from dtuhpc.commands import BSub


@click.command()
@click.argument("script_path", nargs=1, type=str)
@click.pass_obj
def bsub(ctx: CLIContext, script_path: str):
    """Submit a job to queue."""
    conn = ctx.connection

    cmd = BSub(conn)
    cmd.run(f"< {script_path}")
    conn.close()
