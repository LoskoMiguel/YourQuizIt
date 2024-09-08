import json
from app.utils import generar_preguntas
from flask import Blueprint, request, render_template, session

quiz = Blueprint('quiz', __name__)

@quiz.route("/quizzes", methods=["GET", "POST"])
def preguntas():
    if request.method == "POST":
        nivel = request.form.get("nivel")
        cantidad = int(request.form.get("cantidad"))
        preguntas_generadas = generar_preguntas(nivel, cantidad)

        # Guardar respuestas para compararlas después en la sesión del usuario
        respuestas_correctas = {f"question{index+1}": pregunta["answer"] for index, pregunta in enumerate(preguntas_generadas)}
        session['respuestas_correctas'] = respuestas_correctas

        # Esto es solo para depuración (Después lo eliminamos)
        print(respuestas_correctas)
        
        return render_template("preguntas.html", preguntas=preguntas_generadas, nivel=nivel)

    return render_template("preguntas.html")

@quiz.route("/resultados", methods=["POST"])
def resultados():
    puntos = 0
    respuestas_db = {} # Para el caso de que se quiera guardar las respuestas en una base de datos
    respuestas_correctas_usuario = {}
    respuestas_usuario = {key: value for key, value in request.form.items() if key.startswith('question')}
    preguntas_usuario = {key: value for key, value in request.form.items() if key.startswith('q_text_')}

    print(f"Preguntas del usuario: {preguntas_usuario}")

    # Recuperar las respuestas correctas de la sesión del usuario
    respuestas_correctas = session.get('respuestas_correctas', {})
    
    # Comparar las respuestas del usuario con las respuestas correctas
    for pregunta, respuesta in respuestas_usuario.items():
        respuestas_db[pregunta] = respuesta
        if respuestas_correctas.get(pregunta) == respuesta:
            puntos += 1
            respuestas_correctas_usuario[pregunta] = respuesta

    # Calcular el porcentaje de respuestas correctas y mostrar un mensaje personalizado
    if not respuestas_correctas:
        mensaje = "No hay ejercicios disponibles."
    else:
        total_preguntas = len(respuestas_correctas)
        porcentaje_correctas = (puntos / total_preguntas) * 100
        porcentaje_correctas_formateado = f"{porcentaje_correctas:.0f}%"

        if porcentaje_correctas == 100:
            mensaje = "¡Excelente! Puntaje perfecto."
        elif porcentaje_correctas >= 80:
            mensaje = "¡Muy bien! Has acertado la mayoría."
        elif porcentaje_correctas >= 50:
            mensaje = "Buen trabajo, pero puedes mejorar."
        else:
            mensaje = "Necesitas mejorar. Sigue practicando."

    # Crear una lista con los detalles de las respuestas del usuario (Tipo analítica)
    detalles_respuestas = []
    for pregunta, respuesta in respuestas_usuario.items():
        correcto = respuestas_correctas.get(pregunta) == respuesta
        detalles_respuestas.append({
            "pregunta": preguntas_usuario.get(f"q_text_{pregunta}"),
            "respuesta_usuario": respuesta,
            "correcto": correcto,
            "respuesta_correcta": respuestas_correctas.get(pregunta)
        })

    # Esto es solo para depuración (Después lo eliminamos)
    print(f"""
        Puntos: {puntos}
        Total de preguntas: {total_preguntas}
        Respuestas correctas: {respuestas_correctas}
        Respuestas del usuario: {respuestas_usuario}
        Respuetas correctas del usuario: {respuestas_correctas_usuario}
        Porcentaje de respuestas correctas: {porcentaje_correctas_formateado}
    """)

    return render_template(
        "resultados.html",
        mensaje=mensaje,
        puntos=puntos,
        total_preguntas=total_preguntas,
        porcentaje_correctas=porcentaje_correctas_formateado,
        detalles_respuestas=detalles_respuestas
    )