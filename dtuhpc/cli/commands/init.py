import os
from io import StringIO

import click

from dtuhpc.cli.cli_config import CLIConfig
from dtuhpc.commands import BSub
from dtuhpc.jobwriter.job_reader import JobReader


@click.command()
@click.option(
    "--poetry",
    is_flag=True,
    default=False,
    help="Use poetry to install dependencies on HPC.",
)
@click.option(
    "--custom-job",
    default=None,
    type=click.Path(exists=True),
    help="Use a custom job to initiate repository on HPC.",
)
@click.pass_obj
def init(config: CLIConfig, poetry: bool, custom_job: click.Path):
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

    if poetry and custom_job is not None:
        raise ValueError("Cannot use both poetry and custom job.")
    elif poetry:
        job_path = "default_jobs/init-poetry.toml"
    elif custom_job is not None:
        job_path = custom_job
    else:
        job_path = "default_jobs/init-pip.toml"

    job_reader = JobReader(job_path, variables)
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
