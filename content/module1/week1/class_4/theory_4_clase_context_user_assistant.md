# Ingeniería de Prompts para Generative AI - Teoría (45 minutos)

## Descripción

La **Ingeniería de Prompts** es una disciplina fundamental para interactuar de manera efectiva con modelos de **Inteligencia Artificial Generativa (GenAI)**. Un prompt bien diseñado puede influir significativamente en la calidad y relevancia de las respuestas generadas por el modelo. En esta sección, exploraremos los conceptos clave que sustentan la creación de prompts efectivos, incluyendo la importancia del contexto, la diferenciación de roles, y los distintos tipos de prompts que puedes utilizar para optimizar las interacciones con GenAI.

## Contenidos

### 1. Importancia del Contexto en los Prompts

El contexto proporciona información adicional que guía al modelo a generar respuestas más precisas y coherentes. Incluir un contexto adecuado ayuda al modelo a entender mejor la intención detrás de la solicitud y a enfocar la respuesta en la dirección deseada.

**Ejemplo:**

- **Sin Contexto:**

Describe los beneficios de la inteligencia artificial en la medicina.

- **Con Contexto:**

Contexto: Eres un experto en tecnología médica.

Describe los beneficios de la inteligencia artificial en la medicina.


**Referencias:**
- [OpenAI - Prompt Design](https://beta.openai.com/docs/guides/completion/prompt-design)
- [Towards Data Science - Context in AI Prompts](https://towardsdatascience.com/context-in-ai-prompts-5b7b1d6f1c1a)

### 2. Diferenciación de Roles: Usuario vs. Asistente

Entender y definir claramente los roles de **Usuario** y **Asistente** en los prompts puede mejorar la fluidez y efectividad de las interacciones con GenAI.

- **Usuario:** Es quien realiza la solicitud o proporciona el prompt.
- **Asistente:** Es el modelo de GenAI que responde a la solicitud.

**Implementación en Prompts:**

```python
class ModeloGenerativo:
  # ... (código anterior)
  
  def crear_prompt_usuario(self, mensaje):
      return f"Usuario: {mensaje}"
  
  def crear_prompt_asistente(self, respuesta):
      return f"Asistente: {respuesta}"
```

**Ejemplo de Conversación:**

```python
Usuario: ¿Cuáles son las aplicaciones de la IA en la educación?
Asistente: La IA en la educación permite la personalización del aprendizaje, adaptándose a las necesidades individuales de cada estudiante.
```

**Referencias:**

OpenAI - Chat Models
Understanding AI Roles in Prompts

**Referencias:**
- [OpenAI - Chat Models](https://platform.openai.com/docs/guides/text-generation)

### 3. Tipos de Prompts: Zero-Shot, One-Shot y Few-Shot

La manera en que estructuramos los prompts puede influir en la capacidad del modelo para generar respuestas adecuadas. Existen tres tipos principales de prompts:

* Zero-Shot Prompts

Definición: El modelo responde sin recibir ejemplos previos.

Uso: Útil cuando se espera que el modelo entienda la tarea basándose únicamente en la descripción proporcionada.

Ejemplo:

```bash
Por favor, describe los beneficios de la inteligencia artificial en la agricultura.
```

* One-Shot Prompts

Definición: El modelo recibe un único ejemplo antes de la solicitud.

Uso: Ayuda al modelo a entender mejor el formato y la expectativa de la respuesta.

Ejemplo:

```bash
Tarea: Describe los beneficios de la inteligencia artificial en la educación.
Respuesta: La inteligencia artificial en la educación permite la personalización del aprendizaje, adaptándose a las necesidades individuales de cada estudiante.

Tarea: Describe los beneficios de la inteligencia artificial en la agricultura.
```

* Few-Shot Prompts

Definición: El modelo recibe varios ejemplos antes de la solicitud.

Uso: Proporciona múltiples referencias para guiar al modelo hacia respuestas más coherentes y precisas.

Ejemplo:

```bash
Tarea: Describe los beneficios de la inteligencia artificial en la educación.
Respuesta: La inteligencia artificial en la educación permite la personalización del aprendizaje, adaptándose a las necesidades individuales de cada estudiante.

Ejemplo:
Tarea: Describe los beneficios de la inteligencia artificial en la salud.
Respuesta: La inteligencia artificial en la salud mejora el diagnóstico temprano, optimiza tratamientos y gestiona eficientemente los datos médicos.

Tarea: Describe los beneficios de la inteligencia artificial en la agricultura.
```

### 4. Técnicas Avanzadas en Ingeniería de Prompts

Para maximizar la efectividad de los prompts, se pueden emplear técnicas avanzadas como:

* Formateo de Plantillas: Utilizar plantillas predefinidas que estructuren la solicitud de manera consistente.

Ejemplo:

```python
def formatear_prompt(self, plantilla, variables):
    try:
        prompt_formateado = plantilla.format(**variables)
        return prompt_formateado
    except KeyError as e:
        print(f"Error: Falta la variable {e} en el diccionario de variables.")
        return plantilla
```

* Limpieza de Prompts: Asegurar que los prompts estén bien estructurados y libres de errores que puedan confundir al modelo.

Ejemplo:

```python
def limpiar_prompt(self, prompt):
    prompt = prompt.strip()
    prompt = prompt.capitalize()
    return prompt
```

**Referencias:**
- [Prompt Engineering for ChatGPT](https://www.promptingguide.ai/)
- [Langchain - Prompt Management](https://python.langchain.com/v0.1/docs/modules/model_io/prompts/)


### Relación con Generative AI

La ingeniería de prompts es una habilidad crucial para interactuar eficazmente con modelos de GenAI. Al diseñar prompts bien estructurados que incluyan el contexto adecuado y utilizar distintos tipos de prompts según la necesidad, puedes mejorar significativamente la calidad y relevancia de las respuestas generadas. Esta práctica te permitirá desarrollar aplicaciones más precisas y útiles, optimizando la interacción con modelos avanzados de lenguaje y otros sistemas generativos.

### Conclusión

Al finalizar esta sesión teórica, habrás adquirido una comprensión profunda de los fundamentos de la ingeniería de prompts para modelos de Generative AI. Serás capaz de diseñar prompts efectivos que incorporen el contexto adecuado, diferenciar roles entre usuario y asistente, y aplicar distintos tipos de prompts para maximizar la eficacia de tus interacciones con GenAI. Estas habilidades son esenciales para desarrollar soluciones más robustas y alineadas con los objetivos específicos de tus proyectos en el campo de la inteligencia artificial.

### Preguntas Frecuentes

**¿Cómo determino el contexto adecuado para un prompt?**

Analiza el propósito de la tarea y qué información adicional puede ayudar al modelo a entender mejor lo que se espera. Por ejemplo, si el asistente debe escribir un artículo científico, especifica su rol y el tema a tratar.

**¿Qué tipo de prompt debo usar para obtener una respuesta más detallada?**

Los Few-Shot Prompts suelen generar respuestas más detalladas ya que el modelo recibe varios ejemplos que guían su comportamiento.

```python
ejemplos_few_shot = [
    {
        "tarea": "Describe los beneficios de la inteligencia artificial en la educación.",
        "respuesta": "La inteligencia artificial en la educación permite la personalización del aprendizaje y optimiza la gestión de recursos."
    },
    {
        "tarea": "Describe los beneficios de la inteligencia artificial en la salud.",
        "respuesta": "La inteligencia artificial en la salud mejora el diagnóstico temprano y personaliza tratamientos para pacientes."
    }
]
```

**¿Es posible combinar distintos tipos de prompts en una sola solicitud?**

Sí, puedes combinar One-Shot y Few-Shot prompts para adaptar la complejidad y el detalle de las respuestas según tus necesidades específicas.

```python
contexto = "Contexto: Eres un asistente de IA que ayuda a escribir artículos científicos."
prompt = modelo_gpt.crear_one_shot_prompt(tarea, ejemplo_one_shot)
texto = modelo_gpt.generar_texto(prompt)
```

Si tienes alguna pregunta adicional o necesitas más detalles sobre algún tema específico, ¡no dudes en preguntar!