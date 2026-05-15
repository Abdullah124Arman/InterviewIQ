# 🎯 InterviewIQ — AI Mock Interview & Placement Preparation Platform

> Practice smarter. Get hired faster.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![Flask](https://img.shields.io/badge/Flask-Backend-lightgrey)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-green)
![LLaMA](https://img.shields.io/badge/LLaMA-3.3--70b-purple)
![JWT](https://img.shields.io/badge/Auth-JWT-orange)

## 🌐 Live Demo
👉 [InterviewIQ on Streamlit Cloud](https://interviewiq-dqngpaawqyy8zczshahyf2.streamlit.app/)

## 📌 Backend API
👉 [Flask REST API on Render](https://interviewiq-backend-2i3i.onrender.com)

---

## 🚀 What is InterviewIQ?

InterviewIQ is a full-stack AI-powered mock interview and placement preparation platform. Users can practice technical interviews with AI-generated questions, receive detailed AI evaluation on their answers, and track their performance through an analytics dashboard.

Built as a complete software product — not a demo — with real authentication, a hosted PostgreSQL database, REST API backend, and LLM-powered interview engine.

---

## ✨ Features

### 🔐 Authentication System
- User Signup and Login
- JWT-based authentication with protected routes
- Secure session handling and logout

### 🤖 AI Mock Interview Engine
- Topic-based interview question generation
- Resume-based personalized interview generation (upload PDF)
- Anti-repetition logic — never gets the same question twice
- Role selection: Machine Learning Engineer, Software Engineer, Data Scientist, Frontend Developer, Backend Developer

### 📊 AI Answer Evaluation
- AI scoring system (0-10)
- Correctness feedback
- Clarity and communication feedback
- Improvement suggestions
- Ideal answer generation for weak answers (score < 5)

### 📈 Dashboard & Analytics
- Total interviews count
- Average score tracking
- Best topic and weak topic identification
- Performance trend chart (line graph)
- Topic-wise performance visualization (bar chart)

### 📁 Interview History
- Grouped by role
- Full session history with questions, answers, scores, feedback
- Resume interview tracking

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit + Plotly + Pandas |
| Backend | Flask + Flask-JWT-Extended + SQLAlchemy |
| Database | PostgreSQL (Supabase) |
| AI / LLM | LLaMA 3.3-70b via Groq API |
| Resume Parsing | PyPDF2 |
| Authentication | JWT (JSON Web Tokens) |
| Deployment | Streamlit Community Cloud (Frontend) + Render (Backend) |
| Version Control | GitHub |

---

## ⚙️ How It Works

```plaintext
User Signup/Login
      ↓
JWT Token Issued
      ↓
Select Role + Topic + Difficulty (or Upload Resume)
      ↓
Groq API generates personalized interview question
      ↓
User submits answer
      ↓
LLaMA 3.3-70b evaluates answer → Score + Feedback + Ideal Answer
      ↓
Results stored in PostgreSQL (Supabase)
      ↓
Dashboard updates with performance analytics

🗄️ Database Schema

users

id, username, email, password_hash, created_at

interview_sessions

id, user_id, role, topic, difficulty, timestamp

questions

id, session_id, generated_question

answers

id, question_id, user_answer, score, correctness_feedback, clarity_feedback, communication_feedback, improvement_suggestions, ideal_answer



📁 Project Structure
InterviewIQ/
│
├── frontend/
│   ├── app.py
│   └── pages/
│       ├── login.py
│       ├── signup.py
│       ├── dashboard.py
│       ├── interview.py
│       ├── results.py
│       └── analytics.py
│
├── backend/
│   ├── app.py
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── interview_routes.py
│   │   └── analytics_routes.py
│   ├── models/
│   │   ├── user_model.py
│   │   ├── interview_model.py
│   │   └── answer_model.py
│   ├── services/
│   │   ├── groq_service.py
│   │   ├── evaluation_service.py
│   │   └── analytics_service.py
│   ├── auth/
│   │   └── jwt_handler.py
│   └── database/
│       └── db_config.py
│
├── requirements.txt
├── .env.example
└── README.md
🏃 Run Locally
1. Clone the repository
git clone https://github.com/Abdullah124Arman/InterviewIQ.git
cd InterviewIQ
2. Create virtual environment
python -m venv venv
venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Set up environment variables

Create a .env file:

GROQ_API_KEY=your_groq_api_key
DATABASE_URL=your_supabase_postgresql_url
JWT_SECRET_KEY=your_jwt_secret
5. Run Backend
cd backend
python app.py
6. Run Frontend
cd frontend
streamlit run app.py


👨‍💻 Author

Abdullah Arman — B.Tech CSE, Parul University

GitHub: @Abdullah124Arman
LinkedIn: Abdullah Arman