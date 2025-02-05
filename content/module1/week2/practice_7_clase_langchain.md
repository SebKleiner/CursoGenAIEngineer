# Crear tu propio chatbot con LangChain - Práctica (45 minutos)

## Descripción

En esta guía, exploraremos el uso de LangChain para crear chatbots interactivos utilizando modelos de lenguaje de OpenAI. LangChain es una biblioteca poderosa que facilita la integración de modelos de inteligencia artificial en aplicaciones conversacionales. A lo largo de las siguientes actividades, aprenderás a construir diferentes tipos de chatbots con funcionalidades avanzadas.

## Objetivos

- Crear un chatbot básico con LangChain y OpenAI.
- Implementar memoria en el chatbot para recordar el contexto de la conversación.
- Integrar un chatbot con documentos para responder preguntas basadas en información almacenada.
- Desarrollar habilidades prácticas para implementar chatbots que utilicen IA generativa y consultas de datos en tiempo real.

Cada ejercicio introduce nuevos conceptos y herramientas clave para desarrollar chatbots cada vez más sofisticados, permitiéndote experimentar con el potencial de los modelos de lenguaje en aplicaciones del mundo real.

Asegúrate de tener un entorno de programación adecuado y de seguir cada paso detalladamente para obtener los mejores resultados. ¡Manos a la obra!

## Actividades

### Ejercicio 1: Crear un Chatbot Simple con LangChain
En este ejercicio, vamos a crear un chatbot simple que interactúe con el usuario utilizando un modelo de lenguaje. Vamos a utilizar el modelo `gpt-3.5-turbo` de OpenAI, que es uno de los modelos más populares y accesibles.

#### Paso 1: Instalar las dependencias necesarias
Primero, asegúrate de tener instaladas las bibliotecas necesarias. Puedes instalarlas usando pip en tu terminal de PyCharm:

```bash
pip install langchain langchain-community openai python-dotenv
```

* `langchain`: La biblioteca principal que vamos a utilizar.

* `openai`: Para interactuar con los modelos de OpenAI.

* `python-dotenv`: Para manejar variables de entorno de manera segura.

#### Paso 2: Configurar las variables de entorno
Crea un archivo .env en la raíz de tu proyecto y añade tu clave de API de OpenAI:

```
OPENAI_API_KEY=tu_clave_de_api_aquí
```

#### Paso 3: Crear el script del chatbot
Ahora, crea un archivo Python en tu proyecto, por ejemplo, chatbot.py, y añade el siguiente código:

```python
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# Cargar las variables de entorno
load_dotenv()

# Configurar el modelo de chat
chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)

# Mensaje de sistema para definir el comportamiento del chatbot
system_message = SystemMessage(content="Eres un asistente útil que responde preguntas de manera clara y concisa.")

# Función para interactuar con el chatbot
def chat_with_bot():
    print("¡Hola! Soy tu chatbot asistente. Puedes empezar a hacer preguntas. Escribe 'salir' para terminar.")
    while True:
        user_input = input("Tú: ")
        if user_input.lower() == "salir":
            print("Chatbot: ¡Hasta luego!")
            break
        
        # Crear el mensaje del usuario
        user_message = HumanMessage(content=user_input)
        
        # Obtener la respuesta del chatbot
        response = chat([system_message, user_message])
        
        # Mostrar la respuesta del chatbot
        print(f"Chatbot: {response.content}")

if __name__ == "__main__":
    chat_with_bot()
```

#### Paso 4: Ejecutar el chatbot
Guarda el archivo y ejecuta el script en PyCharm. Deberías ver un mensaje de bienvenida y el chatbot estará listo para responder a tus preguntas.

```
¡Hola! Soy tu chatbot asistente. Puedes empezar a hacer preguntas. Escribe 'salir' para terminar.
Tú: ¿Qué es LangChain?
Chatbot: LangChain es una biblioteca de Python que facilita la creación de aplicaciones que interactúan con modelos de lenguaje, como GPT. Proporciona herramientas para gestionar conversaciones, integrar datos externos y más.
Tú: salir
Chatbot: ¡Hasta luego!
```

**Explicación del Código**
Carga de variables de entorno: Usamos python-dotenv para cargar la clave de API de OpenAI desde el archivo `.env`.

1. Configuración del modelo: Utilizamos ChatOpenAI para configurar el modelo gpt-3.5-turbo con una temperatura de 0.7, lo que controla la creatividad de las respuestas.

2. Mensaje de sistema: Definimos un mensaje de sistema que guía el comportamiento del chatbot.

3. Interacción con el usuario: El bucle while permite al usuario interactuar con el chatbot hasta que decida salir.

4. Respuesta del chatbot: El chatbot genera una respuesta basada en el mensaje del usuario y el mensaje de sistema.

