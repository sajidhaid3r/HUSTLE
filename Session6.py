import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
st.title("AI CHAT WITH HISTORY")

@st.cache_resource
def get_ai_client():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

client=get_ai_client()

if "messages" not in st.session_state:
    st.session_state.messages=[]

if "gemini_chat" not in st.session_state:
    st.session_state.gemini_chat=client.chats.create(model="gemini-2.5-flash")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if user_message:=st.chat_input("Say something"):

    with st.chat_message("user"):
        st.write(user_message)

    st.session_state.messages.append({"role":"user","content": user_message})

    with st.spinner("Thinking...."):
        response=st.session_state.gemini_chat.send_message(user_message)
    
    with st.chat_message("AI"):
        st.write(response.text)

    st.session_state.messages.append({"role":"AI","content":response.text})


#Create a download button to download the chat history
#USE A LOOP AND ITERATE OVER THE MESSAGES
    st.download_button(
        label="Download Chat History",
        data="\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages]),
        file_name="chat_history.txt",
        mime="text/plain"
    )

#CREATE THE CONTEXT WINDOW/ RATE LIMITER
