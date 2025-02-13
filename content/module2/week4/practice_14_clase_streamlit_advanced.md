# Práctica: Implementación de Chatbot Multi-Modelo con Streamlit (45 minutos)

## Descripción

En esta sesión práctica, implementaremos un chatbot capaz de utilizar múltiples modelos de lenguaje. Aplicaremos los conceptos avanzados de Streamlit vistos en la teoría y crearemos una interfaz robusta y eficiente.

## Objetivos

- Implementar un sistema de chat multi-modelo
- Utilizar componentes avanzados de Streamlit
- Manejar el estado de la aplicación de manera eficiente
- Crear una interfaz de usuario intuitiva y responsive

## Actividades

### 1. Estructura del Proyecto (5 minutos)

Organizar el proyecto:
```bash
mi_app_genai/
├── models/
│   ├── __init__.py
│   ├── base_model.py
│   ├── openai_model.py
│   ├── deepseek_model.py
│   └── llama_model.py
├── utils/
│   ├── __init__.py
│   └── session_state.py
├── components/
│   ├── __init__.py
│   └── chat_components.py
└── app.py
```

### 2. Implementación de Modelos (15 minutos)

1. `models/base_model.py`:
```python
from abc import ABC, abstractmethod

class BaseModel(ABC):
    def __init__(self, api_key):
        self.api_key = api_key

    @abstractmethod
    def generar_texto(self, prompt, **kwargs):
        pass

    @abstractmethod
    def nombre_modelo(self):
        pass
```

2. `models/openai_model.py`:
```python
import openai
from .base_model import BaseModel

class OpenAIModel(BaseModel):
    def __init__(self, api_key):
        super().__init__(api_key)
        openai.api_key = api_key

    def nombre_modelo(self):
        return "OpenAI GPT-3.5"

    def generar_texto(self, prompt, **kwargs):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un asistente útil."},
                    {"role": "user", "content": prompt}
                ],
                temperature=kwargs.get('temperature', 0.7),
                max_tokens=kwargs.get('max_tokens', 150)
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
```

3. `models/deepseek_model.py`:
```python
import requests
from .base_model import BaseModel

class DeepseekModel(BaseModel):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.api_url = "https://api.deepseek.com/v1/chat/completions"

    def nombre_modelo(self):
        return "Deepseek"

    def generar_texto(self, prompt, **kwargs):
        try:
            response = requests.post(
                self.api_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": kwargs.get('temperature', 0.7),
                    "max_tokens": kwargs.get('max_tokens', 150)
                }
            )
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            return f"Error: {str(e)}"
```

### 3. Implementación de Componentes (10 minutos)

1. `components/chat_components.py`:
```python
import streamlit as st

def mensaje_chat(contenido, is_user=True, key=None):
    with st.container():
        if is_user:
            st.markdown(f"""
                <div style='background-color: #e6f3ff; padding: 10px; border-radius: 10px; margin: 5px 0;'>
                    <b>Usuario:</b> {contenido}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style='background-color: #f0f0f0; padding: 10px; border-radius: 10px; margin: 5px 0;'>
                    <b>Asistente:</b> {contenido}
                </div>
                """, unsafe_allow_html=True)

def selector_modelo():
    return st.sidebar.selectbox(
        "Selecciona el modelo",
        ["OpenAI GPT-3.5", "Deepseek", "LLaMA"],
        key="modelo_seleccionado"
    )

def configuracion_modelo():
    with st.sidebar:
        st.header("Configuración")
        temperatura = st.slider(
            "Temperatura",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            key="temperatura"
        )
        max_tokens = st.slider(
            "Máximo de tokens",
            min_value=50,
            max_value=500,
            value=150,
            step=50,
            key="max_tokens"
        )
        return {"temperature": temperatura, "max_tokens": max_tokens}
```

### 4. Implementación Principal (15 minutos)

`app.py`:
```python
import streamlit as st
from models.openai_model import OpenAIModel
from models.deepseek_model import DeepseekModel
from components.chat_components import mensaje_chat, selector_modelo, configuracion_modelo

# Configuración inicial
st.set_page_config(
    page_title="ChatBot Multi-Modelo",
    page_icon="🤖",
    layout="wide"
)

# Inicialización del estado
if 'mensajes' not in st.session_state:
    st.session_state.mensajes = []
if 'modelo_actual' not in st.session_state:
    st.session_state.modelo_actual = None

def inicializar_modelo(nombre_modelo):
    if nombre_modelo == "OpenAI GPT-3.5":
        return OpenAIModel(st.secrets["OPENAI_API_KEY"])
    elif nombre_modelo == "Deepseek":
        return DeepseekModel(st.secrets["DEEPSEEK_API_KEY"])
    return None

def main():
    st.title("🤖 ChatBot Multi-Modelo")

    # Sidebar
    modelo_seleccionado = selector_modelo()
    configuracion = configuracion_modelo()

    # Inicializar modelo si cambia la selección
    if (not st.session_state.modelo_actual or 
        st.session_state.modelo_actual.nombre_modelo() != modelo_seleccionado):
        st.session_state.modelo_actual = inicializar_modelo(modelo_seleccionado)

    # Área de chat
    for msg in st.session_state.mensajes:
        mensaje_chat(msg["contenido"], msg["is_user"])

    # Input del usuario
    with st.form("chat_input", clear_on_submit=True):
        user_input = st.text_area("Tu mensaje:", key="user_input")
        submitted = st.form_submit_button("Enviar")

        if submitted and user_input:
            # Agregar mensaje del usuario
            st.session_state.mensajes.append({
                "contenido": user_input,
                "is_user": True
            })

            # Generar respuesta
            if st.session_state.modelo_actual:
                with st.spinner("Generando respuesta..."):
                    respuesta = st.session_state.modelo_actual.generar_texto(
                        user_input,
                        **configuracion
                    )
                    st.session_state.mensajes.append({
                        "contenido": respuesta,
                        "is_user": False
                    })
                st.experimental_rerun()

if __name__ == "__main__":
    main()
```

### 5. Pruebas y Optimización

1. Crear archivo `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "tu-api-key-openai"
DEEPSEEK_API_KEY = "tu-api-key-deepseek"
```

2. Ejecutar la aplicación:
```bash
streamlit run app.py
```

## Ejercicios Adicionales

1. **Implementar Persistencia**
   - Agregar función para guardar el historial en un archivo
   - Permitir cargar conversaciones anteriores

2. **Mejorar la Interfaz**
   - Agregar avatares para usuario y bot
   - Implementar temas personalizados
   - Agregar animaciones de carga

3. **Funcionalidades Avanzadas**
   - Implementar sistema de prompts predefinidos
   - Agregar exportación de conversaciones
   - Implementar comparación de respuestas entre modelos

## Recursos

- [Streamlit Session State](https://docs.streamlit.io/library/api-reference/session-state)
- [Streamlit Forms](https://docs.streamlit.io/library/api-reference/forms)
- [Streamlit Components](https://docs.streamlit.io/library/api-reference/components)

## Próxima Clase
En la siguiente sesión, implementaremos logging, monitoreo y optimizaremos el rendimiento de nuestra aplicación. 