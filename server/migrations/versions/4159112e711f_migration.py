"""migration

Revision ID: 4159112e711f
Revises: c7d243d5fb79
Create Date: 2024-12-20 02:13:23.430179

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4159112e711f'
down_revision = 'c7d243d5fb79'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('_password_hash',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('_password_hash',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###
