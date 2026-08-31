import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(title="CloudSentry AI Fleet")

# Payload Schema
class AlertPayload(BaseModel):
    service: str
    severity: str
    trace_log: str

# Serve Web Application Static Files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
async def serve_index():
    return FileResponse("static/index.html")

@app.post("/v1/alerts/ingest")
async def ingest_alert(payload: AlertPayload):
    # Simulated zero-trust compliance & diagnostic pipeline response
    sanitized_log = payload.trace_log.replace("Secret123!", "[REDACTED_CREDENTIAL]")
    
    return {
        "status": "RESOLVED",
        "compliance": {
            "pii_redacted": True,
            "sanitized_trace": sanitized_log
        },
        "diagnostic": {
            "model": "gemini-3.5-flash",
            "root_cause": "SQL injection payload detected in unauthenticated request headers.",
            "recommendation": "Block IP range and execute Cloud Run rollback to safe build v1.0.4."
        },
        "remediation": {
            "action": "AUTOMATIC_ROLLBACK_SUCCESSFUL",
            "service": payload.service
        }
    }
