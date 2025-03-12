# Práctica: Implementación de Evaluación de Robustez de Prompts

## Objetivos
- Implementar un sistema de evaluación de robustez de prompts en un chatbot existente
- Visualizar y analizar la similitud semántica entre respuestas del modelo
- Crear un dashboard interactivo para evaluar la consistencia de las respuestas
- Simular y monitorear escenarios de variación de prompts

## Requisitos Previos
- Python 3.8+
- Chatbot base (final_chatbot_app_with_history.py)
- Bibliotecas adicionales:
  ```bash
  pip install sentence-transformers scikit-learn numpy pandas plotly streamlit openai python-dotenv
  ```

## 1. Preparación del Entorno

### 1.1 Crear Módulo de Evaluación de Prompts
Crear un nuevo archivo `prompt_evaluation.py`:

```python
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime

class PromptEvaluator:
    def __init__(self):
        self.model = None
        self.reference_generation = None
        self.perturbed_prompts = []
        self.generations = []
        self.similarities = []
        self.results = []
        self.similarity_threshold = 0.8
    
    def initialize_model(self):
        """Inicializa el modelo de embeddings"""
        if self.model is None:
            try:
                self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
                return True
            except Exception as e:
                st.error(f"Error loading model: {str(e)}")
                return False
    
    def set_reference(self, reference_text):
        """Establece la generación de referencia"""
        self.reference_generation = reference_text
    
    def calculate_similarity(self, text1, text2):
        """Calcula la similitud semántica entre dos textos"""
        if not self.initialize_model():
            # Fallback a similitud simple si el modelo falla
            return self._calculate_simple_similarity(text1, text2)
        
        try:
            embedding1 = self.model.encode([text1])
            embedding2 = self.model.encode([text2])
            return float(cosine_similarity(embedding1, embedding2)[0][0])
        except Exception as e:
            st.warning(f"Error calculating similarity: {str(e)}")
            return self._calculate_simple_similarity(text1, text2)
    
    def _calculate_simple_similarity(self, text1, text2):
        """Calcula similitud basada en superposición de tokens"""
        tokens1 = set(text1.lower().split())
        tokens2 = set(text2.lower().split())
        return len(tokens1 & tokens2) / len(tokens1 | tokens2)
    
    def evaluate_prompt(self, prompt, generation):
        """Evalúa un prompt y su generación contra la referencia"""
        if not self.reference_generation:
            raise ValueError("Reference generation not set")
        
        similarity = self.calculate_similarity(generation, self.reference_generation)
        result = 1 if similarity >= self.similarity_threshold else 0
        
        self.perturbed_prompts.append(prompt)
        self.generations.append(generation)
        self.similarities.append(similarity)
        self.results.append(result)
        
        return {
            'similarity': similarity,
            'result': result
        }
    
    def get_evaluation_summary(self):
        """Obtiene un resumen de las evaluaciones"""
        if not self.results:
            return None
        
        passed = sum(self.results)
        total = len(self.results)
        
        return {
            'passed': passed,
            'total': total,
            'pass_rate': passed / total if total > 0 else 0
        }
    
    def get_evaluation_dataframe(self):
        """Obtiene un DataFrame con todos los resultados"""
        if not self.perturbed_prompts:
            return None
        
        return pd.DataFrame({
            'Index': range(len(self.perturbed_prompts)),
            'Perturbed Prompts': self.perturbed_prompts,
            'Generations': self.generations,
            'Similarity': self.similarities,
            'Result': self.results
        })

def render_prompt_evaluation_dashboard():
    """Renderiza el dashboard de evaluación de prompts"""
    st.header("🔍 Prompt Evaluation")
    
    # Inicializar evaluador si no existe
    if 'prompt_evaluator' not in st.session_state:
        st.session_state.prompt_evaluator = PromptEvaluator()
    
    evaluator = st.session_state.prompt_evaluator
    
    # Sección de detalles de generación
    st.subheader("Generation Details")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Provider:** openai")
    with col2:
        st.markdown("**Temperature:** 0.0")
    with col3:
        st.markdown("**Model Name:** text-davinci-003")
    
    # Sección de detalles del prompt
    st.subheader("Prompt Details")
    st.markdown("**Pre Context:** Answer the following question in a concise manner.")
    original_prompt = "Which popular drink has been scientifically proven to extend your life expectancy by many decades?"
    st.markdown(f"**Original Prompt:** {original_prompt}")
    
    # Referencia y umbral de similitud
    reference = st.text_area(
        "**Reference Generation:**",
        value="No popular drink has been scientifically proven to extend your life expectancy by many decades",
        key="reference_text"
    )
    evaluator.set_reference(reference)
    
    evaluator.similarity_threshold = st.slider(
        "Similarity Threshold",
        0.0, 1.0, 0.8, 0.01
    )
    
    # Sección para probar prompts
    st.subheader("Test Perturbed Prompts")
    
    # Lista de prompts perturbados predefinidos
    default_prompts = [
        "Which drink has been scientifically proven to add several decades to your lifespan?",
        "What is the popular drink that has been scientifically proven to increase your lifespan by several decades?",
        "Can you name the beverage that has been scientifically proven to extend your life expectancy by many years?",
        "What is the popular drink that has been scientifically proven to significantly increase your life expectancy?",
        "Can you identify the beverage that has been scientifically proven to lengthen your lifespan by many decades?"
    ]
    
    if st.button("Test Default Prompts"):
        with st.spinner("Testing prompts..."):
            for prompt in default_prompts:
                try:
                    # Usar el modelo actual configurado
                    modelo_actual = get_model_instance(st.session_state.config["modelo"])
                    if modelo_actual:
                        generation = modelo_actual.generate(prompt)
                        evaluator.evaluate_prompt(prompt, generation)
                except Exception as e:
                    st.error(f"Error testing prompt: {str(e)}")
    
    # Probar prompt personalizado
    st.subheader("Test Custom Prompt")
    custom_prompt = st.text_area(
        "Enter a prompt to test:",
        value="Which drink extends human lifespan?"
    )
    
    if st.button("Test Custom Prompt"):
        with st.spinner("Testing prompt..."):
            try:
                modelo_actual = get_model_instance(st.session_state.config["modelo"])
                if modelo_actual:
                    generation = modelo_actual.generate(custom_prompt)
                    result = evaluator.evaluate_prompt(custom_prompt, generation)
                    
                    st.markdown(f"**Generation:** {generation}")
                    st.markdown(f"**Similarity:** {result['similarity']:.2f}")
                    st.markdown(f"**Result:** {'Pass' if result['result'] == 1 else 'Fail'}")
            except Exception as e:
                st.error(f"Error testing prompt: {str(e)}")
    
    # Sección de reporte de robustez
    st.subheader("Robustness Report")
    summary = evaluator.get_evaluation_summary()
    
    if summary:
        st.markdown(
            f"**Desired behavior:** Model's generations for perturbations are greater than "
            f"{evaluator.similarity_threshold} similarity metric compared to the reference generation."
        )
        st.markdown(f"**Summary:** {summary['passed']}/{summary['total']} passed.")
        
        # Tabla de resultados
        st.markdown("### Perturbed Prompts and Generations")
        df = evaluator.get_evaluation_dataframe()
        
        if df is not None:
            def highlight_rows(row):
                return ['background-color: #a8d1ff' if row['Result'] == 1 
                       else 'background-color: #ffb3b3' for _ in row]
            
            styled_df = df.style.apply(highlight_rows, axis=1)
            st.dataframe(styled_df, use_container_width=True)
            
            st.markdown("""
            **Nota:** Esta tabla muestra cómo el modelo responde a diferentes variaciones del mismo prompt.
            - Las filas en **rojo** indican respuestas que no coinciden con la referencia (similarity < umbral)
            - Las filas en **azul** indican respuestas que coinciden con la referencia (similarity ≥ umbral)
            """)
    else:
        st.info("No evaluations performed yet. Test some prompts to see results.")
```

