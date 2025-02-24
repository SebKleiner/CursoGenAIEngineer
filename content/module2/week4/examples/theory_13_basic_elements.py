import streamlit as st

def demo_text_elements():
    st.title("Mi Aplicación GenAI")
    st.header("Bienvenido")
    st.subheader("Generación de Texto")
    st.text("Texto simple")
    st.markdown("**Texto** con *formato*")

def demo_input_elements():
    st.header("Elementos de Input")
    nombre = st.text_input("Ingresa tu nombre")
    edad = st.number_input("Ingresa tu edad", min_value=0, max_value=120)
    opcion = st.selectbox("Selecciona una opción", ["A", "B", "C"])
    
    if nombre and edad:
        st.write(f"Hola {nombre}, tienes {edad} años y seleccionaste {opcion}")

def demo_layout_elements():
    st.header("Elementos de Layout")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("Columna 1")
        st.button("Botón 1")
    with col2:
        st.write("Columna 2")
        st.button("Botón 2")

    with st.sidebar:
        st.write("Barra lateral")
        st.slider("Ajusta un valor", 0, 100)

def main():
    st.set_page_config(page_title="Demo Elementos Básicos", page_icon="📚")
    
    tab1, tab2, tab3 = st.tabs(["Texto", "Input", "Layout"])
    
    with tab1:
        demo_text_elements()
    with tab2:
        demo_input_elements()
    with tab3:
        demo_layout_elements()

if __name__ == "__main__":
    main() 