import streamlit as st
import time
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
from collections import deque, defaultdict
from openai import OpenAI
import os
from dotenv import load_dotenv
import logging
import json
from pathlib import Path
import uuid
from streamlit.runtime.scriptrunner import get_script_run_ctx

# Configuración de directorios
HISTORY_DIR = Path("chat_history")
HISTORY_DIR.mkdir(exist_ok=True)

# Definir costos por modelo (por 1K tokens)
MODEL_COSTS = {
    "GPT-3.5": 0.002,  # $0.002 por 1K tokens
    "Deepseek": 0.001, # $0.001 por 1K tokens (simulado)
    "LLaMA-2": 0.0015  # $0.0015 por 1K tokens (simulado)
}

class StreamlitLogger:
    _instance = None
    _logger = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StreamlitLogger, cls).__new__(cls)
            cls._logger = cls._instance._configure_logger()
        return cls._instance

    def _configure_logger(self):
        if self._logger is None:
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.INFO)
            
            # Limpiar handlers existentes
            logger.handlers = []
            
            # Handler para archivo
            os.makedirs('logs', exist_ok=True)
            file_handler = logging.FileHandler(
                f'logs/chatbot_{datetime.now().strftime("%Y%m%d")}.log'
            )
            file_handler.setLevel(logging.INFO)
            
            # Handler para consola
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # Formato común para ambos handlers
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            # Agregar ambos handlers
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
            
            # Asegurar que los mensajes se propaguen
            logger.propagate = False
            
            return logger
        return self._logger
    
    def get_logger(self):
        try:
            ctx = get_script_run_ctx()
            if ctx is None:
                return self._logger
            session_logger = logging.getLogger(f"{__name__}.{ctx.session_id}")
            # Copiar configuración del logger principal
            session_logger.handlers = self._logger.handlers
            session_logger.setLevel(self._logger.level)
            session_logger.propagate = False
            return session_logger
        except Exception as e:
            print(f"Error getting logger: {e}")  # Debug
            return self._logger

class MetricsCollector:
    @staticmethod
    def initialize_metrics():
        if 'metrics' not in st.session_state:
            st.session_state.metrics = {
                'requests_count': 0,
                'error_count': 0,
                'response_times': [],
                'model_usage': {},
                'token_usage': {},
                'costs': [],
                'costs_by_model': defaultdict(float)
            }
    
    def __init__(self):
        self.logger = StreamlitLogger().get_logger()
        MetricsCollector.initialize_metrics()
    
    def log_request(self, model_name, response_time, tokens_used):
        self.logger.info(
            f"Request: modelo={model_name}, tiempo={response_time:.2f}s, "
            f"tokens={tokens_used}"
        )
        
        metrics = st.session_state.metrics
        metrics['requests_count'] += 1
        metrics['response_times'].append(response_time)
        
        if model_name not in metrics['model_usage']:
            metrics['model_usage'][model_name] = 0
            metrics['token_usage'][model_name] = 0
            
        metrics['model_usage'][model_name] += 1
        metrics['token_usage'][model_name] += tokens_used
        
        # Calcular y registrar costo
        cost = (tokens_used / 1000) * MODEL_COSTS[model_name]
        metrics['costs'].append({
            'timestamp': datetime.now(),
            'model': model_name,
            'cost': cost,
            'tokens': tokens_used
        })
        metrics['costs_by_model'][model_name] += cost
        
        self.logger.info(
            f"Métricas actualizadas: total_requests={metrics['requests_count']}, "
            f"costo_actual=${cost:.4f}, costo_total=${sum(metrics['costs_by_model'].values()):.4f}"
        )
    
    def log_error(self, model_name, error_type):
        self.logger.error(f"Error en modelo {model_name}: {error_type}")
        st.session_state.metrics['error_count'] += 1

