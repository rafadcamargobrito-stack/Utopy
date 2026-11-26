"""initial schema

Revision ID: 0001_initial
Revises:
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("role", sa.Enum("citizen", "moderator", "public_agent", "admin", name="userrole"), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_table("discussions",
        sa.Column("id", sa.Integer(), primary_key=True), sa.Column("title", sa.String(180), nullable=False),
        sa.Column("category", sa.String(60), nullable=False), sa.Column("excerpt", sa.Text(), nullable=False),
        sa.Column("author_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("is_published", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_index("ix_discussions_category", "discussions", ["category"])
    op.create_table("discussion_replies",
        sa.Column("id", sa.Integer(), primary_key=True), sa.Column("discussion_id", sa.Integer(), sa.ForeignKey("discussions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("author_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False), sa.Column("body", sa.Text(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_discussion_replies_discussion_id", "discussion_replies", ["discussion_id"])
    op.create_table("discussion_supports",
        sa.Column("id", sa.Integer(), primary_key=True), sa.Column("discussion_id", sa.Integer(), sa.ForeignKey("discussions.id", ondelete="CASCADE"), nullable=False), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    )
    op.create_index("ix_discussion_supports_discussion_id", "discussion_supports", ["discussion_id"])
    op.create_index("ix_discussion_supports_user_id", "discussion_supports", ["user_id"])
    op.create_table("project_ideas",
        sa.Column("id", sa.Integer(), primary_key=True), sa.Column("title", sa.String(180), nullable=False), sa.Column("area", sa.String(60), nullable=False), sa.Column("description", sa.Text(), nullable=False),
        sa.Column("author_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False), sa.Column("status", sa.String(50), nullable=False, server_default="Ideia inicial"), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_project_ideas_area", "project_ideas", ["area"])
    op.create_table("project_idea_supports",
        sa.Column("id", sa.Integer(), primary_key=True), sa.Column("project_idea_id", sa.Integer(), sa.ForeignKey("project_ideas.id", ondelete="CASCADE"), nullable=False), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    )
    op.create_index("ix_project_idea_supports_project_idea_id", "project_idea_supports", ["project_idea_id"])
    op.create_index("ix_project_idea_supports_user_id", "project_idea_supports", ["user_id"])
    op.create_table("officials",
        sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(150), nullable=False), sa.Column("role", sa.String(100), nullable=False), sa.Column("party", sa.String(120), nullable=False), sa.Column("projects", sa.Integer(), nullable=False, server_default="0"), sa.Column("activities", sa.Integer(), nullable=False, server_default="0"), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table("activities",
        sa.Column("id", sa.Integer(), primary_key=True), sa.Column("official_id", sa.Integer(), sa.ForeignKey("officials.id"), nullable=True), sa.Column("title", sa.String(180), nullable=False), sa.Column("description", sa.Text(), nullable=False), sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table("works",
        sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(180), nullable=False), sa.Column("area", sa.String(60), nullable=False), sa.Column("progress", sa.Integer(), nullable=False, server_default="0"), sa.Column("value", sa.Numeric(14,2), nullable=False, server_default="0"), sa.Column("deadline", sa.String(40), nullable=False),
    )
    op.create_table("transparency_documents",
        sa.Column("id", sa.Integer(), primary_key=True), sa.Column("title", sa.String(220), nullable=False), sa.Column("file_url", sa.String(500), nullable=False), sa.Column("year", sa.Integer(), nullable=False), sa.Column("source", sa.String(250), nullable=False), sa.Column("published_at", sa.DateTime(timezone=True), nullable=False),
    )

def downgrade():
    for name in ["transparency_documents", "works", "activities", "officials", "project_idea_supports", "project_ideas", "discussion_supports", "discussion_replies", "discussions", "users"]:
        op.drop_table(name)
