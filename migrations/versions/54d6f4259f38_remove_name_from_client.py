"""remove name from client

Revision ID: 54d6f4259f38
Revises: 882dc8e97b5b
Create Date: 2024-06-12 12:19:51.028193

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54d6f4259f38'
down_revision: Union[str, None] = '882dc8e97b5b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('client', 'name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('client', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
