import streamlit as st
import pandas as pd
import time

def demo_session_state():
    st.header("Demo de Estado")
    
    if 'contador' not in st.session_state:
        st.session_state.contador = 0

    st.write(f"Contador actual: {st.session_state.contador}")
    
    if st.button("Incrementar"):
        st.session_state.contador += 1

def demo_cache():
    st.header("Demo de Cache")
    
    @st.cache_data
    def cargar_datos():
        # Simulamos carga de datos
        time.sleep(2)
        return pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6]
        })
    
    with st.spinner("Cargando datos..."):
        df = cargar_datos()
        st.write("Datos cargados:", df)
        st.info("Los datos se cargan una sola vez y se cachean")

def main():
    st.set_page_config(page_title="Demo Estado y Cache", page_icon="💾")
    
    tab1, tab2 = st.tabs(["Estado", "Cache"])
    
    with tab1:
        demo_session_state()
    with tab2:
        demo_cache()

if __name__ == "__main__":
    main() 