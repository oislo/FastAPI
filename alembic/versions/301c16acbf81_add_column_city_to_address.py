"""add column city to address

Revision ID: 301c16acbf81
Revises: 60ce2613abc9
Create Date: 2022-12-07 21:46:24.571207

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '301c16acbf81'
down_revision = '60ce2613abc9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("address", sa.Column("city", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("city", "address")
