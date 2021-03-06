"""Initial migration.

Revision ID: 04011c4bdcd7
Revises: 
Create Date: 2022-06-09 02:18:51.240714

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '04011c4bdcd7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sensor_data_target', sa.Column('driving_name', sa.String(length=255), nullable=True))
    op.drop_column('sensor_data_target', 'AccY')
    op.drop_column('sensor_data_target', 'GyroX')
    op.drop_column('sensor_data_target', 'GyroZ')
    op.drop_column('sensor_data_target', 'GyroY')
    op.drop_column('sensor_data_target', 'AccZ')
    op.drop_column('sensor_data_target', 'AccX')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sensor_data_target', sa.Column('AccX', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('sensor_data_target', sa.Column('AccZ', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('sensor_data_target', sa.Column('GyroY', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('sensor_data_target', sa.Column('GyroZ', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('sensor_data_target', sa.Column('GyroX', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('sensor_data_target', sa.Column('AccY', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.drop_column('sensor_data_target', 'driving_name')
    # ### end Alembic commands ###
