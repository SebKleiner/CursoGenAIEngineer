import streamlit as st
import time
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
from collections import deque
from openai import OpenAI
import os
from dotenv import load_dotenv
import logging
import json
from pathlib import Path
import uuid

# Configuración de directorios
HISTORY_DIR = Path("chat_history")
HISTORY_DIR.mkdir(exist_ok=True)

class StreamlitLogger:
    def __init__(self):
        self.logger = self._configure_logger()
    
    def _configure_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        os.makedirs('logs', exist_ok=True)
        file_handler = logging.FileHandler(
            f'logs/chatbot_{datetime.now().strftime("%Y%m%d")}.log'
        )
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def get_logger(self):
        return self.logger

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

class ConversationManager:
    def __init__(self):
        self.history_file = HISTORY_DIR / "conversations.json"
        self.current_conversation_id = self._get_or_create_conversation_id()
        self._load_or_initialize_history()
    
    def _get_or_create_conversation_id(self):
        if 'conversation_id' not in st.session_state:
            st.session_state.conversation_id = str(uuid.uuid4())
        return st.session_state.conversation_id
    
    def _load_or_initialize_history(self):
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                self.history = json.load(f)
        else:
            self.history = {}
        
        if self.current_conversation_id not in self.history:
            self.history[self.current_conversation_id] = {
                "created_at": datetime.now().isoformat(),
                "messages": []
            }
    
    def save_message(self, message):
        self.history[self.current_conversation_id]["messages"].append({
            "timestamp": datetime.now().isoformat(),
            **message
        })
        
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
        
        self._update_cache()
    
    def _update_cache(self):
        messages = self.history[self.current_conversation_id]["messages"]
        
        st.session_state.conversation_cache.clear()
        st.session_state.cache_timestamps.clear()
        
        interactions = []
        for i in range(len(messages)-1, -1, -2):
            if i > 0:
                assistant_msg = messages[i]
                user_msg = messages[i-1]
                
                interaction = {
                    "timestamp": datetime.fromisoformat(assistant_msg["timestamp"]),
                    "user_message": user_msg,
                    "assistant_message": assistant_msg
                }
                interactions.insert(0, interaction)
                
                if len(interactions) >= 3:
                    break
        
        for interaction in interactions:
            st.session_state.conversation_cache.append(interaction)
            st.session_state.cache_timestamps.append(interaction["timestamp"])
    
    def get_current_conversation(self):
        return self.history[self.current_conversation_id]["messages"]
    
    def new_conversation(self):
        st.session_state.conversation_id = str(uuid.uuid4())
        self.current_conversation_id = st.session_state.conversation_id
        self.history[self.current_conversation_id] = {
            "created_at": datetime.now().isoformat(),
            "messages": []
        }
        st.session_state.conversation_cache.clear()
        st.session_state.cache_timestamps.clear()
    
    def list_conversations(self):
        return [{
            "id": conv_id,
            "created_at": data["created_at"],
            "message_count": len(data["messages"])
        } for conv_id, data in self.history.items()]

    def load_conversation(self, conversation_id):
        """Carga una conversación existente y actualiza el caché"""
        if conversation_id in self.history:
            st.session_state.conversation_id = conversation_id
            self.current_conversation_id = conversation_id
            # Actualizar el caché con las últimas 3 interacciones de esta conversación
            self._update_cache()
            return True
        return False

class ModelBase:
    def __init__(self, name, api_key=None):
        self.name = name
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
            self.logger.error(f"Error en OpenAI: {str(e)}")
            raise

class DeepseekModel(ModelBase):
    def __init__(self):
        super().__init__("Deepseek")
    
    def generate(self, prompt):
        return f"Respuesta simulada de Deepseek: {prompt}"

class LlamaModel(ModelBase):
    def __init__(self):
        super().__init__("LLaMA")
    
    def generate(self, prompt):
        return f"Respuesta simulada de LLaMA: {prompt}"

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

def render_metrics():
    st.subheader("📈 Métricas de Uso")
    
    metrics = st.session_state.metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Requests", metrics['requests_count'])
    
    with col2:
        error_rate = metrics['error_count'] / metrics['requests_count'] if metrics['requests_count'] > 0 else 0
        st.metric("Error Rate", f"{error_rate:.2%}")
    
    with col3:
        avg_time = sum(metrics['response_times']) / len(metrics['response_times']) if metrics['response_times'] else 0
        st.metric("Avg Response Time", f"{avg_time:.2f}s")
    
    if metrics['model_usage']:
        col1, col2 = st.columns(2)
        with col1:
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

def render_cache_metrics():
    st.subheader("📊 Métricas de Caché")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Interacciones en Caché", len(st.session_state.conversation_cache))
    
    with col2:
        if st.session_state.cache_timestamps:
            oldest = min(st.session_state.cache_timestamps)
            age = datetime.now() - oldest
            st.metric("Edad del Caché", f"{int(age.total_seconds() / 60)} min")
        else:
            st.metric("Edad del Caché", "0 min")

