"""empty message

Revision ID: 67f7fe6ab3da
Revises: 
Create Date: 2019-03-27 13:20:00.714193

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67f7fe6ab3da'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('disciplinas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(), nullable=True),
    sa.Column('data_criacao', sa.DateTime(), nullable=True),
    sa.Column('ativado', sa.Boolean(), nullable=True),
    sa.Column('data_deletado', sa.DateTime(), nullable=True),
    sa.Column('id_deletor', sa.Integer(), nullable=True),
    sa.Column('id_criador', sa.Integer(), nullable=True),
    sa.Column('motivo_delete', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nome')
    )
    op.create_table('professores',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(), nullable=True),
    sa.Column('unidade_academica_id', sa.Integer(), nullable=True),
    sa.Column('data_criacao', sa.DateTime(), nullable=True),
    sa.Column('ativado', sa.Boolean(), nullable=True),
    sa.Column('data_deletado', sa.DateTime(), nullable=True),
    sa.Column('id_deletor', sa.Integer(), nullable=True),
    sa.Column('id_criador', sa.Integer(), nullable=True),
    sa.Column('motivo_delete', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nome')
    )
    op.create_table('usuarios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=True),
    sa.Column('hhash', sa.String(), nullable=True),
    sa.Column('nome', sa.String(length=120), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('curso', sa.String(length=64), nullable=True),
    sa.Column('periodo', sa.Integer(), nullable=True),
    sa.Column('is_admin', sa.Integer(), nullable=True),
    sa.Column('data_criacao', sa.DateTime(), nullable=True),
    sa.Column('avatar', sa.String(length=120), nullable=True),
    sa.Column('ativado', sa.Boolean(), nullable=True),
    sa.Column('data_deletado', sa.DateTime(), nullable=True),
    sa.Column('id_deletor', sa.Integer(), nullable=True),
    sa.Column('motivo_delete', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('arquivos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('arquivo', sa.String(length=120), nullable=False),
    sa.Column('ano', sa.Integer(), nullable=True),
    sa.Column('semestre', sa.String(length=80), nullable=True),
    sa.Column('tipo_conteudo', sa.String(length=120), nullable=True),
    sa.Column('observacoes', sa.Text(), nullable=True),
    sa.Column('data_submissao', sa.DateTime(), nullable=True),
    sa.Column('nota', sa.Integer(), nullable=True),
    sa.Column('data_deletado', sa.DateTime(), nullable=True),
    sa.Column('ativado', sa.Boolean(), nullable=True),
    sa.Column('id_deletor', sa.Integer(), nullable=True),
    sa.Column('motivo_delete', sa.String(length=600), nullable=True),
    sa.Column('professor_id', sa.Integer(), nullable=True),
    sa.Column('disciplina_id', sa.Integer(), nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['disciplina_id'], ['disciplinas.id'], ),
    sa.ForeignKeyConstraint(['professor_id'], ['professores.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comentarios_disc',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('conteudo', sa.Text(), nullable=False),
    sa.Column('data_criacao', sa.DateTime(), nullable=True),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('disciplina_id', sa.Integer(), nullable=False),
    sa.Column('respondeu_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['disciplina_id'], ['disciplinas.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comentarios_prof',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('conteudo', sa.Text(), nullable=False),
    sa.Column('data_criacao', sa.DateTime(), nullable=True),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('professor_id', sa.Integer(), nullable=False),
    sa.Column('respondeu_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['professor_id'], ['professores.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('questoes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('enunciado', sa.Text(), nullable=False),
    sa.Column('data_criacao', sa.DateTime(), nullable=True),
    sa.Column('correta', sa.Integer(), nullable=True),
    sa.Column('ativado', sa.Boolean(), nullable=True),
    sa.Column('disciplina_id', sa.Integer(), nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['disciplina_id'], ['disciplinas.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('alternativas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('conteudo', sa.Text(), nullable=False),
    sa.Column('opcao', sa.Integer(), nullable=True),
    sa.Column('questao_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['questao_id'], ['questoes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('avaliacao_arquivo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nota', sa.Integer(), nullable=False),
    sa.Column('data_nota', sa.DateTime(), nullable=True),
    sa.Column('arquivo_id', sa.Integer(), nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['arquivo_id'], ['arquivos.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comentarios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('conteudo', sa.Text(), nullable=False),
    sa.Column('data_criacao', sa.DateTime(), nullable=True),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('questao_id', sa.Integer(), nullable=False),
    sa.Column('respondeu_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['questao_id'], ['questoes.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comentarios')
    op.drop_table('avaliacao_arquivo')
    op.drop_table('alternativas')
    op.drop_table('questoes')
    op.drop_table('comentarios_prof')
    op.drop_table('comentarios_disc')
    op.drop_table('arquivos')
    op.drop_table('usuarios')
    op.drop_table('professores')
    op.drop_table('disciplinas')
    # ### end Alembic commands ###