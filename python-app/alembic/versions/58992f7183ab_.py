""".

Revision ID: 58992f7183ab
Revises: ce367a2f050c
Create Date: 2024-11-10 21:22:00.837667

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '58992f7183ab'
down_revision: Union[str, None] = 'ce367a2f050c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('partidas', 'lances',
               existing_type=mysql.VARCHAR(length=2048),
               type_=sa.String(length=96048),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('partidas', 'lances',
               existing_type=sa.String(length=96048),
               type_=mysql.VARCHAR(length=2048),
               existing_nullable=False)
    # ### end Alembic commands ###