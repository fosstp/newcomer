from invoke import Collection, task
from . import db


@task
def test(c):
    """跑測試"""
    c.run('pytest tp_enroll/tests.py')


namespace = Collection(db, test)
