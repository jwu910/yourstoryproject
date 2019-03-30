"""empty message

Revision ID: a56f61dee447
Revises: 00a8a030975b
Create Date: 2019-01-12 20:13:24.583395

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a56f61dee447'
down_revision = '00a8a030975b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('account', 'password_hash',
                    existing_type=sa.VARCHAR(length=128),
                    nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('account', 'password_hash',
                    existing_type=sa.VARCHAR(length=128),
                    nullable=True)
    # ### end Alembic commands ###
