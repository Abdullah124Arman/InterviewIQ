import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from PyPDF2 import PdfReader
from streamlit_mic_recorder import mic_recorder


st.set_page_config(page_title="InterviewIQ", layout="wide")

BACKEND_URL = "http://127.0.0.1:5000"

# =========================
# SESSION STATE
# =========================

if "token" not in st.session_state:
    st.session_state.token = None

if "username" not in st.session_state:
    st.session_state.username = None

if "page" not in st.session_state:
    st.session_state.page = "Login"
if "question" not in st.session_state:
     st.session_state.question = ""

if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""
if "transcribed_text" not in st.session_state:
    st.session_state.transcribed_text = ""

# =========================
# UI
# =========================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #030712;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("InterviewIQ")

# =========================
# SIDEBAR
# =========================
if st.session_state.token:

    st.sidebar.title("InterviewIQ")

    st.sidebar.markdown(
        f"### 👋 Hello, {st.session_state.username}"
    )

    st.sidebar.divider()

    if st.sidebar.button("Logout"):

        st.session_state.token = None
        st.session_state.username = None
        st.session_state.page = "Login"

        if "question" in st.session_state:
            del st.session_state["question"]

        if "session_id" in st.session_state:
            del st.session_state["session_id"]

        st.rerun()

    page = st.sidebar.radio(
        "InterviewIQ Menu",
        ["Dashboard", "Mock Interview", "Interview History"]
    )

else:

    st.sidebar.title("InterviewIQ")

    st.sidebar.markdown("### Welcome")

    st.sidebar.divider()

    if st.session_state.page == "Login":

        if st.sidebar.button("Go to Signup"):
            st.session_state.page = "Signup"
            st.rerun()

        page = "Login"

    else:

        if st.sidebar.button("Go to Login"):
            st.session_state.page = "Login"
            st.rerun()

        page = "Signup"

# =========================
# SIGNUP
# =========================

if page == "Signup":

    st.header("Create Account")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Signup"):

        if not username or not email or not password:

            st.warning("Please fill all fields")

        else:

            with st.spinner("Creating account..."):

                response = requests.post(
                    f"{BACKEND_URL}/signup",
                    json={
                        "username": username,
                        "email": email,
                        "password": password
                    }
                )

                data = response.json()

                if response.status_code == 201:

                    st.success(data["message"])

                    st.session_state.page = "Login"

                    st.rerun()

                else:
                    st.error(data["message"])

# =========================
# LOGIN
# =========================

