import click

from dtuhpc.cli.cli_context import CLIContext


@click.command()
@click.argument("command", nargs=1, type=str, required=True)
@click.pass_obj
def exec(ctx: CLIContext, command: str):
    """Executes COMMAND on the DTU HPC Server."""
    conn = ctx.connection
    conn.run(command)

    conn.close()
