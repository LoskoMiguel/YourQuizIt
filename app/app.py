import os
from flask import Flask, session
from app.routes.main import main as main_blueprint
from app.routes.quiz import quiz as quiz_blueprint
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

app.register_blueprint(main_blueprint)
app.register_blueprint(quiz_blueprint)
if __name__ == "__main__":
    app.run(debug=True, port=5000)