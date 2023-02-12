import click

from dtuhpc.cli.cli_config import CLIConfig
from dtuhpc.cli.commands.server.bkill import bkill
from dtuhpc.cli.commands.server.bqueues import bqueues
from dtuhpc.cli.commands.server.bstat import bstat
from dtuhpc.cli.commands.server.bsub import bsub
from dtuhpc.cli.commands.server.nodestat import nodestat
from dtuhpc.cli.commands.server.showstart import showstart


@click.group(name="c")
@click.pass_obj
def server_command(config: CLIConfig):
    config.load_config()
    """Execute a predefined command."""


server_command.add_command(bkill)
server_command.add_command(nodestat)
server_command.add_command(bqueues)
server_command.add_command(bstat)
server_command.add_command(bsub)
server_command.add_command(showstart)
