import json

# Example text that we assume is the output from GPT or another LLM
model_output = """
{
  "title": "Introducción a la Inteligencia Artificial",
  "summary": "La IA se enfoca en crear máquinas capaces de realizar tareas que normalmente requieren inteligencia humana...",
  "keywords": ["IA", "Aprendizaje Automático", "Redes Neuronales"]
}
"""

def parse_json_output(output_text):
    try:
        # Attempt to parse the JSON
        data = json.loads(output_text)
        print("Título:", data["title"])
        print("Resumen:", data["summary"])
        print("Palabras clave:", data["keywords"])
        return data
    except json.JSONDecodeError as e:
        print("Error al decodificar JSON:", e)
        return None

if __name__ == "__main__":
    parsed_data = parse_json_output(model_output)
    if parsed_data is not None:
        print("\nEl JSON se parseó correctamente.")
    else:
        print("\nNo se pudo parsear el JSON.")