class ConversationManager:
    def __init__(self):
        self.logger = StreamlitLogger().get_logger()
        self.history_file = HISTORY_DIR / "conversations.json"
        self.current_conversation_id = self._get_or_create_conversation_id()
        self._load_or_initialize_history()
        self.logger.info(f"ConversationManager inicializado. ID actual: {self.current_conversation_id}")
    
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
        self.logger.info(f"Guardando mensaje en conversación {self.current_conversation_id[:8]}")
        self.history[self.current_conversation_id]["messages"].append({
            "timestamp": datetime.now().isoformat(),
            **message
        })
        
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
        
        self._update_cache()
        self.logger.debug(f"Mensaje guardado y caché actualizado")
    
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
        old_id = self.current_conversation_id
        st.session_state.conversation_id = str(uuid.uuid4())
        self.current_conversation_id = st.session_state.conversation_id
        self.history[self.current_conversation_id] = {
            "created_at": datetime.now().isoformat(),
            "messages": []
        }
        st.session_state.conversation_cache.clear()
        st.session_state.cache_timestamps.clear()
        self.logger.info(f"Nueva conversación creada. ID anterior: {old_id[:8]}, Nuevo ID: {self.current_conversation_id[:8]}")
    
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
            "LLaMA-2": "LLAMA_API_KEY"
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
        super().__init__("LLaMA-2")
    
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
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Conversaciones", total_convs)
    with col2:
        st.metric("Total Mensajes", total_msgs)
    with col3:
        # Botón para descargar todo el historial
        if st.button("📥 Descargar Todo"):
            # Convertir el historial completo a JSON
            full_history = json.dumps(conversation_manager.history, indent=2)
            st.download_button(
                "Descargar Historial Completo",
                full_history,
                "historial_completo.json",
                "application/json",
                use_container_width=True
            )
    
    for conv in conversations:
        with st.expander(f"Conversación {conv['id'][:8]} - {conv['created_at']}"):
            st.write(f"Mensajes: {conv['message_count']}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Cargar", key=f"load_{conv['id']}"):
                    if conversation_manager.load_conversation(conv['id']):
                        st.rerun()
                    else:
                        st.error("Error al cargar la conversación")
            
            with col2:
                # Botón para descargar conversación individual
                if st.button("Descargar", key=f"download_{conv['id']}"):
                    # Obtener solo esta conversación
                    single_conv = {
                        conv['id']: conversation_manager.history[conv['id']]
                    }
                    conv_json = json.dumps(single_conv, indent=2)
                    st.download_button(
                        "Descargar Conversación",
                        conv_json,
                        f"conversacion_{conv['id'][:8]}.json",
                        "application/json",
                        use_container_width=True
                    )

def chat_interface():
    logger = StreamlitLogger().get_logger()
    st.header("💭 Chat con Historial y Caché")
    
    conversation_manager = ConversationManager()
    logger.info("Iniciando interfaz de chat")
    
    for message in conversation_manager.get_current_conversation():
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Escribe tu mensaje..."):
        logger.info("Nuevo mensaje recibido del usuario")
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
                        logger.info(f"Generando respuesta con modelo {modelo_actual.name}")
                        respuesta = modelo_actual.generate(prompt)
                        tokens = len(prompt.split()) + len(respuesta.split())
                        
                        response_time = time.time() - start_time
                        logger.info(
                            f"Respuesta generada exitosamente en {response_time:.2f}s. "
                            f"Tokens utilizados: {tokens}"
                        )
                        
                        MetricsCollector().log_request(
                            modelo_actual.name,
                            response_time,
                            tokens
                        )
                        
                        assistant_message = {"role": "assistant", "content": respuesta}
                        conversation_manager.save_message(assistant_message)
                        st.markdown(respuesta)
                        
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    logger.error(f"Error generando respuesta: {error_msg}")
                    MetricsCollector().log_error(st.session_state.config["modelo"], type(e).__name__)
                    st.error(error_msg)

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

def render_cost_dashboard():
    """Renderiza el dashboard de costos"""
    st.header("💰 Dashboard de Costos")
    
    metrics = st.session_state.metrics
    costs_by_model = metrics['costs_by_model']
    
    # Métricas principales
    total_cost = sum(costs_by_model.values())
    total_tokens = sum(metrics['token_usage'].values())
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Costo Total", f"${total_cost:.4f}")
    with col2:
        st.metric("Total Tokens", f"{total_tokens:,}")
    
    # Gráfico de torta - Costo por modelo
    if costs_by_model:
        st.subheader("Distribución de Costos por Modelo")
        fig = px.pie(
            values=list(costs_by_model.values()),
            names=list(costs_by_model.keys()),
            title="Costo Total por Modelo"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico de barras - Costo por minuto
    st.subheader("Costos por Minuto")
    if metrics['costs']:
        # Agrupar costos por minuto y modelo
        costs_df = pd.DataFrame(metrics['costs'])
        costs_df['minute'] = costs_df['timestamp'].dt.strftime('%H:%M')
        costs_by_minute = costs_df.pivot_table(
            index='minute',
            columns='model',
            values='cost',
            aggfunc='sum'
        ).fillna(0)
        
        fig = px.bar(
            costs_by_minute,
            title="Costos por Minuto y Modelo",
            labels={'value': 'Costo ($)', 'minute': 'Minuto'},
            barmode='stack'
        )
        st.plotly_chart(fig, use_container_width=True)

def main():
    logger = StreamlitLogger().get_logger()
    logger.info("Iniciando aplicación")
    
    st.set_page_config(
        page_title="ChatBot con Historial",
        page_icon="🧠",
        layout="wide"
    )
    
    initialize_session_state()
    st.session_state.config = render_sidebar()
    logger.info(f"Configuración actual: {st.session_state.config}")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Chat", "Caché", "Métricas", "Historial", "Costos"])
    
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
    
    with tab5:
        render_cost_dashboard()

if __name__ == "__main__":
    load_dotenv()
    logger = StreamlitLogger().get_logger()
    logger.info("=== Iniciando nueva sesión de ChatBot ===")
    main() 