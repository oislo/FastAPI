"""add apt_num col to address

Revision ID: 2b95a5a97af6
Revises: 301c16acbf81
Create Date: 2022-12-08 12:19:32.500238

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b95a5a97af6'
down_revision = '301c16acbf81'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('address', sa.Column('apt_num', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('address', 'apt_num')
