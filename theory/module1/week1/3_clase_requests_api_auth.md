# Introducción a Python - Requests, Autenticación y APIs para Tareas de Generative AI (45 minutos)

## Descripción

En esta sesión teórica, exploraremos el uso de la librería `requests` en Python para interactuar con APIs externas, implementando mecanismos de autenticación y manejando respuestas de manera efectiva. Nos enfocaremos en cómo estas herramientas son fundamentales para desarrollar aplicaciones de **Inteligencia Artificial Generativa (GenAI)**, permitiendo la comunicación fluida con modelos avanzados como los proporcionados por OpenAI. A través de ejemplos prácticos y conceptos clave, consolidarás tu comprensión sobre cómo integrar APIs en tus proyectos de GenAI.

## Objetivos

- **Comprender el protocolo HTTP** y las operaciones básicas de comunicación con APIs.
- **Aprender a utilizar la librería `requests`** en Python para realizar solicitudes HTTP.
- **Implementar mecanismos de autenticación** para acceder a APIs seguras.
- **Manejar respuestas y errores** al interactuar con APIs externas.
- **Aplicar estos conceptos en el contexto de GenAI**, optimizando la integración con modelos generativos.

## Contenidos

### 1. Fundamentos de HTTP y APIs

#### **¿Qué es HTTP?**
HTTP (**HyperText Transfer Protocol**) es el protocolo fundamental para la comunicación en la web. Define cómo los mensajes son formateados y transmitidos, y qué acciones deben tomar los servidores y navegadores en respuesta a diversos comandos.

#### **Componentes Clave de HTTP:**
- **Métodos HTTP:**
  - **GET:** Solicita datos de un recurso específico.
  - **POST:** Envía datos al servidor para crear o actualizar un recurso.
  - **PUT:** Actualiza un recurso existente.
  - **DELETE:** Elimina un recurso específico.
- **URLs y Endpoints:**
  - **URL (Uniform Resource Locator):** Dirección que se utiliza para acceder a recursos en la web.
  - **Endpoint:** Punto final de comunicación en una API donde se pueden realizar solicitudes.

#### **¿Qué es una API?**
Una **API (Application Programming Interface)** es un conjunto de definiciones y protocolos que permiten que diferentes aplicaciones se comuniquen entre sí. En el contexto de GenAI, las APIs permiten interactuar con modelos de lenguaje avanzados para generar texto, imágenes y más.

### 2. Introducción a la Librería `requests` en Python

#### **¿Por qué `requests`?**
La librería `requests` es una de las más populares y sencillas de usar para realizar solicitudes HTTP en Python. Proporciona una interfaz amigable para interactuar con APIs sin necesidad de manejar los detalles de bajo nivel del protocolo HTTP.

#### **Instalación de `requests`:**

```bash
pip install requests
```

#### Estructura Básica de una Solicitud:

```python
import requests

# Realizar una solicitud GET
response = requests.get('https://api.example.com/data')

# Verificar el estado de la respuesta
if response.status_code == 200:
    datos = response.json()
    print(datos)
else:
    print(f"Error: {response.status_code}")
```

### 3. Realización de Solicitudes HTTP

#### Solicitudes GET:
Utilizadas para solicitar datos de un servidor. No deben modificar el estado del recurso.

Ejemplo: Obtener una lista de APIs públicas

```python
import requests

def obtener_apis_publicas():
    url = "https://api.publicapis.org/entries"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

datos = obtener_apis_publicas()
if datos:
    print(f"Total de APIs disponibles: {len(datos['entries'])}")
```

#### Solicitudes POST:
Utilizadas para enviar datos al servidor, por ejemplo, para crear un nuevo recurso.

Ejemplo: Enviar datos a una API de prueba

```python
import requests

def enviar_datos_api():
    url = "https://httpbin.org/post"
    payload = {"clave": "valor"}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

respuesta = enviar_datos_api()
if respuesta:
    print("Datos enviados exitosamente:")
    print(respuesta)
```

### 4. Autenticación en APIs

#### ¿Por qué es importante la autenticación?
La autenticación asegura que solo usuarios autorizados puedan acceder a los recursos de una API. Protege los datos y garantiza que las solicitudes sean legítimas.

#### Métodos Comunes de Autenticación:
API Keys: Claves únicas proporcionadas por la API para identificar al usuario.
Bearer Tokens: Tokens de acceso que se incluyen en los encabezados de las solicitudes.
OAuth: Protocolo de autorización que permite a las aplicaciones acceder a los recursos de los usuarios sin exponer sus credenciales.

#### Implementación de API Keys:
Ejemplo: Autenticación con la API de OpenAI

```python
import requests

class ModeloOpenAI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://api.openai.com/v1/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generar_texto(self, prompt, modelo="text-davinci-003", max_tokens=150):
        payload = {
            "model": modelo,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        response = requests.post(self.url, headers=self.headers, json=payload)
        if response.status_code == 200:
            return response.json()["choices"][0]["text"].strip()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

if __name__ == "__main__":
    api_key = "tu_api_key_aquí"  # Reemplaza con tu clave API de OpenAI
    modelo_openai = ModeloOpenAI(api_key)
    prompt = "Escribe un poema sobre la inteligencia artificial."
    texto_generado = modelo_openai.generar_texto(prompt)
    if texto_generado:
        print("Texto Generado por OpenAI:")
        print(texto_generado)
```

