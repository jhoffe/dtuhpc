import os
import sys
from io import StringIO
from typing import Optional

import click

from dtuhpc.cli.cli_context import CLIContext
from dtuhpc.console import console
from dtuhpc.jobwriter.job_reader import JobReader


@click.command()
@click.option("--pr", "-p", default=None, type=int)
@click.option("--branch", "-b", default=None, type=str)
@click.option("--jsm", "-j", is_flag=True, type=bool, default=False)
@click.argument("job_name", type=str, default=None)
@click.pass_obj
def deploy(
    ctx: CLIContext,
    pr: Optional[int],
    branch: Optional[str],
    job_name: Optional[str],
    jsm: bool,
):
    """Deploy a job."""
    gh = ctx.github

    repo = ctx.git_repo
    repo_remote = repo.remote("origin")
    repo_url = repo_remote.url
    repo.close()

    repo_id = (
        repo_url.replace("git@github.com:", "")
        .replace("https://github.com/", "")
        .replace(".git", "")
    )

    gh_repo = gh.get_repo(repo_id)

    if pr is not None:
        pr = gh_repo.get_pull(pr)
        branch_name = pr.head.ref
    elif branch is not None:
        branch_name = branch
    else:
        method = console.prompt_list("Branch or PR: ", ["Branch", "PR"])

        if method == 0:
            all_branches = gh_repo.get_branches()
            all_branch_names = [branch.name for branch in all_branches]

            branch_index = console.prompt_list("Pick a branch: ", all_branch_names)
            branch_name = all_branch_names[branch_index]
        else:
            pull_requests = gh_repo.get_pulls(state="open", sort="created")

            options = [
                f"#{pr.number}: {pr.title} ({pr.head.ref})" for pr in pull_requests
            ]

            if len(options) == 0:
                console.error("No open pull requests.")
                sys.exit(1)

            option_idx = console.prompt_list("Pick a PR: ", options)
            pr = pull_requests[option_idx]
            branch_name = pr.head.ref

    ctx.cwd = ctx.config["project"]["path"]

    conn = ctx.connection
    conn.run("git fetch")
    conn.run(f"git checkout {branch_name}")
    conn.run("git pull")

    job_reader = JobReader(job_name)
    job_reader.parse()
    job_contents = job_reader.to_str()

    deploy_job_path = os.path.join(
        ctx.config["ssh"]["default_cwd"], ".dtuhpc/", "deploy_job.sh"
    )
    conn.conn.put(StringIO(job_contents), deploy_job_path)

    jsm = " -jsm y" if jsm else ""

    conn.run(f"bsub -cwd {ctx.cwd}{jsm} < {deploy_job_path}")
    conn.run(f"rm {deploy_job_path}")

    conn.close()
