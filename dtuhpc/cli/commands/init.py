import os
from io import StringIO

import click

from dtuhpc.cli.cli_config import CLIConfig
from dtuhpc.commands import BSub
from dtuhpc.jobwriter.job_reader import JobReader


@click.command()
@click.pass_obj
def init(config: CLIConfig):
    """Initiates the current project on DTU's HPC server."""
    config.load_config()
    repo = config.git_repo()
    repo_remote = repo.remote("origin")
    repo_url = repo_remote.url
    repo.close()

    project_name = config.config["project"]["name"]
    project_path = config.config["project"]["path"]
    variables = {
        "project_name": project_name,
        "project_path": project_path,
        "git_url": repo_url,
    }

    job_reader = JobReader("default_jobs/init-poetry.toml", variables)
    job_reader.parse()

    conn = config.connection()

    conn.run("mkdir -p .dtuhpc")
    conn.conn.put(
        StringIO(job_reader.to_str()),
        os.path.join(config.cwd, ".dtuhpc/", f"initialize_{project_name}_job.sh"),
    )

    bsub = BSub(conn)
    bsub.run(f"< .dtuhpc/initialize_{project_name}_job.sh")

    conn.close()
