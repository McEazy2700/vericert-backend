"""create application tables

Revision ID: 62103ad0066d
Revises: 280338cf4489
Create Date: 2024-06-11 16:26:37.170858

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "62103ad0066d"
down_revision: Union[str, None] = "280338cf4489"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "package",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column(
            "price", sa.BigInteger(), nullable=False, comment="Price in micro algos"
        ),
        sa.Column(
            "storage_capacity",
            sa.BigInteger(),
            nullable=False,
            comment="Storage capacity in KB",
        ),
        sa.Column("monthly_requests", sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "client",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("image_url", sa.String(), nullable=True),
        sa.Column("used_storage", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "client_package",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("client_id", sa.BigInteger(), nullable=False),
        sa.Column("package_id", sa.BigInteger(), nullable=False),
        sa.Column("api_public_key", sa.String(), nullable=False),
        sa.Column("api_secret_key_hash", sa.String(), nullable=False),
        sa.Column("has_pending_payment", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["client_id"],
            ["client.id"],
        ),
        sa.ForeignKeyConstraint(
            ["package_id"],
            ["package.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("api_secret_key_hash"),
    )
    op.create_index(
        op.f("ix_client_package_api_public_key"),
        "client_package",
        ["api_public_key"],
        unique=True,
    )
    op.create_table(
        "ipfs_asset",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("ipfs_hash", sa.String(), nullable=False),
        sa.Column("pin_size", sa.BigInteger(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("is_duplicate", sa.Boolean(), nullable=False),
        sa.Column("extension", sa.String(), nullable=True),
        sa.Column("client_id", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(
            ["client_id"],
            ["client.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("ipfs_hash"),
    )
    document_visibility = postgresql.ENUM(
        "PUBLIC", "PRIVATE", name="documentvisibility", create_type=False
    )
    document_visibility.create(op.get_bind())
    op.create_table(
        "document",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column(
            "visibility",
            document_visibility,
            nullable=False,
        ),
        sa.Column("authorised_email", sa.JSON(), nullable=True),
        sa.Column("ipfs_asset_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["ipfs_asset_id"],
            ["ipfs_asset.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("document")
    op.drop_table("ipfs_asset")
    op.drop_index(op.f("ix_client_package_api_public_key"), table_name="client_package")
    op.drop_table("client_package")
    op.drop_table("client")
    op.drop_table("package")
    # ### end Alembic commands ###
