from database.db_config import db
from datetime import datetime

class InterviewSession(db.Model):

    __tablename__ = "interview_sessions"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    role = db.Column(db.String(100), nullable=False)

    difficulty = db.Column(db.String(50), nullable=False)

    topic = db.Column(db.String(100), nullable=False)

    question = db.Column(db.Text, nullable=True)

    answer = db.Column(db.Text, nullable=True)

    feedback = db.Column(db.Text, nullable=True)

    score = db.Column(db.Integer, nullable=True)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )