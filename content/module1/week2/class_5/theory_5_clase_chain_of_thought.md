# Chain of Thought y One-Shot vs Many-Shots en Generative AI - Teoría de la Clase 5 (45 minutos)

## Descripción

En esta clase teórica, exploraremos en profundidad dos conceptos avanzados de la ingeniería de prompts para **Inteligencia Artificial Generativa (GenAI)**: **Chain of Thought (CoT)** y **One-Shot vs Many-Shots**. Estos enfoques son esenciales para mejorar la calidad, coherencia y precisión de las respuestas generadas por modelos de lenguaje como GPT-4. Además, integraremos estos conceptos con las clases de Python previamente desarrolladas (`ModeloGenerativo` y `ModeloGPT`) para ilustrar cómo aplicar estas técnicas en proyectos prácticos de GenAI.

## Objetivos

- **Comprender la técnica Chain of Thought (CoT)** y su impacto en el razonamiento de los modelos generativos.
- **Diferenciar entre One-Shot y Many-Shots** en la creación de prompts y conocer sus aplicaciones específicas.
- **Aplicar estrategias avanzadas de prompting** para mejorar la calidad de las respuestas generadas por GenAI.
- **Integrar CoT y One-Shot/Many-Shots** utilizando las clases de Python `ModeloGenerativo` y `ModeloGPT`.
- **Desarrollar habilidades críticas** para diseñar prompts efectivos que maximicen el rendimiento de los modelos generativos.

## Contenidos

### 1. Chain of Thought (CoT)

#### **Definición y Concepto**

**Chain of Thought (CoT)** es una técnica que guía al modelo de IA a generar una secuencia lógica de pensamientos o pasos intermedios antes de proporcionar una respuesta final. Este enfoque mejora la capacidad del modelo para resolver problemas complejos que requieren múltiples etapas de razonamiento.

#### **Importancia de CoT**

- **Mejora el Razonamiento:** Facilita que el modelo desglosa tareas complejas en pasos más manejables.
- **Aumenta la Coherencia:** Las respuestas generadas son más lógicas y estructuradas.
- **Reduce Errores:** Minimiza la probabilidad de respuestas incorrectas al seguir un proceso paso a paso.

#### **Ejemplo de Chain of Thought**

**Contexto:** Eres un asistente de IA que ayuda a resolver problemas matemáticos paso a paso.

**Tarea:** Calcula la suma de los primeros 10 números naturales.

**Chain of Thought:**

Identificar los primeros 10 números naturales: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10.
Aplicar la fórmula de la suma de una serie aritmética: S = n(n + 1)/2.
Sustituir n = 10: S = 10(10 + 1)/2 = 55.
Concluir que la suma es 55.

Respuesta: La suma de los primeros 10 números naturales es 55.


#### **Implementación en Prompts con `ModeloGenerativo`**

Para implementar CoT, estructuramos el prompt de manera que el modelo genere los pasos intermedios antes de la respuesta final. Utilizaremos la clase `ModeloGenerativo` previamente definida para facilitar esta implementación.

```python
class ModeloGenerativo:
    def __init__(self, nombre, version):
        self._nombre = nombre
        self._version = version

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, valor):
        self._version = valor

    def cargar_modelo(self):
        # Código para cargar el modelo
        pass

    def generar_texto(self, prompt):
        # Código para generar texto basado en el prompt
        pass

    def limpiar_prompt(self, prompt):
        prompt = prompt.strip()
        prompt = prompt.capitalize()
        return prompt

    def formatear_prompt(self, plantilla, variables):
        try:
            prompt_formateado = plantilla.format(**variables)
            return prompt_formateado
        except KeyError as e:
            print(f"Error: Falta la variable {e} en el diccionario de variables.")
            return plantilla

```

Integración con Chain of Thought:

Extendemos la clase ModeloGenerativo para incluir métodos que permitan la incorporación de Chain of Thought en los prompts.