elif page == "Login":

    st.header("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if not email or not password:

            st.warning("Please fill all fields")

        else:

            with st.spinner("Logging in..."):

                response = requests.post(
                    f"{BACKEND_URL}/login",
                    json={
                        "email": email,
                        "password": password
                    }
                )

                data = response.json()

                if response.status_code == 200:

                    st.session_state.token = data["access_token"]
                    st.session_state.username = data["username"]
                    st.session_state.question = ""
                    st.session_state.voice_text = ""

                    st.success("Login successful")

                    st.session_state.page = "Dashboard"

                    st.rerun()

                else:
                    st.error(data["message"])

# =========================
# DASHBOARD
# =========================
elif page == "Dashboard":

    st.header(f"Welcome {st.session_state.username}")

    st.subheader("AI Powered Mock Interview Platform")

    st.write(
        "Practice technical interviews with AI-generated questions and instant feedback."
    )

    st.divider()

    response = requests.get(
        f"{BACKEND_URL}/history",
        headers={
            "Authorization": f"Bearer {st.session_state.token}"
        }
    )

    total_interviews = 0
    average_score = 0

    best_topic = "N/A"
    best_topic_score = 0

    weak_topic = "N/A"
    weak_topic_score = 10

    scores = []

    topic_scores = {}

    if response.status_code == 200:

        history = response.json()

        total_interviews = len(history)

        for item in history:

            evaluation = item.get("evaluation") or ""

            topic = item.get("topic", "Unknown")

            if "Score:" in evaluation:

                try:

                    score_text = evaluation.split(
                        "Score:"
                    )[1].split("/10")[0].strip()

                    score = int(score_text)

                    scores.append(score)

                    if score > best_topic_score:

                        best_topic_score = score
                        best_topic = topic

                    if score < weak_topic_score:

                        weak_topic_score = score
                        weak_topic = topic

                    if topic not in topic_scores:

                        topic_scores[topic] = []

                    topic_scores[topic].append(score)

                except:
                    pass

    if scores:

        average_score = round(
            sum(scores) / len(scores),
            1
        )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Interviews",
            total_interviews
        )

    with col2:

        st.metric(
            "Average Score",
            average_score
        )

    with col3:

        st.markdown(
            f"""
### Best Topic
{best_topic} ({best_topic_score}/10)
"""
        )

    with col4:

        st.markdown(
            f"""
### Weak Topic
{weak_topic} ({weak_topic_score}/10)
"""
        )

    st.divider()

    if scores:

        chart_data = pd.DataFrame({
            "Interview": list(range(1, len(scores) + 1)),
            "Score": scores
        })

        st.subheader("Performance Trend")

        st.line_chart(
            chart_data.set_index("Interview")
        )

    if topic_scores:

        topic_average = {}

        for topic, values in topic_scores.items():

            topic_average[topic] = round(
                sum(values) / len(values),
                1
            )

        topic_chart_data = pd.DataFrame({
            "Topic": list(topic_average.keys()),
            "Average Score": list(topic_average.values())
        })

        st.subheader("Topic-wise Performance")

        fig = px.bar(
            topic_chart_data,
            x="Average Score",
            y="Topic",
            orientation="h",
            height=400
        )

        fig.update_layout(
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            font_color="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            """
### Mock Interview

Generate AI interview questions based on:

- role
- topic
- difficulty

Get instant AI evaluation.
"""
        )

    with col2:

        st.success(
            """
### Interview History

View:

- previous interviews
- AI feedback
- answers
- performance history
"""
        )

    st.divider()

    st.subheader("Quick Start")

    st.write("1. Open Mock Interview")

    st.write("2. Select role and topic")

    st.write("3. Generate question")

    st.write("4. Submit your answer")

    st.write("5. Improve using AI feedback")
# =========================
# MOCK INTERVIEW
# =========================
elif page == "Mock Interview":

    st.header("AI Mock Interview")

    st.success(
        f"Welcome {st.session_state.username}"
    )

    uploaded_resume = st.file_uploader(
        "Upload Resume (Optional)",
        type=["pdf"]
    )

    resume_text = ""
    resume_uploaded = False

    if uploaded_resume is not None:

        pdf_reader = PdfReader(uploaded_resume)

        for pdf_page in pdf_reader.pages:

            text = pdf_page.extract_text()

            if text:
                resume_text += text

        resume_uploaded = True

    if not resume_uploaded:

        role = st.selectbox(
            "Select Role",
            [
                "Machine Learning Engineer",
                "Data Scientist",
                "Backend Developer",
                "Frontend Developer",
                "Software Engineer"
            ]
        )

        topic = st.text_input(
            "Enter Topic"
        )

        difficulty = st.selectbox(
            "Select Difficulty",
            [
                "Easy",
                "Medium",
                "Hard"
            ]
        )

    else:

        st.success(
            "Resume Interview Mode Enabled"
        )

        role = "Resume Interview"
        topic = "Resume Based"
        difficulty = "Personalized"

    # ── Session State Initialization ──
    if "question" not in st.session_state:
        st.session_state.question = ""

    if "evaluation" not in st.session_state:
        st.session_state.evaluation = ""

    if "previous_questions" not in st.session_state:
        st.session_state.previous_questions = []

    if "transcribed_text" not in st.session_state:
        st.session_state.transcribed_text = ""

    if "last_audio_id" not in st.session_state:
        st.session_state.last_audio_id = None

    # ── Generate Question Button ──
    if st.button("Generate Question"):

        response = requests.post(
            f"{BACKEND_URL}/generate-question",
            json={
                "role": role,
                "topic": topic,
                "difficulty": difficulty,
                "resume_text": resume_text,
                "previous_questions":
                    st.session_state.previous_questions
            },
            headers={
                "Authorization":
                    f"Bearer {st.session_state.token}"
            }
        )

        if response.status_code == 200:

            data = response.json()

            st.session_state.question = (
                data["question"]
            )

            st.session_state.session_id = (
                data["session_id"]
            )

            st.session_state.previous_questions.append(
                data["question"]
            )

            # Clear everything for fresh start
            st.session_state.evaluation = ""
            st.session_state.transcribed_text = ""
            st.session_state.last_audio_id = None

            st.rerun()

    # ── Question + Answer Section ──
    if st.session_state.question:

        st.subheader("Interview Question")

        st.info(
            st.session_state.question
        )

        # No key= used here so value= always works
        answer = st.text_area(
            "Your Answer",
            value=st.session_state.get(
                "transcribed_text", ""
            ),
            height=150
        )

        st.markdown("### 🎤 Voice Answer")

        audio = mic_recorder(
            start_prompt="🎙️ Start Recording",
            stop_prompt="⏹️ Stop Recording",
            key="mic"
        )

        # ── Audio Transcription (with loop guard) ──
        if audio and audio.get("id") != st.session_state.last_audio_id:

            st.session_state.last_audio_id = audio["id"]

            with st.spinner("Transcribing your voice..."):

                files = {
                    "audio": (
                        "audio.wav",
                        audio["bytes"],
                        "audio/wav"
                    )
                }

                response = requests.post(
                    f"{BACKEND_URL}/transcribe-audio",
                    files=files
                )

            if response.status_code == 200:

                transcribed_text = (
                    response.json()["text"]
                )

                # Only update transcribed_text
                # no answer_box manipulation needed
                st.session_state.transcribed_text = (
                    transcribed_text
                )

                st.success(
                    "Voice recorded successfully!"
                )
                st.rerun()

            else:

                st.error(
                    "Transcription failed. Please try again."
                )

        # ── Evaluate & Next Question Buttons ──
        col1, col2 = st.columns(2)

        with col1:

            if st.button("Evaluate Answer"):

                # Read directly from answer variable
                # not from session state answer_box
                current_answer = answer

                if not current_answer.strip():

                    st.warning(
                        "Please enter an answer first."
                    )

                else:

                    response = requests.post(
                        f"{BACKEND_URL}/evaluate-answer",
                        json={
                            "session_id":
                                st.session_state.session_id,

                            "question":
                                st.session_state.question,

                            "answer":
                                current_answer,

                            "role": role,
                            "topic": topic,
                            "difficulty": difficulty
                        },
                        headers={
                            "Authorization":
                                f"Bearer {st.session_state.token}"
                        }
                    )

                    if response.status_code == 200:

                        data = response.json()

                        st.session_state.evaluation = (
                            data["evaluation"]
                        )

                        st.rerun()

        with col2:

            if st.button("Next Question"):

                response = requests.post(
                    f"{BACKEND_URL}/generate-question",
                    json={
                        "role": role,
                        "topic": topic,
                        "difficulty": difficulty,
                        "resume_text": resume_text,
                        "previous_questions":
                            st.session_state.previous_questions
                    },
                    headers={
                        "Authorization":
                            f"Bearer {st.session_state.token}"
                    }
                )

                if response.status_code == 200:

                    data = response.json()

                    st.session_state.question = (
                        data["question"]
                    )

                    st.session_state.session_id = (
                        data["session_id"]
                    )

                    st.session_state.previous_questions.append(
                        data["question"]
                    )

                    # Clear everything for next question
                    st.session_state.evaluation = ""
                    st.session_state.transcribed_text = ""
                    st.session_state.last_audio_id = None

                    st.rerun()

        # ── Evaluation Result ──
        if st.session_state.evaluation:

            st.subheader("AI Evaluation")

            st.write(
                st.session_state.evaluation
            )

            if st.button("Reattempt Question"):

                st.session_state.evaluation = ""
                st.session_state.transcribed_text = ""
                st.session_state.last_audio_id = None

                st.rerun()
# =========================
# INTERVIEW HISTORY
# =========================
elif page == "Interview History":

    st.header("Interview History")

    response = requests.get(
        f"{BACKEND_URL}/history",
        headers={
            "Authorization":
            f"Bearer {st.session_state.token}"
        }
    )

    data = response.json()

    if response.status_code == 200:

        history = data

        if len(history) == 0:

            st.info(
                "No interview history found"
            )

        else:

            grouped_history = {}

            for item in history:

                role = item["role"]

                if not role or not role.strip():

                    role = "Resume Interview"

                if role not in grouped_history:

                    grouped_history[role] = []

                grouped_history[role].append(item)

            for role, items in grouped_history.items():

                with st.expander(f"📁 {role}"):

                    valid_items = []

                    for item in items:

                        answer = item.get(
                            "answer",
                            ""
                        )

                        if answer and answer.strip():

                            valid_items.append(item)

                    if len(valid_items) == 0:

                        st.info(
                            "No completed interviews"
                        )

                    else:

                        for index, item in enumerate(
                            valid_items,
                            start=1
                        ):

                            topic = item.get(
                                "topic",
                                "Resume Based"
                            )

                            difficulty = item.get(
                                "difficulty",
                                "Personalized"
                            )

                            with st.expander(
                                f"{index}. {topic} | {difficulty}"
                            ):

                                st.markdown(
                                    "### Question"
                                )

                                st.write(
                                    item["question"]
                                )

                                st.markdown(
                                    "### Your Answer"
                                )

                                st.write(
                                    item["answer"]
                                )

                                st.markdown(
                                    "### AI Evaluation"
                                )

                                st.write(
                                    item["evaluation"]
                                )