# Práctica: Implementación de Monitoreo y Optimización en Chatbot Multi-Modelo (45 minutos)

## Descripción

En esta sesión práctica, implementaremos un sistema completo de monitoreo, logging y optimización para nuestro chatbot multi-modelo. Aplicaremos los conceptos aprendidos para crear una aplicación robusta y monitoreable.

## Objetivos

- Implementar un sistema de logging completo
- Crear un dashboard de monitoreo en tiempo real
- Optimizar el rendimiento de la aplicación
- Implementar manejo avanzado de errores

## Actividades

### 1. Configuración del Sistema de Logging (10 minutos)

1. Crear archivo `utils/logging_config.py`:
```python
import logging
import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx
from datetime import datetime
import os

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
            f'logs/app_{datetime.now().strftime("%Y%m%d")}.log'
        )
        file_handler.setLevel(logging.INFO)
        
        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formato
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def get_logger(self):
        ctx = get_script_run_ctx()
        if ctx is None:
            return self.logger
        return logging.getLogger(f"{__name__}.{ctx.session_id}")

logger = StreamlitLogger().get_logger()
```

### 2. Implementación de Métricas (10 minutos)

1. Crear archivo `utils/metrics.py`:
```python
import streamlit as st
import time
from datetime import datetime
import json

class MetricsCollector:
    def __init__(self):
        if 'metrics' not in st.session_state:
            st.session_state.metrics = {
                'requests': [],
                'errors': [],
                'model_usage': {},
                'response_times': []
            }
    
    def log_request(self, model_name, prompt, response, response_time):
        request_data = {
            'timestamp': datetime.now().isoformat(),
            'model': model_name,
            'prompt_length': len(prompt),
            'response_length': len(response),
            'response_time': response_time
        }
        st.session_state.metrics['requests'].append(request_data)
        
        if model_name not in st.session_state.metrics['model_usage']:
            st.session_state.metrics['model_usage'][model_name] = 0
        st.session_state.metrics['model_usage'][model_name] += 1
        
        st.session_state.metrics['response_times'].append(response_time)
    
    def log_error(self, model_name, error_type, error_message):
        error_data = {
            'timestamp': datetime.now().isoformat(),
            'model': model_name,
            'type': error_type,
            'message': error_message
        }
        st.session_state.metrics['errors'].append(error_data)
    
    def get_summary(self):
        metrics = st.session_state.metrics
        total_requests = len(metrics['requests'])
        total_errors = len(metrics['errors'])
        
        return {
            'total_requests': total_requests,
            'error_rate': total_errors / total_requests if total_requests > 0 else 0,
            'avg_response_time': sum(metrics['response_times']) / len(metrics['response_times']) if metrics['response_times'] else 0,
            'model_usage': metrics['model_usage']
        }
    
    def export_metrics(self):
        return json.dumps(st.session_state.metrics, indent=2)
```

### 3. Implementación del Dashboard (15 minutos)

1. Crear archivo `components/dashboard.py`:
```python
import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

def render_metrics_dashboard(metrics_collector):
    st.header("📊 Dashboard de Monitoreo")
    
    # Métricas principales
    summary = metrics_collector.get_summary()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Requests", summary['total_requests'])
    with col2:
        st.metric("Error Rate", f"{summary['error_rate']:.2%}")
    with col3:
        st.metric("Avg Response Time", f"{summary['avg_response_time']:.2f}s")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Uso de Modelos")
        if summary['model_usage']:
            fig = px.pie(
                values=list(summary['model_usage'].values()),
                names=list(summary['model_usage'].keys()),
                title="Distribución de Uso de Modelos"
            )
            st.plotly_chart(fig)
    
    with col2:
        st.subheader("Tiempos de Respuesta")
        if st.session_state.metrics['response_times']:
            fig = px.line(
                y=st.session_state.metrics['response_times'],
                title="Tiempos de Respuesta por Request"
            )
            st.plotly_chart(fig)
    
    # Tabla de errores recientes
    st.subheader("Errores Recientes")
    if st.session_state.metrics['errors']:
        df_errors = pd.DataFrame(st.session_state.metrics['errors'])
        st.dataframe(df_errors)
```

### 4. Integración en la Aplicación Principal (10 minutos)

Modificar `app.py`:
```python
import streamlit as st
from utils.logging_config import logger
from utils.metrics import MetricsCollector
from components.dashboard import render_metrics_dashboard
import time

# ... (código anterior) ...

def main():
    st.title("🤖 ChatBot Multi-Modelo con Monitoreo")
    
    # Inicializar collector de métricas
    metrics_collector = MetricsCollector()
    
    # Tabs principales
    tab1, tab2 = st.tabs(["Chat", "Dashboard"])
    
    with tab1:
        # Código del chat existente...
        if submitted and user_input:
            start_time = time.time()
            try:
                respuesta = st.session_state.modelo_actual.generar_texto(
                    user_input,
                    **configuracion
                )
                tiempo_respuesta = time.time() - start_time
                
                # Registrar métricas
                metrics_collector.log_request(
                    modelo_seleccionado,
                    user_input,
                    respuesta,
                    tiempo_respuesta
                )
                
                logger.info(f"Respuesta generada por {modelo_seleccionado} en {tiempo_respuesta:.2f}s")
                
            except Exception as e:
                logger.error(f"Error generando respuesta: {str(e)}")
                metrics_collector.log_error(
                    modelo_seleccionado,
                    type(e).__name__,
                    str(e)
                )
                respuesta = f"Error: {str(e)}"
    
    with tab2:
        render_metrics_dashboard(metrics_collector)
        
        # Botón para exportar métricas
        if st.button("Exportar Métricas"):
            st.download_button(
                "Descargar JSON",
                metrics_collector.export_metrics(),
                "metricas.json",
                "application/json"
            )

if __name__ == "__main__":
    main()
```

## Ejercicios Adicionales

1. **Implementar Alertas**
   - Crear un sistema de alertas para errores frecuentes
   - Notificar cuando el tiempo de respuesta supera un umbral

2. **Métricas Avanzadas**
   - Agregar análisis de tokens utilizados
   - Implementar costos estimados por modelo
   - Agregar métricas de uso de memoria

3. **Optimización**
   - Implementar limpieza automática de métricas antiguas
   - Agregar compresión de logs
   - Optimizar el rendimiento del dashboard

## Recursos

- [Plotly Documentation](https://plotly.com/python/)
- [Streamlit Metrics](https://docs.streamlit.io/library/api-reference/metrics)
- [Python Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)

## Conclusión
Has completado la implementación de un sistema completo de monitoreo y optimización para tu chatbot multi-modelo. Esta base te permitirá mantener y mejorar tu aplicación de manera efectiva. 