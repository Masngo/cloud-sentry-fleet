# 🛡️ CloudSentry AI Fleet

**Autonomous Zero-Trust Multi-Agent SRE System & Infrastructure Remediation Control Plane**  
*Built with Gemini 3.5 Flash, Google Agent Development Kit (ADK), Streamlit, and Google Cloud Run.*

---

## 🌟 Overview

**CloudSentry AI Fleet** is an autonomous SRE mitigation system designed to detect, sanitize, analyze, and remediate cloud infrastructure threats in real time. Built to solve critical operational risks in distributed microservice architectures, CloudSentry intercepts log streams, strips sensitive PII/credentials prior to AI analysis, and auto-generates executable remediation code patches.

---

## ✨ Key Features

* **🔍 Ingress Guard Agent**: Parses live log streams, APM traces, and telemetry payloads.
* **🛡️ Model Armor PII Redactor**: Real-time regex and guardrail engine stripping passwords, JWT tokens, and sensitive headers before payload transmission.
* **⚖️ Zero-Trust Policy Agent**: Harnesses **Gemini 3.5 Flash** for rapid Root Cause Analysis (RCA) and threat evaluation.
* **🔧 Remediation Sandbox**: Dynamic generation of ready-to-deploy **Terraform (HCL)** firewall rules and **`gcloud` CLI** isolation commands.
* **📊 Real-Time SRE Analytics**: Live dashboards visualizing resolution latency, threat vector breakdowns, and cumulative neutralizations.
* **📜 Audit & Compliance Engine**: Complete structured JSON execution logging for security post-mortems.

---

## 🕸️ System Architecture & Multi-Agent Topology

CloudSentry operates via a multi-agent orchestration mesh:
[ Telemetry Ingress ] ──> 🔍 Ingress Guard Agent
│
▼
🛡️ Model Armor PII Redactor
│
▼
⚖️ Zero-Trust Policy Agent (Gemini 3.5 Flash)
│
▼
🔧 Remediation Sandbox (Terraform / gcloud)
---

## 🚀 Quick Start (Local Setup)

### 1. Clone & Setup Environment
```bash
git clone [https://github.com/Masngo/cloud-sentry-fleet.git](https://github.com/Masngo/cloud-sentry-fleet.git)
cd cloud-sentry-fleet
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
2. Configure Local Secrets
Create .streamlit/secrets.toml:

Ini, TOML
GEMINI_API_KEY = "your-gemini-api-key-here"
3. Run Streamlit Application
Bash
streamlit run app.py
☁️ Deploy to Google Cloud Run
1. Store API Key in Google Secret Manager
Bash
gcloud secrets create GEMINI_API_KEY --replication-policy="automatic"
echo -n "your-gemini-api-key" | gcloud secrets versions add GEMINI_API_KEY --data-file=-
2. Deploy Container
Bash
gcloud run deploy cloud-sentry-fleet \
    --source . \
    --region us-central1 \
    --allow-unauthenticated \
    --set-secrets="GEMINI_API_KEY=GEMINI_API_KEY:latest"
🛠️ Tech Stack
Frontend / Dashboard: Streamlit, Pandas, NumPy, Graphviz

AI Engine: Gemini 3.5 Flash, Google Agent Development Kit (ADK)

Infrastructure: Google Cloud Run, Google Secret Manager

Remediation: Terraform HCL, Google Cloud SDK (gcloud)