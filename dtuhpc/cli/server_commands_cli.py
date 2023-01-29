from typing import Optional

import click

from dtuhpc.cli.cli_config import CLIConfig
from dtuhpc.commands import BKill, BQueues, BStat, BSub, Nodestat, Showstart


@click.group(name="c")
def server_command():
    """Execute a predefined command."""
    pass


@server_command.command()
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
    config: CLIConfig,
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
    conn = config.connection()

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


@server_command.command()
@click.option("--user", "-u", default=None, type=str)
@click.option("--queue", "-q", default=None, type=str)
@click.argument("job_ids", nargs=-1)
@click.pass_obj
def showstart(config: CLIConfig, user, queue, job_ids):
    """Show start times for jobs."""
    conn = config.connection()

    cmd = Showstart(conn)
    cmd.run(*job_ids, user=user, queue=queue)


@server_command.command()
@click.pass_obj
def bqueues(config: CLIConfig):
    """Show current running jobs."""
    conn = config.connection()

    cmd = BQueues(conn)
    cmd.run()


@server_command.command()
@click.option("--cpu", "-c", default=False, help="Show CPU usage.")
@click.option("--memory", "-m", default=False, help="Show memory usage.")
@click.option("--user", "-u", default=None, type=str)
@click.option("--queue", "-q", default=None, type=str)
@click.argument("job_ids", nargs=-1)
@click.pass_obj
def bstat(
    config: CLIConfig,
    cpu: bool,
    memory: bool,
    user: Optional[str],
    queue: Optional[str],
    job_ids: list[str],
):
    """Show current running jobs."""
    conn = config.connection()

    cmd = BStat(conn)
    cmd.run(
        *job_ids,
        cpu_usage=cpu,
        memory_usage=memory,
        user=user,
        queue=queue,
    )


@server_command.command()
@click.option("--kill-all", "-a", default=False, is_flag=True)
@click.option("--done", "-d", default=False, is_flag=True)
@click.option("--list-signals", "-l", default=False, is_flag=True)
@click.option("--remove-without-waiting", "-r", default=False, is_flag=True)
@click.option("--application-profile", "-app", default=None, type=str)
@click.option("--kill-reason", "-K", default=None, type=str)
@click.option("--group-name", "-g", default=None, type=str)
@click.option("--job-name", "-J", default=None, type=str)
@click.option("--host-name", "-m", default=None, type=str)
@click.option("--queue", "-q", default=None, type=str)
@click.option("--signal-name", "-s", default=None, type=str)
@click.option("--status", "-S", default=None, type=str)
@click.option("--zero", "-z", default=None, type=str)
@click.argument("job_ids", nargs=-1)
@click.pass_obj
def bkill(
    config: CLIConfig,
    kill_all,
    done,
    list_signals,
    remove_without_waiting,
    application_profile,
    kill_reason,
    group_name,
    job_name,
    host_name,
    queue,
    signal_name,
    status,
    zero,
    job_ids,
):
    """Kill a job."""
    conn = config.connection()

    cmd = BKill(conn)
    cmd.run(
        *job_ids,
        kill_all=kill_all,
        as_done=done,
        list_signals=list_signals,
        remove_without_waiting=remove_without_waiting,
        application_profile_name=application_profile,
        kill_reason=kill_reason,
        group_name=group_name,
        job_name=job_name,
        host_name=host_name,
        queue=queue,
        signal_name=signal_name,
        status=status,
        kill_all_satisfying=zero,
    )


@server_command.command()
@click.argument("script_path", nargs=1, type=str)
@click.pass_obj
def bsub(config: CLIConfig, script_path: str):
    """Submit a job to queue."""
    conn = config.connection()

    cmd = BSub(conn)
    cmd.run(f"< {script_path}")
