import streamlit as st

def on_change_callback():
    st.write("¡El valor ha cambiado!")

def handle_click(btn_id):
    st.session_state[f'btn_{btn_id}_clicked'] = True
    st.write(f"Botón {btn_id} fue presionado")

def demo_callbacks():
    st.header("Demo de Callbacks")
    
    valor = st.slider(
        "Ajusta el valor", 
        0, 100, 
        key="mi_slider",
        on_change=on_change_callback
    )
    
    st.write("Valor actual:", valor)

def demo_custom_events():
    st.header("Demo de Eventos Personalizados")
    
    for i in range(1, 4):
        if f'btn_{i}_clicked' not in st.session_state:
            st.session_state[f'btn_{i}_clicked'] = False
        
        if st.button(f"Acción {i}", key=f"btn_{i}", on_click=handle_click, args=(i,)):
            st.write(f"Estado del botón {i}: {st.session_state[f'btn_{i}_clicked']}")

def main():
    st.set_page_config(page_title="Demo Callbacks y Eventos", page_icon="🎮")
    
    tab1, tab2 = st.tabs(["Callbacks", "Eventos Personalizados"])
    
    with tab1:
        demo_callbacks()
    with tab2:
        demo_custom_events()

if __name__ == "__main__":
    main() 