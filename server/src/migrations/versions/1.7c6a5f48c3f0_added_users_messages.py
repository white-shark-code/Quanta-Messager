"""Added users & messages

Revision ID: 7c6a5f48c3f0
Revises: First revision
Create Date: 2025-06-20 12:05:34.645496

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from fastapi_users_db_sqlalchemy.generics import GUID, TIMESTAMPAware

# revision identifiers, used by Alembic.
revision: str = '7c6a5f48c3f0'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'group_chats',
        sa.Column('public_key', sa.LargeBinary(), nullable=False),
        sa.Column('id', GUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('creation_datetime', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'user',
        sa.Column('id', GUID(), nullable=False),
        sa.Column('email', sa.String(length=320), nullable=False),
        sa.Column('hashed_password', sa.String(length=1024), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_superuser', sa.Boolean(), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('accesstoken',
    sa.Column('user_id', GUID(), nullable=False),
    sa.Column('token', sa.String(length=43), nullable=False),
    sa.Column('created_at', TIMESTAMPAware(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('token')
    )
    op.create_index(
        op.f('ix_accesstoken_created_at'),
        'accesstoken',
        ['created_at'],
        unique=False
    )
    op.create_table(
        'dialog_chats',
        sa.Column('user0', GUID(), nullable=False),
        sa.Column('user1', GUID(), nullable=False),
        sa.Column('id', GUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('creation_datetime', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user0'], ['user.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user1'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'group_messages',
        sa.Column('chat_id', GUID(), nullable=False),
        sa.Column('id', GUID(), nullable=False),
        sa.Column('owner_id', GUID(), nullable=False),
        sa.Column('encrypted_message', sa.LargeBinary(), nullable=False),
        sa.Column('creation_datetime', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['chat_id'], ['group_chats.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_groups',
    sa.Column('user_id', GUID(), nullable=False),
    sa.Column('group_chat_id', GUID(), nullable=False),
    sa.Column('joined_data', sa.DateTime(), nullable=False),
    sa.Column(
        'role',
        sa.Enum(
            'READER',
            'USER',
            'KEYMAN',
            'MODERATOR',
            'SMALL_ADMIN',
            'ADMIN',
            name='roles'
        ),
        nullable=False
    ),
    sa.ForeignKeyConstraint(['group_chat_id'], ['group_chats.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'group_chat_id')
    )
    op.create_table('dialog_messages',
    sa.Column('chat_id', GUID(), nullable=False),
    sa.Column('id', GUID(), nullable=False),
    sa.Column('owner_id', GUID(), nullable=False),
    sa.Column('encrypted_message', sa.LargeBinary(), nullable=False),
    sa.Column('creation_datetime', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['dialog_chats.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dialog_messages')
    op.drop_table('user_groups')
    op.drop_table('group_messages')
    op.drop_table('dialog_chats')
    op.drop_index(op.f('ix_accesstoken_created_at'), table_name='accesstoken')
    op.drop_table('accesstoken')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('group_chats')
    # ### end Alembic commands ###
