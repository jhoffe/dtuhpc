import click

from dtuhpc.cli.cli_context import CLIContext


@click.command()
@click.pass_obj
def ssh(context: CLIContext):
    """SSH into DTU's server."""
    conn = context.connection
    conn.open_shell()
    conn.close()
