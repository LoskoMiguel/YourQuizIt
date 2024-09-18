from flask import Flask, session
from app.routes.main import main as main_blueprint
from app.routes.quiz import quiz as quiz_blueprint

app = Flask(__name__)
app.secret_key = "loskoalbeiroviveenelbosque"

app.register_blueprint(main_blueprint)
app.register_blueprint(quiz_blueprint)

if __name__ == "__main__":
    app.run(debug=True, port=5000)