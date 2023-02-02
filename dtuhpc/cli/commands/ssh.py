import click

from dtuhpc.cli.cli_config import CLIConfig


@click.command()
@click.pass_obj
def ssh(config: CLIConfig):
    """SSH into DTU's server."""
    conn = config.connection()
    conn.open_shell()
    conn.close()
