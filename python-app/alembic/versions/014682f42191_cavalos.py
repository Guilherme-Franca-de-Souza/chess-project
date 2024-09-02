"""cavalos

Revision ID: 014682f42191
Revises: 2327354f4758
Create Date: 2024-09-01 20:06:38.341852

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '014682f42191'
down_revision: Union[str, None] = '2327354f4758'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posicoes', sa.Column('cavalos_brancas', sa.JSON(), nullable=False))
    op.add_column('posicoes', sa.Column('cavalos_negras', sa.JSON(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posicoes', 'cavalos_negras')
    op.drop_column('posicoes', 'cavalos_brancas')
    # ### end Alembic commands ###