"""create items table

Revision ID: d1684241010b
Revises:
Create Date: 2021-06-27 17:21:08.154741

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d1684241010b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "items",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(64), nullable=False),
        sa.Column("description", sa.Unicode(), nullable=False),
        sa.Column("price", sa.Numeric(), nullable=False),
        sa.Column("is_offer", sa.Boolean(), nullable=False),
    )


def downgrade():
    op.drop_table("items")
