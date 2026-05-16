"""create items table

Revision ID: d1684241010b
Revises:
Create Date: 2021-06-27 17:21:08.154741

"""

import sqlmodel as sm

from alembic import op

# revision identifiers, used by Alembic.
revision = "d1684241010b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "items",
        sm.Column("id", sm.Integer, primary_key=True),
        sm.Column("name", sm.String(64), nullable=False),
        sm.Column("description", sm.Unicode(), nullable=False),
        sm.Column("price", sm.Numeric(), nullable=False),
        sm.Column("is_offer", sm.Boolean(), nullable=False),
    )


def downgrade():
    op.drop_table("items")
