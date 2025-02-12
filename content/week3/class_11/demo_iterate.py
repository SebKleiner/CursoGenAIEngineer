import json
import time


def call_gpt(prompt):
    """
    Mock function simulating a call to GPT or another LLM.
    In a real scenario, you'd use an API call here.
    For demonstration, it returns a string that may or may not be valid JSON.
    """
    # Here we'll simulate a random failure to produce valid JSON
    import random
    if random.choice([True, False]):
        # Return valid JSON half the time
        return '{"name": "Demo", "value": 42}'
    else:
        # Return invalid JSON the other half
        return 'Oops, invalid JSON!'


def get_valid_json(prompt, max_retries=3):
    """
    Attempts to get valid JSON from GPT by repeatedly refining the prompt
    and re-calling GPT if parsing fails.
    """
    attempt = 0
    while attempt < max_retries:
        attempt += 1
        response = call_gpt(prompt)
        try:
            data = json.loads(response)
            print(f"Valid JSON received on attempt {attempt}: {data}")
            return data
        except json.JSONDecodeError:
            print(f"Attempt {attempt} failed to parse JSON. Retrying...\n")
            # Refine the prompt with an added instruction to strictly return JSON
            prompt += "\nPor favor, solo devuelve JSON válido. No incluyas texto adicional."
            time.sleep(1)  # Just to simulate some delay or real-time scenario

    print("Máximo número de reintentos alcanzado. No se pudo obtener JSON válido.")
    return None


if __name__ == "__main__":
    base_prompt = (
        "Genera un objeto JSON con claves 'name' y 'value'. "
        "No incluyas explicación ni texto adicional."
    )
    final_data = get_valid_json(base_prompt)
    if final_data is not None:
        print("JSON Final:", final_data)
    else:
        print("No se pudo obtener JSON válido tras varios intentos.")
