"""update document asset_id

Revision ID: 8c85cd2abf66
Revises: cdbe5521a3ed
Create Date: 2024-06-12 15:22:53.200903

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c85cd2abf66'
down_revision: Union[str, None] = 'cdbe5521a3ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('document', 'asset_id',
               existing_type=sa.BIGINT(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('document', 'asset_id',
               existing_type=sa.BIGINT(),
               nullable=False)
    # ### end Alembic commands ###
