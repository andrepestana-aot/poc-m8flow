from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"

def upgrade():
    # Example 1: add an index on an upstream table column (low risk)
    op.create_index("ix_pi_status", "process_instance", ["status"])

    # Example 2: add a nullable column (medium risk but usually non-breaking)
    op.add_column("process_instance", sa.Column("tenant_id", sa.String(), nullable=True))

def downgrade():
    op.drop_column("process_instance", "tenant_id")
    op.drop_index("ix_pi_status", table_name="process_instance")
