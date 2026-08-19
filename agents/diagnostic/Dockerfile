FROM python:3.11-slim
WORKDIR /app
COPY agents/diagnostic/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY agents/diagnostic/ ./agents/diagnostic
COPY shared/ ./shared
EXPOSE 8001
CMD ["uvicorn", "agents.diagnostic.agent:app", "--host", "0.0.0.0", "--port", "8001"]
