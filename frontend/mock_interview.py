import streamlit as st
import requests

st.set_page_config(
    page_title="Mock Interview",
    layout="centered"
)

st.title("AI Mock Interview")

if "access_token" not in st.session_state:
    st.error("Please login first")
    st.stop()

st.success(f"Welcome {st.session_state['username']}")

role = st.selectbox(
    "Select Role",
    [
        "Software Engineer",
        "Machine Learning Engineer",
        "Data Scientist",
        "HR Interview"
    ]
)

difficulty = st.selectbox(
    "Select Difficulty",
    [
        "Easy",
        "Medium",
        "Hard"
    ]
)

topic = st.text_input("Enter Topic")

if st.button("Generate Question"):

    headers = {
        "Authorization":
        f"Bearer {st.session_state['access_token']}"
    }

    payload = {
        "role": role,
        "difficulty": difficulty,
        "topic": topic
    }

    response = requests.post(
        "http://127.0.0.1:5000/generate-question",
        json=payload,
        headers=headers
    )

    data = response.json()

    if response.status_code == 200:

        st.session_state["session_id"] = data["session_id"]

        st.session_state["question"] = data["question"]

        st.subheader("Generated Question")

        st.write(data["question"])

    else:
        st.error("Failed to generate question")