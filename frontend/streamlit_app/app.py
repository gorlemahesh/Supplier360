import streamlit as st
import boto3, botocore, time, random

# ====== CONFIGURATION ======
REGION = "us-east-1"
AGENT_ID = "XZTBPTDN4C"              
AGENT_ALIAS_ID = "ROHEX5JVZ3"   
# =============================

client = boto3.client("bedrock-agent-runtime", region_name=REGION)

# ---------- BACKOFF ----------
def _backoff(attempt, base=0.6, factor=2.0, max_delay=10):
    return min(max_delay, base * (factor ** (attempt - 1))) * (0.5 + random.random()/2)

# ---------- CALL AGENT ----------
def ask_agent(message, session_id="supplier360-session", retries=5):
    attempt = 1

    while True:
        try:
            resp = client.invoke_agent(
                agentId=AGENT_ID,
                agentAliasId=AGENT_ALIAS_ID,
                sessionId=session_id,
                inputText=message,
                enableTrace=False,
            )

            text_parts = []
            stream = resp["completion"]

            for event in stream:
                if "chunk" in event:
                    text_parts.append(event["chunk"]["bytes"].decode("utf-8", errors="ignore"))

            return "".join(text_parts).strip()

        except botocore.exceptions.ClientError as e:
            msg = str(e)
            if any(x in msg for x in ["Throttling", "Too Many Requests", "Rate exceeded"]) and attempt < retries:
                time.sleep(_backoff(attempt))
                attempt += 1
                continue
            raise

# ---------- STREAMLIT UI ----------
st.set_page_config(
    page_title="Supplier360 Risk Assessment",
    page_icon="https://img.icons8.com/color/96/combo-chart--v1.png",
    layout="centered"
)

st.markdown(
    """
    <div style="display:flex; align-items:center; gap:12px; margin-top:10px;">
        <img src="https://img.icons8.com/color/96/combo-chart--v1.png" width="60">
        <h1 style="margin:0; padding:0;">Supplier360 Risk Assessment</h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center; color: #9ca3af;'>Run the full Supplier360 AI Risk Report.</p>",
    unsafe_allow_html=True
)

# Session
if "history" not in st.session_state:
    st.session_state.history = []
if "session_id" not in st.session_state:
    st.session_state.session_id = f"local-{int(time.time())}"

# Display history
for role, text in st.session_state.history:
    with st.chat_message(role):
        st.write(text)

# Input field
supplier = st.chat_input("Enter supplier name (e.g., Ford Motor Company)")

if supplier:
    st.session_state.history.append(("user", supplier))
    with st.chat_message("user"):
        st.write(supplier)

    # Build prompt for Supplier360 agent
    message = (
        f"Run Supplier360 risk analysis for supplier '{supplier}'. "
        f"Report type = 'full'. "
        f"Return the complete formatted supplier risk report."
    )

    with st.chat_message(" ", avatar=None):
        with st.spinner(f" Generating Supplier360 report for {supplier}…"):
            try:
                reply = ask_agent(message, st.session_state.session_id)
            except Exception as e:
                reply = f"⚠️ Error: {e}"
            reply = reply.replace("<REDACTED>", "")
            st.write(reply)

    st.session_state.history.append(("assistant", reply))

# Quick demo buttons
st.divider()
st.write("Quick suppliers:")
cols = st.columns(4, gap="medium")
examples = ["General Motors", "Toyota Motor Corporation", "Samsung Electronics", "DuPont de Nemours"]

for i, name in enumerate(examples):
    if cols[i].button(name, use_container_width=True):
        st.session_state.history.append(("user", name))
        with st.chat_message(" ", avatar=None):
            with st.spinner(f" Fetching Supplier360 report for {name}…"):
                try:
                    reply = ask_agent(
                        f"Run Supplier360 risk analysis for supplier '{name}'. Report type = 'full'. Return the formatted report.",
                        st.session_state.session_id
                    )
                except Exception as e:
                    reply = f"⚠️ Error: {e}"
            reply = reply.replace("<REDACTED>", "")
            st.write(reply)
        st.session_state.history.append(("assistant", reply))
