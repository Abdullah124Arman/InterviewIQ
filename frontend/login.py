import streamlit as st
import requests

st.set_page_config(
    page_title="InterviewIQ Login",
    layout="centered"
)

st.title("InterviewIQ")
st.subheader("Login")

email = st.text_input("Email")

password = st.text_input(
    "Password",
    type="password"
)

if st.button("Login"):

    payload = {
        "email": email,
        "password": password
    }

    response = requests.post(
        "http://127.0.0.1:5000/login",
        json=payload
    )

    data = response.json()

    if response.status_code == 200:

        st.session_state["access_token"] = data["access_token"]

        st.session_state["username"] = data["username"]

        st.success("Login successful")

        st.write(f"Welcome {data['username']}")

    else:
        st.error(data["message"])