from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.interview_model import InterviewSession

from services.ai_service import (
    generate_interview_question,
    evaluate_answer
)
from models.interview_model import InterviewSession
from database.db_config import db

interview_bp = Blueprint("interview", __name__)

@interview_bp.route("/generate-question", methods=["POST"])
@jwt_required()
def generate_question():

    current_user_id = get_jwt_identity()

    data = request.get_json()

    role = data.get("role")
    difficulty = data.get("difficulty")
    topic = data.get("topic")
    resume_text = data.get("resume_text", "")
    previous_questions = data.get(
    "previous_questions",
    []
)

    question = generate_interview_question(
    role,
    difficulty,
    topic,
    resume_text,
    previous_questions
)

    new_session = InterviewSession(
        user_id=current_user_id,
        role=role,
        difficulty=difficulty,
        topic=topic,
        question=question
    )

    db.session.add(new_session)
    db.session.commit()

    return jsonify({
        "question": question,
        "session_id": new_session.id
    }), 200
@interview_bp.route("/evaluate-answer", methods=["POST"])
@jwt_required()
def evaluate_user_answer():

    data = request.get_json()

    session_id = data.get("session_id")
    answer = data.get("answer")

    session = InterviewSession.query.get(session_id)

    if not session:
        return jsonify({
            "message": "Interview session not found"
        }), 404

    evaluation = evaluate_answer(
        session.question,
        answer
    )

    session.answer = answer
    session.feedback = evaluation

    db.session.commit()

    return jsonify({
        "evaluation": evaluation
    }), 200
@interview_bp.route("/history", methods=["GET"])
@jwt_required()

def get_history():

    user_id = int(get_jwt_identity())

    sessions = InterviewSession.query.filter_by(
    user_id=user_id
).order_by(
    InterviewSession.id.desc()
).all()

    history = []

    for session in sessions:

        history.append({
            "role": session.role,
            "difficulty": session.difficulty,
            "topic": session.topic,
            "question": session.question,
            "answer": session.answer,
            "evaluation": session.feedback
        })

    return jsonify(history), 200