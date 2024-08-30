from flask import Flask, request, render_template, redirect

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
    ejercicios = {}
    if request.method == "POST":    
        for pregunta, respuesta in respuestas.items():
            ejercicios[pregunta] = request.form.get(pregunta)
            if ejercicios[pregunta] == respuesta:
                puntos += 1

        if not respuestas:
            return "<h2>No hay ejercicios disponibles.</h2>"
        elif puntos == len(respuestas):
            return "<h2>¡Excelente! Puntaje perfecto.</h2>"
        elif puntos == 1:
            return "<h2>Buen trabajo, pero debes mejorar. 2 puntos buenos.</h2>"
        else:
            return "<h2>Sacaste todas malas.</h2>"

    return render_template("preguntas.html", data=respuestas, puntos=puntos, len=len, ejercicios=ejercicios)

if __name__ == "__main__":
    app.run(debug=True, port=5000)