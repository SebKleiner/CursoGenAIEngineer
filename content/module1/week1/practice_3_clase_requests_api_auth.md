# Requests, APIs y Authentication para Tareas de Generative AI - Práctica (45 minutos)

## Descripción

En esta sesión práctica, profundizarás en el uso de la librería `requests` en Python para interactuar con APIs, implementando autenticación y manejando respuestas de manera efectiva. Además, integrarás estas habilidades en un proyecto de GenAI, estableciendo las bases para la comunicación con APIs externas como la de OpenAI. A través de ejercicios estructurados, aprenderás a realizar solicitudes HTTP, manejar autenticación, y definir especificaciones claras para tu proyecto final.

## Objetivos

- **Utilizar la librería `requests`** para realizar solicitudes HTTP en Python.
- **Implementar autenticación** en las solicitudes a APIs.
- **Interactuar con APIs externas**, específicamente la API de OpenAI.
- **Definir y documentar especificaciones del proyecto**, asegurando una base sólida para el desarrollo.
- **Integrar prácticas de manejo de APIs** en un mini-proyecto de GenAI.

## Actividades

### 1. Uso de la Librería `requests`

#### **Ejercicio 1: Realizar Solicitudes GET y POST**

**Objetivo:** Familiarizarse con las operaciones básicas de la librería `requests` para interactuar con APIs mediante solicitudes GET y POST.

**Instrucciones:**

1. **Instalación de la librería `requests`:**

    Asegúrate de tener instalada la librería `requests`. Si no la tienes, instálala utilizando pip:

    ```bash
    pip install requests
    ```

2. **Realizar una Solicitud GET:**

    - Crea un archivo llamado `api_requests.py`.
    - Implementa una función para realizar una solicitud GET a una API pública (por ejemplo, la API de Public APIs).

    ```python
    import requests

    def obtener_imagen_perro(url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Lanza error si la respuesta no es 200
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")
            return None

    if __name__ == "__main__":
        url_get = "https://dog.ceo/api/breeds/image/random"
        datos = obtener_imagen_perro(url_get)
        if datos:
            print(f"Imagen de perro: {datos['message']}")
        else:
            print("No se pudo obtener la información.")
    ```

3. **Realizar una Solicitud POST:**

    - Implementa una función para realizar una solicitud POST a una API de prueba como httpbin.org.
    
    ```python
    import requests

    def enviar_datos_api(url, payload, headers=None):
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

    if __name__ == "__main__":
        url_post = "https://httpbin.org/post"
        payload = {"clave": "valor"}
        headers = {"Content-Type": "application/json"}
        respuesta = enviar_datos_api(url_post, payload, headers)
        if respuesta:
            print("Datos enviados exitosamente:")
            print(respuesta)
    ```