```python
import requests
from database import BaseDatos

class ModeloGPT(ModeloGenerativo):
    def __init__(self, nombre, version, api_key, db: BaseDatos):
        super().__init__(nombre, version)
        self.api_key = api_key
        self.url = "https://api.openai.com/v1/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.db = db

    def generar_texto_con_cot(self, prompt, cot_steps):
        prompt_cot = f"""
        {prompt}

        Chain of Thought:
        {cot_steps}

        Respuesta:
        """
        prompt_limpio = self.limpiar_prompt(prompt_cot)
        payload = {
            "model": "text-davinci-003",
            "prompt": prompt_limpio,
            "max_tokens": 150,
            "temperature": 0.7
        }
        response = requests.post(self.url, headers=self.headers, json=payload)
        if response.status_code == 200:
            texto_generado = response.json()["choices"][0]["text"].strip()
            self.db.guardar_interaccion(prompt_limpio, texto_generado)
            return texto_generado
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
```

Ejemplo de Uso:

```python
if __name__ == "__main__":
    api_key = "tu_api_key_aquí"  # Reemplaza con tu clave API de OpenAI
    db = BaseDatos()
    modelo_gpt = ModeloGPT("GPT-4", "v1.0", api_key, db)
    prompt = "Contexto: Eres un asistente de IA que ayuda a resolver problemas matemáticos paso a paso.\n\nTarea: Calcula la suma de los primeros 10 números naturales."
    cot_steps = """
    1. Identificar los primeros 10 números naturales: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10.
    2. Aplicar la fórmula de la suma de una serie aritmética: S = n(n + 1)/2.
    3. Sustituir n = 10: S = 10(10 + 1)/2 = 55.
    4. Concluir que la suma es 55.
    """
    texto_generado = modelo_gpt.generar_texto_con_cot(prompt, cot_steps)
    print(texto_generado)
```


### **Beneficios y Limitaciones**

#### **Beneficios:**

- Mejora la precisión en tareas complejas.
- Facilita el seguimiento del razonamiento del modelo.
- Permite detectar y corregir errores en etapas intermedias.

#### **Limitaciones:**

- Incrementa el número de tokens utilizados.
- Puede ralentizar la generación de respuestas.
- Requiere una estructuración cuidadosa del prompt.

### 2. One-Shot vs Many-Shots

#### **Definición y Concepto**

**One-Shot Prompts:** Proporcionan un único ejemplo antes de la solicitud principal. Ayudan al modelo a entender el formato y la expectativa de la respuesta con un solo caso de referencia.

**Many-Shots Prompts:** Incluyen múltiples ejemplos antes de la solicitud principal. Ofrecen al modelo una variedad de casos que guían de manera más completa la generación de respuestas.

#### **Aplicaciones y Uso Adecuado**

**One-Shot Prompts:**

- Útiles cuando:
    - Se necesita una guía específica y clara.
    - Las tareas tienen patrones de respuesta consistentes.
- Ejemplos de Uso:
    - Resumen de textos.
    - Traducción específica.

**Many-Shots Prompts:**

- Eficaces cuando:
    - Las tareas requieren mayor contextualización.
    - Se manejan múltiples variaciones de una tarea.
- Ejemplos de Uso:
    - Generación de diferentes estilos de escritura.
    - Respuestas a preguntas variadas.

#### **Ejemplos Comparativos**

**One-Shot Prompt:**

```python
prompt_one_shot = """
Ejemplo:
Tarea: Resume el siguiente párrafo.
Respuesta: [Resumen]

Tarea: Resume el siguiente párrafo.
Respuesta:
"""
```

Many-Shots Prompt:

```python
prompt_many_shots = """
Ejemplo 1:
Tarea: Resume el siguiente párrafo.
Respuesta: [Resumen 1]

Ejemplo 2:
Tarea: Resume el siguiente párrafo.
Respuesta: [Resumen 2]

Tarea: Resume el siguiente párrafo.
Respuesta:
"""
```

Implementación con ModeloGenerativo
Podemos utilizar los métodos crear_one_shot_prompt y crear_many_shots_prompt de la clase ModeloGenerativo para implementar One-Shot y Many-Shots prompts.

