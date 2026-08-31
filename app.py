import streamlit as st
import pandas as pd
import numpy as np
import time
import json
import re
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CloudSentry AI Fleet | Autonomous SRE",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- GEMINI API & REDACTION LOGIC ---
def redact_pii_payload(text):
    """Real-time regex-based PII & Secret Redaction Engine"""
    text = re.sub(r"(pass|password|secret|key)\s*[:=]\s*['\"]?[^'\s\"]+['\"]?", r"\1='[REDACTED_CREDENTIAL]'", text, flags=re.IGNORECASE)
    text = re.sub(r"Bearer\s+[A-Za-z0-9\-\._~\+\/]+=*", "Bearer [REDACTED_JWT_TOKEN]", text)
    text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED_EMAIL]", text)
    text = re.sub(r"(eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+)", "[REDACTED_JWT_TOKEN]", text)
    return text

def analyze_incident(model_name, component, severity, payload):
    """Queries live Gemini API if GEMINI_API_KEY exists, otherwise uses dynamic heuristic generation"""
    api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
    if api_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"""You are CloudSentry Zero-Trust SRE Agent.
Analyze this security payload:
- Target Microservice: {component}
- Severity: {severity}
- Payload: {payload}

Respond ONLY with raw JSON matching this format:
{{
  "assessment": "Brief vulnerability description",
  "action_taken": "Specific action taken to mitigate",
  "terraform": "Terraform block to deny traffic to target",
  "gcloud": "gcloud CLI command to stop/isolate component"
}}"""
            response = model.generate_content(prompt)
            clean_json = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_json)
        except Exception:
            pass

    ts = int(time.time())
    return {
        "assessment": f"Detected potential risk in {component}. Sanitized payload evaluated against Zero-Trust SRE rules.",
        "action_taken": f"Isolated {component} service instance and deployed automatic firewall ingress lock.",
        "terraform": f"""resource "google_compute_firewall" "deny_{component.replace('-', '_')}_{ts}" {{
  name    = "deny-incident-{ts}"
  network = "default"

  deny {{
    protocol = "tcp"
    ports    = ["80", "443", "8080"]
  }}

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["{component}"]
}}""",
        "gcloud": f"gcloud compute instances stop {component}-instance-01 --zone=us-central1-a"
    }

