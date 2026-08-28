```python
import streamlit as st
from langchain_groq import ChatGroq

# Streamlit page setup
st.set_page_config(
    page_title="Chatbot",
    page_icon="🤖",
    layout="centered",
)

st.title("💬 Generative AI Chatbot")

# Get Groq API key
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error("GROQ_API_KEY not found. Please add it in Streamlit Secrets.")
    st.stop()

# Initiate chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Show chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Initialize Groq LLM
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.0,
    api_key=api_key,
)

# Input box
user_prompt = st.chat_input("Ask Chatbot...")

if user_prompt:

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Save user message
    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    # Get response from Groq
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

    # Save assistant response
    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": assistant_response,
        }
    )

    # Show assistant response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
```
