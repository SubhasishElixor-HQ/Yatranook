"""Initial Yatranook schema.

Revision ID: 0001_initial
Revises:
"""

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects import postgresql

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(320), nullable=False),
        sa.Column("full_name", sa.String(160), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_table(
        "destinations",
        sa.Column("id", sa.String(80), primary_key=True),
        sa.Column("name", sa.String(180), nullable=False),
        sa.Column("location", sa.String(220), nullable=False),
        sa.Column("region", sa.String(120), nullable=False, server_default="Odisha"),
        sa.Column("category", sa.String(40), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("image", sa.Text(), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("duration", sa.String(80), nullable=True),
        sa.Column("price_label", sa.String(240), nullable=True),
        sa.Column("tags", sa.JSON(), nullable=False, server_default=sa.text("'[]'::json")),
        sa.Column("source_name", sa.String(180), nullable=True),
        sa.Column("source_url", sa.Text(), nullable=True),
        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
    )
    op.create_index("ix_destinations_name", "destinations", ["name"])
    op.create_index("ix_destinations_location", "destinations", ["location"])
    op.create_index("ix_destinations_region", "destinations", ["region"])
    op.create_index("ix_destinations_category", "destinations", ["category"])
    op.create_table(
        "tourism_documents",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("source_name", sa.String(200), nullable=False),
        sa.Column("source_url", sa.Text(), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=False, server_default=sa.text("'{}'::json")),
        sa.Column("embedding", Vector(1536), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tourism_documents_embedding_hnsw ON tourism_documents USING hnsw (embedding vector_cosine_ops)"
    )
    op.create_table(
        "trips",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("title", sa.String(180), nullable=False),
        sa.Column("origin", sa.String(220), nullable=False),
        sa.Column("region", sa.String(160), nullable=False, server_default=""),
        sa.Column("budget", sa.Numeric(12, 2), nullable=False),
        sa.Column("budget_type", sa.String(20), nullable=False),
        sa.Column("travelers", sa.Integer(), nullable=False),
        sa.Column("duration", sa.String(20), nullable=False),
        sa.Column("interests", sa.JSON(), nullable=False, server_default=sa.text("'[]'::json")),
        sa.Column("itinerary", sa.JSON(), nullable=False, server_default=sa.text("'{}'::json")),
        sa.Column("estimated_total", sa.Numeric(12, 2), nullable=True),
        sa.Column("status", sa.String(24), nullable=False, server_default="draft"),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
    )
    op.create_index("ix_trips_user_id", "trips", ["user_id"])
    op.create_index("ix_trips_status", "trips", ["status"])


def downgrade() -> None:
    op.drop_index("ix_trips_status", table_name="trips")
    op.drop_index("ix_trips_user_id", table_name="trips")
    op.drop_table("trips")
    op.execute("DROP INDEX IF EXISTS ix_tourism_documents_embedding_hnsw")
    op.drop_table("tourism_documents")
    op.drop_index("ix_destinations_category", table_name="destinations")
    op.drop_index("ix_destinations_region", table_name="destinations")
    op.drop_index("ix_destinations_location", table_name="destinations")
    op.drop_index("ix_destinations_name", table_name="destinations")
    op.drop_table("destinations")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