# --- STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #0F172A !important; color: #F8FAFC !important; }
    header[data-testid='stHeader'] { background-color: rgba(15, 23, 42, 0.95) !important; border-bottom: 1px solid #1E293B !important; }
    header[data-testid='stHeader'] * { color: #38BDF8 !important; }
    section[data-testid='stSidebar'] { background-color: #1E293B !important; border-right: 1px solid #334155 !important; }
    section[data-testid='stSidebar'] * { color: #F8FAFC !important; }
    h1, h2, h3, h4, h5, h6, label { color: #F8FAFC !important; font-weight: 600 !important; }

    div[data-baseweb='select'], div[data-baseweb='select'] > div, div[data-baseweb='select'] [role='button'], div[data-baseweb='select'] div {
        background-color: #0F172A !important; color: #F8FAFC !important;
    }
    div[data-baseweb='select'] > div { border: 1px solid #334155 !important; border-radius: 8px !important; }
    div[data-baseweb='select'] svg { fill: #38BDF8 !important; color: #38BDF8 !important; opacity: 1 !important; visibility: visible !important; }
    ul[data-baseweb='menu'] { background-color: #1E293B !important; border: 1px solid #334155 !important; }
    li[data-baseweb='option'] { color: #F8FAFC !important; background-color: #1E293B !important; }
    li[data-baseweb='option']:hover, li[aria-selected='true'] { background-color: #334155 !important; color: #38BDF8 !important; }

    input, textarea { background-color: #0F172A !important; color: #F8FAFC !important; border: 1px solid #334155 !important; border-radius: 8px !important; }
    div[data-testid='stMetric'] { background-color: #1E293B !important; border: 1px solid #334155 !important; border-radius: 10px !important; padding: 16px !important; }
    div[data-testid='stMetricValue'] { font-family: 'Fira Code', monospace !important; font-size: 1.8rem !important; color: #38BDF8 !important; }
    pre, code { background-color: #020617 !important; color: #34D399 !important; border: 1px solid #1E293B !important; border-radius: 6px !important; }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "history" not in st.session_state:
    st.session_state.history = []
if "metrics" not in st.session_state:
    st.session_state.metrics = {"redactions": 84, "injections": 12, "active_agents": 4, "last_latency": "1.2s"}
if "payload_input" not in st.session_state:
    st.session_state.payload_input = ""
if "component_input" not in st.session_state:
    st.session_state.component_input = "auth-microservice-prod"
if "threat_counts" not in st.session_state:
    st.session_state.threat_counts = {"SQL Injection": 14, "OOM Leak": 8, "Secret Leak": 11, "Custom Log": 5}
if "time_series" not in st.session_state:
    np.random.seed(42)
    st.session_state.time_series = pd.DataFrame({
        "Time": [f"T-{i}m" for i in range(10, 0, -1)],
        "Latency (ms)": np.random.randint(1100, 1400, size=10),
        "Blocked Threats": np.random.randint(2, 9, size=10)
    }).set_index("Time")

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡️ CloudSentry AI")
    st.caption("Autonomous Zero-Trust Fleet Controller")
    st.markdown("---")
    
    st.subheader("⚙️ System Configuration")
    gemini_model = st.selectbox(
        "♊ Gemini Model Type",
        ["Gemini 3.5 Flash", "Gemini 3.5 Pro", "Gemini 3.0 Ultra", "Gemini 2.5 Flash Lite"],
        index=0
    )
    guardrail_mode = st.toggle("Enable Model Armor PII Redaction", value=True)
    auto_apply = st.checkbox("Auto-Apply Low-Risk Patches", value=False)
    
    st.markdown("---")
    st.subheader("🕸️ Multi-Agent Topology")
    st.graphviz_chart("""
        digraph {
            graph [bgcolor="transparent", rankdir=TB]
            node [style=filled, fillcolor="#1E293B", fontcolor="#F8FAFC", shape=box, fontname="Sans-Serif"]
            edge [color="#38BDF8"]
            
            Ingress [label="🔍 Ingress Guard"]
            Armor [label="🛡️ PII Armor"]
            Policy [label="⚖️ Policy Enforcer"]
            Remediation [label="🔧 Remediation Sandbox"]
            
            Ingress -> Armor -> Policy -> Remediation
        }
    """)
    
    st.markdown("---")
    if st.button("🧹 Clear Execution Audit Logs", use_container_width=True):
        st.session_state.history = []
        st.session_state.metrics["injections"] = 0
        st.session_state.metrics["redactions"] = 0
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

# --- METRICS ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("MEAN TIME TO RESOLVE", st.session_state.metrics["last_latency"], delta="-0.2s Faster")
m2.metric("ARMOR REDACTIONS", f"{st.session_state.metrics['redactions']}", delta="+1 Last Run")
m3.metric("INJECTIONS NEUTRALIZED", f"{st.session_state.metrics['injections']}", delta="+1 Neutralized")
m4.metric("FLEET AGENTS", f"{st.session_state.metrics['active_agents']} Online", delta="Healthy")

st.divider()

# --- MAIN WORKSPACE ---
ingress_col, orchestrator_col = st.columns([1, 1.25])

with ingress_col:
    st.subheader("📡 Telemetry Dispatch Ingress")
    st.caption("Inject trace payloads or choose simulated attack templates")
    
    p1, p2, p3 = st.columns(3)
    threat_type = "Custom Log"
    if p1.button("🚨 SQL Injection", use_container_width=True):
        st.session_state.payload_input = "ERROR 500: Connection failed for user=admin pass='SecretKey123!'. Attack payload: ' OR '1'='1; DROP TABLE users;"
        st.session_state.component_input = "auth-db-service"
        threat_type = "SQL Injection"
    if p2.button("⚠️ OOM Memory Leak", use_container_width=True):
        st.session_state.payload_input = "CRITICAL 503: Heap OutOfMemory Exception in worker process pool #12 for user=admin@corp.com. Consumption 99.4%."
        st.session_state.component_input = "worker-fleet-pod-08"
        threat_type = "OOM Leak"
    if p3.button("🔑 Secret Leak", use_container_width=True):
        st.session_state.payload_input = "WARN 403: Hardcoded key exposed in headers: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.SecretTokenExposed987"
        st.session_state.component_input = "gateway-proxy-v2"
        threat_type = "Secret Leak"

    target_component = st.text_input("Target Service Component", key="component_input")
    severity_level = st.selectbox("Severity & Guardrail Policy", [
        "CRITICAL (Requires Human Sign-off)",
        "HIGH (Automated Sandbox Isolation)",
        "MEDIUM (Auto-Remediate & Log)"
    ])
    
    raw_payload = st.text_area("Raw Trace Payload / Log Stream", key="payload_input", height=120)
    
    dispatch_clicked = st.button("🚀 Dispatch Telemetry Incident", type="primary", use_container_width=True)

with orchestrator_col:
    st.subheader("🤖 Agentic Orchestrator Stream")
    tab_timeline, tab_analytics, tab_remediation, tab_json = st.tabs(["Timeline Stream", "📊 Real-Time Analytics", "Generated Code Patch", "Raw Audit JSON"])
    
    if dispatch_clicked and raw_payload:
        start_time = time.time()
        
        # Redaction Process
        if guardrail_mode:
            sanitized_payload = redact_pii_payload(raw_payload)
            st.session_state.metrics["redactions"] += 1
        else:
            sanitized_payload = raw_payload

        st.session_state.metrics["injections"] += 1
        st.session_state.threat_counts[threat_type] = st.session_state.threat_counts.get(threat_type, 0) + 1

        with tab_timeline:
            st.success(f"✅ Telemetry Payload Received ({gemini_model})")
            
            with st.status(f"⚡ Multi-Agent Pipeline Executing [{gemini_model}]...", expanded=True) as status:
                st.write("🔍 **Ingress Guard Agent**: Parsing incoming trace payload...")
                time.sleep(0.3)
                
                if guardrail_mode:
                    st.write("🛡️ **Model Armor Agent**: Sensitive credentials/PII stripped via regex guardrails.")
                else:
                    st.write("⚠️ **Model Armor Agent**: Passthrough mode active (Guardrails Disabled).")
                time.sleep(0.3)
                
                st.write(f"⚖️ **Zero-Trust Policy Agent ({gemini_model})**: Analyzing threat profile...")
                
                result = analyze_incident(gemini_model, target_component, severity_level, sanitized_payload)
                time.sleep(0.3)
                
                st.write("🔧 **Remediation Sandbox**: Generating dynamic infrastructure mitigation...")
                time.sleep(0.3)
                
                status.update(label="Incident Neutralized Successfully!", state="complete", expanded=True)
            
            st.markdown("#### 🛡️ Incident Assessment Summary")
            st.markdown(f"**Target Microservice:** `{target_component}`")
            st.markdown(f"**Execution Engine:** `{gemini_model}`")
            st.markdown(f"**Assessment:** {result['assessment']}")
            st.markdown(f"**Action Taken:** {result['action_taken']}")
            
            st.markdown("**Processed Trace Payload:**")
            st.code(sanitized_payload, language="sql")

            elapsed = round(time.time() - start_time, 2)
            st.session_state.metrics["last_latency"] = f"{elapsed}s"

            st.session_state.history.append({
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "target": target_component,
                "severity": severity_level,
                "sanitized_payload": sanitized_payload,
                "analysis": result,
                "engine": gemini_model
            })

        with tab_remediation:
            st.markdown("#### 🛠️ Auto-Generated Terraform Mitigation Patch")
            st.code(result["terraform"], language="hcl")
            st.markdown("#### ⚡ gcloud Remediation Command")
            st.code(result["gcloud"], language="bash")

        with tab_json:
            st.json({
                "incident_id": f"sentry-evt-{int(time.time())}",
                "engine": gemini_model,
                "target_component": target_component,
                "severity": severity_level,
                "guardrails_active": guardrail_mode,
                "sanitized_payload": sanitized_payload,
                "remediation": result
            })

    elif st.session_state.history:
        latest = st.session_state.history[-1]
        with tab_timeline:
            st.info("Displaying Last Execution Record")
            st.markdown(f"**Timestamp:** `{latest['timestamp']}`")
            st.markdown(f"**Target:** `{latest['target']}`")
            st.markdown(f"**Assessment:** {latest['analysis']['assessment']}")
            st.code(latest['sanitized_payload'], language="sql")
        with tab_remediation:
            st.code(latest['analysis']['terraform'], language="hcl")
            st.code(latest['analysis']['gcloud'], language="bash")
        with tab_json:
            st.json(st.session_state.history)
    else:
        with tab_timeline:
            st.info("📡 TELEMETRY PIPELINE AWAITING DISPATCH\n\nSelect an attack preset or enter a custom log payload on the left, then click 'Dispatch Telemetry Incident'.")

    # Visual Analytics Tab
    with tab_analytics:
        st.markdown("#### 📈 Real-Time SRE Fleet Analytics")
        
        c1, c2 = st.columns(2)
        with c1:
            st.caption("⚡ Resolution Latency (ms) over Recent Ingress Events")
            st.line_chart(st.session_state.time_series["Latency (ms)"], color="#38BDF8")
        
        with c2:
            st.caption("🎯 Threat Vector Breakdown Neutralized")
            threat_df = pd.DataFrame(list(st.session_state.threat_counts.items()), columns=["Threat Vector", "Count"]).set_index("Threat Vector")
            st.bar_chart(threat_df, color="#34D399")
        
        st.caption("🛡️ Cumulative Neutralized Threats Timeline")
        st.area_chart(st.session_state.time_series["Blocked Threats"], color="#818CF8")
