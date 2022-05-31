"""Initial migration.

Revision ID: 462ac2e87a9b
Revises: f6aa4c3a51ed
Create Date: 2022-05-31 14:55:10.078314

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '462ac2e87a9b'
down_revision = 'f6aa4c3a51ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('driver_rate_total_upd', sa.Column('driving_name', sa.String(length=255), nullable=True))
    op.drop_column('driver_rate_total_upd', 'driver_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('driver_rate_total_upd', sa.Column('driver_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('driver_rate_total_upd', 'driving_name')
    # ### end Alembic commands ###