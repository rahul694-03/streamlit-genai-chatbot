```python
import streamlit as st
from langchain_groq import ChatGroq

# -----------------------------
# Streamlit Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Generative AI Chatbot",
    page_icon="🤖",
    layout="centered",
)

st.title("💬 Generative AI Chatbot")

# -----------------------------
# Get Groq API Key
# -----------------------------
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error("GROQ_API_KEY not found. Please add it in Streamlit Secrets.")
    st.stop()

# -----------------------------
# Initialize Chat History
# -----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------------
# Display Previous Messages
# -----------------------------
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# Initialize Groq LLM
# -----------------------------
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.0,
    api_key=api_key,
)

# -----------------------------
# Chat Input
# -----------------------------
user_prompt = st.chat_input("Ask Chatbot...")

if user_prompt:

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Save user message
    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    # -----------------------------
    # Get Response From Groq
    # -----------------------------
    try:
        response = llm.invoke(
            [
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },
                *st.session_state.chat_history,
            ]
        )

        assistant_response = response.content

    except Exception as e:
        st.error(f"Groq API Error: {e}")
        st.stop()

    # -----------------------------
    # Save Assistant Response
    # -----------------------------
    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": assistant_response,
        }
    )

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
```
