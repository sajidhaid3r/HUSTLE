import operator

import streamlit as st

st.title("CALCULATOR")

num1 = st.number_input("Enter first number:")
num2 = st.number_input("Enter second number:")
operator = st.selectbox("Select an operator", ["+", "-", "*", "/"])

if st.button("Calculate"):
    if operator == "+":
        result = num1 + num2
    elif operator == "-":
        result = num1 - num2
    elif operator == "*":
        result = num1 * num2
    elif operator == "/":
        if num2 != 0:
            result = num1 / num2
        else:
            result = "Error: Division by zero"
    st.write(f"Result: {result}")