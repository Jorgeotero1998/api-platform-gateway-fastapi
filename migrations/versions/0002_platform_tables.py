"""platform tables

Revision ID: 0002_platform_tables
Revises: 0001_init_users
Create Date: 2026-07-04
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0002_platform_tables"
down_revision = "0001_init_users"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "platform_api_keys",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("key_hash", sa.String(length=64), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ux_platform_api_keys_key_hash", "platform_api_keys", ["key_hash"], unique=True)

    op.create_table(
        "platform_usage_logs",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("api_key_hash", sa.String(length=64), nullable=False),
        sa.Column("method", sa.String(length=16), nullable=False),
        sa.Column("path", sa.String(length=300), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_platform_usage_logs_api_key_hash", "platform_usage_logs", ["api_key_hash"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_platform_usage_logs_api_key_hash", table_name="platform_usage_logs")
    op.drop_table("platform_usage_logs")
    op.drop_index("ux_platform_api_keys_key_hash", table_name="platform_api_keys")
    op.drop_table("platform_api_keys")

