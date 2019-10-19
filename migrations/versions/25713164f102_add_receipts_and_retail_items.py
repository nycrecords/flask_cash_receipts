"""Add Receipts and Retail Items

Revision ID: 25713164f102
Revises: e3fe3eb8982d
Create Date: 2019-10-18 19:03:19.806178

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "25713164f102"
down_revision = "e3fe3eb8982d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "receipt",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("username", sa.String(length=32), nullable=False),
        sa.Column("pin", sa.String(length=32), nullable=False),
        sa.Column("transaction_time", sa.DateTime(), nullable=False),
        sa.Column("subtotal", sa.Float(), nullable=False),
        sa.Column("total", sa.Float(), nullable=False),
        sa.Column("tax", sa.Float(), nullable=False),
        sa.Column("items", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "retail_items",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=250), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("tax", sa.Float(), nullable=False),
        sa.Column("event_name", sa.String(length=32), nullable=False),
        sa.Column("custom_attributes", sa.Text()),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("retail_items")
    op.drop_table("receipt")
    # ### end Alembic commands ###
