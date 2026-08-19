FROM python:3.11-slim
WORKDIR /app
COPY agents/remediation/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY agents/remediation/ ./agents/remediation
COPY shared/ ./shared
EXPOSE 8002
CMD ["uvicorn", "agents.remediation.agent:app", "--host", "0.0.0.0", "--port", "8002"]
