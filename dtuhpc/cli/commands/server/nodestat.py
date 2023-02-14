import click

from dtuhpc.cli.cli_context import CLIContext
from dtuhpc.commands import Nodestat


@click.command()
@click.option("--cpu", "-c", default=False, is_flag=True)
@click.option("--features", "-f", default=False, is_flag=True)
@click.option("--gpu", "-g", default=False, is_flag=True)
@click.option("--gpu_model", "-G", default=False, is_flag=True)
@click.option("--jobs", "-j", default=False, is_flag=True)
@click.option("--queue_jobs", "-J", default=False, is_flag=True)
@click.option("--load_util", "-l", default=False, is_flag=True)
@click.option("--visual_load_util", "-v", default=False, is_flag=True)
@click.option("--memory", "-m", default=False, is_flag=True)
@click.option("--reserved", "-r", default=False, is_flag=True)
@click.argument("queues", nargs=-1)
@click.pass_obj
def nodestat(
    ctx: CLIContext,
    cpu,
    features,
    gpu,
    gpu_model,
    jobs,
    queue_jobs,
    load_util,
    visual_load_util,
    memory,
    reserved,
    queues,
):
    """Print the nodestat from the server."""
    conn = ctx.connection

    cmd = Nodestat(conn)
    cmd.run(
        *queues,
        cpu=cpu,
        features=features,
        gpu=gpu,
        gpu_model=gpu_model,
        jobs=jobs,
        queue_jobs=queue_jobs,
        load_utilization=load_util,
        visual_load_utilization=visual_load_util,
        memory=memory,
        reserved_slots=reserved,
    )

    conn.close()
