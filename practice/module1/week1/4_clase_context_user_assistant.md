# Ingeniería de Prompts para Generative AI - Práctica (45 minutos)

## Descripción

En esta sesión práctica, te adentrarás en el arte de la **Ingeniería de Prompts**, una habilidad esencial para maximizar la efectividad de los modelos de **Inteligencia Artificial Generativa (GenAI)**. Aprenderás a diseñar prompts que proporcionen el contexto adecuado, a diferenciar entre los roles de usuario y asistente, y a utilizar distintos tipos de prompts (One-Shot, Few-Shot, Zero-Shot) para obtener resultados más precisos y coherentes. A través de ejercicios prácticos, consolidarás tu capacidad para crear prompts efectivos que optimicen la generación de texto por parte de los modelos de lenguaje.

## Objetivos

- **Comprender la importancia del contexto** en la creación de prompts efectivos.
- **Diferenciar entre los roles de usuario y asistente** en la interacción con modelos de GenAI.
- **Aplicar distintos tipos de prompts** (One-Shot, Few-Shot, Zero-Shot) para mejorar la calidad de las respuestas generadas.
- **Desarrollar habilidades avanzadas en la ingeniería de prompts**, mejorando la precisión y relevancia de las salidas de los modelos generativos.
- **Integrar prácticas de ingeniería de prompts** en un mini-proyecto de GenAI.

## Actividades

### 1. Comprendiendo el Contexto en los Prompts

#### **Ejercicio 1: Añadir Contexto a los Prompts**

**Objetivo:** Aprender a incluir información contextual en los prompts para guiar al modelo de GenAI hacia respuestas más precisas y relevantes.

**Instrucciones:**

1. **Definir el Contexto:**
   - Reflexiona sobre el propósito de tu prompt. ¿Qué información adicional puede ayudar al modelo a entender mejor la tarea?

2. **Implementar el Método `añadir_contexto`:**
   - Añade un método en la clase `ModeloGenerativo` para incorporar contexto en los prompts.

   ```python
   class ModeloGenerativo:
       # ... (código anterior)
       
       def añadir_contexto(self, prompt, contexto):
           return f"{contexto}\n\n{prompt}"

3 . **Ejemplo de Uso:**

- Crea un contexto que defina el rol del asistente y utilízalo para generar un prompt.
   
    ```python
    class ModeloGPT(ModeloGenerativo):
        # ... (código anterior)
        
        def generar_texto_con_contexto(self, prompt, contexto):
            prompt_con_contexto = self.añadir_contexto(prompt, contexto)
            return self.generar_texto(prompt_con_contexto)

    if __name__ == "__main__":
        modelo_gpt = ModeloGPT("GPT-4", "v1.0", "tu_api_key", db)
        contexto = "Contexto: Eres un asistente de IA que ayuda a escribir artículos científicos."
        prompt = "Describe los beneficios de la inteligencia artificial en la medicina."
        texto_generado = modelo_gpt.generar_texto_con_contexto(prompt, contexto)
        print(texto_generado)
    ```

### 2. Roles en la Interacción con GenAI

#### **Ejercicio 2: Diferenciar entre Usuario y Asistente**

Objetivo: Entender y aplicar los roles de usuario y asistente en los prompts para mejorar la calidad de las respuestas generadas.

**Instrucciones:**

1. Definir Roles:

* Usuario: Quien proporciona el prompt o la solicitud.
* Asistente: El modelo de GenAI que responde a la solicitud.

2. Implementar Métodos para Roles:

* Añade métodos en la clase ModeloGenerativo para manejar interacciones de usuario y asistente.

 ```python
class ModeloGenerativo:
    # ... (código anterior)
    
    def crear_prompt_usuario(self, mensaje):
        return f"Usuario: {mensaje}"
    
    def crear_prompt_asistente(self, respuesta):
        return f"Asistente: {respuesta}"
 ```

3. Ejemplo de Uso:

* Simula una conversación entre el usuario y el asistente.

 ```python