### 5. Manejo de Respuestas y Errores

#### Verificación de Estado de la Respuesta:

Siempre es importante verificar el código de estado de la respuesta para manejar errores adecuadamente.

```python
response = requests.get(url)
if response.status_code == 200:
    datos = response.json()
    # Procesar datos
else:
    print(f"Error: {response.status_code} - {response.text}")
```

#### Manejo de Excepciones:
Utiliza bloques try-except para capturar y manejar excepciones que puedan ocurrir durante las solicitudes.

```python
import requests

def obtener_datos_con_excepcion(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza una excepción para códigos de estado 4xx/5xx
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Error de conexión: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Tiempo de espera agotado: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Error inesperado: {req_err}")
    return None
```


### 6. Integración con Generative AI

#### Caso de Estudio: API de OpenAI para Generación de Textos

Objetivo: Integrar la API de OpenAI en una aplicación para generar textos basados en prompts proporcionados por el usuario.

#### Pasos:

1. Configuración Inicial:

* Obtén una clave API de OpenAI.
* Instala la librería requests.

2. Definición de la Clase ModeloOpenAI:

* Maneja la autenticación y las solicitudes a la API.
* Implementa métodos para generar texto y manejar respuestas.

3. Implementación y Pruebas:

* Crea instancias de la clase y prueba la generación de textos con diferentes prompts.
* Maneja errores y valida las respuestas recibidas.

Ejemplo Completo:

```python
import requests

class ModeloOpenAI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://api.openai.com/v1/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generar_texto(self, prompt, modelo="text-davinci-003", max_tokens=150):
        payload = {
            "model": modelo,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        try:
            response = requests.post(self.url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["text"].strip()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Error en la solicitud: {req_err}")
        return None

if __name__ == "__main__":
    api_key = "tu_api_key_aquí"  # Reemplaza con tu clave API de OpenAI
    modelo_openai = ModeloOpenAI(api_key)
    prompt = "Escribe un cuento sobre un robot que aprende a sentir emociones."
    texto_generado = modelo_openai.generar_texto(prompt)
    if texto_generado:
        print("Texto Generado por OpenAI:")
        print(texto_generado)
```


### 7. Buenas Prácticas

#### Manejo Seguro de Claves API:

* No expongas tus claves API en el código fuente.
* Utiliza variables de entorno o archivos de configuración seguros.

```python
import os

api_key = os.getenv("OPENAI_API_KEY")
```

#### Validación y Sanitización de Inputs:

* Asegura que los prompts y otros datos ingresados sean válidos y seguros.

#### Optimización de Solicitudes:

* Limita la cantidad de solicitudes para evitar sobrecargar la API.
* Implementa caching cuando sea apropiado.

#### Manejo de Errores:

* Captura y maneja adecuadamente las excepciones.
* Proporciona retroalimentación clara al usuario en caso de errores.


### 8. Resumen y Conclusión
En esta sesión, has aprendido a:

* Utilizar la librería requests para interactuar con APIs externas.
* Implementar mecanismos de autenticación para acceder a APIs seguras.
* Manejar respuestas y errores de manera efectiva.
* Integrar estos conceptos en el desarrollo de aplicaciones de Generative AI, optimizando la comunicación con modelos avanzados como los de OpenAI.

Estos conocimientos son fundamentales para desarrollar aplicaciones robustas y escalables en el campo de la inteligencia artificial generativa, permitiéndote aprovechar al máximo las capacidades de los modelos de lenguaje y otros recursos externos.

## Referencias

- [Requests Documentation](https://requests.readthedocs.io/en/latest/)
- [Real Python - Python Requests Module](https://realpython.com/python-requests/)
- [OpenAI API Documentation](https://beta.openai.com/docs/api-reference/introduction)
- [W3Schools - Python HTTP Requests](https://www.w3schools.com/python/module_requests.asp)
- [Python Exception Handling](https://docs.python.org/3/tutorial/errors.html)
- [Environment Variables in Python](https://realpython.com/python-environment-variables/)

## Preguntas Frecuentes

1. **¿Qué hago si recibo un error de autenticación al usar la API?**

   - Verifica que tu clave API sea correcta y esté activa.
   - Asegúrate de incluirla correctamente en los encabezados de la solicitud.

2. **¿Cómo manejo solicitudes que tardan demasiado en responder?**

   - Utiliza el parámetro `timeout` en las solicitudes.

     ```python
     response = requests.post(url, headers=headers, json=payload, timeout=10)
     ```

3. **¿Es posible realizar solicitudes asíncronas con requests?**

   - La librería `requests` no soporta asíncronía de forma nativa. Para solicitudes asíncronas, considera usar `aiohttp`.

Si tienes alguna pregunta adicional o necesitas más detalles sobre algún tema específico, ¡no dudes en preguntar!
