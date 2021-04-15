"""empty message

Revision ID: c8346659977c
Revises: e0d19eabb586
Create Date: 2021-04-15 17:21:51.855271

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8346659977c'
down_revision = 'e0d19eabb586'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trade', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_trade_time'), ['time'], unique=False)
        batch_op.drop_column('predicted_price')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trade', schema=None) as batch_op:
        batch_op.add_column(sa.Column('predicted_price', sa.FLOAT(), nullable=True))
        batch_op.drop_index(batch_op.f('ix_trade_time'))

    # ### end Alembic commands ###