#### Paso 5: Experimentar y Modificar
¡Felicidades! Has creado tu primer chatbot con LangChain. Ahora puedes experimentar modificando el código, cambiando el mensaje de sistema, o ajustando la temperatura para ver cómo afecta las respuestas del chatbot.

---

### Ejercicio 2: Chatbot con Memoria usando LangChain
En este ejercicio, vamos a utilizar la clase `ConversationBufferMemory` de LangChain para permitir que el chatbot recuerde el contexto de la conversación.

#### Paso 1: Instalar dependencias adicionales
Si no lo has hecho ya, asegúrate de tener instaladas las bibliotecas necesarias:

```bash
pip install langchain openai python-dotenv
```
#### Paso 2: Configurar las variables de entorno
Asegúrate de tener tu clave de API de OpenAI en el archivo `.env`:

```
OPENAI_API_KEY=tu_clave_de_api_aquí
```

#### Paso 3: Crear el script del chatbot con memoria
Crea un archivo Python, por ejemplo, `chatbot_memoria.py`, y añade el siguiente código:

```python
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Cargar las variables de entorno
load_dotenv()

# Configurar el modelo de chat
chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)

# Configurar la memoria para recordar el contexto de la conversación
memory = ConversationBufferMemory()

# Crear una cadena de conversación con memoria
conversation = ConversationChain(llm=chat, memory=memory, verbose=True)

# Función para interactuar con el chatbot
def chat_with_bot():
    print("¡Hola! Soy tu chatbot con memoria. Puedes empezar a hacer preguntas. Escribe 'salir' para terminar.")
    while True:
        user_input = input("Tú: ")
        if user_input.lower() == "salir":
            print("Chatbot: ¡Hasta luego!")
            break
        
        # Obtener la respuesta del chatbot
        response = conversation.predict(input=user_input)
        
        # Mostrar la respuesta del chatbot
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    chat_with_bot()
```

#### Paso 4: Ejecutar el chatbot
Guarda el archivo y ejecuta el script en PyCharm. Ahora el chatbot recordará el contexto de la conversación. Por ejemplo:

```plaintext
¡Hola! Soy tu chatbot con memoria. Puedes empezar a hacer preguntas. Escribe 'salir' para terminar.
Tú: ¿Cómo estás?
Chatbot: ¡Hola! Estoy bien, ¿y tú?
Tú: Estoy bien también. ¿Qué sabes sobre LangChain?
Chatbot: LangChain es una biblioteca de Python que facilita la creación de aplicaciones que interactúan con modelos de lenguaje, como GPT. Proporciona herramientas para gestionar conversaciones, integrar datos externos y más.
Tú: ¿Puedes darme un ejemplo de cómo usar LangChain?
Chatbot: Claro, un ejemplo básico es crear un chatbot como este. Puedes usar `ConversationChain` para mantener una conversación con memoria, como lo estamos haciendo ahora.
Tú: salir
Chatbot: ¡Hasta luego!
```

**Explicación del Código**
1) Memoria: Usamos `ConversationBufferMemory` para almacenar el historial de la conversación. Esto permite que el chatbot recuerde el contexto de lo que se ha hablado.

2) ConversationChain: Es una cadena de LangChain que combina el modelo de lenguaje (llm) con la memoria (`memory`). El parámetro `verbose=True` muestra detalles de la conversación en la consola.

3) Interacción con el usuario: El bucle `while` permite al usuario interactuar con el chatbot hasta que decida salir.

4) Respuesta del chatbot: El chatbot genera una respuesta basada en el historial de la conversación.

---
### Ejercicio 3: Chatbot que Consulta Documentos con LangChain
En este ejercicio, vamos a utilizar la clase VectorstoreIndexCreator de LangChain para permitir que el chatbot consulte un documento (por ejemplo, un archivo de texto) y responda preguntas basadas en su contenido.

#### Paso 1: Instalar dependencias adicionales
Asegúrate de tener instaladas las bibliotecas necesarias:

```bash
pip install langchain openai python-dotenv tiktoken faiss-cpu
```
* `tiktoken`: Para manejar tokens en el modelo de OpenAI.
* `faiss-cpu`: Para la búsqueda de vectores (permite buscar información en documentos).

#### Paso 2: Configurar las variables de entorno
Asegúrate de tener tu clave de API de OpenAI en el archivo `.env`:

```plaintext
OPENAI_API_KEY=tu_clave_de_api_aquí
```

#### Paso 3: Crear el script del chatbot que consulta documentos
Crea un archivo Python, por ejemplo, `chatbot_documentos.py`, y añade el siguiente código:

