"""test

Revision ID: de94de025975
Revises: 
Create Date: 2022-09-18 14:40:31.833619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de94de025975'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('test', sa.String(), nullable=True))


def downgrade():
    pass
