import os
from typing import Optional

import click

from dtuhpc.cli.cli_config import CLIConfig
from dtuhpc.console import console


@click.command()
@click.option("--pr", "-p", default=None, type=int)
@click.option("--branch", "-b", default=None, type=str)
@click.argument("job_name", type=str, default=None)
@click.pass_obj
def deploy(
    config: CLIConfig, pr: Optional[int], branch: Optional[str], job_name: Optional[str]
):
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

            branch_name = console.prompt_list("Pick a branch: ", all_branch_names)
        else:
            all_branches = gh_repo.get_branches()
            all_branch_names = [branch.name for branch in all_branches]

            pull_requests = gh_repo.get_pulls(state="open", sort="created")

            options = [
                f"#{pr.number}: {pr.title} ({pr.head.ref})" for pr in pull_requests
            ]

            if len(options) == 0:
                console.error("No open pull requests.")
                os.sys.exit(1)

            option_idx = console.prompt_list("Pick a PR: ", options)
            pr = pull_requests[option_idx]
            branch_name = pr.head.ref

    config.cwd = config.config["project"]["path"]

    conn = config.connection()
    conn.run("git fetch")
    conn.run(f"git checkout {branch_name}")

    conn.run(f"source venv/bin/activate && python {job_name} | bsub")

    conn.close()
    conn.close()
