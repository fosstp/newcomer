"""rename table

Revision ID: 71e7d79b4f2c
Revises: 771f1d687213
Create Date: 2018-11-20 15:46:08.817690

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71e7d79b4f2c'
down_revision = '771f1d687213'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('newcomer', 'new_students')


def downgrade():
    op.rename_table('new_students', 'newcomer')