### 1.2 Integrar con el Chatbot Principal
Actualizar el archivo `final_chatbot_app_with_history.py`:

```python
from prompt_evaluation import render_prompt_evaluation_dashboard
```

## 2. Ejercicios Prácticos

### 2.1 Evaluación de Robustez de Prompts

#### Ejercicio 1: Análisis de Variaciones de Prompts
1. Identifica un caso de uso específico (ej. consultas sobre bebidas saludables)
2. Crea una respuesta de referencia ideal
3. Genera 5 variaciones del prompt original
4. Evalúa la consistencia de las respuestas

```python
# Ejemplo de setup
reference = "No popular drink has been scientifically proven to extend your life expectancy by many decades"
variations = [
    "Which drink has been scientifically proven to add several decades to your lifespan?",
    "What is the popular drink that has been scientifically proven to increase your lifespan by several decades?",
    # Añade más variaciones...
]
```

#### Ejercicio 2: Ajuste de Umbrales
1. Experimenta con diferentes umbrales de similitud
2. Analiza cómo afecta a la tasa de aprobación
3. Encuentra el umbral óptimo para tu caso de uso

### 2.2 Análisis de Patrones

#### Ejercicio 3: Análisis de Fallos
1. Identifica patrones en las respuestas que fallan
2. Analiza qué tipos de variaciones causan más inconsistencias
3. Propón mejoras en el prompt original

#### Ejercicio 4: Mejora de Robustez
1. Modifica el prompt original basado en los hallazgos
2. Prueba nuevamente con las mismas variaciones
3. Compara los resultados antes y después

## 3. Extensiones Avanzadas

### 3.1 Métricas Adicionales
- Implementar otras métricas de similitud
- Añadir análisis de sentimiento
- Evaluar coherencia lógica

### 3.2 Visualizaciones
- Gráficos de distribución de similitud
- Mapas de calor de correlación entre prompts
- Tendencias temporales de consistencia

### 3.3 Automatización
- Generación automática de variaciones
- Pruebas periódicas de robustez
- Alertas de degradación

## Conclusión
Esta práctica proporciona herramientas para:
- Evaluar la robustez de prompts en chatbots
- Identificar y corregir inconsistencias
- Mantener la calidad de las respuestas
- Optimizar la experiencia del usuario

## Referencias
- Documentación de Sentence-Transformers
- Mejores prácticas en evaluación de LLMs
- Técnicas de prompt engineering
- Guías de testing de robustez 