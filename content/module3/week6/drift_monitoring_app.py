import streamlit as st
import numpy as np
from sentence_transformers import SentenceTransformer
from textblob import TextBlob
import nltk
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from collections import deque, defaultdict
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from pathlib import Path
import os
from sklearn.decomposition import PCA
import seaborn as sns
import matplotlib.pyplot as plt

# Descargar recursos necesarios de NLTK
nltk.download('punkt')

class EnterpriseDriftMonitor:
    def __init__(self, window_size=10):
        self.window_size = window_size
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Ventanas de datos por tipo de implementación
        self.windows = {
            'prompt_engineering': {'inputs': deque(maxlen=window_size), 'outputs': deque(maxlen=window_size)},
            'rag': {'inputs': deque(maxlen=window_size), 'outputs': deque(maxlen=window_size)},
            'fine_tuned': {'inputs': deque(maxlen=window_size), 'outputs': deque(maxlen=window_size)},
            'custom_model': {'inputs': deque(maxlen=window_size), 'outputs': deque(maxlen=window_size)}
        }
        
        # Referencias baseline
        self.baselines = {k: None for k in self.windows.keys()}
        
        # Histórico de métricas
        self.metrics_history = defaultdict(list)
        
        # Clusters temáticos
        self.topic_clusters = None
        self.n_clusters = 5
        
        # Umbrales específicos por tipo
        self.thresholds = {
            'prompt_engineering': {'embedding': 0.3, 'response_consistency': 0.25},
            'rag': {'embedding': 0.35, 'knowledge_coverage': 0.3},
            'fine_tuned': {'domain_drift': 0.4, 'performance_drop': 0.3},
            'custom_model': {'model_decay': 0.45, 'data_shift': 0.35}
        }
        
        # Inicializar con algunos datos de ejemplo
        self._add_sample_data()
        self.pca = PCA(n_components=2)
        self.embedding_cache = defaultdict(dict)
    
    def _add_sample_data(self):
        """Agrega datos de ejemplo para inicializar las métricas"""
        sample_conversations = [
            ("¿Cómo puedo devolver un producto?", "Para devolver un producto, siga estos pasos..."),
            ("¿Cuál es la política de reembolso?", "Nuestra política de reembolso establece que..."),
            ("Necesito ayuda con mi pedido", "Por supuesto, ¿podría proporcionarme el número de pedido?"),
            ("¿Dónde está mi envío?", "Para rastrear su envío, necesito el número de seguimiento..."),
            ("¿Tienen descuentos disponibles?", "Sí, actualmente tenemos las siguientes promociones...")
        ]
        
        for prompt, response in sample_conversations:
            self.add_interaction('prompt_engineering', prompt, response)
            self.add_interaction('rag', prompt, response)
            self.add_interaction('fine_tuned', prompt, response)
            self.add_interaction('custom_model', prompt, response)
    
    def add_interaction(self, implementation_type, user_input, model_output, metadata=None):
        """Registra una nueva interacción con metadatos adicionales"""
        window = self.windows[implementation_type]
        window['inputs'].append({
            'text': user_input,
            'metadata': metadata or {},
            'timestamp': datetime.now()
        })
        window['outputs'].append({
            'text': model_output,
            'metadata': metadata or {},
            'timestamp': datetime.now()
        })
        
        if not self.baselines[implementation_type] and len(window['inputs']) == self.window_size:
            self.baselines[implementation_type] = {
                'inputs': list(window['inputs']),
                'outputs': list(window['outputs'])
            }
            self._initialize_topic_clusters(implementation_type)
        
        if len(window['inputs']) == self.window_size:
            self._calculate_implementation_metrics(implementation_type)
    
    def _initialize_topic_clusters(self, implementation_type):
        """Inicializa clusters temáticos para la línea base"""
        texts = [item['text'] for item in self.baselines[implementation_type]['inputs']]
        embeddings = self.embedding_model.encode(texts)
        self.topic_clusters = KMeans(n_clusters=self.n_clusters).fit(embeddings)
    
    def _calculate_implementation_metrics(self, implementation_type):
        """Calcula métricas específicas según el tipo de implementación"""
        current_time = datetime.now()
        window = self.windows[implementation_type]
        baseline = self.baselines[implementation_type]
        
        # Métricas base
        metrics = {
            'timestamp': current_time,
            'implementation_type': implementation_type
        }
        
        # Métricas específicas por tipo
        if implementation_type == 'prompt_engineering':
            metrics.update(self._calculate_prompt_engineering_metrics(window, baseline))
        elif implementation_type == 'rag':
            metrics.update(self._calculate_rag_metrics(window, baseline))
        elif implementation_type == 'fine_tuned':
            metrics.update(self._calculate_fine_tuned_metrics(window, baseline))
        elif implementation_type == 'custom_model':
            metrics.update(self._calculate_custom_model_metrics(window, baseline))
        
        self.metrics_history[implementation_type].append(metrics)
    
    def _calculate_embedding_drift(self, texts1, texts2):
        """Calcula el drift entre dos conjuntos de textos usando embeddings"""
        if not texts1 or not texts2:
            return 0.0
        
        emb1 = self.embedding_model.encode(texts1)
        emb2 = self.embedding_model.encode(texts2)
        
        centroid1 = np.mean(emb1, axis=0)
        centroid2 = np.mean(emb2, axis=0)
        
        return 1 - np.dot(centroid1, centroid2) / (
            np.linalg.norm(centroid1) * np.linalg.norm(centroid2)
        )
    
    def _calculate_prompt_engineering_metrics(self, window, baseline):
        """Métricas específicas para prompt engineering"""
        current_inputs = [item['text'] for item in window['inputs']]
        current_outputs = [item['text'] for item in window['outputs']]
        baseline_inputs = [item['text'] for item in baseline['inputs']]
        baseline_outputs = [item['text'] for item in baseline['outputs']]
        
        embedding_drift = self._calculate_embedding_drift(baseline_inputs, current_inputs)
        response_consistency = self._calculate_embedding_drift(baseline_outputs, current_outputs)
        
        return {
            'embedding': embedding_drift,
            'response_consistency': response_consistency
        }
    
    def _calculate_rag_metrics(self, window, baseline):
        """Métricas específicas para RAG"""
        current_inputs = [item['text'] for item in window['inputs']]
        current_outputs = [item['text'] for item in window['outputs']]
        
        embedding_drift = self._calculate_embedding_drift(
            [item['text'] for item in baseline['inputs']],
            current_inputs
        )
        
        # Simulación de cobertura de conocimiento
        knowledge_coverage = np.random.uniform(0.6, 1.0)  # En producción, usar métricas reales
        
        return {
            'embedding': embedding_drift,
            'knowledge_coverage': knowledge_coverage
        }
    
    def _calculate_fine_tuned_metrics(self, window, baseline):
        """Métricas específicas para modelos fine-tuned"""
        current_inputs = [item['text'] for item in window['inputs']]
        
        domain_drift = self._calculate_embedding_drift(
            [item['text'] for item in baseline['inputs']],
            current_inputs
        )
        
        # Simulación de caída de rendimiento
        performance_drop = np.random.uniform(0.0, 0.5)  # En producción, usar métricas reales
        
        return {
            'domain_drift': domain_drift,
            'performance_drop': performance_drop
        }
    
    def _calculate_custom_model_metrics(self, window, baseline):
        """Métricas específicas para modelos personalizados"""
        current_inputs = [item['text'] for item in window['inputs']]
        current_outputs = [item['text'] for item in window['outputs']]
        
        model_decay = self._calculate_embedding_drift(
            [item['text'] for item in baseline['outputs']],
            current_outputs
        )
        
        data_shift = self._calculate_embedding_drift(
            [item['text'] for item in baseline['inputs']],
            current_inputs
        )
        
        return {
            'model_decay': model_decay,
            'data_shift': data_shift
        }
    
    def get_alerts(self, implementation_type=None):
        """Obtiene alertas activas para un tipo de implementación específico"""
        alerts = []
        types_to_check = [implementation_type] if implementation_type else self.windows.keys()
        
        for imp_type in types_to_check:
            if not self.metrics_history[imp_type]:
                continue
            
            latest = self.metrics_history[imp_type][-1]
            thresholds = self.thresholds[imp_type]
            
            for metric, threshold in thresholds.items():
                if metric in latest and latest[metric] > threshold:
                    alerts.append({
                        'type': f"{imp_type.upper()} - {metric}",
                        'value': latest[metric],
                        'threshold': threshold,
                        'timestamp': latest['timestamp']
                    })
        
        return alerts
    
    def plot_metrics(self, implementation_type=None):
        """Genera visualizaciones de métricas para análisis"""
        if not any(self.metrics_history.values()):
            return None
        
        types_to_plot = [implementation_type] if implementation_type else self.windows.keys()
        fig = go.Figure()
        
        for imp_type in types_to_plot:
            if not self.metrics_history[imp_type]:
                continue
            
            df = pd.DataFrame(self.metrics_history[imp_type])
            metrics_to_plot = [col for col in df.columns if col not in ['timestamp', 'implementation_type']]
            
            for metric in metrics_to_plot:
                fig.add_trace(go.Scatter(
                    x=df['timestamp'],
                    y=df[metric],
                    name=f"{imp_type} - {metric}",
                    mode='lines+markers'
                ))
        
        fig.update_layout(
            title='Métricas de Drift por Tipo de Implementación',
            xaxis_title='Tiempo',
            yaxis_title='Valor',
            height=500
        )
        
        return fig
    
    def _calculate_embeddings(self, texts):
        """Calcula embeddings para un conjunto de textos"""
        if not texts:
            return np.array([])
        return self.embedding_model.encode(texts)
    
    def visualize_embedding_drift(self, implementation_type):
        """Visualiza el drift en el espacio de embeddings"""
        window = self.windows[implementation_type]
        baseline = self.baselines[implementation_type]
        
        if not baseline:
            return None
        
        # Obtener textos y calcular embeddings
        current_texts = [item['text'] for item in window['inputs']]
        baseline_texts = [item['text'] for item in baseline['inputs']]
        
        # Calcular embeddings
        current_embeddings = self._calculate_embeddings(current_texts)
        baseline_embeddings = self._calculate_embeddings(baseline_texts)
        
        # Combinar embeddings y aplicar PCA
        all_embeddings = np.vstack([baseline_embeddings, current_embeddings])
        embeddings_2d = self.pca.fit_transform(all_embeddings)
        
        # Separar puntos de baseline y actuales
        n_baseline = len(baseline_texts)
        baseline_points = embeddings_2d[:n_baseline]
        current_points = embeddings_2d[n_baseline:]
        
        # Crear visualización con Plotly
        fig = go.Figure()
        
        # Puntos del baseline
        fig.add_trace(go.Scatter(
            x=baseline_points[:, 0],
            y=baseline_points[:, 1],
            mode='markers',
            name='Baseline',
            marker=dict(size=10, color='blue', symbol='circle')
        ))
        
        # Puntos actuales
        fig.add_trace(go.Scatter(
            x=current_points[:, 0],
            y=current_points[:, 1],
            mode='markers',
            name='Actual',
            marker=dict(size=10, color='red', symbol='diamond')
        ))
        
        fig.update_layout(
            title='Visualización de Data Drift (PCA)',
            xaxis_title='Componente Principal 1',
            yaxis_title='Componente Principal 2',
            height=400
        )
        
        return fig
    
    def visualize_similarity_heatmap(self, implementation_type):
        """Genera un heatmap de similitud entre prompts actuales y baseline"""
        window = self.windows[implementation_type]
        baseline = self.baselines[implementation_type]
        
        if not baseline:
            return None
        
        # Obtener textos
        current_texts = [item['text'] for item in window['inputs']][-5:]  # Últimos 5 para claridad
        baseline_texts = [item['text'] for item in baseline['inputs']][:5]  # Primeros 5 para claridad
        
        # Calcular embeddings
        current_embeddings = self._calculate_embeddings(current_texts)
        baseline_embeddings = self._calculate_embeddings(baseline_texts)
        
        # Calcular matriz de similitud
        similarity_matrix = np.zeros((len(current_texts), len(baseline_texts)))
        for i, curr_emb in enumerate(current_embeddings):
            for j, base_emb in enumerate(baseline_embeddings):
                similarity_matrix[i, j] = np.dot(curr_emb, base_emb) / (
                    np.linalg.norm(curr_emb) * np.linalg.norm(base_emb)
                )
        
        # Crear heatmap con Plotly
        fig = go.Figure(data=go.Heatmap(
            z=similarity_matrix,
            x=[f'Base {i+1}' for i in range(len(baseline_texts))],
            y=[f'Actual {i+1}' for i in range(len(current_texts))],
            colorscale='RdBu',
            zmin=0,
            zmax=1
        ))
        
        fig.update_layout(
            title='Heatmap de Similitud',
            height=400
        )
        
        return fig
    
    def visualize_drift_trend(self, implementation_type):
        """Visualiza la tendencia del drift a lo largo del tiempo"""
        if not self.metrics_history[implementation_type]:
            return None
        
        df = pd.DataFrame(self.metrics_history[implementation_type])
        
        fig = go.Figure()
        
        metrics_to_plot = [col for col in df.columns if col not in ['timestamp', 'implementation_type']]
        for metric in metrics_to_plot:
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df[metric],
                name=metric,
                mode='lines+markers'
            ))
        
        fig.update_layout(
            title='Tendencia de Drift en el Tiempo',
            xaxis_title='Tiempo',
            yaxis_title='Valor de Drift',
            height=400
        )
        
        return fig