```python
class ModeloGenerativo:
    # ... (código anterior)

    def crear_one_shot_prompt(self, tarea, ejemplo):
        return f"Ejemplo:\nTarea: {ejemplo['tarea']}\nRespuesta: {ejemplo['respuesta']}\n\nTarea: {tarea}\nRespuesta:"

    def crear_many_shots_prompt(self, tarea, ejemplos):
        prompt = ""
        for i, ejemplo in enumerate(ejemplos, 1):
            prompt += f"Ejemplo {i}:\nTarea: {ejemplo['tarea']}\nRespuesta: {ejemplo['respuesta']}\n\n"
        prompt += f"Tarea: {tarea}\nRespuesta:"
        return prompt
```

Integración con Chain of Thought:

Podemos combinar CoT con Many-Shots para proporcionar al modelo no solo ejemplos variados sino también una estructura lógica de razonamiento.

```python
class ModeloGPT(ModeloGenerativo):
    # ... (código anterior)

    def generar_texto_con_cot_many_shots(self, tarea, ejemplos, cot_steps_list):
        prompt = "Contexto: Eres un asistente de IA que ayuda a resolver problemas complejos paso a paso.\n\n"
        for i, (ejemplo, cot_steps) in enumerate(zip(ejemplos, cot_steps_list), 1):
            prompt += f"Ejemplo {i}:\n"
            prompt += f"Tarea: {ejemplo['tarea']}\n"
            prompt += f"Chain of Thought:\n{cot_steps}\nRespuesta: {ejemplo['respuesta']}\n\n"
        prompt += f"Tarea: {tarea}\nChain of Thought:\n"
        return self.generar_texto(prompt)
```

Ejemplo de Uso:


```python
if __name__ == "__main__":
    api_key = "tu_api_key_aquí"  # Reemplaza con tu clave API de OpenAI
    db = BaseDatos()
    modelo_gpt = ModeloGPT("GPT-4", "v1.0", api_key, db)
    
    tarea = "Determina el tiempo de encuentro de dos vehículos que viajan en direcciones opuestas."
    ejemplos = [
        {
            "tarea": "Determina el tiempo de encuentro de dos vehículos que viajan en direcciones opuestas.",
            "cot_steps": "1. Identificar las velocidades de ambos vehículos.\n2. Calcular la distancia total entre los vehículos.\n3. Establecer la ecuación de movimiento: tiempo = distancia / (velocidad1 + velocidad2).\n4. Resolver la ecuación para encontrar el tiempo de encuentro.",
            "respuesta": "El tiempo de encuentro es X horas."
        },
        {
            "tarea": "Calcula el tiempo necesario para que dos trenes se encuentren si uno viaja a 80 km/h y el otro a 60 km/h, estando separados por 300 km.",
            "cot_steps": "1. Sumar las velocidades de ambos trenes: 80 + 60 = 140 km/h.\n2. Calcular el tiempo: 300 / 140 ≈ 2.14 horas.\n3. Concluir que los trenes se encontrarán en aproximadamente 2.14 horas.",
            "respuesta": "Los trenes se encontrarán en aproximadamente 2.14 horas."
        }
    ]
    cot_steps_list = [
        "1. Identificar las velocidades de ambos vehículos.\n2. Calcular la distancia total entre los vehículos.\n3. Establecer la ecuación de movimiento: tiempo = distancia / (velocidad1 + velocidad2).\n4. Resolver la ecuación para encontrar el tiempo de encuentro.",
        "1. Sumar las velocidades de ambos trenes: 80 + 60 = 140 km/h.\n2. Calcular el tiempo: 300 / 140 ≈ 2.14 horas.\n3. Concluir que los trenes se encontrarán en aproximadamente 2.14 horas."
    ]
    
    texto_generado = modelo_gpt.generar_texto_con_cot_many_shots(tarea, ejemplos, cot_steps_list)
    print(texto_generado)
```

#### Ventajas y Desventajas

##### One-Shot Prompts:

Ventajas:
- Menor consumo de tokens.
- Más rápido de diseñar.

Desventajas:
- Menos robusto ante variaciones en la tarea.
- Mayor riesgo de respuestas inconsistentes.

##### Many-Shots Prompts:

Ventajas:
- Mejora la coherencia y precisión.
- Mayor flexibilidad para manejar variaciones.

