"""mensagem

Revision ID: ce367a2f050c
Revises: 
Create Date: 2024-09-24 00:14:13.253786

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce367a2f050c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ambientes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('descricao', sa.String(length=4096), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cenarios',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('fen', sa.String(length=2048), nullable=False),
    sa.Column('descricao', sa.String(length=2048), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('jogadores',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(length=255), nullable=False),
    sa.Column('profundidade', sa.Integer(), nullable=False),
    sa.Column('redes_neurais', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('partidas',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('lances', sa.String(length=2048), nullable=False),
    sa.Column('resultado', sa.String(length=45), nullable=False),
    sa.Column('vencedor_id', sa.Integer(), nullable=True),
    sa.Column('brancas_id', sa.Integer(), nullable=False),
    sa.Column('negras_id', sa.Integer(), nullable=False),
    sa.Column('ambiente_id', sa.Integer(), nullable=False),
    sa.Column('cenario_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['ambiente_id'], ['ambientes.id'], ),
    sa.ForeignKeyConstraint(['brancas_id'], ['jogadores.id'], ),
    sa.ForeignKeyConstraint(['cenario_id'], ['cenarios.id'], ),
    sa.ForeignKeyConstraint(['negras_id'], ['jogadores.id'], ),
    sa.ForeignKeyConstraint(['vencedor_id'], ['jogadores.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('brancas_id', 'negras_id', 'cenario_id', name='_brancas_negras_cenario_uc')
    )
    op.create_table('posicoes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('numero_sequencia', sa.Integer(), nullable=False),
    sa.Column('fen', sa.String(length=4096), nullable=False),
    sa.Column('diferenca_material', sa.Integer(), nullable=False),
    sa.Column('rei_brancas', sa.JSON(), nullable=False),
    sa.Column('rei_negras', sa.JSON(), nullable=False),
    sa.Column('dama_brancas', sa.JSON(), nullable=False),
    sa.Column('dama_negras', sa.JSON(), nullable=False),
    sa.Column('torres_brancas', sa.JSON(), nullable=False),
    sa.Column('torres_negras', sa.JSON(), nullable=False),
    sa.Column('bispos_brancas', sa.JSON(), nullable=False),
    sa.Column('bispos_negras', sa.JSON(), nullable=False),
    sa.Column('cavalos_brancas', sa.JSON(), nullable=False),
    sa.Column('cavalos_negras', sa.JSON(), nullable=False),
    sa.Column('peoes_brancas', sa.JSON(), nullable=False),
    sa.Column('peoes_negras', sa.JSON(), nullable=False),
    sa.Column('check', sa.Integer(), nullable=False),
    sa.Column('mate', sa.Integer(), nullable=False),
    sa.Column('empate_repeticoes', sa.Integer(), nullable=False),
    sa.Column('empate_50', sa.Integer(), nullable=False),
    sa.Column('empate_afogamento', sa.Integer(), nullable=False),
    sa.Column('empate_material_insuficiente', sa.Integer(), nullable=False),
    sa.Column('partida_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['partida_id'], ['partidas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('avaliacoes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('valor', sa.Float(), nullable=False),
    sa.Column('tempo_segundos', sa.String(length=255), nullable=True),
    sa.Column('melhor_lance', sa.String(length=255), nullable=False),
    sa.Column('ambiente_id', sa.Integer(), nullable=False),
    sa.Column('jogador_id', sa.Integer(), nullable=False),
    sa.Column('posicao_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['ambiente_id'], ['ambientes.id'], ),
    sa.ForeignKeyConstraint(['jogador_id'], ['jogadores.id'], ),
    sa.ForeignKeyConstraint(['posicao_id'], ['posicoes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('avaliacoes')
    op.drop_table('posicoes')
    op.drop_table('partidas')
    op.drop_table('jogadores')
    op.drop_table('cenarios')
    op.drop_table('ambientes')
    # ### end Alembic commands ###
