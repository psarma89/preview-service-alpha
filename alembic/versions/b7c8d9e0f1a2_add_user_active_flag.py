"""Add is_active flag to users

Revision ID: b7c8d9e0f1a2
Revises: a1b2c3d4e5f6
Create Date: 2024-02-02 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "b7c8d9e0f1a2"
down_revision: Union[str, None] = "a1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False))


def downgrade() -> None:
    op.drop_column("users", "is_active")
