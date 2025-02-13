# Componentes Avanzados de Streamlit y Multi-Modelo (45 minutos)

## Descripción

En esta sesión teórica, profundizaremos en características avanzadas de Streamlit y aprenderemos a integrar múltiples modelos de lenguaje en nuestra aplicación. Exploraremos callbacks, componentes personalizados y técnicas de manejo de estado avanzadas.

## Objetivos

- Dominar componentes avanzados de Streamlit
- Implementar callbacks y manejo de eventos
- Integrar múltiples modelos de lenguaje
- Crear componentes personalizados
- Manejar el estado de la aplicación de manera eficiente

## Contenido

### 1. Componentes Avanzados

#### Forms y Batch Processing
```python
import streamlit as st

with st.form("mi_formulario"):
    nombre = st.text_input("Nombre")
    edad = st.number_input("Edad")
    submitted = st.form_submit_button("Enviar")
    if submitted:
        st.write(f"Datos procesados: {nombre}, {edad}")
```

#### Componentes Interactivos Avanzados
```python
import streamlit as st
import pandas as pd

# Dataframes interactivos
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
edited_df = st.data_editor(df)

# Selectores múltiples
opciones = st.multiselect(
    'Selecciona modelos:',
    ['GPT-3', 'GPT-4', 'Claude', 'LLaMA']
)

# Progress bars dinámicos
progress_bar = st.progress(0)
for i in range(100):
    progress_bar.progress(i + 1)
```

### 2. Callbacks y Eventos

#### Manejo de Callbacks
```python
import streamlit as st

def on_change_callback():
    st.write("¡El valor ha cambiado!")

valor = st.slider("Ajusta el valor", 0, 100, key="mi_slider")
if st.session_state.mi_slider != valor:
    on_change_callback()
```

#### Eventos Personalizados
```python
import streamlit as st

def handle_click(btn_id):
    st.session_state[f'btn_{btn_id}_clicked'] = True

if 'btn_1_clicked' not in st.session_state:
    st.session_state.btn_1_clicked = False

if st.button("Acción 1", on_click=handle_click, args=(1,)):
    st.write("Botón 1 presionado")
```

### 3. Integración Multi-Modelo

#### Clase Base para Modelos
```python
class ModeloBase:
    def __init__(self, api_key):
        self.api_key = api_key
    
    def generar_texto(self, prompt):
        raise NotImplementedError

class ModeloOpenAI(ModeloBase):
    def generar_texto(self, prompt):
        # Implementación específica para OpenAI
        pass

class ModeloDeepseek(ModeloBase):
    def generar_texto(self, prompt):
        # Implementación específica para Deepseek
        pass
```

#### Factory de Modelos
```python
class ModelFactory:
    @staticmethod
    def crear_modelo(tipo, api_key):
        if tipo == "openai":
            return ModeloOpenAI(api_key)
        elif tipo == "deepseek":
            return ModeloDeepseek(api_key)
        else:
            raise ValueError(f"Modelo no soportado: {tipo}")
```

### 4. Estado Avanzado

#### Gestión de Sesión Compleja
```python
import streamlit as st

class SessionState:
    def __init__(self):
        self.initialize_state()
    
    def initialize_state(self):
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'modelo_actual' not in st.session_state:
            st.session_state.modelo_actual = None
        if 'configuracion' not in st.session_state:
            st.session_state.configuracion = {
                'temperatura': 0.7,
                'max_tokens': 150
            }

    def actualizar_historial(self, mensaje):
        st.session_state.chat_history.append(mensaje)
    
    def cambiar_modelo(self, nuevo_modelo):
        st.session_state.modelo_actual = nuevo_modelo
```

### 5. Componentes Personalizados

#### Creación de Componentes
```python
import streamlit as st
import streamlit.components.v1 as components

def chat_message(mensaje, is_user=True):
    with st.container():
        col1, col2 = st.columns([1, 9])
        with col1:
            if is_user:
                st.image("user_avatar.png", width=50)
            else:
                st.image("bot_avatar.png", width=50)
        with col2:
            st.markdown(f"{'**Usuario:**' if is_user else '**Bot:**'} {mensaje}")
```

#### Integración de HTML/JavaScript
```python
def render_custom_chat():
    components.html(
        """
        <div style="border: 1px solid #ccc; padding: 10px; border-radius: 5px;">
            <div id="chat-messages"></div>
            <script>
                function addMessage(text, isUser) {
                    const messages = document.getElementById('chat-messages');
                    const msg = document.createElement('div');
                    msg.className = isUser ? 'user-message' : 'bot-message';
                    msg.textContent = text;
                    messages.appendChild(msg);
                }
            </script>
        </div>
        """,
        height=400
    )
```

### 6. Optimización y Rendimiento

#### Caching Avanzado
```python
import streamlit as st
from datetime import timedelta

@st.cache_data(ttl=timedelta(hours=1))
def obtener_datos_api():
    # Datos que se cachean por 1 hora
    pass

@st.cache_resource
def cargar_modelo():
    # El modelo se carga una vez y se mantiene en memoria
    pass
```

#### Manejo de Recursos
```python
import streamlit as st
import gc

def limpiar_recursos():
    if st.session_state.get('modelo_actual'):
        del st.session_state.modelo_actual
        gc.collect()

st.sidebar.button("Limpiar Recursos", on_click=limpiar_recursos)
```

## Referencias

- [Streamlit Advanced Features](https://docs.streamlit.io/library/advanced-features)
- [Custom Components](https://docs.streamlit.io/library/components)
- [Session State API](https://docs.streamlit.io/library/api-reference/session-state)
- [Caching](https://docs.streamlit.io/library/advanced-features/caching)

## Próxima Clase
En la siguiente sesión, exploraremos el sistema de logging de Streamlit, técnicas de monitoreo y optimización avanzada para nuestro chatbot multi-modelo. 