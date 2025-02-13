# Introducción a Streamlit para Aplicaciones de GenAI (45 minutos)

## Descripción

En esta sesión teórica, exploraremos Streamlit, un framework de Python que permite crear aplicaciones web interactivas de manera rápida y sencilla. Nos enfocaremos en cómo Streamlit puede ser utilizado para crear interfaces de usuario para aplicaciones de Inteligencia Artificial Generativa.

## Objetivos

- Comprender qué es Streamlit y sus ventajas para aplicaciones de GenAI
- Aprender los componentes básicos de Streamlit
- Entender el ciclo de vida de una aplicación Streamlit
- Conocer las mejores prácticas para estructurar una aplicación Streamlit

## Contenido

### 1. Introducción a Streamlit

#### ¿Qué es Streamlit?
- Framework de Python para crear aplicaciones web
- Enfocado en aplicaciones de datos y ML/AI
- No requiere conocimientos de HTML/CSS/JavaScript

#### Ventajas de Streamlit
- Desarrollo rápido
- API intuitiva
- Actualizaciones en tiempo real
- Integración perfecta con librerías de Python

### 2. Componentes Básicos

#### Elementos de Texto
```python
import streamlit as st

st.title("Mi Aplicación GenAI")
st.header("Bienvenido")
st.subheader("Generación de Texto")
st.text("Texto simple")
st.markdown("**Texto** con *formato*")
```

#### Elementos de Input
```python
nombre = st.text_input("Ingresa tu nombre")
edad = st.number_input("Ingresa tu edad", min_value=0, max_value=120)
opcion = st.selectbox("Selecciona una opción", ["A", "B", "C"])
```

#### Elementos de Layout
```python
col1, col2 = st.columns(2)
with col1:
    st.write("Columna 1")
with col2:
    st.write("Columna 2")

with st.sidebar:
    st.write("Barra lateral")
```

### 3. Estado y Sesión

#### Manejo de Estado
```python
if 'contador' not in st.session_state:
    st.session_state.contador = 0

st.session_state.contador += 1
```

#### Persistencia de Datos
```python
@st.cache_data
def cargar_datos():
    return pd.read_csv("datos.csv")
```

### 4. Ciclo de Vida de la Aplicación

#### Ejecución del Script
- Streamlit ejecuta el script de arriba a abajo
- Cada interacción recarga el script completo
- Uso de caché para optimizar rendimiento

#### Manejo de Eventos
```python
if st.button("Procesar"):
    st.write("Procesando...")
```

### 5. Estructura Recomendada

```python
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Mi App GenAI",
    page_icon="🤖",
    layout="wide"
)

# Funciones auxiliares
def procesar_texto(texto):
    return texto.upper()

# Sidebar
with st.sidebar:
    st.title("Configuración")
    modelo = st.selectbox("Modelo", ["GPT-3", "GPT-4"])

# Contenido principal
st.title("Generador de Texto")
texto_input = st.text_area("Ingresa el texto")

if st.button("Generar"):
    resultado = procesar_texto(texto_input)
    st.write("Resultado:", resultado)
```

### 6. Mejores Prácticas

1. **Organización del Código**
   - Separar lógica de negocio de la interfaz
   - Usar funciones para modularizar
   - Mantener el código principal limpio

2. **Rendimiento**
   - Usar st.cache_data para datos estáticos
   - Minimizar recálculos innecesarios
   - Optimizar operaciones costosas

3. **Experiencia de Usuario**
   - Proporcionar feedback claro
   - Manejar errores gracefully
   - Mantener la interfaz intuitiva

### 7. Ejemplo Práctico

```python
import streamlit as st
import time

def main():
    st.title("Demo de Generación de Texto")
    
    # Configuración en sidebar
    with st.sidebar:
        temperatura = st.slider("Temperatura", 0.0, 1.0, 0.7)
        max_tokens = st.number_input("Max Tokens", 1, 500, 100)
    
    # Área principal
    prompt = st.text_area("Ingresa tu prompt:")
    
    if st.button("Generar"):
        with st.spinner("Generando..."):
            # Simulamos procesamiento
            time.sleep(2)
            st.success("¡Texto generado!")
            st.write(f"Prompt: {prompt}")
            st.write(f"Configuración: Temp={temperatura}, Tokens={max_tokens}")

if __name__ == "__main__":
    main()
```

## Referencias

- [Documentación oficial de Streamlit](https://docs.streamlit.io/)
- [Galería de ejemplos de Streamlit](https://streamlit.io/gallery)
- [Streamlit Cheat Sheet](https://docs.streamlit.io/library/cheatsheet)
- [Streamlit Components](https://streamlit.io/components)

## Próxima Clase
En la siguiente sesión, exploraremos características más avanzadas de Streamlit y comenzaremos a construir nuestro chatbot con múltiples modelos. 