```python
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator

# Cargar las variables de entorno
load_dotenv()

# Cargar el documento de texto
ruta_documento = "documento.txt"  # Cambia esto por la ruta de tu archivo de texto
loader = TextLoader(ruta_documento)

# Crear un índice de búsqueda basado en el documento
index = VectorstoreIndexCreator().from_loaders([loader])

# Configurar el modelo de chat
chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)

# Función para interactuar con el chatbot
def chat_with_bot():
    print("¡Hola! Soy tu chatbot que puede consultar documentos. Puedes hacerme preguntas sobre el contenido. Escribe 'salir' para terminar.")
    while True:
        user_input = input("Tú: ")
        if user_input.lower() == "salir":
            print("Chatbot: ¡Hasta luego!")
            break
        
        # Obtener la respuesta del chatbot basada en el documento
        response = index.query(user_input, llm=chat)
        
        # Mostrar la respuesta del chatbot
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    chat_with_bot()
```

#### Paso 4: Preparar el documento de texto
Crea un archivo de texto llamado `documento.txt` en la misma carpeta que tu script. Añade algún contenido, por ejemplo:

```plaintext
LangChain es una biblioteca de Python que facilita la creación de aplicaciones que interactúan con modelos de lenguaje, como GPT. Proporciona herramientas para gestionar conversaciones, integrar datos externos y más.

OpenAI es una empresa que desarrolla modelos de lenguaje avanzados, como GPT-3 y GPT-4. Estos modelos pueden generar texto, responder preguntas y realizar tareas de procesamiento de lenguaje natural.

PyCharm es un entorno de desarrollo integrado (IDE) popular para Python. Es ampliamente utilizado por desarrolladores para escribir, depurar y probar código.
```

#### Paso 5: Ejecutar el chatbot
Guarda el archivo y ejecuta el script en PyCharm. Ahora el chatbot podrá responder preguntas basadas en el contenido del documento. Por ejemplo:

```plaintext
¡Hola! Soy tu chatbot que puede consultar documentos. Puedes hacerme preguntas sobre el contenido. Escribe 'salir' para terminar.
Tú: ¿Qué es LangChain?
Chatbot: LangChain es una biblioteca de Python que facilita la creación de aplicaciones que interactúan con modelos de lenguaje, como GPT. Proporciona herramientas para gestionar conversaciones, integrar datos externos y más.
Tú: ¿Quién desarrolla GPT-4?
Chatbot: OpenAI es la empresa que desarrolla modelos de lenguaje avanzados, como GPT-3 y GPT-4.
Tú: salir
Chatbot: ¡Hasta luego!
```

**Explicación del Código**
1) Carga del documento: Usamos `TextLoader` para cargar un archivo de texto. Puedes cambiar esto para cargar otros tipos de documentos, como PDFs o páginas web.

2) Índice de búsqueda: `VectorstoreIndexCreator` crea un índice de búsqueda basado en el contenido del documento. Esto permite al chatbot buscar información relevante en el texto.

3) Consulta del chatbot: El método `index.query` permite al chatbot responder preguntas basadas en el contenido del documento.

4) Interacción con el usuario: El bucle `while` permite al usuario interactuar con el chatbot hasta que decida salir.

#### Paso 6: Experimentar y Modificar
Ahora que tienes un chatbot que puede consultar documentos, puedes experimentar con las siguientes ideas:

1) Cambiar el tipo de documento: Prueba cargar un archivo PDF o una página web usando `PyPDFLoade`r o `WebBaseLoader`.

```python
from langchain.document_loaders import PyPDFLoader

loader = PyPDFLoader("documento.pdf")
```

2) Añadir múltiples documentos: Puedes cargar varios documentos y crear un índice combinado.

```python
loader1 = TextLoader("documento1.txt")
loader2 = TextLoader("documento2.txt")
index = VectorstoreIndexCreator().from_loaders([loader1, loader2])
```

## Relación con Generative AI

A lo largo de esta guía, hemos trabajado con diferentes funcionalidades de LangChain para la creación de chatbots. En el primer ejercicio, establecimos las bases creando un chatbot simple que responde preguntas en tiempo real utilizando el modelo de OpenAI. Luego, exploramos cómo mejorar la experiencia del usuario incorporando memoria en el chatbot, permitiéndole recordar el contexto de la conversación. Finalmente, aprendimos a integrar documentos como fuente de información, dotando al chatbot de la capacidad de responder preguntas basadas en contenido específico.

Estos conceptos se pueden combinar y expandir para desarrollar aplicaciones más avanzadas, como asistentes virtuales especializados en áreas específicas, chatbots educativos o herramientas de soporte automatizadas.

## Conclusión

El uso de LangChain en el desarrollo de chatbots demuestra el potencial de los modelos de lenguaje en la automatización de interacciones inteligentes. Desde la creación de un chatbot básico hasta la incorporación de memoria y la consulta de documentos, cada ejercicio en esta guía ha permitido construir una base sólida para desarrollar aplicaciones conversacionales más avanzadas.

Te animamos a seguir explorando y experimentando con LangChain, ajustando los parámetros del modelo, incorporando nuevas fuentes de información y optimizando la experiencia del usuario. La integración de inteligencia artificial en chatbots es un campo en constante evolución, y con estas herramientas, tienes todo lo necesario para seguir innovando. 

---