Desventajas:
- Mayor consumo de tokens.
- Requiere más tiempo para diseñar y seleccionar ejemplos adecuados.


### 3. Técnicas Avanzadas de Prompting

#### Combinar Chain of Thought con Many-Shots

Integrar CoT con Many-Shots permite que el modelo no solo siga una secuencia lógica de pensamiento, sino que también se beneficie de múltiples ejemplos para mejorar la calidad de las respuestas.

Ejemplo de Prompt Combinado:

```python
contexto = "Contexto: Eres un asistente de IA que ayuda a resolver problemas complejos paso a paso."
tarea = "Determina el tiempo de encuentro de dos vehículos que viajan en direcciones opuestas."

prompt_combinado = f"""
{contexto}

Ejemplo 1:
Tarea: Determina el tiempo de encuentro de dos vehículos que viajan en direcciones opuestas.
Chain of Thought:
1. Identificar las velocidades de ambos vehículos.
2. Calcular la distancia total entre los vehículos.
3. Establecer la ecuación de movimiento: tiempo = distancia / (velocidad1 + velocidad2).
4. Resolver la ecuación para encontrar el tiempo de encuentro.
Respuesta:
El tiempo de encuentro es X horas.

Ejemplo 2:
Tarea: Calcula el tiempo necesario para que dos trenes se encuentren si uno viaja a 80 km/h y el otro a 60 km/h, estando separados por 300 km.
Chain of Thought:
1. Sumar las velocidades de ambos trenes: 80 + 60 = 140 km/h.
2. Calcular el tiempo: 300 / 140 ≈ 2.14 horas.
3. Concluir que los trenes se encontrarán en aproximadamente 2.14 horas.
Respuesta:
Los trenes se encontrarán en aproximadamente 2.14 horas.

Tarea: {tarea}
Chain of Thought:
"""
```


### Optimización de Prompts

- **Claridad y Precisión:** Asegúrate de que las instrucciones sean claras y específicas.
- **Uso de Plantillas:** Establece estructuras predefinidas para mantener la consistencia.
- **Evitar Ambigüedades:** Utiliza lenguaje directo para minimizar interpretaciones erróneas.

Ejemplo de Plantilla Optimizada:

```python
def formatear_prompt(contexto, ejemplos, tarea):
    prompt = f"{contexto}\n\n"
    for i, ejemplo in enumerate(ejemplos, 1):
        prompt += f"Ejemplo {i}:\n"
        prompt += f"Tarea: {ejemplo['tarea']}\n"
        prompt += f"Chain of Thought:\n{ejemplo['cot']}\nRespuesta: {ejemplo['respuesta']}\n\n"
    prompt += f"Tarea: {tarea}\nChain of Thought:"
    return prompt
```

Integración con las Clases de Python:

Utilizamos las clases ModeloGenerativo y ModeloGPT para implementar las técnicas avanzadas de prompting.

```python
class ModeloGPT(ModeloGenerativo):
    # ... (código anterior)

    def generar_texto_con_cot_many_shots(self, tarea, ejemplos, cot_steps_list):
        prompt = "Contexto: Eres un asistente de IA que ayuda a resolver problemas complejos paso a paso.\n\n"
        for i, (ejemplo, cot_steps) in enumerate(zip(ejemplos, cot_steps_list), 1):
            prompt += f"Ejemplo {i}:\n"
            prompt += f"Tarea: {ejemplo['tarea']}\n"
            prompt += f"Chain of Thought:\n{cot_steps}\nRespuesta: {ejemplo['respuesta']}\n\n"
        prompt += f"Tarea: {tarea}\nChain of Thought:\n"
        return self.generar_texto(prompt)
```

Ejemplo Completo de Uso:

