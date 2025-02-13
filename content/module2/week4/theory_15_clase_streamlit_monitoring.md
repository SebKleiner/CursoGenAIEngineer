# Monitoreo, Logging y Optimización en Streamlit (45 minutos)

## Descripción

En esta sesión teórica, exploraremos las capacidades de monitoreo y logging de Streamlit, así como técnicas avanzadas de optimización. Aprenderemos a utilizar streamlit.logger._loggers para monitorear nuestra aplicación y mejorar su rendimiento.

## Objetivos

- Comprender el sistema de logging de Streamlit
- Implementar monitoreo efectivo de la aplicación
- Optimizar el rendimiento y uso de recursos
- Utilizar técnicas avanzadas de debugging
- Implementar métricas y analytics

## Contenido

### 1. Sistema de Logging en Streamlit

El sistema de logging en Streamlit nos permite rastrear y registrar eventos importantes en nuestra aplicación. La configuración básica establece un logger personalizado que puede escribir tanto en la consola como en archivos, permitiéndonos mantener un registro detallado de la actividad de la aplicación. El acceso a los loggers de Streamlit nos da información específica de cada sesión.

#### Configuración Básica
```python
import streamlit as st
import logging

# Configurar logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Configurar handler
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
```

#### Acceso a Loggers de Streamlit
```python
from streamlit.logger import get_logger
from streamlit.runtime.scriptrunner import get_script_run_ctx

def get_streamlit_logger():
    ctx = get_script_run_ctx()
    if ctx is None:
        return get_logger(__name__)
    return get_logger(f"{__name__}.{ctx.session_id}")
```

### 2. Monitoreo de Eventos

El monitoreo de eventos nos permite seguir las interacciones de los usuarios y el rendimiento de nuestra aplicación. Implementamos decoradores y funciones auxiliares para registrar automáticamente tiempos de ejecución y acciones del usuario, proporcionando insights valiosos sobre el uso de la aplicación.

#### Tracking de Interacciones
```python
def log_user_interaction(action, details=None):
    logger = get_streamlit_logger()
    session_id = get_script_run_ctx().session_id
    logger.info(f"User Action: {action} | Session: {session_id} | Details: {details}")

# Uso
if st.button("Procesar"):
    log_user_interaction("button_click", "Procesar clicked")
```

#### Monitoreo de Rendimiento
```python
import time
from functools import wraps

def monitor_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        logger = get_streamlit_logger()
        logger.info(f"Function {func.__name__} took {execution_time:.2f} seconds")
        return result
    return wrapper

@monitor_performance
def proceso_pesado():
    time.sleep(2)  # Simulación de proceso
    return "Proceso completado"
```

### 3. Métricas y Analytics

La recolección de métricas nos permite entender mejor cómo se está utilizando nuestra aplicación. La clase MetricsCollector mantiene un registro de solicitudes, errores, tiempos de respuesta y uso de modelos, permitiéndonos generar informes detallados y visualizar tendencias.

#### Recolección de Métricas
```python
class MetricsCollector:
    def __init__(self):
        if 'metrics' not in st.session_state:
            st.session_state.metrics = {
                'requests_count': 0,
                'error_count': 0,
                'response_times': [],
                'model_usage': {}
            }

    def log_request(self, model_name, response_time):
        st.session_state.metrics['requests_count'] += 1
        st.session_state.metrics['response_times'].append(response_time)
        
        if model_name not in st.session_state.metrics['model_usage']:
            st.session_state.metrics['model_usage'][model_name] = 0
        st.session_state.metrics['model_usage'][model_name] += 1

    def log_error(self, error_type):
        st.session_state.metrics['error_count'] += 1
        logger = get_streamlit_logger()
        logger.error(f"Error occurred: {error_type}")

    def get_summary(self):
        metrics = st.session_state.metrics
        avg_response_time = sum(metrics['response_times']) / len(metrics['response_times']) if metrics['response_times'] else 0
        return {
            'total_requests': metrics['requests_count'],
            'error_rate': metrics['error_count'] / metrics['requests_count'] if metrics['requests_count'] > 0 else 0,
            'avg_response_time': avg_response_time,
            'model_usage': metrics['model_usage']
        }
```

### 4. Optimización de Recursos

La gestión eficiente de recursos es crucial para mantener el rendimiento de nuestra aplicación. Implementamos monitoreo de memoria y técnicas de caché inteligente para optimizar el uso de recursos y mejorar los tiempos de respuesta.

#### Gestión de Memoria
```python
import psutil
import gc

def monitor_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    logger = get_streamlit_logger()
    logger.info(f"Memory usage: {memory_info.rss / 1024 / 1024:.2f} MB")

def optimize_memory():
    gc.collect()
    monitor_memory()
```

#### Cache Inteligente
```python
from datetime import datetime, timedelta

@st.cache_data(ttl=timedelta(hours=1), show_spinner=False)
def fetch_data_with_monitoring():
    logger = get_streamlit_logger()
    start_time = time.time()
    
    try:
        data = fetch_expensive_data()
        execution_time = time.time() - start_time
        logger.info(f"Data fetch completed in {execution_time:.2f} seconds")
        return data
    except Exception as e:
        logger.error(f"Error fetching data: {str(e)}")
        raise
```

### 5. Debugging Avanzado

Las herramientas de debugging nos permiten identificar y resolver problemas rápidamente. Implementamos un modo de debug que puede activarse en tiempo de ejecución y un sistema robusto de captura de excepciones para mejor manejo de errores.

#### Herramientas de Debug
```python
import pdb
import sys

def debug_mode():
    if st.checkbox("Activar modo debug"):
        st.write("Modo debug activado")
        logger = get_streamlit_logger()
        logger.setLevel(logging.DEBUG)
        
        # Agregar handler para debug
        debug_handler = logging.FileHandler('debug.log')
        debug_handler.setLevel(logging.DEBUG)
        logger.addHandler(debug_handler)
```

#### Captura de Excepciones
```python
def safe_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_streamlit_logger()
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"Error in {func.__name__}")
            st.error(f"Se produjo un error: {str(e)}")
            if st.session_state.get('debug_mode'):
                st.exception(e)
    return wrapper
```

### 6. Visualización de Métricas

La visualización efectiva de métricas nos ayuda a entender rápidamente el estado de nuestra aplicación. El dashboard de monitoreo presenta métricas clave en un formato fácil de entender, permitiendo identificar tendencias y problemas potenciales.

#### Dashboard de Monitoreo
```python
def render_metrics_dashboard():
    metrics = MetricsCollector().get_summary()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Requests", metrics['total_requests'])
    with col2:
        st.metric("Error Rate", f"{metrics['error_rate']:.2%}")
    with col3:
        st.metric("Avg Response Time", f"{metrics['avg_response_time']:.2f}s")

    st.subheader("Uso de Modelos")
    st.bar_chart(metrics['model_usage'])
```

## Referencias

- [Streamlit Logging Documentation](https://docs.streamlit.io/library/api-reference/logging)
- [Python Logging](https://docs.python.org/3/library/logging.html)
- [Streamlit Caching](https://docs.streamlit.io/library/advanced-features/caching)
- [Performance Monitoring](https://docs.streamlit.io/library/advanced-features/performance)
