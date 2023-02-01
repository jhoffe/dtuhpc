import os
from io import StringIO
from typing import Optional

import click

from dtuhpc.cli.cli_config import CLIConfig
from dtuhpc.cli.server_commands_cli import server_command
from dtuhpc.commands import BSub
from dtuhpc.console import console
from dtuhpc.jobwriter.commands import Command, LoadModuleCommand
from dtuhpc.jobwriter.job_writer import JobWriter
from dtuhpc.jobwriter.options import (
    ErrorOutputFilePathOption,
    MemoryPerCoreOption,
    NameOption,
    NCPUCoresOption,
    QueueOption,
    SingleHostOption,
    StandardOutputFilePathOption,
    WallTimeOption,
)


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
    ctx.obj = CLIConfig(config_path=config, hide=hide, cwd=cwd)


@cli.command()
@click.pass_obj
def init(config: CLIConfig):
    """Initiates the current project on DTU's HPC server."""
    repo = config.git_repo()
    repo_remote = repo.remote("origin")
    repo_url = repo_remote.url
    repo.close()

    project_name = config.config["project"]["name"]
    project_path = config.config["project"]["path"]

    job_writer = JobWriter()

    job_writer.add_option(QueueOption("hpc"))
    job_writer.add_option(NameOption(f"init_{project_name}"))
    job_writer.add_option(WallTimeOption(0, 15))
    job_writer.add_option(NCPUCoresOption(2))
    job_writer.add_option(SingleHostOption())
    job_writer.add_option(MemoryPerCoreOption(4))
    job_writer.add_option(StandardOutputFilePathOption(f"out_init_{project_name}.out"))
    job_writer.add_option(ErrorOutputFilePathOption(f"out_init_{project_name}.err"))

    job_writer.add_command(Command(f"git clone {repo_url} {project_path}"))
    job_writer.add_command(Command(f"cd {project_path}"))
    job_writer.add_command(LoadModuleCommand("python3/3.10.7"))
    job_writer.add_command(Command("python3 -m venv venv"))
    job_writer.add_command(Command("source venv/bin/activate"))
    job_writer.add_command(Command("python -m pip install -r requirements.txt"))

    conn = config.connection()

    conn.run("mkdir -p .dtuhpc")
    conn._conn.put(
        StringIO(job_writer.to_string()),
        os.path.join(config.cwd, ".dtuhpc/", f"initialize_{project_name}_job.sh"),
    )

    bsub = BSub(conn)
    bsub.run(f"< .dtuhpc/initialize_{project_name}_job.sh")

    conn.close()


@cli.command()
@click.option("--pr", "-p", default=False, is_flag=True)
@click.option("--branch", "-b", default=False, is_flag=True)
@click.argument("job_name", type=str, default=None)
@click.pass_obj
def deploy(config: CLIConfig, pr: bool, branch: bool, job_name: Optional[str]):
    """Deploy a job."""
    gh = config.github()

    repo = config.git_repo()
    repo_remote = repo.remote("origin")
    repo_url = repo_remote.url
    repo.close()

    repo_id = (
        repo_url.replace("git@github.com:", "")
        .replace("https://github.com/", "")
        .replace(".git", "")
    )

    gh_repo = gh.get_repo(repo_id)

    all_branches = gh_repo.get_branches()

    for branch in all_branches:
        print(branch.name)

    pull_requests = gh_repo.get_pulls(state="open", sort="created")

    options = [f"#{pr.number}: {pr.title} ({pr.head.ref})" for pr in pull_requests]

    if len(options) == 0:
        console.error("No open pull requests.")
        os.sys.exit(1)

    option_idx = console.prompt_list("Pick a PR: ", options)
    pr = pull_requests[option_idx]
    branch_name = pr.head.ref
    print(branch_name)

    conn = config.connection()

    conn.run("git fetch")
    conn.run(f"git checkout {branch_name}")
    BSub(conn).run(f"< {job_name}")

    conn.close()


@cli.command()
@click.argument("command", nargs=1, type=str, required=True)
@click.pass_obj
def exec(config: CLIConfig, command: str):
    """Executes COMMAND on the DTU HPC Server."""
    conn = config.connection()
    conn.run(command)

    conn.close()


@cli.command()
@click.pass_obj
def ssh(config: CLIConfig):
    """SSH into DTU's server."""
    conn = config.connection()
    conn.open_shell()
    conn.close()


if __name__ == "__main__":
    cli.add_command(server_command)

    cli()