```python
if __name__ == "__main__":
    api_key = "tu_api_key_aquí"  # Reemplaza con tu clave API de OpenAI
    db = BaseDatos()
    modelo_gpt = ModeloGPT("GPT-4", "v1.0", api_key, db)
    
    tarea = "Determina el tiempo de encuentro de dos vehículos que viajan en direcciones opuestas."
    ejemplos = [
        {
            "tarea": "Determina el tiempo de encuentro de dos vehículos que viajan en direcciones opuestas.",
            "cot_steps": "1. Identificar las velocidades de ambos vehículos.\n2. Calcular la distancia total entre los vehículos.\n3. Establecer la ecuación de movimiento: tiempo = distancia / (velocidad1 + velocidad2).\n4. Resolver la ecuación para encontrar el tiempo de encuentro.",
            "respuesta": "El tiempo de encuentro es X horas."
        },
        {
            "tarea": "Calcula el tiempo necesario para que dos trenes se encuentren si uno viaja a 80 km/h y el otro a 60 km/h, estando separados por 300 km.",
            "cot_steps": "1. Sumar las velocidades de ambos trenes: 80 + 60 = 140 km/h.\n2. Calcular el tiempo: 300 / 140 ≈ 2.14 horas.\n3. Concluir que los trenes se encontrarán en aproximadamente 2.14 horas.",
            "respuesta": "Los trenes se encontrarán en aproximadamente 2.14 horas."
        }
    ]
    cot_steps_list = [
        "1. Identificar las velocidades de ambos vehículos.\n2. Calcular la distancia total entre los vehículos.\n3. Establecer la ecuación de movimiento: tiempo = distancia / (velocidad1 + velocidad2).\n4. Resolver la ecuación para encontrar el tiempo de encuentro.",
        "1. Sumar las velocidades de ambos trenes: 80 + 60 = 140 km/h.\n2. Calcular el tiempo: 300 / 140 ≈ 2.14 horas.\n3. Concluir que los trenes se encontrarán en aproximadamente 2.14 horas."
    ]
    
    texto_generado = modelo_gpt.generar_texto_con_cot_many_shots(tarea, ejemplos, cot_steps_list)
    print(texto_generado)
```

#### Beneficios y Limitaciones

**One-Shot Prompts:**

Ventajas:
- Menor consumo de tokens.
- Más rápido de diseñar.

Desventajas:
- Menos robusto ante variaciones en la tarea.
- Mayor riesgo de respuestas inconsistentes.

**Many-Shots Prompts:**

Ventajas:
- Mejora la coherencia y precisión.
- Mayor flexibilidad para manejar variaciones.

Desventajas:
- Mayor consumo de tokens.
- Requiere más tiempo para diseñar y seleccionar ejemplos adecuados.

### 4. Integración con Clases de Python

#### Clase ModeloGenerativo

La clase ModeloGenerativo proporciona una base para manejar prompts y generar textos. Hemos extendido esta clase para incluir métodos específicos que permiten la incorporación de técnicas avanzadas como Chain of Thought y Many-Shots.

```python
class ModeloGenerativo:
    def __init__(self, nombre, version):
        self._nombre = nombre
        self._version = version

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, valor):
        self._version = valor

    def cargar_modelo(self):
        # Código para cargar el modelo
        pass

    def generar_texto(self, prompt):
        # Código para generar texto basado en el prompt
        pass

    def limpiar_prompt(self, prompt):
        prompt = prompt.strip()
        prompt = prompt.capitalize()
        return prompt

    def formatear_prompt(self, plantilla, variables):
        try:
            prompt_formateado = plantilla.format(**variables)
            return prompt_formateado
        except KeyError as e:
            print(f"Error: Falta la variable {e} en el diccionario de variables.")
            return plantilla

    def crear_one_shot_prompt(self, tarea, ejemplo):
        return f"Ejemplo:\nTarea: {ejemplo['tarea']}\nRespuesta: {ejemplo['respuesta']}\n\nTarea: {tarea}\nRespuesta:"

    def crear_many_shots_prompt(self, tarea, ejemplos):
        prompt = ""
        for i, ejemplo in enumerate(ejemplos, 1):
            prompt += f"Ejemplo {i}:\nTarea: {ejemplo['tarea']}\nRespuesta: {ejemplo['respuesta']}\n\n"
        prompt += f"Tarea: {tarea}\nRespuesta:"
        return prompt
```

#### Clase ModeloGPT

La clase ModeloGPT hereda de ModeloGenerativo y añade funcionalidades específicas para interactuar con la API de OpenAI, incluyendo la incorporación de Chain of Thought y Many-Shots.