**Recursos:**
- [Requests Documentation](https://requests.readthedocs.io/en/latest/)
- [Real Python - Python Requests Module](https://realpython.com/python-requests/)
- [W3Schools - Python HTTP Requests](https://www.w3schools.com/python/module_requests.asp)

### 2. Implementación de Autenticación en APIs

#### **Ejercicio 2: Autenticación con la API de OpenAI**

**Objetivo:** Implementar autenticación para interactuar de manera segura con la API de OpenAI utilizando una clave API.

**Instrucciones:**

1. **Obtener una Clave API de OpenAI:**

    - Regístrate en [OpenAI](https://openai.com/) y genera una clave API desde el panel de control.

2. **Realizar una Solicitud Autenticada:**

    - Modifica el archivo `api_requests.py` para incluir una función que realice una solicitud POST a la API de OpenAI para generar texto.

    ```python
    import requests

    class ModeloOpenAI:
        def __init__(self, api_key):
            self.api_key = api_key
            self.url = "https://api.openai.com/v1/chat/completions"
            self.headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

        def generar_texto(self, prompt, modelo="gpt-3.5-turbo", max_tokens=150):
            messages = [
                {"role": "system", "content": "Eres un asistente de IA que ayuda a generar textos."},
                {"role": "user", "content": prompt},
            ]
            payload = {
                "model": modelo,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
            response = requests.post(self.url, headers=self.headers, json=payload)
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"].strip()
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

    if __name__ == "__main__":
        api_key = "API_KEY_OPENAI"  # Reemplaza con tu clave API de OpenAI
        modelo_openai = ModeloOpenAI(api_key)
        prompt = "Escribe un poema sobre la inteligencia artificial."
        texto_generado = modelo_openai.generar_texto(prompt)
        if texto_generado:
            print("Texto Generado por OpenAI:")
            print(texto_generado)
    ```

3. **Pruebas de la Solicitud Autenticada:**

    - Ejecuta el script y verifica que se genere el texto correctamente.

    ```bash
    python api_requests.py
    ```

**Recursos:**
- [OpenAI API Documentation](https://beta.openai.com/docs/api-reference/introduction)
- [Real Python - Using APIs with Python](https://realpython.com/python-api/)
- [OpenAI - How to Use the API](https://beta.openai.com/docs/introduction)

### 3. Integración con APIs Externas

#### **Ejercicio 3: Integración de la API de OpenAI en un Proyecto de GenAI**

**Objetivo:** Integrar la funcionalidad de generación de texto de la API de OpenAI en un mini-proyecto de GenAI, estableciendo una base para futuras expansiones.

**Instrucciones:**

1. **Definir las Especificaciones del Proyecto:**

    - Crea un documento `especificaciones_proyecto.md` donde defines los objetivos, funcionalidades y alcance de tu proyecto.

    **Ejemplo de Especificaciones:**

    ```markdown
    # Generador de Textos Personalizado con GenAI

    ## Objetivos
    - Desarrollar una aplicación que permita a los usuarios ingresar prompts y generar textos utilizando la API de OpenAI.
    - Almacenar prompts y respuestas en una base de datos para futuras referencias.
    - Implementar una interfaz de usuario sencilla para interactuar con el generador de textos.

    ## Funcionalidades
    - **Ingreso de Prompts:** Los usuarios pueden ingresar prompts personalizados.
    - **Generación de Textos:** Utilizar la API de OpenAI para generar textos basados en los prompts.
    - **Almacenamiento de Interacciones:** Guardar prompts y respuestas en una base de datos.
    - **Historial de Generaciones:** Mostrar un historial de las últimas interacciones.

    ## Alcance
    - Implementación básica con una interfaz de línea de comandos.
    - Uso de SQLite para el almacenamiento de datos.
    - Posibilidad de expandir a una interfaz web en futuras versiones.
    ```

2. **Implementar el Almacenamiento de Datos:**

    - Utiliza SQLite para almacenar prompts y respuestas.
    - Crea un archivo `database.py` para manejar las operaciones de la base de datos.

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

3. **Integrar la Base de Datos con el Modelo OpenAI:**

    - Modifica la clase `ModeloOpenAI` para guardar automáticamente cada interacción en la base de datos.

    ```python
    class ModeloOpenAI:
        def __init__(self, api_key):
            self.api_key = api_key
            self.url = "https://api.openai.com/v1/chat/completions"
            self.headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

        def generar_texto(self, prompt, modelo="gpt-3.5-turbo", max_tokens=150):
            messages = [
                {"role": "system", "content": "Eres un asistente de IA que ayuda a generar textos."},
                {"role": "user", "content": prompt},
            ]
            payload = {
                "model": modelo,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
            response = requests.post(self.url, headers=self.headers, json=payload)
            if response.status_code == 200:
                texto_generado = response.json()["choices"][0]["message"]["content"].strip()
                self.db.guardar_interaccion(prompt, texto_generado)
                return texto_generado
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

    if __name__ == "__main__":
        api_key = "API_KEY_OPENAI"  # Reemplaza con tu clave API de OpenAI
        db = BaseDatos()
        modelo_openai = ModeloOpenAI(api_key)
        prompt = "Escribe un poema sobre la inteligencia artificial."
        texto_generado = modelo_openai.generar_texto(prompt)
        if texto_generado:
            print("Texto Generado por OpenAI:")
            print(texto_generado)
        db.cerrar_conexion()
    ```


4. **Crear la Aplicación Principal:**

    - Desarrolla un script `app.py` que combine todas las funcionalidades y permita la interacción del usuario.

    ```python
    from modelo_openai import ModeloOpenAI
    from database import BaseDatos

    def main():
        api_key = "tu_api_key_aquí"  # Reemplaza con tu clave API de OpenAI
        db = BaseDatos()
        modelo = ModeloOpenAI(api_key, db)

        print("=== Generador de Textos Personalizado con GenAI ===")
        while True:
            prompt = input("Ingresa tu prompt (o 'salir' para terminar): ")
            if prompt.lower() == 'salir':
                break
            texto_generado = modelo.generar_texto(prompt)
            if texto_generado:
                print("\n**Respuesta Generada:**")
                print(texto_generado)
                print("-" * 50)
        
        print("Guardando y cerrando la aplicación...")
        db.cerrar_conexion()

    if __name__ == "__main__":
        main()
    ```

**Recursos:**
- [SQLite3 Documentation](https://docs.python.org/3/library/sqlite3.html)
- [Real Python - Working with SQLite in Python](https://realpython.com/python-sql-libraries/)
- [Python SQLite Tutorial](https://www.sqlitetutorial.net/sqlite-python/)
- [OpenAI API Usage](https://beta.openai.com/docs/api-reference/introduction)

### 4. Mini-Proyecto Integrado

#### **Ejercicio 4: Desarrollo del Mini-Proyecto de Generación de Textos**

**Objetivo:** Aplicar todos los conocimientos adquiridos en la sesión para desarrollar una aplicación completa que permita la generación de textos personalizados, integrando OOP, manejo de strings, solicitudes HTTP, autenticación y almacenamiento de datos.

**Instrucciones:**

1. **Estructura del Proyecto:**

    - Organiza tu proyecto en los siguientes archivos:
        - `modelo_generativo.py`: Contiene las clases base y subclases para la generación de textos.
        - `database.py`: Maneja las operaciones de la base de datos.
        - `app.py`: Script principal para la interacción con el usuario.
        - `especificaciones_proyecto.md`: Documento de especificaciones.
    
    2. **Implementación Completa:**

        - **modelo_generativo.py:**
        
            ```python
            import requests
            from database import BaseDatos

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


                def generar_texto(self, prompt, modelo="gpt-3.5-turbo", max_tokens=150):
                    messages = [
                        {"role": "system", "content": "Eres un asistente de IA que ayuda a generar textos."},
                        {"role": "user", "content": prompt},
                    ]
                    payload = {
                        "model": modelo,
                        "messages": messages,
                        "max_tokens": max_tokens,
                        "temperature": 0.7
                    }
                    response = requests.post(self.url, headers=self.headers, json=payload)
                    if response.status_code == 200:
                        texto_generado = response.json()["choices"][0]["message"]["content"].strip()
                        self.db.guardar_interaccion(prompt, texto_generado)
                        return texto_generado
                    else:
                        print(f"Error: {response.status_code} - {response.text}")
                        return None
            ```

        - **database.py:**
        
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

        - **app.py:**
        
            ```python
            from modelo_generativo import ModeloGPT
            from database import BaseDatos

            def main():
                api_key = "tu_api_key_aquí"  # Reemplaza con tu clave API de OpenAI
                db = BaseDatos()
                modelo = ModeloGPT("GPT-4", "v1.0", api_key, db)

                print("=== Generador de Textos Personalizado con GenAI ===")
                while True:
                    plantilla = input("Ingresa una plantilla de prompt (o 'salir' para terminar): ")
                    if plantilla.lower() == 'salir':
                        break
                    try:
                        num_variables = int(input("¿Cuántas variables deseas ingresar? "))
                    except ValueError:
                        print("Por favor, ingresa un número válido.")
                        continue
                    variables = {}
                    for _ in range(num_variables):
                        clave = input("Nombre de la variable: ")
                        valor = input(f"Valor para '{clave}': ")
                        variables[clave] = valor

                    texto_generado = modelo.generar_texto(plantilla, variables)
                    if texto_generado:
                        print(f"\n**Respuesta Generada:**\n{texto_generado}\n{'-'*50}")
                    else:
                        print("No se pudo generar el texto.")

                print("Guardando y cerrando la aplicación...")
                db.cerrar_conexion()

            if __name__ == "__main__":
                main()
            ```

    3. **Ejecutar la Aplicación:**

        - Asegúrate de haber reemplazado `"tu_api_key_aquí"` con tu clave API de OpenAI en `app.py`.
        - Ejecuta la aplicación:

        ```bash
        python app.py
        ```

        - **Ejemplo de Uso:**

            ```
            === Generador de Textos Personalizado con GenAI ===
            Ingresa una plantilla de prompt (o 'salir' para terminar): Escribe un artículo sobre {tema} que incluya {detalle}.
            ¿Cuántas variables deseas ingresar? 2
            Nombre de la variable: tema
            Valor para 'tema': la inteligencia artificial en la educación
            Nombre de la variable: detalle
            Valor para 'detalle': los beneficios de personalizar el aprendizaje

            **Respuesta Generada:**
            Texto generado por GPT-4 versión v1.0 para el prompt: Escribe un artículo sobre la inteligencia artificial en la educación que incluya los beneficios de personalizar el aprendizaje.
            --------------------------------------------------
            ```

**Recursos:**
- [SQLite3 Documentation](https://docs.python.org/3/library/sqlite3.html)
- [Real Python - Working with SQLite in Python](https://realpython.com/python-sql-libraries/)
- [Python SQLite Tutorial](https://www.sqlitetutorial.net/sqlite-python/)
- [OpenAI API Usage](https://beta.openai.com/docs/api-reference/introduction)
- [Python Requests Module](https://docs.python-requests.org/en/latest/)

## Relación con Generative AI

Estos ejercicios prácticos te permiten integrar múltiples conceptos de Python y OOP en un proyecto de Generative AI. Al manejar solicitudes HTTP y autenticación con APIs externas, estableces una base sólida para interactuar con modelos de lenguaje avanzados como los de OpenAI. Además, al implementar una base de datos para almacenar interacciones, aseguras la escalabilidad y mantenibilidad de tu aplicación, aspectos cruciales en proyectos de GenAI.

## Conclusión

Al finalizar esta sesión práctica, habrás adquirido habilidades clave para interactuar con APIs externas utilizando Python, implementar autenticación segura, y gestionar datos eficientemente en un proyecto de Generative AI. Estas competencias te permitirán desarrollar aplicaciones más robustas y escalables, aprovechando al máximo las capacidades de los modelos generativos en tus proyectos de inteligencia artificial.

---
