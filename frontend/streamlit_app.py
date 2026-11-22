
import streamlit as st
import requests
from pathlib import Path

st.set_page_config(
    page_title="Banking AI Assistant",
    page_icon="🏦",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"

# Load CSS
css_path = Path(__file__).with_name("style.css")

if css_path.exists():
    st.markdown(
        f"<style>{css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True
    )

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# Sidebar
with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            <div class="brand-icon">🏦</div>
            <div>
                <h2>Banking AI</h2>
                <p>MULTI-AGENT ASSISTANT</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Backend Status")

    try:
        health = requests.get(
            f"{API_URL}/health",
            timeout=5
        )

        if health.status_code == 200:
            st.success("Backend Connected")
        else:
            st.error("Backend Error")

    except requests.exceptions.RequestException:
        st.error("Backend Offline")

    st.divider()

    st.subheader("Upload Banking Documents")

    uploaded_files = st.file_uploader(
        "Upload PDF, TXT or DOCX",
        type=["pdf", "txt", "docx"],
        accept_multiple_files=True
    )

    if st.button("Upload to AWS S3", use_container_width=True):

        if not uploaded_files:
            st.warning("Please select a document.")
        else:

            for uploaded_file in uploaded_files:

                try:
                    response = requests.post(
                        f"{API_URL}/upload",
                        files={
                            "file": (
                                uploaded_file.name,
                                uploaded_file.getvalue(),
                                uploaded_file.type
                            )
                        },
                        timeout=120
                    )

                    if response.status_code == 200:

                        st.success(
                            f"{uploaded_file.name} uploaded successfully."
                        )

                        st.session_state.uploaded_files.append(
                            uploaded_file.name
                        )

                    else:
                        st.error(
                            f"{uploaded_file.name}: "
                            f"{response.text}"
                        )

                except requests.exceptions.RequestException as error:
                    st.error(f"Upload error: {error}")

    if st.session_state.uploaded_files:
        st.caption("Uploaded documents")

        for name in dict.fromkeys(
            st.session_state.uploaded_files
        ):
            st.write(f"📄 {name}")

    st.divider()

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        '<div class="user-profile">🤖 Banking AI Assistant</div>',
        unsafe_allow_html=True
    )


# Main interface
st.markdown(
    """
    <div class="hero">
        <div class="hero-logo">🏦</div>
        <h1>Banking <span>Multi-Agent AI</span></h1>
        <p>
            Intelligent banking assistance powered by
            AWS Bedrock, LangGraph and Amazon S3.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Example prompts
st.markdown("### What can I help you with?")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("🏦 Account Services")
    st.caption("KYC, savings and account opening")

with col2:
    st.info("🛡️ Fraud Detection")
    st.caption("Suspicious transactions and fraud")

with col3:
    st.info("💳 Loan & Payments")
    st.caption("EMI, UPI, NEFT and RTGS")


# Chat history
st.divider()

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        if message.get("agent"):
            st.caption(f"Handled by: {message['agent']}")

        st.markdown(message["content"])


# Chat input
question = st.chat_input(
    "Ask your banking question..."
)

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner(
            "Supervisor is routing your request to the correct agent..."
        ):

            try:

                response = requests.post(
                    f"{API_URL}/chat",
                    json={"question": question},
                    timeout=180
                )

                response.raise_for_status()

                result = response.json()

                answer = result["answer"]
                agent = result["agent"]

                st.caption(f"Active Agent: {agent}")

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "agent": agent
                })

            except requests.exceptions.Timeout:

                st.error(
                    "Request timed out. Please try again."
                )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to FastAPI. "
                    "Please start your backend."
                )

            except requests.exceptions.HTTPError as error:

                st.error(
                    f"Backend error: {error}"
                )

            except Exception as error:

                st.error(
                    f"Unexpected error: {error}"
                )
