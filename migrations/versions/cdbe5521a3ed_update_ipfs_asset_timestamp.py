"""update ipfs_asset timestamp

Revision ID: cdbe5521a3ed
Revises: 54d6f4259f38
Create Date: 2024-06-12 15:19:33.038903

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'cdbe5521a3ed'
down_revision: Union[str, None] = '54d6f4259f38'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('ipfs_asset', 'timestamp',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.String(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('ipfs_asset', 'timestamp',
               existing_type=sa.String(),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False)
    # ### end Alembic commands ###