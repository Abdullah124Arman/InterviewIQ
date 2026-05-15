from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_interview_question(
    role,
    difficulty,
    topic,
    resume_text="",
    previous_questions=None
):

    if previous_questions is None:

        previous_questions = []

    if resume_text.strip():

        prompt = f"""
You are an expert technical interviewer.

The candidate uploaded their resume.

Analyze the resume carefully and generate ONE personalized interview question.

You can ask from:
- projects
- technical skills
- certifications
- education
- internships
- tools and technologies
- achievements
- programming languages

IMPORTANT RULES:
- Do NOT ask generic textbook questions
- Do NOT repeatedly start with:
  "Can you walk me through..."
- Use varied styles like:
  - Explain...
  - Why did you choose...
  - How would you...
  - What challenges did you face...
  - What is your understanding of...
  - Compare...
  - Describe...
- Ask realistic interview questions
- Questions should feel natural and professional
- Sometimes ask conceptual questions from skills mentioned in resume
- Sometimes ask project-based questions
- Keep variety between questions

Previously Asked Questions:
{previous_questions}

IMPORTANT:
- Do NOT repeat previous questions
- Do NOT ask same concept with minor wording changes
- Choose a different area/topic from resume

Resume:
{resume_text}

Return ONLY the interview question.
"""

    else:

        prompt = f"""
You are an AI interviewer.

Generate one professional mock interview question.

Role:
{role}

Difficulty:
{difficulty}

Topic:
{topic}

Previously Asked Questions:
{previous_questions}

IMPORTANT:
- Do NOT repeat previous questions
- Ask different concepts each time

Only return the interview question.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7
    )

    question = response.choices[0].message.content

    return question

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7
    )

    question = response.choices[0].message.content

    return question


def evaluate_answer(question, answer):

    prompt = f"""
You are an AI interviewer.

Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer professionally.

Keep each section short and concise.

Give response in this exact format:

Score: X/10

Correctness:
(2-3 short lines)

Clarity:
(2-3 short lines)

Communication:
(2-3 short lines)

Improvement Suggestions:
(2-3 short lines)

If the answer is weak, incorrect, below 6/10, or contains phrases like "I don't know",
then ALSO provide:

Ideal Answer:
(provide a strong concise ideal answer)
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.5
    )

    evaluation = response.choices[0].message.content

    return evaluation