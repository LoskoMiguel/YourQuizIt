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
    if request.method == "POST":
        ejercicios = {}
        for pregunta, respuesta in respuestas.items():
            ejercicios[pregunta] = request.form.get(pregunta)
            if ejercicios[pregunta] == respuesta:
                puntos += 1

        if not respuestas:
            mensaje = "No hay ejercicios disponibles."
        elif puntos == len(respuestas):
            mensaje = "¡Excelente! Puntaje perfecto."
        elif puntos == 1:
            mensaje = "Buen trabajo, pero debes mejorar. 2 puntos buenos."
        else:
            mensaje = "Sacaste todas malas."

        return render_template("resultados.html", mensaje=mensaje)

    return render_template("preguntas.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)