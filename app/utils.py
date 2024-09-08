import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generar_preguntas(nivel, cantidad):
    print(f"\nGenerando {cantidad} preguntas de nivel {nivel}...\n\n")

    prompt = f"""
    Necesito practicar mi inglés.
    Genera {cantidad} preguntas de inglés de nivel {nivel} centradas en gramática y vocabulario.
    Las preguntas deben ser tipo quiz con posibilidad de seleccionar la opción correcta entre a, b, c, d. Evita preguntas de cultura general.
    Cada vez que generes preguntas, asegúrate de que sean únicas y diferentes para promover el aprendizaje. Evita repetir preguntas similares entre solicitudes.
    Devuelve las preguntas en formato JSON. Cada pregunta debe tener el siguiente formato:
    [{{
        "question": "Texto de la pregunta",
        "options": ["Opción 1", "Opción 2", "Opción 3", "Opción 4"],
        "answer": "Respuesta correcta"
        "question_name": "question1"
    }}]
    """
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an English teacher who creates unique and diverse quizzes focused on grammar and vocabulary. Each quiz should contain new questions and avoid repeating previous ones to ensure variety in practice."},
            {"role": "user", "content": prompt}
        ],
        model="gpt-3.5-turbo-0125"
    )

    try:
        content = response.choices[0].message.content.strip()

        questions = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Error al parsear JSON: {e}")
        questions = []

    print(questions)

    return questions