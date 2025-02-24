import streamlit as st
import time
import plotly.express as px
import pandas as pd

class MetricsCollector:
    def __init__(self):
        if 'metrics' not in st.session_state:
            st.session_state.metrics = {
                'requests_count': 0,
                'error_count': 0,
                'response_times': [],
                'model_usage': {
                    'GPT-3': 0,
                    'GPT-4': 0,
                    'Claude': 0
                }
            }
    
    def simulate_request(self, model_name):
        start_time = time.time()
        time.sleep(0.5)  # Simular procesamiento
        response_time = time.time() - start_time
        
        st.session_state.metrics['requests_count'] += 1
        st.session_state.metrics['response_times'].append(response_time)
        st.session_state.metrics['model_usage'][model_name] += 1
    
    def simulate_error(self):
        st.session_state.metrics['error_count'] += 1

def render_metrics_dashboard():
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
    
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.pie(
            values=list(metrics['model_usage'].values()),
            names=list(metrics['model_usage'].keys()),
            title="Uso de Modelos"
        )
        st.plotly_chart(fig1)
    
    with col2:
        if metrics['response_times']:
            fig2 = px.line(
                y=metrics['response_times'],
                title="Tiempos de Respuesta"
            )
            st.plotly_chart(fig2)

def main():
    st.set_page_config(page_title="Demo Métricas", page_icon="📊", layout="wide")
    
    st.title("Demo de Métricas y Monitoreo")
    
    metrics_collector = MetricsCollector()
    
    col1, col2 = st.columns(2)
    with col1:
        modelo = st.selectbox("Selecciona un modelo", ['GPT-3', 'GPT-4', 'Claude'])
        if st.button("Simular Request"):
            metrics_collector.simulate_request(modelo)
    
    with col2:
        if st.button("Simular Error"):
            metrics_collector.simulate_error()
    
    st.divider()
    render_metrics_dashboard()

if __name__ == "__main__":
    main() 