"""add serie and author_serie_association tables

Revision ID: a82e5ea0e65b
Revises: aa01a2c5f5b4
Create Date: 2023-12-12 23:53:55.337650

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "a82e5ea0e65b"
down_revision = "aa01a2c5f5b4"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "series",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("name", sa.String),
        sa.Column("editor", sa.String),
        sa.Column("published_date", sa.String),
        sa.Column("edition", sa.String),
        sa.Column("format", sa.String),
        sa.Column("ean", sa.String),
        sa.Column("image", sa.String),
        sa.Column("synopsis", sa.String),
    )

    op.create_table(
        "author_serie_association",
        sa.Column("serie_id", sa.Integer, sa.ForeignKey("series.id"), index=True),
        sa.Column("author_id", sa.Integer, sa.ForeignKey("authors.id"), index=True),
        sa.Column("role", sa.Integer),
    )


def downgrade():
    op.drop_table("series")
    op.drop_table("author_serie_association")
