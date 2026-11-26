"""project idea workflow

Revision ID: 0002_project_idea_workflow
Revises: 0001_initial
"""
from alembic import op
import sqlalchemy as sa

revision = "0002_project_idea_workflow"
down_revision = "0001_initial"
branch_labels = None
depends_on = None

def upgrade():
    op.add_column("project_ideas", sa.Column("technical_note", sa.Text(), nullable=True))
    op.add_column("project_ideas", sa.Column("decision_reason", sa.Text(), nullable=True))
    op.add_column("project_ideas", sa.Column("responsible_department", sa.String(length=160), nullable=True))
    op.add_column("project_ideas", sa.Column("estimated_cost", sa.Numeric(14, 2), nullable=True))
    op.add_column("project_ideas", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True))
    op.execute("UPDATE project_ideas SET updated_at = created_at WHERE updated_at IS NULL")
    op.create_index("ix_project_ideas_status", "project_ideas", ["status"])
    op.create_index("uq_discussion_support_user", "discussion_supports", ["discussion_id", "user_id"], unique=True)
    op.create_index("uq_project_idea_support_user", "project_idea_supports", ["project_idea_id", "user_id"], unique=True)
    op.create_table(
        "project_idea_comments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("project_idea_id", sa.Integer(), sa.ForeignKey("project_ideas.id", ondelete="CASCADE"), nullable=False),
        sa.Column("author_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_project_idea_comments_project_idea_id", "project_idea_comments", ["project_idea_id"])
    op.create_table(
        "project_idea_status_history",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("project_idea_id", sa.Integer(), sa.ForeignKey("project_ideas.id", ondelete="CASCADE"), nullable=False),
        sa.Column("actor_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("from_status", sa.String(length=50), nullable=True),
        sa.Column("to_status", sa.String(length=50), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_project_idea_status_history_project_idea_id", "project_idea_status_history", ["project_idea_id"])

def downgrade():
    op.drop_table("project_idea_status_history")
    op.drop_table("project_idea_comments")
    op.drop_index("uq_project_idea_support_user", table_name="project_idea_supports")
    op.drop_index("uq_discussion_support_user", table_name="discussion_supports")
    op.drop_index("ix_project_ideas_status", table_name="project_ideas")
    for col in ["updated_at", "estimated_cost", "responsible_department", "decision_reason", "technical_note"]:
        op.drop_column("project_ideas", col)