```python
import requests
from database import BaseDatos

class ModeloGPT(ModeloGenerativo):
    def __init__(self, nombre, version, api_key, db: BaseDatos):
        super().__init__(nombre, version)
        self.api_key = api_key
        self.url = "https://api.openai.com/v1/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.db = db

    def generar_texto_con_cot(self, prompt, cot_steps):
        prompt_cot = f"""
        {prompt}

        Chain of Thought:
        {cot_steps}

        Respuesta:
        """
        prompt_limpio = self.limpiar_prompt(prompt_cot)
        payload = {
            "model": "text-davinci-003",
            "prompt": prompt_limpio,
            "max_tokens": 150,
            "temperature": 0.7
        }
        response = requests.post(self.url, headers=self.headers, json=payload)
        if response.status_code == 200:
            texto_generado = response.json()["choices"][0]["text"].strip()
            self.db.guardar_interaccion(prompt_limpio, texto_generado)
            return texto_generado
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    def generar_texto_con_cot_many_shots(self, tarea, ejemplos, cot_steps_list):
        prompt = "Contexto: Eres un asistente de IA que ayuda a resolver problemas complejos paso a paso.\n\n"
        for i, (ejemplo, cot_steps) in enumerate(zip(ejemplos, cot_steps_list), 1):
            prompt += f"Ejemplo {i}:\n"
            prompt += f"Tarea: {ejemplo['tarea']}\n"
            prompt += f"Chain of Thought:\n{cot_steps}\nRespuesta: {ejemplo['respuesta']}\n\n"
        prompt += f"Tarea: {tarea}\nChain of Thought:\n"
        return self.generar_texto(prompt)
```

#### Clase BaseDatos

La clase BaseDatos maneja las operaciones de la base de datos SQLite para almacenar prompts y respuestas generadas.

```python
import sqlite3

class BaseDatos:
    def __init__(self, nombre_db="interacciones.db"):
        self.conn = sqlite3.connect(nombre_db)
        self.cursor = self.conn.cursor()
        self.crear_tabla()

    def crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS interacciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt TEXT NOT NULL,
                respuesta TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def guardar_interaccion(self, prompt, respuesta):
        self.cursor.execute("""
            INSERT INTO interacciones (prompt, respuesta)
            VALUES (?, ?)
        """, (prompt, respuesta))
        self.conn.commit()

    def obtener_interacciones(self, limite=5):
        self.cursor.execute("""
            SELECT prompt, respuesta FROM interacciones
            ORDER BY id DESC
            LIMIT ?
        """, (limite,))
        return self.cursor.fetchall()

    def cerrar_conexion(self):
        self.conn.close()

if __name__ == "__main__":
    db = BaseDatos()
    db.guardar_interaccion("Ejemplo de prompt", "Ejemplo de respuesta")
    interacciones = db.obtener_interacciones()
    for interaccion in interacciones:
        print(f"Prompt: {interaccion[0]}\nRespuesta: {interaccion[1]}\n")
    db.cerrar_conexion()
```


#### Integración Completa: Aplicación Principal

Desarrollamos un script app.py que combina todas las funcionalidades y permite la interacción del usuario, integrando CoT y Many-Shots con las clases de Python.

