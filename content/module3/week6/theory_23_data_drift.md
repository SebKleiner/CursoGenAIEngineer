# Monitoreo de Data Drift en Modelos de Lenguaje

## Objetivos de Aprendizaje
- Comprender el concepto de data drift y su impacto en sistemas de IA generativa
- Identificar los diferentes tipos de drift que afectan a los LLMs
- Aprender métodos para detectar y cuantificar el drift
- Implementar estrategias de monitoreo continuo

## 1. Introducción al Data Drift

### Enfoques de Implementación de LLMs en Empresas
Existen cuatro aproximaciones principales para implementar LLMs en producción:

1. **Ingeniería de Prompts con Contexto**
   - Llamadas directas a proveedores de IA como OpenAI, Cohere o Anthropic
   - Prompts cuidadosamente diseñados para obtener respuestas específicas
   - Vulnerabilidad al drift por cambios en el modelo subyacente

2. **Generación Aumentada por Recuperación (RAG)**
   - Enriquecimiento de prompts con datos externos relevantes
   - Mayor control sobre el contenido de las respuestas
   - Posible drift por cambios en los datos de referencia

3. **Modelo Fine-tuneado**
   - Actualización del modelo con datos específicos del dominio
   - Reduce la necesidad de augmentación en los prompts
   - Susceptible al drift cuando los datos del dominio evolucionan

4. **Modelo Entrenado desde Cero**
   - Construcción de LLMs específicos para el dominio
   - Mayor control pero mayor complejidad
   - Requiere monitoreo continuo de la calidad y relevancia

### Problemas de Rendimiento en LLMs

#### 1. Nuevos Tipos de Prompts
- Cambios en el comportamiento de los usuarios
- Nuevos productos o procesos no contemplados
- Evolución natural del caso de uso

#### 2. Variaciones en las Respuestas
- **Robustez del Modelo**
  - Variaciones lingüísticas del mismo prompt
  - Ejemplo: "¿Cómo devolver un producto?" vs "Estoy confundido sobre cómo devolver mis zapatos"
  
- **Cambios en Modelos Subyacentes**
  - Actualizaciones silenciosas en APIs de terceros
  - Variaciones de rendimiento entre versiones
  - Ejemplo documentado: Variaciones significativas entre versiones de GPT-3.5 y GPT-4

### ¿Qué es el Data Drift?
El data drift se refiere a los cambios en las distribuciones de datos a lo largo del tiempo que pueden afectar el rendimiento de los modelos de machine learning. En el contexto de los Modelos de Lenguaje Grandes (LLMs), el data drift puede manifestarse tanto en los datos de entrada (prompts) como en las salidas generadas.

### Importancia del Monitoreo de Drift
- **Degradación del rendimiento**: El drift puede causar que los modelos generen respuestas menos precisas o relevantes
- **Sesgos emergentes**: Pueden surgir nuevos sesgos o amplificarse los existentes
- **Costos operativos**: Respuestas de baja calidad pueden aumentar los tokens consumidos y los costos asociados
- **Experiencia del usuario**: La calidad inconsistente afecta la confianza y satisfacción del usuario

## 2. Tipos de Drift en Sistemas LLM

### Drift en Datos de Entrada (Input Drift)
- **Drift conceptual**: Cambios en el significado o contexto de los términos utilizados
- **Drift de distribución**: Cambios en la frecuencia o patrones de ciertos tipos de consultas
- **Drift de complejidad**: Variaciones en la longitud o complejidad de los prompts
- **Drift temático**: Evolución de los temas o dominios de las consultas

Ejemplo de código para detectar drift de complejidad:
```python
def calcular_drift_complejidad(prompts_referencia, prompts_nuevos):
    # Función para calcular métricas de complejidad
    def metricas_complejidad(prompts):
        longitudes = [len(p.split()) for p in prompts]
        return {
            'longitud_media': np.mean(longitudes),
            'longitud_std': np.std(longitudes),
            'complejidad_lexica': len(set(''.join(prompts))) / len(''.join(prompts))
        }
    
    ref_metrics = metricas_complejidad(prompts_referencia)
    new_metrics = metricas_complejidad(prompts_nuevos)
    
    return {k: abs(ref_metrics[k] - new_metrics[k]) for k in ref_metrics}
```