if __name__ == "__main__":
    modelo_gpt = ModeloGPT("GPT-4", "v1.0", "tu_api_key", db)
    mensaje_usuario = "¿Cuáles son las aplicaciones de la IA en la educación?"
    prompt_usuario = modelo_gpt.crear_prompt_usuario(mensaje_usuario)
    contexto = "Contexto: Eres un asistente de IA especializado en educación."
    prompt_completo = modelo_gpt.añadir_contexto(prompt_usuario, contexto)
    respuesta = modelo_gpt.generar_texto(prompt_completo)
    prompt_asistente = modelo_gpt.crear_prompt_asistente(respuesta)
    print(prompt_asistente)
 ```

### 3. Tipos de Prompts: One-Shot, Few-Shot y Zero-Shot

#### **Ejercicio 3: Aplicar Diferentes Tipos de Prompts**

Objetivo: Utilizar distintos tipos de prompts para evaluar cómo afectan la calidad y precisión de las respuestas generadas por los modelos de GenAI.

**Instrucciones:**

1. Definir los Tipos de Prompts:

* Zero-Shot: El modelo responde sin ejemplos previos.
* One-Shot: El modelo recibe un único ejemplo antes de la solicitud.
* Few-Shot: El modelo recibe varios ejemplos antes de la solicitud.

2. Implementar Métodos para Cada Tipo de Prompt:

 ```python
class ModeloGenerativo:
    # ... (código anterior)
    
    def crear_zero_shot_prompt(self, tarea):
        return f"Por favor, {tarea}"
    
    def crear_one_shot_prompt(self, tarea, ejemplo):
        return f"Ejemplo:\nTarea: {ejemplo['tarea']}\nRespuesta: {ejemplo['respuesta']}\n\nTarea: {tarea}"
    
    def crear_few_shot_prompt(self, tarea, ejemplos):
        prompt = ""
        for ejemplo in ejemplos:
            prompt += f"Ejemplo:\nTarea: {ejemplo['tarea']}\nRespuesta: {ejemplo['respuesta']}\n\n"
        prompt += f"Tarea: {tarea}"
        return prompt
 ```

3. Ejemplo de Uso:

Genera texto utilizando los tres tipos de prompts y compara los resultados.

 ```python
if __name__ == "__main__":
    modelo_gpt = ModeloGPT("GPT-4", "v1.0", "tu_api_key", db)
    
    tarea = "Describe los beneficios de la inteligencia artificial en la agricultura."
    
    # Zero-Shot
    prompt_zero_shot = modelo_gpt.crear_zero_shot_prompt(tarea)
    texto_zero_shot = modelo_gpt.generar_texto(prompt_zero_shot)
    print("Zero-Shot Response:")
    print(texto_zero_shot)
    
    # One-Shot
    ejemplo_one_shot = {
        "tarea": "Describe los beneficios de la inteligencia artificial en la educación.",
        "respuesta": "La inteligencia artificial en la educación permite la personalización del aprendizaje, adaptándose a las necesidades individuales de cada estudiante."
    }
    prompt_one_shot = modelo_gpt.crear_one_shot_prompt(tarea, ejemplo_one_shot)
    texto_one_shot = modelo_gpt.generar_texto(prompt_one_shot)
    print("\nOne-Shot Response:")
    print(texto_one_shot)
    
    # Few-Shot
    ejemplos_few_shot = [
        {
            "tarea": "Describe los beneficios de la inteligencia artificial en la educación.",
            "respuesta": "La inteligencia artificial en la educación permite la personalización del aprendizaje, adaptándose a las necesidades individuales de cada estudiante."
        },
        {
            "tarea": "Describe los beneficios de la inteligencia artificial en la salud.",
            "respuesta": "La inteligencia artificial en la salud mejora el diagnóstico temprano, optimiza tratamientos y gestiona eficientemente los datos médicos."
        }
    ]
    prompt_few_shot = modelo_gpt.crear_few_shot_prompt(tarea, ejemplos_few_shot)
    texto_few_shot = modelo_gpt.generar_texto(prompt_few_shot)
    print("\nFew-Shot Response:")
    print(texto_few_shot)
 ```


### 4. Mini-Proyecto: Optimización de Prompts para Generación de Textos

Objetivo: Aplicar los conceptos aprendidos sobre contexto, roles y tipos de prompts para desarrollar una aplicación que genere textos optimizados utilizando diferentes estrategias de ingeniería de prompts.

#### **Instrucciones:**

1. Definir la Clase GeneradorOptimo:

* Gestiona diferentes tipos de prompts y genera textos utilizando las estrategias aprendidas.

 ```python
