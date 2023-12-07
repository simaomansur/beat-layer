"""Added profile_pic and bio columns

Revision ID: 41798ff2594d
Revises: 
Create Date: 2023-12-05 13:45:40.819849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41798ff2594d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_pic', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('bio', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('bio')
        batch_op.drop_column('profile_pic')

    # ### end Alembic commands ###