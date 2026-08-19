import os, httpx
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from gateway.auth import verify_api_key

app = FastAPI(title="Agent Gateway")

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "CloudSentry Agent Gateway",
        "documentation": "/docs"
    }

class AlertPayload(BaseModel):
    service_name: str
    environment: str
    severity: str
    log_trace: str
    timestamp: str

@app.post("/v1/alerts/ingest")
async def ingest_alert(payload: AlertPayload, token: str = Depends(verify_api_key)):
    async with httpx.AsyncClient() as client:
        comp_res = await client.post("http://compliance-agent:8003/sanitize", json=payload.model_dump())
        sanitized_data = comp_res.json()
        
        diag_res = await client.post("http://diagnostic-agent:8001/analyze", json=sanitized_data["sanitized_payload"])
        rca_data = diag_res.json()
        
        remed_res = await client.post("http://remediation-agent:8002/remediate", json={"service_name": payload.service_name, "analysis": rca_data["analysis"]})
        return {"status": "executed", "security": sanitized_data, "rca": rca_data, "remediation": remed_res.json()}
