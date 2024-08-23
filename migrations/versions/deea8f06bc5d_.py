"""empty message

Revision ID: deea8f06bc5d
Revises: 
Create Date: 2024-08-22 20:55:41.080473

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'deea8f06bc5d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('event')
    op.drop_table('health_declaration')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('health_declaration',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('event_id', sa.VARCHAR(length=8), nullable=False),
    sa.Column('full_name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('phone_number', sa.VARCHAR(length=20), nullable=False),
    sa.Column('year_of_birth', sa.INTEGER(), nullable=False),
    sa.Column('symptoms', sa.VARCHAR(length=200), nullable=True),
    sa.Column('autoimmune_disease', sa.VARCHAR(length=100), nullable=True),
    sa.Column('other_medical_condition', sa.VARCHAR(length=100), nullable=True),
    sa.Column('medication', sa.VARCHAR(length=3), nullable=False),
    sa.Column('allergies', sa.VARCHAR(length=100), nullable=True),
    sa.Column('pregnant', sa.VARCHAR(length=3), nullable=False),
    sa.Column('additional_info', sa.TEXT(), nullable=True),
    sa.Column('flagged', sa.BOOLEAN(), nullable=True),
    sa.Column('instructor_checked', sa.BOOLEAN(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['event.unique_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('event',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('date', sa.DATE(), nullable=True),
    sa.Column('expected_participants', sa.INTEGER(), nullable=True),
    sa.Column('unique_id', sa.VARCHAR(length=8), nullable=False),
    sa.Column('contact_name', sa.VARCHAR(length=100), nullable=True),
    sa.Column('contact_number', sa.VARCHAR(length=20), nullable=True),
    sa.Column('is_done', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('unique_id')
    )
    # ### end Alembic commands ###