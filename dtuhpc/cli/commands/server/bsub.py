import click

from dtuhpc.cli.cli_config import CLIConfig
from dtuhpc.commands import BSub


@click.command()
@click.argument("script_path", nargs=1, type=str)
@click.pass_obj
def bsub(config: CLIConfig, script_path: str):
    """Submit a job to queue."""
    conn = config.connection()

    cmd = BSub(conn)
    cmd.run(f"< {script_path}")
    conn.close()
