"""empty message

Revision ID: a57327d07443
Revises: f34f9924bc39
Create Date: 2021-04-14 15:06:37.927522

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a57327d07443'
down_revision = 'f34f9924bc39'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('balance', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'balance')
    # ### end Alembic commands ###