def initialize_session_state():
    """Inicializa el estado de la sesión de Streamlit"""
    if 'drift_monitor' not in st.session_state:
        st.session_state.drift_monitor = EnterpriseDriftMonitor()
    if 'implementation_type' not in st.session_state:
        st.session_state.implementation_type = 'prompt_engineering'
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

def render_sidebar():
    """Renderiza la barra lateral con configuraciones"""
    st.sidebar.title("⚙️ Configuración de Monitoreo")
    
    # Selección de tipo de implementación
    implementation_type = st.sidebar.selectbox(
        "Tipo de Implementación",
        ['prompt_engineering', 'rag', 'fine_tuned', 'custom_model'],
        key='implementation_type'
    )
    
    # Ajuste de umbrales
    st.sidebar.subheader("Umbrales de Alertas")
    for metric, threshold in st.session_state.drift_monitor.thresholds[implementation_type].items():
        new_threshold = st.sidebar.slider(
            f"Umbral para {metric}",
            0.0, 1.0, threshold,
            key=f"threshold_{implementation_type}_{metric}"
        )
        st.session_state.drift_monitor.thresholds[implementation_type][metric] = new_threshold
    
    # Botón para limpiar historial
    if st.sidebar.button("Limpiar Historial"):
        st.session_state.chat_history = []
        st.rerun()

