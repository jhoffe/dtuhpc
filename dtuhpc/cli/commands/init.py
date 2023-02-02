import os
from io import StringIO

import click

from dtuhpc.cli.cli_config import CLIConfig
from dtuhpc.commands import BSub
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


@click.command()
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
