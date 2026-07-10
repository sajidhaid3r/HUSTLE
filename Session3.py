import streamlit as st

st.title("THE MULTIVERSE OF CHATBOTS")

personality=st.selectbox("Who do you want to talk to?",[
    "Virat Kohli","An angry Ravi Shastri","Haider","A crazy Ronaldo fan"
])

from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

user_message=st.text_input("What do you want to say to ")
if st.button("SEND"):
    if user_message:
        ai_instruction=f"You are acting as {personality}. Respond to the user message in a way that reflects the personality of {personality}. User message: {user_message}"
        with st.spinner("Connecting to the multiverse..."):
            response=client.models.generate_content(
                model="gemini-2.5-flash",
                contents=ai_instruction
            )
            st.success("Message received!")
            st.write(response.text)
    else:
        st.warning("Please enter a message first.")