### Drift en Datos de Salida (Output Drift)
- **Drift de estilo**: Cambios en el tono, formalidad o estructura de las respuestas
- **Drift de contenido**: Variaciones en la información o recomendaciones proporcionadas
- **Drift de calidad**: Degradación en la coherencia, precisión o relevancia
- **Drift de comportamiento**: Cambios en cómo el modelo maneja ciertos tipos de consultas

## 3. Métricas para Detectar Data Drift

### Métricas Estadísticas Básicas

#### Divergencia de Kullback-Leibler (KL)
La divergencia KL mide la diferencia entre dos distribuciones de probabilidad P y Q:

\[ D_{KL}(P||Q) = \sum_{i} P(i) \log \frac{P(i)}{Q(i)} \]

```python
def kl_divergence(p, q):
    return np.sum(np.where(p != 0, p * np.log(p / q), 0))
```

#### Distancia de Jensen-Shannon (JS)
Una versión simétrica y normalizada de la divergencia KL:

\[ JSD(P||Q) = \frac{1}{2}D_{KL}(P||M) + \frac{1}{2}D_{KL}(Q||M) \]
donde \[ M = \frac{1}{2}(P + Q) \]

```python
def jensen_shannon_distance(p, q):
    m = 0.5 * (p + q)
    return 0.5 * kl_divergence(p, m) + 0.5 * kl_divergence(q, m)
```

#### Prueba de Kolmogorov-Smirnov
```python
from scipy import stats

def ks_test(muestra_referencia, muestra_nueva):
    statistic, p_value = stats.ks_2samp(muestra_referencia, muestra_nueva)
    return {
        'estadistico': statistic,
        'p_valor': p_value,
        'drift_detectado': p_value < 0.05
    }
```

### Métricas Específicas para Texto

#### Embedding Drift
```python
from sentence_transformers import SentenceTransformer
import numpy as np

def calcular_embedding_drift(textos_referencia, textos_nuevos, modelo='all-MiniLM-L6-v2'):
    # Cargar modelo de embeddings
    model = SentenceTransformer(modelo)
    
    # Calcular embeddings
    embeddings_ref = model.encode(textos_referencia)
    embeddings_new = model.encode(textos_nuevos)
    
    # Calcular centroides
    centroide_ref = np.mean(embeddings_ref, axis=0)
    centroide_new = np.mean(embeddings_new, axis=0)
    
    # Calcular distancia coseno entre centroides
    drift_score = 1 - np.dot(centroide_ref, centroide_new) / (
        np.linalg.norm(centroide_ref) * np.linalg.norm(centroide_new)
    )
    
    return drift_score
```

#### Análisis de Sentimiento y Complejidad Léxica
```python
from textblob import TextBlob
import nltk
from nltk.tokenize import word_tokenize

def analizar_drift_linguistico(textos_referencia, textos_nuevos):
    def metricas_texto(textos):
        sentimientos = [TextBlob(texto).sentiment.polarity for texto in textos]
        vocabulario = set(word_tokenize(' '.join(textos).lower()))
        return {
            'sentimiento_medio': np.mean(sentimientos),
            'riqueza_vocabulario': len(vocabulario) / sum(len(texto.split()) for texto in textos)
        }
    
    metricas_ref = metricas_texto(textos_referencia)
    metricas_new = metricas_texto(textos_nuevos)
    
    return {k: abs(metricas_ref[k] - metricas_new[k]) for k in metricas_ref}
```

### Métricas de Rendimiento del Modelo

#### Perplexidad
La perplexidad se calcula como:

\[ \text{Perplexity} = \exp(-\frac{1}{N}\sum_{i=1}^N \log p(x_i)) \]