class GeneradorOptimo:
    def __init__(self, modelo: ModeloGenerativo):
        self.modelo = modelo
    
    def generar_con_zero_shot(self, tarea):
        prompt = self.modelo.crear_zero_shot_prompt(tarea)
        return self.modelo.generar_texto(prompt)
    
    def generar_con_one_shot(self, tarea, ejemplo):
        prompt = self.modelo.crear_one_shot_prompt(tarea, ejemplo)
        return self.modelo.generar_texto(prompt)
    
    def generar_con_few_shot(self, tarea, ejemplos):
        prompt = self.modelo.crear_few_shot_prompt(tarea, ejemplos)
        return self.modelo.generar_texto(prompt)
 ```

2. Implementar la Aplicación Principal:

Permite al usuario seleccionar el tipo de prompt y generar textos en consecuencia.

 ```python
from modelo_generativo import ModeloGPT
from database import BaseDatos

def main():
    api_key = "tu_api_key_aquí"  # Reemplaza con tu clave API de OpenAI
    db = BaseDatos()
    modelo = ModeloGPT("GPT-4", "v1.0", api_key, db)
    generador = GeneradorOptimo(modelo)

    print("=== Generador de Textos Optimizado con Ingeniería de Prompts ===")
    while True:
        tarea = input("Ingresa la tarea para generar texto (o 'salir' para terminar): ")
        if tarea.lower() == 'salir':
            break
        
        tipo_prompt = input("Selecciona el tipo de prompt (zero, one, few): ").lower()
        
        if tipo_prompt == 'zero':
            respuesta = generador.generar_con_zero_shot(tarea)
            print(f"\n**Zero-Shot Response:**\n{respuesta}\n{'-'*50}")
        
        elif tipo_prompt == 'one':
            ejemplo = {}
            ejemplo['tarea'] = input("Ingresa una tarea de ejemplo: ")
            ejemplo['respuesta'] = input("Ingresa la respuesta para el ejemplo: ")
            respuesta = generador.generar_con_one_shot(tarea, ejemplo)
            print(f"\n**One-Shot Response:**\n{respuesta}\n{'-'*50}")
        
        elif tipo_prompt == 'few':
            try:
                num_ejemplos = int(input("¿Cuántos ejemplos deseas ingresar? "))
            except ValueError:
                print("Por favor, ingresa un número válido.")
                continue
            ejemplos = []
            for i in range(num_ejemplos):
                print(f"\nEjemplo {i+1}:")
                tarea_ejemplo = input("Ingresa la tarea de ejemplo: ")
                respuesta_ejemplo = input("Ingresa la respuesta para el ejemplo: ")
                ejemplos.append({"tarea": tarea_ejemplo, "respuesta": respuesta_ejemplo})
            respuesta = generador.generar_con_few_shot(tarea, ejemplos)
            print(f"\n**Few-Shot Response:**\n{respuesta}\n{'-'*50}")
        
        else:
            print("Tipo de prompt no reconocido. Por favor, elige entre 'zero', 'one' o 'few'.")

    print("Guardando y cerrando la aplicación...")
    db.cerrar_conexion()

if __name__ == "__main__":
    main()
 ```

3. Ejecutar y Probar la Aplicación:

* Ejecuta app.py y prueba diferentes tipos de prompts para observar cómo varían las respuestas generadas.

 ```python
python app.py
 ```

### Relación con Generative AI

La ingeniería de prompts es una habilidad crucial para interactuar eficazmente con modelos de GenAI. Al diseñar prompts bien estructurados que incluyan el contexto adecuado y utilizar distintos tipos de prompts según la necesidad, puedes mejorar significativamente la calidad y relevancia de las respuestas generadas. Esta práctica te permitirá desarrollar aplicaciones más precisas y útiles, optimizando la interacción con modelos avanzados de lenguaje y otros sistemas generativos.

### Conclusión

Al finalizar esta sesión práctica, habrás adquirido una comprensión profunda de cómo diseñar prompts efectivos para modelos de Generative AI. Serás capaz de incorporar contextos específicos, diferenciar roles de usuario y asistente, y aplicar distintos tipos de prompts para maximizar la eficacia de tus aplicaciones de IA generativa. Estas habilidades te permitirán desarrollar soluciones más robustas y alineadas con los objetivos específicos de tus proyectos en el campo de la inteligencia artificial.