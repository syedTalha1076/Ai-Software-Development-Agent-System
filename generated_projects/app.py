import streamlit as st

# 1. Core Calculator Logic Implementation
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Division by zero!"
    return a / b

# 2. Streamlit User Interface (UI) Development
st.title("Simple Calculator")

# Initialize session state for inputs and result if not already present
if "num1" not in st.session_state:
    st.session_state.num1 = 0.0
if "num2" not in st.session_state:
    st.session_state.num2 = 0.0
if "result" not in st.session_state:
    st.session_state.result = ""

# Input widgets
col1, col2 = st.columns(2)
with col1:
    st.session_state.num1 = st.number_input("First Number", value=st.session_state.num1, key="input_num1")
with col2:
    st.session_state.num2 = st.number_input("Second Number", value=st.session_state.num2, key="input_num2")

# Operation buttons
st.write("### Choose an operation:")
col_ops = st.columns(4)

with col_ops[0]:
    if st.button("+"):
        st.session_state.result = add(st.session_state.num1, st.session_state.num2)
with col_ops[1]:
    if st.button("-"):
        st.session_state.result = subtract(st.session_state.num1, st.session_state.num2)
with col_ops[2]:
    if st.button("*"):
        st.session_state.result = multiply(st.session_state.num1, st.session_state.num2)
with col_ops[3]:
    if st.button("/"):
        st.session_state.result = divide(st.session_state.num1, st.session_state.num2)

# Clear button
if st.button("Clear"):
    st.session_state.num1 = 0.0
    st.session_state.num2 = 0.0
    st.session_state.result = ""
    # st.rerun() # Not strictly necessary if keys are managed well, but can force a refresh

# Result display
st.write("---")
st.write("### Result:")
st.write(f"**{st.session_state.result}**")
