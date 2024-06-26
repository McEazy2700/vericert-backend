"""update asset is_duplicate

Revision ID: 21821fe28b4b
Revises: 8c85cd2abf66
Create Date: 2024-06-12 15:55:35.752680

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '21821fe28b4b'
down_revision: Union[str, None] = '8c85cd2abf66'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('ipfs_asset', 'is_duplicate',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('ipfs_asset', 'is_duplicate',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###
