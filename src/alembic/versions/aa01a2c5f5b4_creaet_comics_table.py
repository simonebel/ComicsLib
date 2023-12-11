"""creaet comics table

Revision ID: aa01a2c5f5b4
Revises: 
Create Date: 2023-11-24 16:42:07.896703

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "aa01a2c5f5b4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "comics",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("drawer_id", sa.Integer, sa.ForeignKey("authors.id"), index=True),
        sa.Column("scenarist_id", sa.Integer, sa.ForeignKey("authors.id"), index=True),
        sa.Column("serie", sa.String),
        sa.Column("title", sa.String),
        sa.Column("editor", sa.String),
        sa.Column("published_date", sa.String),
        sa.Column("edition", sa.String),
        sa.Column("format", sa.String),
        sa.Column("ean", sa.String),
        sa.Column("image", sa.String),
    )

    op.create_table(
        "authors",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("first_name", sa.String, index=True),
        sa.Column("last_name", sa.String, index=True),
        sa.Column("nick_name", sa.String, index=True),
        sa.Column("biography", sa.String),
        sa.Column("activity", sa.String),
    )


def downgrade():
    op.drop_table("comics")
    op.drop_table("authors")
