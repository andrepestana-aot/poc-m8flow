from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None

def upgrade():
    op.create_table(
        "m8flow_tenant",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
    )

    op.create_table(
        "m8flow_connector_credential",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("tenant_id", sa.String(), sa.ForeignKey("m8flow_tenant.id"), nullable=False),
        sa.Column("connector_key", sa.String(), nullable=False),
        sa.Column("secret_json", sa.Text(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
    )
    op.create_unique_constraint(
        "uq_tenant_connector_key",
        "m8flow_connector_credential",
        ["tenant_id", "connector_key"],
    )

    op.create_table(
        "m8flow_connector_call_log",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("tenant_id", sa.String(), nullable=False),
        sa.Column("connector_key", sa.String(), nullable=False),
        sa.Column("command", sa.String(), nullable=False),
        sa.Column("status_code", sa.Integer(), nullable=True),
        sa.Column("request_json", sa.Text(), nullable=True),
        sa.Column("response_json", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
    )

def downgrade():
    op.drop_table("m8flow_connector_call_log")
    op.drop_constraint("uq_tenant_connector_key", "m8flow_connector_credential", type_="unique")
    op.drop_table("m8flow_connector_credential")
    op.drop_table("m8flow_tenant")
