"""link public agents to profiles and add institutional proposals

Revision ID: 0003_official_management_content
Revises: 0002_project_idea_workflow
"""
from alembic import op
import sqlalchemy as sa

revision = "0003_official_management_content"
down_revision = "0002_project_idea_workflow"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("officials") as batch_op:
        batch_op.add_column(sa.Column("user_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key("fk_officials_user_id_users", "users", ["user_id"], ["id"])
        batch_op.create_index("ix_officials_user_id", ["user_id"], unique=True)
    op.create_table(
        "official_proposals",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("official_id", sa.Integer(), sa.ForeignKey("officials.id"), nullable=False),
        sa.Column("title", sa.String(180), nullable=False),
        sa.Column("area", sa.String(60), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("status", sa.String(50), nullable=False, server_default="Apresentada"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_official_proposals_official_id", "official_proposals", ["official_id"])


def downgrade():
    op.drop_index("ix_official_proposals_official_id", table_name="official_proposals")
    op.drop_table("official_proposals")
    with op.batch_alter_table("officials") as batch_op:
        batch_op.drop_index("ix_officials_user_id")
        batch_op.drop_constraint("fk_officials_user_id_users", type_="foreignkey")
        batch_op.drop_column("user_id")
