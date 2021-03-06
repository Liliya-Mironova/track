"""empty message

Revision ID: c4814ccd07c3
Revises: 
Create Date: 2019-03-24 17:02:21.641228

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4814ccd07c3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chats',
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.Column('is_group_chat', sa.Boolean(), nullable=True),
    sa.Column('topic', sa.String(length=80), nullable=False),
    sa.Column('last_message', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('chat_id')
    )
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('nick', sa.String(length=80), nullable=False),
    sa.Column('avatar', sa.String(length=80), nullable=True),
    sa.Column('external_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('nick')
    )
    op.create_table('messages',
    sa.Column('message_id', sa.Integer(), nullable=False),
    sa.Column('chat_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('content', sa.String(length=80), nullable=False),
    sa.Column('added_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['chats.chat_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('message_id')
    )
    op.create_table('passwords',
    sa.Column('password_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('password_hash', sa.String(length=80), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('password_id')
    )
    op.create_table('attachments',
    sa.Column('attach_id', sa.Integer(), nullable=False),
    sa.Column('chat_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('message_id', sa.Integer(), nullable=True),
    sa.Column('type_', sa.String(length=80), nullable=False),
    sa.Column('url', sa.String(length=80), nullable=True),
    sa.ForeignKeyConstraint(['chat_id'], ['chats.chat_id'], ),
    sa.ForeignKeyConstraint(['message_id'], ['messages.message_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('attach_id')
    )
    op.create_table('members',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.Column('new_messages', sa.String(), nullable=True),
    sa.Column('last_read_message_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['chat_id'], ['chats.chat_id'], ),
    sa.ForeignKeyConstraint(['last_read_message_id'], ['messages.message_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('user_id', 'chat_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('members')
    op.drop_table('attachments')
    op.drop_table('passwords')
    op.drop_table('messages')
    op.drop_table('users')
    op.drop_table('chats')
    # ### end Alembic commands ###
