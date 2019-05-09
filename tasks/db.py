from invoke import task


@task
def upgrade(c, ini_file):
    """執行 db migrations 至最新版"""
    c.run('alembic -c {} upgrade head'.format(ini_file))

