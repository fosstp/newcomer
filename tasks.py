from invoke import task


@task
def test(c):
    c.run('pytest tp_enroll/tests.py')
