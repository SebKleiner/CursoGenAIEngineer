# Introducción
Los Agentes IA representan un desarrollo emocionante en la IA Generativa, permitiendo que los Modelos de Lenguaje Grandes (LLMs) evolucionen de asistentes a agentes capaces de realizar acciones. Los frameworks de Agentes IA permiten a los desarrolladores crear aplicaciones que brindan a los LLMs acceso a herramientas y gestión de estado. Estos frameworks también mejoran la visibilidad, permitiendo a usuarios y desarrolladores monitorear las acciones planificadas por los LLMs, mejorando así la gestión de experiencias.

# Esta lección cubrirá las siguientes áreas:
- Entender qué es un Agente IA - ¿Qué es exactamente un Agente IA?
- Explorar cuatro frameworks diferentes de Agentes IA - ¿Qué los hace únicos?
- Aplicar estos Agentes IA a diferentes casos de uso - ¿Cuándo deberíamos usar Agentes IA?

# Objetivos
- Explicar qué son los Agentes IA y cómo pueden usarse.
- Comprender las diferencias entre algunos de los frameworks populares de Agentes IA y en qué se distinguen.
- Entender cómo funcionan los Agentes IA para construir aplicaciones con ellos.

# ¿Qué son los Agentes IA?
Los Agentes IA son un campo muy emocionante en el mundo de la IA Generativa. Con esta emoción viene a veces cierta confusión en términos y su aplicación. Para mantener las cosas simples e inclusivas con la mayoría de las herramientas que se refieren a Agentes IA, usaremos esta definición:

Los Agentes IA permiten a los Modelos de Lenguaje Grandes (LLMs) realizar tareas dándoles acceso a un estado y herramientas.

## Agentes LangChain  
Los Agentes LangChain son una implementación práctica y poderosa dentro del ecosistema de frameworks para Agentes IA. Específicamente diseñados para trabajar con Modelos de Lenguaje Grandes (LLMs) como GPT de OpenAI, estos agentes actúan como **sistemas autónomos** que combinan capacidades de razonamiento con acceso a herramientas externas.

### Estructura
```python
from langchain.agents import initialize_agent

agente = initialize_agent(
    llm=modelo_ia,  # Ej: ChatGPT
    tools=[...],  # Herramientas disponibles
    agent="zero-shot-react-description"  # Estrategia de razonamiento
)
```

### Ejemplo
1. Instalar las dependencias
```bash
pip install langchain langchain_openai langchain_community openai wikipedia

```

2. Crear un archivo llamado langchain_agent.py

3. Ingrsar el siguiente código
```python
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain_openai import ChatOpenAI
from langchain.utilities import WikipediaAPIWrapper
from langchain.chains import LLMMathChain
from dotenv import load_dotenv

# Cargar variables de entorno (API Key de OpenAI)
load_dotenv()

# 1. Inicializar modelo LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

# 2. Definir herramientas
wikipedia = WikipediaAPIWrapper()

tools = [
    Tool(
        name="Wikipedia",
        func=wikipedia.run,
        description="Útil para buscar información en Wikipedia sobre temas históricos, científicos o técnicos."
    )
]

# 3. Crear agente
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True  # Muestra el proceso de razonamiento
)

# 4. Ejecutar agente
if __name__ == "__main__":
    pregunta = """
    Investiga: 
    1. ¿Quién ganó el Premio Nobel de Física en 2023?s
    """

    respuesta = agent.invoke(pregunta)
    print("\nRespuesta final:")
    print(respuesta["output"])
```
4. Ejecuta el código


Links de interés
- [Agentes](https://python.langchain.com/v0.1/docs/modules/agents/agent_types/)
- [Utilities](https://api.python.langchain.com/en/latest/community/utilities.html)
- [Chains](https://python.langchain.com/v0.1/docs/modules/chains/)


## Agentes AutoGen
AutoGen es una biblioteca de Microsoft que permite la creación de agentes autónomos de inteligencia artificial que pueden colaborar entre sí. Está diseñada para facilitar la construcción de sistemas multi-agente, optimizando la interacción entre humanos y modelos de lenguaje.

### Ejemplo 
1. Instalar las dependencias
```bash
pip install pyautogen
```

2. Crear un archivo llamado autogen_agent.py

3. Ingrsar el siguiente código
```python
import autogen
import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Obtener API Key desde el .env
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("No se encontró la API Key en el archivo .env")

# Configurar OpenAI API
config_list = [
    {
        "model": "gpt-4",
        "api_key": api_key
    }
]

# Agente de usuario
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    code_execution_config={"use_docker": False} 
)

# Agente asistente con modelo configurado
assistant_proxy = autogen.AssistantAgent(
    name="assistant_proxy",
    system_message="Eres un experto en Python. Responde siempre con código Python funcional.",
    llm_config={"config_list": config_list}
)

# Iniciar la conversación
user_proxy.initiate_chat(
    assistant_proxy,
    message="¿Puedes escribir un código en Python que calcule la secuencia de Fibonacci hasta el décimo término?"
)
``` 
4. Ejecuta el código

Links de interés:
- [Ejemplos](https://microsoft.github.io/autogen/0.2/docs/Examples/)
- [Guía de Usuario](https://microsoft.github.io/autogen/stable/user-guide/extensions-user-guide/index.html)


## Ejercicio:
Explorá los módulos que tienen de los agentes que vimos y generá un script con la que te resulte más interesante.