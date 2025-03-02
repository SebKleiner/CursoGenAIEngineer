import streamlit as st
import pandas as pd
import time

def demo_forms():
    st.header("Demo de Forms")
    
    with st.form("mi_formulario"):
        nombre = st.text_input("Nombre")
        edad = st.number_input("Edad")
        submitted = st.form_submit_button("Enviar")
        if submitted:
            st.success(f"Datos procesados: {nombre}, {edad}")

def demo_interactive_components():
    st.header("Componentes Interactivos")
    
    # Dataframes interactivos
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    st.write("DataFrame Editable:")
    edited_df = st.data_editor(df)
    
    # Selectores múltiples
    st.write("Selector Múltiple:")
    opciones = st.multiselect(
        'Selecciona modelos:',
        ['GPT-3', 'GPT-4', 'Claude', 'LLaMA']
    )
    
    # Progress bars
    st.write("Barra de Progreso:")
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress_bar.progress(i + 1)

def main():
    st.set_page_config(page_title="Demo Componentes Avanzados", page_icon="🔧")
    
    tab1, tab2 = st.tabs(["Forms", "Componentes Interactivos"])
    
    with tab1:
        demo_forms()
    with tab2:
        demo_interactive_components()

if __name__ == "__main__":
    main() 