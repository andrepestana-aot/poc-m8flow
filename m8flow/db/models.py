from sqlalchemy import (
    Column, String, DateTime, Boolean, ForeignKey, Text, Integer, func, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Tenant(Base):
    __tablename__ = "m8flow_tenant"
    id = Column(String, primary_key=True)          # e.g., uuid
    name = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

class ConnectorCredential(Base):
    __tablename__ = "m8flow_connector_credential"
    id = Column(String, primary_key=True)          # uuid
    tenant_id = Column(String, ForeignKey("m8flow_tenant.id"), nullable=False)
    connector_key = Column(String, nullable=False) # e.g., "http", "salesforce"
    secret_json = Column(Text, nullable=False)     # store encrypted in real life
    is_active = Column(Boolean, nullable=False, server_default="true")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    tenant = relationship("Tenant")

    __table_args__ = (
        UniqueConstraint("tenant_id", "connector_key", name="uq_tenant_connector_key"),
    )

class ConnectorCallLog(Base):
    __tablename__ = "m8flow_connector_call_log"
    id = Column(String, primary_key=True)          # uuid
    tenant_id = Column(String, nullable=False)
    connector_key = Column(String, nullable=False)
    command = Column(String, nullable=False)
    status_code = Column(Integer, nullable=True)
    request_json = Column(Text, nullable=True)
    response_json = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
