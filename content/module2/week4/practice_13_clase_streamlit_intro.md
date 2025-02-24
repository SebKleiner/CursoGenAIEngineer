# Práctica: Creación de una Aplicación Básica con Streamlit (45 minutos)

## Descripción

En esta sesión práctica, implementaremos una aplicación básica usando Streamlit. Crearemos una interfaz simple para interactuar con modelos de generación de texto, sentando las bases para nuestro chatbot multi-modelo.

## Objetivos

- Configurar un entorno de desarrollo para Streamlit
- Crear una aplicación básica con elementos de UI
- Implementar interacciones básicas con el usuario
- Estructurar el código de manera organizada

## Actividades

### 1. Configuración del Entorno (5 minutos)

1. Crear un nuevo directorio para el proyecto:
```bash
mkdir mi_app_genai
cd mi_app_genai
```

2. Crear un entorno virtual e instalar dependencias:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install streamlit openai
```

### 2. Creación de la Aplicación Básica (15 minutos)

Crear un archivo `app.py`:

```python
import streamlit as st
import openai

# Configuración inicial
st.set_page_config(
    page_title="Mi App GenAI",
    page_icon="🤖",
    layout="wide"
)

# Configuración de OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]

def generar_texto(prompt, temperatura=0.7, max_tokens=150):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente útil."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperatura,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("🤖 Generador de Texto con IA")
    
    # Sidebar para configuración
    with st.sidebar:
        st.header("Configuración")
        temperatura = st.slider(
            "Temperatura",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            help="Controla la creatividad del modelo"
        )
        max_tokens = st.slider(
            "Máximo de tokens",
            min_value=50,
            max_value=500,
            value=150,
            help="Longitud máxima de la respuesta"
        )
    
    # Área principal
    prompt = st.text_area(
        "Ingresa tu prompt:",
        height=100,
        placeholder="Escribe aquí lo que quieres que genere la IA..."
    )
    
    if st.button("Generar", type="primary"):
        if prompt:
            with st.spinner("Generando respuesta..."):
                respuesta = generar_texto(prompt, temperatura, max_tokens)
                st.write("### Respuesta:")
                st.write(respuesta)
        else:
            st.warning("Por favor, ingresa un prompt.")

if __name__ == "__main__":
    main()
```

### 3. Agregar Manejo de Estado (15 minutos)

Modificar `app.py` para incluir historial de generaciones:

```python
# ... (código anterior) ...

def main():
    # Inicializar historial en session_state
    if 'historial' not in st.session_state:
        st.session_state.historial = []
    
    st.title("🤖 Generador de Texto con IA")
    
    # Tab para alternar entre generación e historial
    tab1, tab2 = st.tabs(["Generador", "Historial"])
    
    with tab1:
        # ... (código de generación anterior) ...
        if st.button("Generar", type="primary"):
            if prompt:
                with st.spinner("Generando respuesta..."):
                    respuesta = generar_texto(prompt, temperatura, max_tokens)
                    st.write("### Respuesta:")
                    st.write(respuesta)
                    
                    # Guardar en historial
                    st.session_state.historial.append({
                        "prompt": prompt,
                        "respuesta": respuesta,
                        "temperatura": temperatura,
                        "max_tokens": max_tokens
                    })
            else:
                st.warning("Por favor, ingresa un prompt.")
    
    with tab2:
        st.header("Historial de Generaciones")
        if not st.session_state.historial:
            st.info("Aún no hay generaciones en el historial.")
        else:
            for i, item in enumerate(reversed(st.session_state.historial)):
                with st.expander(f"Generación {len(st.session_state.historial) - i}"):
                    st.write("**Prompt:**", item["prompt"])
                    st.write("**Respuesta:**", item["respuesta"])
                    st.write("---")
                    st.write(f"Temperatura: {item['temperatura']}")
                    st.write(f"Max tokens: {item['max_tokens']}")

# ... (resto del código) ...
```

### 4. Ejecutar y Probar la Aplicación (10 minutos)

- [Documentación de Streamlit - Secrets](https://docs.streamlit.io/develop/api-reference/connections/secrets.toml)

1. Crear archivo `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "tu-api-key-aqui"
```

2. Ejecutar la aplicación:
```bash
streamlit run app.py
```

3. Probar diferentes prompts y configuraciones:
   - Generar textos con diferentes temperaturas
   - Verificar el historial de generaciones
   - Probar el manejo de errores

## Ejercicios Adicionales

1. **Agregar Exportación de Historial**
   - Implementar un botón para descargar el historial en formato JSON

2. **Mejorar la Interfaz**
   - Agregar más opciones de configuración
   - Implementar temas claros/oscuros
   - Agregar tooltips informativos

3. **Implementar Cache**
   - Usar `@st.cache_data` para optimizar operaciones repetitivas

## Recursos

- [Documentación de Streamlit](https://docs.streamlit.io/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Streamlit Components](https://streamlit.io/components)

## Próxima Clase
En la siguiente sesión, expandiremos nuestra aplicación para incluir más funcionalidades y comenzar la integración con múltiples modelos de lenguaje. 