def render_metrics_dashboard():
    """Renderiza el dashboard de métricas"""
    st.subheader("📊 Dashboard de Métricas")
    
    # Mostrar progreso hacia la línea base
    implementation_type = st.session_state.implementation_type
    window = st.session_state.drift_monitor.windows[implementation_type]
    current_interactions = len(window['inputs'])
    window_size = st.session_state.drift_monitor.window_size
    
    # Barra de progreso
    st.progress(current_interactions / window_size)
    st.caption(f"Interacciones: {current_interactions}/{window_size} necesarias para línea base")
    
    # Mostrar alertas activas
    alerts = st.session_state.drift_monitor.get_alerts(st.session_state.implementation_type)
    if alerts:
        st.warning("⚠️ Alertas Activas")
        for alert in alerts:
            st.error(
                f"🚨 {alert['type']}: {alert['value']:.3f} > {alert['threshold']}"
            )
    
    # Pestañas para diferentes visualizaciones
    tab1, tab2, tab3 = st.tabs(["Distribución", "Similitud", "Tendencia"])
    
    with tab1:
        fig_dist = st.session_state.drift_monitor.visualize_embedding_drift(implementation_type)
        if fig_dist:
            st.plotly_chart(fig_dist, use_container_width=True)
        else:
            st.info("Esperando datos suficientes para visualizar distribución")
    
    with tab2:
        fig_sim = st.session_state.drift_monitor.visualize_similarity_heatmap(implementation_type)
        if fig_sim:
            st.plotly_chart(fig_sim, use_container_width=True)
        else:
            st.info("Esperando datos suficientes para visualizar similitud")
    
    with tab3:
        fig_trend = st.session_state.drift_monitor.visualize_drift_trend(implementation_type)
        if fig_trend:
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("Esperando datos suficientes para visualizar tendencia")

def chat_interface():
    """Renderiza la interfaz de chat"""
    st.subheader("💬 Chat de Prueba")
    
    # Mostrar historial de chat
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Input del usuario
    if prompt := st.chat_input("Escribe tu mensaje..."):
        # Agregar mensaje del usuario al historial
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Simular respuesta del modelo
        with st.chat_message("assistant"):
            response = f"Esta es una respuesta simulada para: {prompt}"
            st.write(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Registrar interacción para monitoreo
        st.session_state.drift_monitor.add_interaction(
            st.session_state.implementation_type,
            prompt,
            response
        )

def main():
    st.set_page_config(
        page_title="Monitor de Data Drift",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("🔍 Monitor de Data Drift para LLMs")
    
    initialize_session_state()
    render_sidebar()
    
    # Dividir pantalla en dos columnas
    col1, col2 = st.columns([2, 1])
    
    with col1:
        chat_interface()
    
    with col2:
        render_metrics_dashboard()

if __name__ == "__main__":
    main() 