```python
from modelo_generativo import ModeloGPT
from database import BaseDatos

def main():
    api_key = "tu_api_key_aquí"  # Reemplaza con tu clave API de OpenAI
    db = BaseDatos()
    modelo = ModeloGPT("GPT-4", "v1.0", api_key, db)

    print("=== Generador de Prompts Avanzado con Chain of Thought y Many-Shots ===")
    while True:
        tarea = input("Ingresa la tarea para generar texto (o 'salir' para terminar): ")
        if tarea.lower() == 'salir':
            break
        
        tipo_prompt = input("Selecciona el tipo de prompt (cot_one, cot_many, one, many): ").lower()
        
        if tipo_prompt == 'cot_one':
            ejemplo = {}
            ejemplo['tarea'] = input("Ingresa una tarea de ejemplo: ")
            ejemplo['cot_steps'] = input("Ingresa los pasos de Chain of Thought para el ejemplo: ")
            ejemplo['respuesta'] = input("Ingresa la respuesta para el ejemplo: ")
            texto_generado = modelo.generar_texto_con_cot(tarea, ejemplo['cot_steps'])
            print(f"\n**Respuesta Generada con CoT One-Shot:**\n{texto_generado}\n{'-'*50}")
        
        elif tipo_prompt == 'cot_many':
            try:
                num_ejemplos = int(input("¿Cuántos ejemplos deseas ingresar? "))
            except ValueError:
                print("Por favor, ingresa un número válido.")
                continue
            ejemplos = []
            cot_steps_list = []
            for i in range(num_ejemplos):
                print(f"\nEjemplo {i+1}:")
                tarea_ejemplo = input("Ingresa la tarea de ejemplo: ")
                cot_steps = input("Ingresa los pasos de Chain of Thought para el ejemplo: ")
                respuesta_ejemplo = input("Ingresa la respuesta para el ejemplo: ")
                ejemplos.append({"tarea": tarea_ejemplo, "cot": cot_steps, "respuesta": respuesta_ejemplo})
                cot_steps_list.append(cot_steps)
            texto_generado = modelo.generar_texto_con_cot_many_shots(tarea, ejemplos, cot_steps_list)
            print(f"\n**Respuesta Generada con CoT Many-Shots:**\n{texto_generado}\n{'-'*50}")
        
        elif tipo_prompt == 'one':
            ejemplo = {}
            ejemplo['tarea'] = input("Ingresa una tarea de ejemplo: ")
            ejemplo['respuesta'] = input("Ingresa la respuesta para el ejemplo: ")
            prompt_one_shot = modelo.crear_one_shot_prompt(tarea, ejemplo)
            texto_generado = modelo.generar_texto(prompt_one_shot)
            print(f"\n**Respuesta Generada con One-Shot:**\n{texto_generado}\n{'-'*50}")
        
        elif tipo_prompt == 'many':
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
            prompt_many_shots = modelo.crear_many_shots_prompt(tarea, ejemplos)
            texto_generado = modelo.generar_texto(prompt_many_shots)
            print(f"\n**Respuesta Generada con Many-Shots:**\n{texto_generado}\n{'-'*50}")
        
        else:
            print("Tipo de prompt no reconocido. Por favor, elige entre 'cot_one', 'cot_many', 'one', o 'many'.")
    
    print("Guardando y cerrando la aplicación...")
    db.cerrar_conexion()

if __name__ == "__main__":
    main()
```

Ejemplo de Uso:

```
=== Generador de Prompts Avanzado con Chain of Thought y Many-Shots ===
Ingresa la tarea para generar texto (o 'salir' para terminar): Calcula el área de un triángulo.
Selecciona el tipo de prompt (cot_one, cot_many, one, many): cot_one

Ingresa una tarea de ejemplo: Calcula el área de un triángulo.
Ingresa los pasos de Chain of Thought para el ejemplo: 1. Identificar la fórmula del área de un triángulo: (base * altura) / 2. 2. Sustituir los valores de base y altura. 3. Realizar la multiplicación y división para obtener el área.
Ingresa la respuesta para el ejemplo: El área del triángulo es X unidades cuadradas.

**Respuesta Generada con CoT One-Shot:**
El área del triángulo es X unidades cuadradas.
--------------------------------------------------
```

Este script proporciona una interfaz interactiva para generar texto utilizando técnicas avanzadas de Chain of Thought y Many-Shots, permitiendo al usuario seleccionar el tipo de prompt y proporcionar los datos necesarios para generar respuestas precisas y coherentes.

### 5. Beneficios y Limitaciones de las Técnicas Avanzadas

#### Beneficios:

**Chain of Thought (CoT):**

- Mayor Precisión: Al desglosar el problema en pasos, se reduce la probabilidad de errores.
- Transparencia: Facilita la comprensión del razonamiento del modelo.
- Flexibilidad: Se puede aplicar a una amplia gama de tareas complejas.

**One-Shot vs Many-Shots:**

**One-Shot:**
- Rapidez: Menor tiempo de diseño.
- Eficiencia: Consume menos tokens.

**Many-Shots:**
- Robustez: Mejor manejo de variaciones en las tareas.
- Calidad: Respuestas más coherentes y precisas.

