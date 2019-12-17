from fabric import task
from invoke import Collection

from ._common import config


@task()
def git_delete_stale(ctx):
    git_branches_to_keep = "|".join(config["available_environments"])
    ctx.run(f'git branch --merged | egrep -v "(^\\*|{git_branches_to_keep})" | xargs git branch -d')


@task()
def git_checkout_pr(ctx, pr_id):
    ctx.run(f"git fetch upstream pull/{pr_id}/head:pr-{pr_id}")
    ctx.run(f"git checkout pr-{pr_id}")


git_collection = Collection("git")
git_collection.add_task(git_delete_stale, name="delete-stale")
git_collection.add_task(git_checkout_pr, name="checkout-pr")
