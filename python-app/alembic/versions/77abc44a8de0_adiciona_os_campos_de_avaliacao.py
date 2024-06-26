"""adiciona os campos de avaliacao

Revision ID: 77abc44a8de0
Revises: 46acf81f7773
Create Date: 2024-06-12 01:38:22.987051

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '77abc44a8de0'
down_revision: Union[str, None] = '46acf81f7773'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posicoes', sa.Column('evaluation', sa.Float(), nullable=False))
    op.add_column('posicoes', sa.Column('imbalance', sa.Float(), nullable=False))
    op.add_column('posicoes', sa.Column('material', sa.Float(), nullable=False))
    op.add_column('posicoes', sa.Column('mobility', sa.Float(), nullable=False))
    op.add_column('posicoes', sa.Column('king_safety', sa.Float(), nullable=False))
    op.add_column('posicoes', sa.Column('threats', sa.Float(), nullable=False))
    op.add_column('posicoes', sa.Column('passed', sa.Float(), nullable=False))
    op.drop_column('posicoes', 'avaliacao')
    op.add_column('sequencias', sa.Column('evaluation', sa.Float(), nullable=False))
    op.add_column('sequencias', sa.Column('imbalance', sa.Float(), nullable=False))
    op.add_column('sequencias', sa.Column('material', sa.Float(), nullable=False))
    op.add_column('sequencias', sa.Column('mobility', sa.Float(), nullable=False))
    op.add_column('sequencias', sa.Column('king_safety', sa.Float(), nullable=False))
    op.add_column('sequencias', sa.Column('threats', sa.Float(), nullable=False))
    op.add_column('sequencias', sa.Column('passed', sa.Float(), nullable=False))
    op.drop_column('sequencias', 'avaliacao')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sequencias', sa.Column('avaliacao', mysql.FLOAT(), nullable=False))
    op.drop_column('sequencias', 'passed')
    op.drop_column('sequencias', 'threats')
    op.drop_column('sequencias', 'king_safety')
    op.drop_column('sequencias', 'mobility')
    op.drop_column('sequencias', 'material')
    op.drop_column('sequencias', 'imbalance')
    op.drop_column('sequencias', 'evaluation')
    op.add_column('posicoes', sa.Column('avaliacao', mysql.FLOAT(), nullable=False))
    op.drop_column('posicoes', 'passed')
    op.drop_column('posicoes', 'threats')
    op.drop_column('posicoes', 'king_safety')
    op.drop_column('posicoes', 'mobility')
    op.drop_column('posicoes', 'material')
    op.drop_column('posicoes', 'imbalance')
    op.drop_column('posicoes', 'evaluation')
    # ### end Alembic commands ###
