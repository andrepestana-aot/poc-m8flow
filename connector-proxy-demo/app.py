import os, json, uuid
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text

app = FastAPI()
engine = create_engine(os.environ["M8FLOW_DATABASE_URI"], pool_pre_ping=True)

@app.get("/v1/commands")
def list_commands():
    # minimal discovery response (shape depends on Spiff proxy expectations)
    return {
        "connectors": [
            {"key": "demo", "commands": [{"key": "ping", "description": "Ping demo connector"}]}
        ]
    }

@app.post("/v1/do/demo/ping")
def do_ping(payload: dict):
    tenant_id = payload.get("tenant_id", "default")
    # credential lookup (simplified)
    with engine.begin() as conn:
        row = conn.execute(text("""
            select secret_json from m8flow_connector_credential
            where tenant_id = :tenant_id and connector_key = 'demo' and is_active = true
            limit 1
        """), {"tenant_id": tenant_id}).fetchone()

        secret = json.loads(row[0]) if row else {}

        log_id = str(uuid.uuid4())
        conn.execute(text("""
            insert into m8flow_connector_call_log
            (id, tenant_id, connector_key, command, status_code, request_json, response_json)
            values (:id, :tenant_id, 'demo', 'ping', 200, :req, :resp)
        """), {
            "id": log_id,
            "tenant_id": tenant_id,
            "req": json.dumps(payload),
            "resp": json.dumps({"ok": True}),
        })

    return {"ok": True, "used_secret_keys": list(secret.keys())}
