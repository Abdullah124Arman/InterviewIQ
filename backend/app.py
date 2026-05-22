from flask import Flask
from dotenv import load_dotenv
from database.db_config import db
from models.user_model import User
from routes.auth_routes import auth_bp
from flask_jwt_extended import JWTManager
import os
from models.interview_model import InterviewSession
from routes.interview_routes import interview_bp

load_dotenv(dotenv_path="../.env")

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

database_url = os.getenv("DATABASE_URL")

print("DATABASE URL:", database_url)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
app.register_blueprint(auth_bp)
app.register_blueprint(interview_bp)
jwt = JWTManager(app)


@app.route("/")
def home():
    return {"message": "InterviewIQ Backend Running"}

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=False)