import streamlit as st

st.title("MY FIRST AI UI")
st.write("This is a basic UI Built with streamlit")

#TAKE USER INPUT

user_message=st.text_input("What is your name?")
#print(user_message)
if st.button("BUTTON TO SUBMIT"):
    st.write(user_message)
