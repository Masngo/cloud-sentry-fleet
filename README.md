# CloudSentry AI Fleet
> Zero-Trust Multi-Agent Infrastructure Orchestrator & Autonomous Remediation Mesh built for the Google Cloud "All Things Agentic" Hackathon.

## System Architecture
CloudSentry operates as an asynchronous, multi-agent fleet on Google Cloud:
1. **Agent Gateway (`/gateway`)**: Ingests alerts, enforces token auth, and routes requests.
2. **Compliance Agent (`/agents/compliance`)**: Implements **Model Armor** for log sanitization.
3. **Diagnostic Agent (`/agents/diagnostic`)**: Leverages **Gemini 3.5 Flash** for RCA.
4. **Remediation Agent (`/agents/remediation`)**: Executes automated rollbacks.

## Spin-Up Instructions (Local Docker Setup)
1. Copy `.env.example` to `.env` and set your credentials.
2. Build and start local services using Docker Compose:
   `docker-compose up --build`
