import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

respuestas = ''

def generar_preguntas(nivel, cantidad):
    print(f"\nGenerando {cantidad} preguntas de nivel {nivel}...\n\n")
    prompt = f"""
    Necesito practicar mi inglés.
    Genera {cantidad} preguntas de inglés de nivel {nivel} centradas en gramática y vocabulario.
    Las preguntas deben ser tipo quiz con posibilidad de seleccionar la opción correcta entre a, b, c, d. Evita preguntas de cultura general.
    Devuelve las preguntas en formato JSON. Cada pregunta debe tener el siguiente formato:
    {{
        "question": "Texto de la pregunta",
        "options": ["Opción 1", "Opción 2", "Opción 3", "Opción 4"],
        "answer": "Respuesta correcta"
        "question_name": "question1"
    }}
    """
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an English teacher who creates quizzes focused on grammar and vocabulary."},
            {"role": "user", "content": prompt}
        ],
        model="gpt-4o-mini"
    )

    try:
        content = response.choices[0].message.content.strip()
        json_start = content.find('[')
        json_end = content.rfind(']') + 1
        json_content = content[json_start:json_end]

        questions = json.loads(json_content)
    except json.JSONDecodeError as e:
        print(f"Error al parsear JSON: {e}")
        questions = []

    print(questions)

    return questions