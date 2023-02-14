import click

from dtuhpc.cli.cli_context import CLIContext
from dtuhpc.cli.commands import deploy, exec, init, server_command, ssh
from dtuhpc.cli.commands.auth import auth


@click.group()
@click.option(
    "--hide/--no-hide",
    default=False,
    show_default=True,
    help="hide output from the server.",
)
@click.option(
    "--config", default=None, type=click.Path(exists=True), help="path to config file."
)
@click.option(
    "--cwd",
    default=None,
    type=str,
    help="default working directory for executing commands.",
)
@click.pass_context
def cli(ctx, hide, config, cwd):
    ctx.obj = CLIContext(config_path=config, hide=hide, cwd=cwd)


def main():
    cli.add_command(server_command)
    cli.add_command(init)
    cli.add_command(exec)
    cli.add_command(deploy)
    cli.add_command(ssh)
    cli.add_command(auth)

    cli()


if __name__ == "__main__":
    main()
