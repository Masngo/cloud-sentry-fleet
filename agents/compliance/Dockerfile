FROM python:3.11-slim
WORKDIR /app
COPY agents/compliance/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY agents/compliance/ ./agents/compliance
EXPOSE 8003
CMD ["uvicorn", "agents.compliance.agent:app", "--host", "0.0.0.0", "--port", "8003"]