def render_cached_interactions():
    st.subheader("💬 Últimas Interacciones")
    
    if not st.session_state.conversation_cache:
        st.info("No hay interacciones en caché")
        return
    
    for idx, interaction in enumerate(st.session_state.conversation_cache):
        time_left = interaction["timestamp"] + timedelta(minutes=30) - datetime.now()
        
        with st.expander(f"Interacción {idx + 1} - Expira en {int(time_left.total_seconds() / 60)} min"):
            st.caption(f"Timestamp: {interaction['timestamp'].strftime('%H:%M:%S')}")
            
            with st.chat_message("user"):
                st.markdown(interaction["user_message"]["content"])
            
            with st.chat_message("assistant"):
                st.markdown(interaction["assistant_message"]["content"])

def render_history_dashboard():
    st.header("📚 Historial de Conversaciones")
    
    conversation_manager = ConversationManager()
    conversations = conversation_manager.list_conversations()
    
    total_convs = len(conversations)
    total_msgs = sum(conv["message_count"] for conv in conversations)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Conversaciones", total_convs)
    with col2:
        st.metric("Total Mensajes", total_msgs)
    
    for conv in conversations:
        with st.expander(f"Conversación {conv['id'][:8]} - {conv['created_at']}"):
            st.write(f"Mensajes: {conv['message_count']}")
            if st.button("Cargar", key=conv['id']):
                # Usar el nuevo método load_conversation
                if conversation_manager.load_conversation(conv['id']):
                    st.rerun()
                else:
                    st.error("Error al cargar la conversación")

def chat_interface():
    st.header("💭 Chat con Historial y Caché")
    
    conversation_manager = ConversationManager()
    
    for message in conversation_manager.get_current_conversation():
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Escribe tu mensaje..."):
        user_message = {"role": "user", "content": prompt}
        conversation_manager.save_message(user_message)
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                start_time = time.time()
                try:
                    modelo_actual = get_model_instance(st.session_state.config["modelo"])
                    if modelo_actual:
                        respuesta = modelo_actual.generate(prompt)
                        tokens = len(prompt.split()) + len(respuesta.split())
                        
                        response_time = time.time() - start_time
                        MetricsCollector().log_request(
                            modelo_actual.name,
                            response_time,
                            tokens
                        )
                        
                        assistant_message = {"role": "assistant", "content": respuesta}
                        conversation_manager.save_message(assistant_message)
                        st.markdown(respuesta)
                        
                except Exception as e:
                    MetricsCollector().log_error(st.session_state.config["modelo"], type(e).__name__)
                    st.error(f"Error: {str(e)}")

def render_sidebar():
    st.sidebar.title("⚙️ Configuración")
    
    if st.sidebar.button("Nueva Conversación"):
        ConversationManager().new_conversation()
        st.rerun()
    
    modelo = st.sidebar.selectbox(
        "Selecciona el modelo",
        ["GPT-3.5", "Deepseek", "LLaMA-2"],
        help="Elige el modelo de lenguaje a utilizar"
    )
    
    temperatura = st.sidebar.slider(
        "Temperatura",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        help="Controla la creatividad de las respuestas"
    )
    
    max_tokens = st.sidebar.number_input(
        "Máximo de tokens",
        min_value=50,
        max_value=2000,
        value=150,
        help="Límite de tokens en la respuesta"
    )
    
    if st.sidebar.button("Limpiar Chat"):
        st.session_state.conversation_cache.clear()
        st.session_state.cache_timestamps.clear()
        ConversationManager().new_conversation()
        st.rerun()
    
    return {
        "modelo": modelo,
        "temperatura": temperatura,
        "max_tokens": max_tokens
    }

def initialize_session_state():
    if 'conversation_cache' not in st.session_state:
        st.session_state.conversation_cache = deque(maxlen=3)
        st.session_state.cache_timestamps = deque(maxlen=3)
    
    if 'config' not in st.session_state:
        st.session_state.config = {
            "modelo": "GPT-3.5",
            "temperatura": 0.7,
            "max_tokens": 150
        }
    
    MetricsCollector.initialize_metrics()

def main():
    st.set_page_config(
        page_title="ChatBot con Historial",
        page_icon="🧠",
        layout="wide"
    )
    
    initialize_session_state()
    st.session_state.config = render_sidebar()
    
    tab1, tab2, tab3, tab4 = st.tabs(["Chat", "Caché", "Métricas", "Historial"])
    
    with tab1:
        chat_interface()
    
    with tab2:
        render_cache_metrics()
        st.divider()
        render_cached_interactions()
    
    with tab3:
        render_metrics()
    
    with tab4:
        render_history_dashboard()

if __name__ == "__main__":
    load_dotenv()
    main() 