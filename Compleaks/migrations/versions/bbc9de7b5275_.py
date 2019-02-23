"""empty message

Revision ID: bbc9de7b5275
Revises: 0fac58c5a72e
Create Date: 2019-02-22 21:36:02.451120

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbc9de7b5275'
down_revision = '0fac58c5a72e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('alternativas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('conteudo', sa.Text(), nullable=False),
    sa.Column('opcao', sa.Integer(), nullable=True),
    sa.Column('questao_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['questao_id'], ['questoes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('alternativas')
    # ### end Alembic commands ###
