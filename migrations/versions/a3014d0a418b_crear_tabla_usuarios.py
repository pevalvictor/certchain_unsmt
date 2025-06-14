"""crear tabla usuarios

Revision ID: a3014d0a418b
Revises: 
Create Date: 2025-05-29 11:42:21.662183

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3014d0a418b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usuarios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre_completo', sa.String(length=100), nullable=False),
    sa.Column('correo', sa.String(length=120), nullable=False),
    sa.Column('contrasena_hash', sa.String(length=128), nullable=False),
    sa.Column('rol', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('correo')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('usuarios')
    # ### end Alembic commands ###
