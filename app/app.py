from flask import Flask, request, render_template

app = Flask(__name__)

respuestas = {
    "respuesta1": "2",
    "respuesta2": "5"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/preguntas", methods=["GET", "POST"])
def preguntas():
    puntos = 0
    if request.method == "POST":    
        for pregunta, respuesta in respuestas.items():
            ejercisios = request.form.get(pregunta)
            if ejercisios == respuesta:
                puntos += 1

    return render_template("preguntas.html", data=respuestas, puntos=puntos, len=len, ejercisios=ejercisios)

if __name__ == "__main__":
    app.run(debug=True, port=5000)