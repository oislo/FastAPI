"""create phone nr for user col

Revision ID: 5421cf84827b
Revises: 
Create Date: 2022-12-07 20:09:25.051761

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5421cf84827b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("phone_number", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "phone_number")
