import os
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from google.genai import types
from agents.diagnostic.tools import query_cloud_logging, query_cloud_monitoring

app = FastAPI(title="Diagnostic Agent")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY", "mock-key"))

class AnalyzeRequest(BaseModel):
    service_name: str
    log_trace: str

@app.post("/analyze")
async def analyze(req: AnalyzeRequest):
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=f"Analyze: {req.service_name}, Trace: {req.log_trace}",
            config=types.GenerateContentConfig(tools=[query_cloud_logging, query_cloud_monitoring])
        )
        return {"service": req.service_name, "analysis": response.text}
    except Exception as e:
        return {"service": req.service_name, "analysis": "Mock Fallback RCA: Memory Pool Exhausted. Rollback advised."}
