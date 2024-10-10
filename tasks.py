from invoke import Collection, task


@task()
def test_hooks(ctx):
    ctx.run("pytest -s --cov=hooks --cov-report=html", pty=True, replace_env=False)


test_collection = Collection("test")
test_collection.add_task(test_hooks, name="hooks")
namespace = Collection(test_collection)
