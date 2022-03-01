"""empty message

Revision ID: 7cd41babb967
Revises: a05152369bcf
Create Date: 2022-02-24 16:23:07.717686

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7cd41babb967'
down_revision = 'a05152369bcf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_comments_timestamp'), 'comments', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_comments_timestamp'), table_name='comments')
    op.drop_column('comments', 'timestamp')
    # ### end Alembic commands ###