#### Limitaciones:

**Chain of Thought (CoT):**
- Consumo de Tokens: Los pasos intermedios aumentan la cantidad de tokens utilizados.
- Complejidad: Requiere una estructuración cuidadosa del prompt.

**One-Shot vs Many-Shots:**

**One-Shot:**
- Menor Robustez: Puede no manejar bien variaciones en la tarea.
- Consistencia: Mayor riesgo de respuestas inconsistentes.

**Many-Shots:**
- Mayor Consumo de Tokens: Necesita más ejemplos, lo que aumenta el uso de tokens.
- Tiempo de Diseño: Requiere más tiempo para seleccionar y diseñar ejemplos adecuados.


### Preguntas Frecuentes

#### ¿Cómo determino el contexto adecuado para un prompt?

Analiza el propósito de la tarea y qué información adicional puede ayudar al modelo a entender mejor lo que se espera. Por ejemplo, si el asistente debe resolver un problema matemático, especifica que debe hacerlo paso a paso y detalla el tipo de problema.

#### ¿Qué tipo de prompt debo usar para obtener una respuesta más detallada?

Los Few-Shot Prompts suelen generar respuestas más detalladas ya que el modelo recibe varios ejemplos que guían su comportamiento.

```python
ejemplos_few_shot = [
    {
        "tarea": "Describe los beneficios de la inteligencia artificial en la educación.",
        "cot": "1. Identificar los beneficios clave como la personalización del aprendizaje.\n2. Explicar cómo optimiza la gestión de recursos educativos.\n3. Concluir con ejemplos específicos de aplicaciones.",
        "respuesta": "La inteligencia artificial en la educación permite la personalización del aprendizaje y optimiza la gestión de recursos, mejorando la eficiencia y adaptándose a las necesidades individuales de cada estudiante."
    },
    {
        "tarea": "Describe los beneficios de la inteligencia artificial en la salud.",
        "cot": "1. Mejorar el diagnóstico temprano de enfermedades.\n2. Optimizar tratamientos personalizados.\n3. Gestionar eficientemente grandes volúmenes de datos médicos.",
        "respuesta": "La inteligencia artificial en la salud mejora el diagnóstico temprano y personaliza tratamientos para pacientes, además de gestionar eficientemente los datos médicos, lo que resulta en una atención más efectiva y precisa."
    }
]
```

#### ¿Es posible combinar distintos tipos de prompts en una sola solicitud?

Sí, puedes combinar Chain of Thought con One-Shot o Many-Shots prompts para adaptar la complejidad y el detalle de las respuestas según tus necesidades específicas.

```python
contexto = "Contexto: Eres un asistente de IA que ayuda a escribir artículos científicos."
ejemplos = [
    {
        "tarea": "Describe los beneficios de la inteligencia artificial en la educación.",
        "cot": "1. Identificar los beneficios clave como la personalización del aprendizaje.\n2. Explicar cómo optimiza la gestión de recursos educativos.\n3. Concluir con ejemplos específicos de aplicaciones.",
        "respuesta": "La inteligencia artificial en la educación permite la personalización del aprendizaje y optimiza la gestión de recursos, mejorando la eficiencia y adaptándose a las necesidades individuales de cada estudiante."
    },
    {
        "tarea": "Describe los beneficios de la inteligencia artificial en la salud.",
        "cot": "1. Mejorar el diagnóstico temprano de enfermedades.\n2. Optimizar tratamientos personalizados.\n3. Gestionar eficientemente grandes volúmenes de datos médicos.",
        "respuesta": "La inteligencia artificial en la salud mejora el diagnóstico temprano y personaliza tratamientos para pacientes, además de gestionar eficientemente los datos médicos, lo que resulta en una atención más efectiva y precisa."
    }
]
tarea = "Describe los beneficios de la inteligencia artificial en la agricultura."

prompt_combinado = formatear_prompt(contexto, ejemplos, tarea)
texto = modelo_gpt.generar_texto(prompt_combinado)
```

Si tienes alguna pregunta adicional o necesitas más detalles sobre algún tema específico, ¡no dudes en preguntar!

