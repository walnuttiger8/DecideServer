"""empty message

Revision ID: 583ac90f66de
Revises: c8346659977c
Create Date: 2021-04-23 11:49:56.218345

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '583ac90f66de'
down_revision = 'c8346659977c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('wallet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('stop_loss', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('take_profit', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('wallet', schema=None) as batch_op:
        batch_op.drop_column('take_profit')
        batch_op.drop_column('stop_loss')

    # ### end Alembic commands ###
