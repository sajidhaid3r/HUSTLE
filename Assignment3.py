import streamlit as st
from google import genai
import os
from dotenv import load_dotenv



# ----------------------------
# Configure Gemini API
# ----------------------------
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Personality selection
personality = st.sidebar.selectbox(
    "Choose Personality",
    [
        "Helpful Assistant",
        "Funny Friend",
        "Strict Teacher",
        "Motivational Coach"
    ]
)

# Create model
model = ("gemini-2.5-flash")

# ----------------------------
# SESSION STATE (Memory Vault)
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🧠 Multiverse Chatbot")

# ----------------------------
# Display Previous Messages
# ----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ----------------------------
# Chat Input
# ----------------------------
if user_message := st.chat_input("Say something..."):

    # Save User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    # Display User Message
    with st.chat_message("user"):
        st.markdown(user_message)

    # Build Prompt
    prompt = f"""
    You are acting as a {personality}.

    User:
    {user_message}
    """

    # Generate Response
    response = client.models.generate_content(
        model=model,
        contents=prompt
    )


    # Save Assistant Response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response.text
        }
    )

    # Display Assistant Response
    with st.chat_message("assistant"):
        st.markdown(response.text)