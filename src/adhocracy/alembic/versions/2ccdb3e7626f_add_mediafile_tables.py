"""Add mediafile tables

Revision ID: 2ccdb3e7626f
Revises: 5209f75543b2
Create Date: 2014-02-21 17:59:57.932147

"""

# revision identifiers, used by Alembic.
revision = '2ccdb3e7626f'
down_revision = '5209f75543b2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mediafile',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.Unicode(length=255), nullable=False),
                    sa.Column('instance_id', sa.Integer(), nullable=True),
                    sa.Column('create_time', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['instance_id'], ['instance.id'],
                                            ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('delegateable_mediafiles',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('mediafile_id', sa.Integer(), nullable=False),
                    sa.Column('delegateable_id', sa.Integer(), nullable=False),
                    sa.Column('create_time', sa.DateTime(), nullable=True),
                    sa.Column('creator_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['creator_id'], ['user.id'], ),
                    sa.ForeignKeyConstraint(['delegateable_id'],
                                            ['delegateable.id'], ),
                    sa.ForeignKeyConstraint(['mediafile_id'],
                                            ['mediafile.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('comment_mediafiles',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('mediafile_id', sa.Integer(), nullable=False),
                    sa.Column('comment_id', sa.Integer(), nullable=False),
                    sa.Column('create_time', sa.DateTime(), nullable=True),
                    sa.Column('creator_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['comment_id'], ['comment.id'], ),
                    sa.ForeignKeyConstraint(['creator_id'], ['user.id'], ),
                    sa.ForeignKeyConstraint(['mediafile_id'],
                                            ['mediafile.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment_mediafiles')
    op.drop_table('delegateable_mediafiles')
    op.drop_table('mediafile')
    ### end Alembic commands ###
