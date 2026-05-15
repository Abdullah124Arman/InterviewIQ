import streamlit as st
import requests

st.set_page_config(
    page_title="InterviewIQ Signup",
    layout="centered"
)

st.title("InterviewIQ")
st.subheader("Create Account")

username = st.text_input("Username")

email = st.text_input("Email")

password = st.text_input(
    "Password",
    type="password"
)

if st.button("Signup"):

    payload = {
        "username": username,
        "email": email,
        "password": password
    }

    response = requests.post(
        "http://127.0.0.1:5000/signup",
        json=payload
    )

    data = response.json()

    if response.status_code == 201:
        st.success(data["message"])

    else:
        st.error(data["message"])