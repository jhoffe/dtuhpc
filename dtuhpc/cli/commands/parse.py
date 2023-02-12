from sys import stdout

import click

from dtuhpc.jobwriter.job_reader import JobReader


@click.command()
@click.argument("job_path", nargs=1, type=str, required=True)
def parse(job_path: str):
    """Initiates the current project on DTU's HPC server."""

    job_reader = JobReader(job_path)
    job_reader.parse()

    stdout.write(job_reader.to_str())
    stdout.close()