```python
def calcular_perplexidad(modelo, texto):
    tokens = modelo.tokenize(texto)
    with torch.no_grad():
        outputs = modelo(tokens)
        loss = outputs.loss
    return torch.exp(loss).item()
```

## 4. Técnicas de Monitoreo de Drift

### Monitoreo de Prompts vs Respuestas

#### Análisis de Drift en Prompts
```python
def analizar_drift_prompts(prompts_baseline, prompts_nuevos):
    """
    Analiza el drift en los prompts comparando con el baseline
    """
    # Calcular embedding drift
    drift_embedding = calcular_embedding_drift(prompts_baseline, prompts_nuevos)
    
    # Identificar nuevos clusters temáticos
    clusters = identificar_clusters_tematicos(prompts_nuevos)
    
    # Detectar anomalías
    anomalias = detectar_anomalias(prompts_baseline, prompts_nuevos)
    
    return {
        'drift_score': drift_embedding,
        'nuevos_temas': clusters,
        'anomalias': anomalias
    }
```

#### Análisis de Drift en Respuestas
```python
def analizar_drift_respuestas(baseline_pairs, nuevos_pairs):
    """
    Analiza el drift en las respuestas, considerando los pares prompt-respuesta
    """
    # Calcular drift de respuestas para prompts similares
    drift_respuestas = []
    for prompt_nuevo, respuesta_nueva in nuevos_pairs:
        prompts_similares = encontrar_prompts_similares(prompt_nuevo, baseline_pairs)
        if prompts_similares:
            drift = calcular_drift_respuesta(
                [p[1] for p in prompts_similares],  # respuestas baseline
                respuesta_nueva
            )
            drift_respuestas.append(drift)
    
    return {
        'drift_medio': np.mean(drift_respuestas),
        'drift_std': np.std(drift_respuestas),
        'respuestas_anomalas': len([d for d in drift_respuestas if d > UMBRAL])
    }
```

### Estrategias de Mitigación

#### Para Drift en Prompts
```python
def mitigar_drift_prompts(monitor, nuevos_prompts):
    """
    Implementa estrategias de mitigación para drift en prompts
    """
    resultados = monitor.analizar_drift_prompts(nuevos_prompts)
    
    if resultados['nuevos_temas']:
        # Actualizar documentos RAG o dataset de fine-tuning
        actualizar_conocimiento_base(resultados['nuevos_temas'])
    
    if resultados['anomalias']:
        # Ajustar prompts de sistema o restricciones
        ajustar_restricciones_prompt(resultados['anomalias'])
    
    return resultados['acciones_tomadas']
```

#### Para Drift en Respuestas
```python
def mitigar_drift_respuestas(monitor, prompt_response_pairs):
    """
    Implementa estrategias de mitigación para drift en respuestas
    """
    resultados = monitor.analizar_drift_respuestas(prompt_response_pairs)
    
    if resultados['drift_medio'] > UMBRAL_CRITICO:
        # Considerar reentrenamiento o ajuste del modelo
        programar_actualizacion_modelo()
    
    if resultados['respuestas_anomalas'] > 0:
        # Ajustar parámetros de generación
        ajustar_parametros_generacion()
    
    return resultados['acciones_tomadas']
```

### Ventanas Temporales
```python
class VentanaDeslizante:
    def __init__(self, tamano_ventana=1000):
        self.tamano_ventana = tamano_ventana
        self.datos_referencia = []
        self.datos_actuales = []
    
    def actualizar(self, nuevo_dato):
        self.datos_actuales.append(nuevo_dato)
        if len(self.datos_actuales) >= self.tamano_ventana:
            self.datos_referencia = self.datos_actuales[-self.tamano_ventana:]
            self.datos_actuales = []
    
    def calcular_drift(self, metrica_fn):
        if not self.datos_actuales or not self.datos_referencia:
            return None
        return metrica_fn(self.datos_referencia, self.datos_actuales)
```

### Métodos de Detección

