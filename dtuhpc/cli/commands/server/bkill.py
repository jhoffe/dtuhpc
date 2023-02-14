import click

from dtuhpc.cli.cli_context import CLIContext
from dtuhpc.commands import BKill


@click.command()
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
    ctx: CLIContext,
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
    conn = ctx.connection

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
    conn.close()
