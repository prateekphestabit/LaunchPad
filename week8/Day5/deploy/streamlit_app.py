import streamlit as st
import requests


# ─────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────
API_URL = "http://localhost:8000"

# ─────────────────────────────────────────
# PAGE SETUP
# ─────────────────────────────────────────
st.set_page_config(
    page_title="TinyLlama Chat",
    page_icon="🦙",
    layout="wide",
)

st.title("🦙 TinyLlama Local LLM")
st.caption("Powered by GGUF Q4 + llama.cpp + FastAPI")

# ─────────────────────────────────────────
# SIDEBAR — Settings
# ─────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")

    mode = st.radio(
        "Mode",
        ["💬 Chat", "⚡ Generate"],
        help="Chat keeps conversation history. Generate is single prompt."
    )

    st.divider()

    temperature = st.slider(
        "Temperature",
        min_value=0.1, max_value=1.5,
        value=0.7, step=0.05,
        help="Higher = more creative. Lower = more focused."
    )

    max_tokens = st.slider(
        "Max Tokens",
        min_value=50, max_value=512,
        value=200, step=50,
        help="Maximum tokens to generate per response."
    )

    top_p = st.slider(
        "Top P",
        min_value=0.1, max_value=1.0,
        value=0.95, step=0.05,
    )

    top_k = st.slider(
        "Top K",
        min_value=1, max_value=100,
        value=40, step=1,
    )

    streaming = st.toggle("🌊 Streaming", value=False)

    st.divider()

    # Health check
    st.subheader("🔌 API Status")
    if st.button("Check Connection"):
        try:
            res = requests.get(f"{API_URL}/health", timeout=3)
            if res.status_code == 200:
                st.success("API is running ✅")
            else:
                st.error("API returned error ❌")
        except:
            st.error("Cannot reach API ❌\nMake sure server is running.")

    st.divider()
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ─────────────────────────────────────────
# INIT CHAT HISTORY
# ─────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ─────────────────────────────────────────
# CHAT MODE
# ─────────────────────────────────────────
if mode == "💬 Chat":

    st.subheader("💬 Chat Mode")
    st.caption("Conversation history is maintained across turns.")

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Type your message..."):

        # Add user message to history
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Call /chat API
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    payload = {
                        "messages": st.session_state.messages,
                        "max_tokens": max_tokens,
                        "temperature": temperature,
                        "top_k": top_k,
                        "top_p": top_p,
                        "stream": False,
                    }

                    res = requests.post(
                        f"{API_URL}/chat",
                        json=payload,
                        timeout=120,
                    )

                    if res.status_code == 200:
                        data = res.json()
                        response_text = data["response"]

                        st.markdown(response_text)

                        # Show stats
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Tokens", data["tokens_generated"])
                        col2.metric("Time", f"{data['time_taken_sec']}s")
                        col3.metric("Tok/sec", data["tokens_per_sec"])

                        # Add assistant response to history
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response_text,
                        })

                    else:
                        st.error(f"API Error: {res.status_code}")

                except requests.exceptions.Timeout:
                    st.error("Request timed out. Try reducing Max Tokens.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# ─────────────────────────────────────────
# GENERATE MODE
# ─────────────────────────────────────────
elif mode == "⚡ Generate":

    st.subheader("⚡ Generate Mode")
    st.caption("Single prompt → single response. No history kept.")

    prompt = st.text_area(
        "Enter your prompt:",
        height=150,
        placeholder="What is compound interest?"
    )

    if st.button("🚀 Generate", type="primary"):
        if not prompt.strip():
            st.warning("Please enter a prompt.")
        else:
            with st.spinner("Generating..."):
                try:
                    payload = {
                        "prompt": prompt,
                        "max_tokens": max_tokens,
                        "temperature": temperature,
                        "top_k": top_k,
                        "top_p": top_p,
                        "stream": False,
                    }

                    res = requests.post(
                        f"{API_URL}/generate",
                        json=payload,
                        timeout=120,
                    )

                    if res.status_code == 200:
                        data = res.json()

                        st.divider()
                        st.subheader("Response")
                        st.markdown(data["response"])

                        st.divider()
                        st.subheader("Stats")
                        col1, col2, col3, col4 = st.columns(4)
                        col1.metric("Request ID", data["request_id"])
                        col2.metric("Tokens Generated", data["tokens_generated"])
                        col3.metric("Time Taken", f"{data['time_taken_sec']}s")
                        col4.metric("Tokens/sec", data["tokens_per_sec"])

                    else:
                        st.error(f"API Error {res.status_code}: {res.text}")

                except requests.exceptions.Timeout:
                    st.error("Request timed out. Try reducing Max Tokens.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")