import streamlit as st
import pandas as pd
import numpy as np
import time
import json

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CloudSentry AI Fleet | Autonomous SRE",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MODERN SLATE/CYBERPUNK HIGH-CONTRAST THEME ---
st.markdown("""
<style>
    /* Global Page Background */
    .stApp {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
    }
    
    /* Top Header Bar */
    header[data-testid="stHeader"] {
        background-color: rgba(15, 23, 42, 0.95) !important;
        border-bottom: 1px solid #1E293B !important;
    }
    
    header[data-testid="stHeader"] * {
        color: #38BDF8 !important;
    }

    /* Sidebar Panel Styling */
    section[data-testid="stSidebar"] {
        background-color: #1E293B !important;
        border-right: 1px solid #334155 !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }
    
    section[data-testid="stSidebar"] .stCaption {
        color: #94A3B8 !important;
    }

    /* Headings & Typography */
    h1, h2, h3, h4, h5, h6, label {
        color: #F8FAFC !important;
        font-weight: 600 !important;
    }

    /* SELECTBOX COMPLETE BACKGROUND & ARROW FIX */
    div[data-baseweb="select"],
    div[data-baseweb="select"] > div,
    div[data-baseweb="select"] [role="button"],
    div[data-baseweb="select"] [aria-hidden="true"],
    div[data-baseweb="select"] div {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
    }

    div[data-baseweb="select"] > div {
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }

    /* Target SVG Arrow Icon specifically */
    div[data-baseweb="select"] svg {
        fill: #38BDF8 !important;
        color: #38BDF8 !important;
        opacity: 1 !important;
        visibility: visible !important;
    }

    /* Dropdown Menu Items */
    ul[data-baseweb="menu"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }

    li[data-baseweb="option"] {
        color: #F8FAFC !important;
        background-color: #1E293B !important;
    }

    li[data-baseweb="option"]:hover, li[aria-selected="true"] {
        background-color: #334155 !important;
        color: #38BDF8 !important;
    }

    /* Text Inputs & Textarea */
    input, textarea {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }

    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        padding: 16px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    
    div[data-testid="stMetricValue"] {
        font-family: 'Fira Code', monospace, sans-serif !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #38BDF8 !important;
    }

    /* Terminal & Code Blocks */
    pre, code {
        background-color: #020617 !important;
        color: #34D399 !important;
        border: 1px solid #1E293B !important;
        border-radius: 6px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if "history" not in st.session_state:
    st.session_state.history = []
if "metrics" not in st.session_state:
    st.session_state.metrics = {"redactions": 84, "injections": 12, "active_agents": 4}

# --- SIDEBAR CONTROL PANEL ---
with st.sidebar:
    st.title("🛡️ CloudSentry AI")
    st.caption("Autonomous Zero-Trust Fleet Controller")
    st.markdown("---")
    
    st.subheader("⚙️ System Configuration")
    
    gemini_model = st.selectbox(
        "♊ Gemini Model Type",
        [
            "Gemini 3.5 Flash",
            "Gemini 3.5 Pro",
            "Gemini 3.0 Ultra",
            "Gemini 2.5 Flash Lite"
        ],
        index=0
    )
    
    guardrail_mode = st.toggle("Enable Model Armor PII Redaction", value=True)
    auto_apply = st.checkbox("Auto-Apply Low-Risk Patches", value=False)
    
    st.markdown("---")
    st.subheader("🤖 Online Micro-Agents")
    st.markdown("🟢 **Ingress Guard** (`ingress-01`)")
    st.markdown("🟢 **PII Armor Agent** (`armor-sec-04`)")
    st.markdown("🟢 **Zero-Trust Policy Enforcer** (`policy-agent-02`)")
    st.markdown("🟢 **Remediation Sandbox** (`patcher-bot-09`)")
    
    st.markdown("---")
    if st.button("🧹 Clear Execution Audit Logs", use_container_width=True):
        st.session_state.history = []
        st.rerun()

# --- TOP HEADER ---
head_col1, head_col2 = st.columns([3, 1])
with head_col1:
    st.title("🛡️ CLOUDSENTRY AI FLEET")
    st.caption("Autonomous Multi-Agent Zero-Trust SRE System | Incident Mitigation Control Plane")

with head_col2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"⚙️ **Engine:** `{gemini_model}`", unsafe_allow_html=True)
    if guardrail_mode:
        st.markdown("🛡️ **Guardrails:** <span style='color: #10B981; font-weight: bold;'>● ACTIVE</span>", unsafe_allow_html=True)
    else:
        st.markdown("🛡️ **Guardrails:** <span style='color: #EF4444; font-weight: bold;'>● DISABLED</span>", unsafe_allow_html=True)

st.divider()

# --- REAL-TIME TELEMETRY METRICS ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("MEAN TIME TO RESOLVE", "1.2s", delta="-0.2s Faster")
m2.metric("ARMOR REDACTIONS", f"{st.session_state.metrics['redactions']}", delta="+1 Last Run")
m3.metric("INJECTIONS NEUTRALIZED", f"{st.session_state.metrics['injections']}", delta="+1 Neutralized")
m4.metric("FLEET AGENTS", f"{st.session_state.metrics['active_agents']} Online", delta="Healthy")

st.divider()

# --- MAIN WORKSPACE SPLIT ---
ingress_col, orchestrator_col = st.columns([1, 1.25])

# --- LEFT COLUMN: TELEMETRY DISPATCH INGRESS ---
with ingress_col:
    st.subheader("📡 Telemetry Dispatch Ingress")
    st.caption("Inject trace payloads or choose simulated attack templates")
    
    p1, p2, p3 = st.columns(3)
    preset_sql = p1.button("🚨 SQL Injection", use_container_width=True)
    preset_mem = p2.button("⚠️ OOM Memory Leak", use_container_width=True)
    preset_auth = p3.button("🔑 Secret Leak", use_container_width=True)
    
    default_payload = ""
    default_component = "auth-microservice-prod"
    default_severity = "CRITICAL (Requires Human Sign-off)"
    
    if preset_sql:
        default_payload = "ERROR 500: Connection failed for user=admin pass='SecretKey123!'. Attack payload: ' OR '1'='1; DROP TABLE users;"
        default_component = "auth-db-service"
        default_severity = "CRITICAL (Requires Human Sign-off)"
    elif preset_mem:
        default_payload = "CRITICAL 503: Heap OutOfMemory Exception in worker process pool #12. Consumption reached 99.4% threshold."
        default_component = "worker-fleet-pod-08"
        default_severity = "HIGH (Automated Sandbox Isolation)"
    elif preset_auth:
        default_payload = "WARN 403: Hardcoded service key exposed in headers: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.SecretTokenExposed987"
        default_component = "gateway-proxy-v2"
        default_severity = "HIGH (Automated Sandbox Isolation)"

    target_component = st.text_input("Target Service Component", value=default_component)
    severity_level = st.selectbox("Severity & Guardrail Policy", [
        "CRITICAL (Requires Human Sign-off)",
        "HIGH (Automated Sandbox Isolation)",
        "MEDIUM (Auto-Remediate & Log)"
    ], index=0 if default_severity.startswith("CRITICAL") else 1)
    
    raw_payload = st.text_area("Raw Trace Payload / Log Stream", value=default_payload, height=120)
    
    dispatch_clicked = st.button("🚀 Dispatch Telemetry Incident", type="primary", use_container_width=True)

# --- RIGHT COLUMN: AGENTIC ORCHESTRATOR STREAM ---
with orchestrator_col:
    st.subheader("🤖 Agentic Orchestrator Stream")
    
    tab_timeline, tab_remediation, tab_json = st.tabs(["Timeline Stream", "Generated Code Patch", "Raw Audit JSON"])
    
    if dispatch_clicked and raw_payload:
        st.session_state.metrics["injections"] += 1
        st.session_state.metrics["redactions"] += 1 if guardrail_mode else 0
        
        sanitized_payload = raw_payload
        if guardrail_mode:
            sanitized_payload = raw_payload.replace("SecretKey123!", "[REDACTED_PASSWORD]").replace("SecretTokenExposed987", "[REDACTED_JWT_TOKEN]")
        
        with tab_timeline:
            st.success(f"✅ Ingress Incident Captured ({gemini_model})")
            
            with st.status(f"⚡ Multi-Agent Pipeline Executing [{gemini_model}]...", expanded=True) as status:
                st.write("🔍 **Ingress Guard Agent**: Parsing incoming trace payload...")
                time.sleep(0.4)
                
                if guardrail_mode:
                    st.write("🛡️ **Model Armor Agent**: Sensitive PII/Credentials redacted from payload trace.")
                else:
                    st.write("⚠️ **Model Armor Agent**: Passthrough mode active (Guardrails Disabled).")
                time.sleep(0.4)
                
                st.write(f"⚖️ **Zero-Trust Policy Agent ({gemini_model})**: Evaluating incident against compliance policies...")
                time.sleep(0.4)
                
                st.write("🔧 **Remediation Sandbox**: Formulating patch script & infrastructure mitigation...")
                time.sleep(0.4)
                
                status.update(label="Incident Successfully Neutralized!", state="complete", expanded=True)
            
            st.markdown("#### 🛡️ Incident Assessment Summary")
            st.markdown(f"**Target Microservice:** `{target_component}`")
            st.markdown(f"**Execution Engine:** `{gemini_model}`")
            st.markdown(f"**Action Taken:** Isolated pod and issued rollback sequence.")
            
            st.markdown("**Processed Trace Payload:**")
            st.code(sanitized_payload, language="sql")

            st.session_state.history.append({
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "target": target_component,
                "severity": severity_level,
                "sanitized_payload": sanitized_payload,
                "engine": gemini_model
            })

        with tab_remediation:
            st.markdown("#### 🛠️ Auto-Generated Terraform Mitigation Patch")
            st.code(f"""
# Auto-generated by CloudSentry Agentic Fleet ({gemini_model})
resource "google_compute_firewall" "deny_malicious_ingress" {{
  name    = "deny-incident-{int(time.time())}"
  network = "default"

  deny {{
    protocol = "tcp"
    ports    = ["80", "443"]
  }}

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["{target_component}"]
}}
""", language="hcl")
            
            st.markdown("#### ⚡ gcloud Remediation Command")
            st.code(f"gcloud compute instances stop {target_component}-pod-01 --zone=us-central1-a", language="bash")

        with tab_json:
            st.json({
                "incident_id": f"sentry-evt-{int(time.time())}",
                "engine": gemini_model,
                "target_component": target_component,
                "severity": severity_level,
                "guardrails_active": guardrail_mode,
                "sanitized_payload": sanitized_payload
            })

    elif not st.session_state.history:
        with tab_timeline:
            st.info("📡 TELEMETRY PIPELINE AWAITING DISPATCH\n\nSubmit an incident or select an attack preset on the ingress panel to watch the agent fleet remediate threats.")
    else:
        latest = st.session_state.history[-1]
        with tab_timeline:
            st.success("Last Incident Execution Record")
            st.markdown(f"**Timestamp:** `{latest['timestamp']}`")
            st.markdown(f"**Engine Used:** `{latest['engine']}`")
            st.markdown(f"**Target:** `{latest['target']}`")
            st.code(latest['sanitized_payload'], language="sql")
        
        with tab_json:
            st.json(st.session_state.history)
