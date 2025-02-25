import streamlit as st
import time
import plotly.express as px
import pandas as pd
import logging
from datetime import datetime
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# Configuración de logging
class StreamlitLogger:
    def __init__(self):
        self.logger = self._configure_logger()
    
    def _configure_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        # Crear directorio de logs si no existe
        os.makedirs('logs', exist_ok=True)
        
        # Handler para archivo
        file_handler = logging.FileHandler(
            f'logs/chatbot_{datetime.now().strftime("%Y%m%d")}.log'
        )
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        return logger

    def get_logger(self):
        return self.logger

# Clase para métricas
class MetricsCollector:
    @staticmethod
    def initialize_metrics():
        if 'metrics' not in st.session_state:
            st.session_state.metrics = {
                'requests_count': 0,
                'error_count': 0,
                'response_times': [],
                'model_usage': {},
                'token_usage': {}
            }
    
    def __init__(self):
        MetricsCollector.initialize_metrics()
    
    def log_request(self, model_name, response_time, tokens_used):
        metrics = st.session_state.metrics
        metrics['requests_count'] += 1
        metrics['response_times'].append(response_time)
        
        if model_name not in metrics['model_usage']:
            metrics['model_usage'][model_name] = 0
            metrics['token_usage'][model_name] = 0
            
        metrics['model_usage'][model_name] += 1
        metrics['token_usage'][model_name] += tokens_used
    
    def log_error(self, model_name, error_type):
        st.session_state.metrics['error_count'] += 1

# Simulación de modelos
class ModelBase:
    def __init__(self, name, api_key=None):
        self.name = name
        # Mapa de nombres de modelo a nombres de variables de entorno
        env_key_map = {
            "GPT-3.5": "GPT35_API_KEY",
            "Deepseek": "DEEPSEEK_API_KEY",
            "LLaMA": "LLAMA_API_KEY"
        }
        
        env_key_name = env_key_map.get(name)
        if not env_key_name:
            raise ValueError(f"Nombre de modelo no reconocido: {name}")
            
        self.api_key = api_key or os.getenv(env_key_name)
        if not self.api_key:
            raise ValueError(f"No se encontró API key para el modelo {name} (variable: {env_key_name})")
    
    def generate(self, prompt):
        raise NotImplementedError("Los modelos específicos deben implementar este método")

