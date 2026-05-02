"""add usuario_id to clientes"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision = '3cb73de467aa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'clientes',
        sa.Column('usuario_id', sa.Integer(), nullable=True)
    )

    op.create_foreign_key(
        'fk_clientes_usuarios',
        'clientes',
        'usuarios',
        ['usuario_id'],
        ['id'],
        ondelete='SET NULL'
    )

    op.create_index(
        'idx_clientes_usuario_id',
        'clientes',
        ['usuario_id']
    )


def downgrade():
    op.drop_index('idx_clientes_usuario_id', table_name='clientes')
    op.drop_constraint('fk_clientes_usuarios', 'clientes', type_='foreignkey')
    op.drop_column('clientes', 'usuario_id')