#### Detección de Anomalías
```python
from sklearn.ensemble import IsolationForest

def detectar_anomalias(datos_referencia, datos_nuevos, contaminacion=0.1):
    # Entrenar detector con datos de referencia
    detector = IsolationForest(contamination=contaminacion)
    detector.fit(datos_referencia)
    
    # Detectar anomalías en nuevos datos
    predicciones = detector.predict(datos_nuevos)
    return {
        'ratio_anomalias': (predicciones == -1).mean(),
        'indices_anomalias': np.where(predicciones == -1)[0]
    }
```

## 5. Implementación de Sistemas de Monitoreo

### Arquitectura de Monitoreo
```python
class MonitorDrift:
    def __init__(self):
        self.metricas = {
            'embedding': calcular_embedding_drift,
            'linguistico': analizar_drift_linguistico,
            'complejidad': calcular_drift_complejidad
        }
        self.ventanas = {
            nombre: VentanaDeslizante() for nombre in self.metricas
        }
        self.umbrales = {
            'embedding': 0.3,
            'linguistico': 0.2,
            'complejidad': 0.25
        }
    
    def procesar_dato(self, texto):
        resultados = {}
        for nombre, metrica in self.metricas.items():
            self.ventanas[nombre].actualizar(texto)
            drift = self.ventanas[nombre].calcular_drift(metrica)
            if drift is not None:
                resultados[nombre] = {
                    'valor': drift,
                    'alarma': drift > self.umbrales[nombre]
                }
        return resultados
```

### Estrategias de Muestreo
- **Muestreo aleatorio**: Selección probabilística para reducir volumen de datos
- **Muestreo estratificado**: Asegurar representación de diferentes categorías de consultas
- **Muestreo basado en tiempo**: Captura de datos en diferentes momentos del día/semana
- **Muestreo adaptativo**: Mayor frecuencia durante períodos de cambio detectado

### Alertas y Acciones
- **Sistemas de notificación**: Alertas automáticas cuando se detecta drift significativo
- **Dashboards de monitoreo**: Visualizaciones en tiempo real del estado del sistema
- **Umbrales adaptativos**: Ajuste automático de límites basado en patrones históricos
- **Planes de mitigación**: Estrategias predefinidas para responder a diferentes tipos de drift

## 6. Casos de Estudio y Mejores Prácticas

### Monitoreo en Chatbots
- Seguimiento de cambios en tipos de consultas de usuarios
- Detección de nuevos temas o intenciones no contempladas
- Evaluación de consistencia en respuestas a consultas similares

### Monitoreo en Sistemas de Recomendación basados en LLM
- Análisis de cambios en preferencias de usuarios
- Detección de nuevas tendencias o categorías emergentes
- Evaluación de diversidad y relevancia de recomendaciones

### Monitoreo en Sistemas de Generación de Contenido
- Seguimiento de cambios estilísticos o tonales
- Detección de sesgos emergentes
- Evaluación de originalidad y calidad del contenido

## 7. Desafíos y Consideraciones Futuras

### Limitaciones Actuales
- Complejidad de establecer líneas base adecuadas
- Dificultad para distinguir entre drift y variabilidad normal
- Costos computacionales del monitoreo continuo

### Tendencias Emergentes
- Monitoreo auto-supervisado y adaptativo
- Técnicas de explicabilidad para entender causas del drift
- Integración con sistemas de reentrenamiento continuo

### Consideraciones Éticas
- Privacidad en el almacenamiento de datos para monitoreo
- Transparencia sobre cambios detectados
- Impacto de las acciones correctivas en diferentes grupos de usuarios

## Conclusión
El monitoreo efectivo de data drift es esencial para mantener sistemas LLM confiables y de alta calidad a lo largo del tiempo. Implementar estrategias robustas de detección y respuesta permite identificar problemas tempranamente, reducir costos operativos y mejorar la experiencia del usuario.

## Referencias y Recursos Adicionales
- "Monitoring Machine Learning Models in Production" - Google Cloud
- "Drift Detection for Text Data" - Towards Data Science
- "Practical Monitoring" - O'Reilly Media
- "ML Monitoring Tools Landscape" - Neptune.ai
- "Embedding Drift Detection" - Arize AI 