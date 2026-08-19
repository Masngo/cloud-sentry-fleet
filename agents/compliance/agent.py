import re
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Compliance Agent")

class SanitizeRequest(BaseModel):
    service_name: str
    log_trace: str
    environment: str
    severity: str
    timestamp: str

@app.post("/sanitize")
async def sanitize(req: SanitizeRequest):
    sanitized = re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', '[REDACTED_PII]', req.log_trace)
    threat = "ignore previous instructions" in req.log_trace.lower()
    if threat: sanitized = "[BLOCKED PROMPT INJECTION]"
    
    payload = req.model_dump()
    payload["log_trace"] = sanitized
    return {"sanitized_payload": payload, "threat_detected": threat}
