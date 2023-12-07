"""Update fields to DateTime and add foreign keys

Revision ID: <revision_id>
Revises: <previous_revision_id>
Create Date: <date_created>

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey

# revision identifiers, used by Alembic.
revision = '<revision_id>'
down_revision = '<previous_revision_id>'
branch_labels = None
depends_on = None

def upgrade():
    # Use batch_alter_table to allow for table alterations on SQLite
    with op.batch_alter_table('beats') as batch_op:
        batch_op.alter_column('date_added',
                              type_=sa.DateTime(),
                              existing_type=sa.String())

    with op.batch_alter_table('layers') as batch_op:
        batch_op.alter_column('date_added',
                              type_=sa.DateTime(),
                              existing_type=sa.Date())
        batch_op.alter_column('created_by',
                              type_=sa.String(),
                              existing_type=sa.String(),
                              new_column_name='user_id',
                              type_=sa.Integer())
        

    with op.batch_alter_table('stems') as batch_op:
        batch_op.alter_column('date_added',
                              type_=sa.DateTime(),
                              existing_type=sa.Date())
        batch_op.alter_column('created_by',
                              type_=sa.String(),
                              existing_type=sa.String(),
                              new_column_name='user_id',
                              type_=sa.Integer(),
                              sqlalchemy.ForeignKey('users.id'))

def downgrade():
    with op.batch_alter_table('beats') as batch_op:
        batch_op.alter_column('date_added',
                              type_=sa.String(),
                              existing_type=sa.DateTime())

    with op.batch_alter_table('layers') as batch_op:
        batch_op.alter_column('date_added',
                              type_=sa.Date(),
                              existing_type=sa.DateTime())
        batch_op.alter_column('user_id',
                              type_=sa.String(),
                              existing_type=sa.Integer(),
                              new_column_name='created_by')

    with op.batch_alter_table('stems') as batch_op:
        batch_op.alter_column('date_added',
                              type_=sa.Date(),
                              existing_type=sa.DateTime())
        batch_op.alter_column('user_id',
                              type_=sa.String(),
                              existing_type=sa.Integer(),
                              new_column_name='created_by')