class OpenAIModel(ModelBase):
    def __init__(self):
        try:
            super().__init__("GPT-3.5")
            self.client = OpenAI(api_key=self.api_key)
            self.logger = StreamlitLogger().get_logger()
            self.logger.info("Modelo OpenAI inicializado correctamente")
        except Exception as e:
            self.logger = StreamlitLogger().get_logger()
            self.logger.error(f"Error inicializando OpenAI: {str(e)}")
            raise
    
    def generate(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=st.session_state.config["temperatura"],
                max_tokens=st.session_state.config["max_tokens"]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger = StreamlitLogger().get_logger()
            logger.error(f"Error en OpenAI: {str(e)}")
            raise

class DeepseekModel(ModelBase):
    def __init__(self):
        super().__init__("Deepseek")
        # Configuración específica de Deepseek
    
    def generate(self, prompt):
        # Implementación real de Deepseek
        return f"Respuesta simulada de Deepseek: {prompt}"

class LlamaModel(ModelBase):
    def __init__(self):
        super().__init__("LLaMA")
        # Configuración específica de LLaMA
    
    def generate(self, prompt):
        # Implementación real de LLaMA
        return f"Respuesta simulada de LLaMA: {prompt}"

# Componentes de UI
def render_sidebar():
    with st.sidebar:
        st.title("⚙️ Configuración")
        
        modelo = st.selectbox(
            "Selecciona el modelo",
            ["GPT-3.5", "Deepseek", "LLaMA-2"],
            help="Elige el modelo de lenguaje a utilizar"
        )
        
        temperatura = st.slider(
            "Temperatura",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            help="Controla la creatividad de las respuestas"
        )
        
        max_tokens = st.number_input(
            "Máximo de tokens",
            min_value=50,
            max_value=2000,
            value=150,
            help="Límite de tokens en la respuesta"
        )
        
        if st.button("Limpiar Chat"):
            st.session_state.messages = []
            st.session_state.metrics = {
                'requests_count': 0,
                'error_count': 0,
                'response_times': [],
                'model_usage': {},
                'token_usage': {}
            }
        
        return {
            "modelo": modelo,
            "temperatura": temperatura,
            "max_tokens": max_tokens
        }

def render_metrics_dashboard():
    st.header("📊 Métricas")
    
    metrics = st.session_state.metrics
    
    # Métricas principales
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Requests", metrics['requests_count'])
    with col2:
        error_rate = metrics['error_count'] / metrics['requests_count'] if metrics['requests_count'] > 0 else 0
        st.metric("Error Rate", f"{error_rate:.2%}")
    with col3:
        avg_time = sum(metrics['response_times']) / len(metrics['response_times']) if metrics['response_times'] else 0
        st.metric("Avg Response Time", f"{avg_time:.2f}s")
    
    # Gráficos
    col1, col2 = st.columns(2)
    with col1:
        if metrics['model_usage']:
            fig1 = px.pie(
                values=list(metrics['model_usage'].values()),
                names=list(metrics['model_usage'].keys()),
                title="Uso de Modelos"
            )
            st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        if metrics['response_times']:
            fig2 = px.line(
                y=metrics['response_times'],
                title="Tiempos de Respuesta"
            )
            st.plotly_chart(fig2, use_container_width=True)

def get_model_instance(model_name):
    model_map = {
        "GPT-3.5": OpenAIModel,
        "Deepseek": DeepseekModel,
        "LLaMA-2": LlamaModel
    }
    try:
        return model_map[model_name]()
    except Exception as e:
        logger = StreamlitLogger().get_logger()
        logger.error(f"Error creando modelo {model_name}: {str(e)}")
        st.error(f"Error al inicializar el modelo: {str(e)}")
        return None

def render_chat():
    st.header("💬 Chat")
    
    # Inicializar mensajes si no existen
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Mostrar mensajes
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input del usuario
    if prompt := st.chat_input("Escribe tu mensaje..."):
        # Agregar mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generar respuesta
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                start_time = time.time()
                try:
                    modelo_actual = get_model_instance(st.session_state.config["modelo"])
                    if modelo_actual:
                        respuesta = modelo_actual.generate(prompt)
                        tokens = len(prompt.split()) + len(respuesta.split())
                        
                        # Registrar métricas
                        response_time = time.time() - start_time
                        MetricsCollector().log_request(
                            modelo_actual.name,
                            response_time,
                            tokens
                        )
                        
                        st.markdown(respuesta)
                        st.session_state.messages.append({"role": "assistant", "content": respuesta})
                except Exception as e:
                    MetricsCollector().log_error(st.session_state.config["modelo"], type(e).__name__)
                    st.error(f"Error: {str(e)}")

def initialize_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'config' not in st.session_state:
        st.session_state.config = {
            "modelo": "GPT-3.5",
            "temperatura": 0.7,
            "max_tokens": 150
        }
    
    MetricsCollector.initialize_metrics()

def main():
    # Configuración de la página
    st.set_page_config(
        page_title="ChatBot Multi-Modelo",
        page_icon="🤖",
        layout="wide"
    )
    
    # Inicializar estado
    initialize_session_state()
    
    # Inicializar logger
    logger = StreamlitLogger().get_logger()
    
    # Configuración desde sidebar
    st.session_state.config = render_sidebar()
    
    # Tabs principales
    tab1, tab2 = st.tabs(["Chat", "Métricas"])
    
    with tab1:
        render_chat()
    
    with tab2:
        render_metrics_dashboard()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>Desarrollado con ❤️ usando Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    load_dotenv()  # Cargar variables de entorno desde .env
    main() 