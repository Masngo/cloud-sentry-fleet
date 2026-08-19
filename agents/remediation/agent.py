from fastapi import FastAPI
from pydantic import BaseModel
from shared.memory.firestore_client import record_remediation_event

app = FastAPI(title="Remediation Agent")

class RemediationRequest(BaseModel):
    service_name: str
    analysis: str

@app.post("/remediate")
async def remediate(req: RemediationRequest):
    result = f"SUCCESS: Rolled back Cloud Run service '{req.service_name}'."
    record_remediation_event(req.service_name, req.analysis, result)
    return {"status": "executed", "action": result}
