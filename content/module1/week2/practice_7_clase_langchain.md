# Crear tu propio chatbot con LangChain - Práctica (45 minutos)

## Descripción

# Crear tu propio chatbot con LangChain en cinco pasos
Este proyecto tiene como objetivo crear un chatbot que utilice GPT-3 para buscar respuestas dentro de documentos. Primero, extraemos contenido de artículos en línea, los dividimos en fragmentos pequeños, calculamos sus incrustaciones (embeddings) y los almacenamos en Deep Lake. Luego, usamos una consulta del usuario para recuperar los fragmentos más relevantes de Deep Lake, que se incorporan a un prompt para generar la respuesta final con el modelo de lenguaje (LLM).

Es importante notar que el uso de LLMs conlleva el riesgo de generar "alucinaciones" o información falsa. Si bien esto puede ser inaceptable para muchos escenarios de soporte al cliente, el chatbot puede seguir siendo valioso para ayudar a los operadores a redactar respuestas que puedan verificar antes de enviarlas a los usuarios.

## Objetivos

- **Introducir LangChain** como una herramienta para construir aplicaciones de inteligencia artificial generativa.
- **Aplicar el uso de modelos de lenguaje** como GPT-3 para la búsqueda y generación de respuestas en función de los documentos.
- **Entender y configurar variables de entorno** como `OPENAI_API_KEY` y `ACTIVELOOP_TOKEN` para la correcta ejecución del chatbot.
- **Desarrollar habilidades prácticas** para implementar chatbots que utilicen IA generativa y consultas de datos en tiempo real.


## Actividades

### 1 Creación del proyecto, prerequisitos e instalación de librerías
Primero, crea tu proyecto en PyCharm para el chatbot. Abre PyCharm y haz clic en “Nuevo proyecto”. Luego asigna un nombre a tu proyecto.

![Creación del proyecto](https://blog.jetbrains.com/wp-content/uploads/2024/08/unnamed-1.png)

#### Crear un proyecto en PyCharm
Una vez que tengas el proyecto listo, genera tu OPENAI_API_KEY en la plataforma de la API de OpenAI, una vez que hayas iniciado sesión (o regístrate en el sitio web de OpenAI). Para hacerlo, ve a la sección “API Keys” en el menú de navegación de la izquierda y luego haz clic en el botón “+Crear nueva clave secreta”. No olvides copiar tu clave.

Después, obtén tu `ACTIVELOOP_TOKEN registrándote en el sitio web de Activeloop. Una vez iniciado sesión, solo haz clic en el botón “Crear token API” y serás dirigido a la página de creación del token. Copia también este token.

Una vez que tengas ambos tokens, abre la configuración en PyCharm, haciendo clic en los tres puntos junto a los botones de ejecución y depuración, y selecciona “Editar”. Deberías ver la siguiente ventana:

![Creación del proyecto](https://blog.jetbrains.com/wp-content/uploads/2024/08/unnamed-3.png)

#### Configuración de ejecución/depuración en PyCharm
Ahora localiza el campo “Variables de entorno” y encuentra el ícono en el lado derecho del campo. Haz clic allí, y verás la siguiente ventana:

#### Variables de entorno en PyCharm
Ahora, haz clic en el botón + para comenzar a agregar tus variables de entorno y ten cuidado con los nombres. Deben ser los mismos que se mencionan arriba: OPENAI_API_KEY y ACTIVELOOP_TOKEN. Cuando termines, solo haz clic en "OK" en la primera ventana y luego en “Aplicar” y “OK” en la segunda.

Esa es una gran ventaja de PyCharm, ya que maneja las variables de entorno de manera automática sin necesidad de realizar llamadas adicionales a ellas, permitiéndonos concentrarnos más en la parte creativa del código.

**Nota:** ActiveLoop es una empresa tecnológica que se enfoca en desarrollar infraestructura de datos y herramientas para aprendizaje automático e inteligencia artificial. La compañía busca agilizar el proceso de gestionar, almacenar y procesar conjuntos de datos a gran escala, especialmente para aplicaciones de aprendizaje profundo y otras aplicaciones de IA.

DeepLake es el producto insignia de ActiveLoop. Ofrece capacidades eficientes de almacenamiento, gestión y acceso de datos, optimizadas para conjuntos de datos a gran escala, comúnmente utilizados en IA.

#### Instalación de las librerías necesarias
Usaremos la clase SeleniumURLLoader de LangChain, que depende de las librerías Python unstructured y selenium. Instálalas usando pip. Se recomienda instalar la versión más reciente, aunque el código ha sido específicamente probado con la versión 0.7.7.

Para hacerlo, usa el siguiente comando en el terminal de PyCharm:

```bash
pip install unstructured selenium
```

Ahora necesitamos instalar langchain, deeplake y openai. Para hacerlo, solo usa este comando en tu terminal (el mismo que usaste para Selenium) y espera un poco hasta que todo esté instalado correctamente:

```bash
pip install langchain==0.0.208 deeplake openai==0.27.8 psutil tiktoken
```

Para asegurarte de que todas las librerías estén correctamente instaladas, agrega las siguientes líneas necesarias para nuestra aplicación de chatbot y haz clic en el botón de ejecución:

```python
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI
from langchain.document_loaders import SeleniumURLLoader
from langchain import PromptTemplate
```

Otra forma de instalar tus librerías es a través de la configuración de PyCharm. Abre la configuración y ve a la sección Proyecto -> Intérprete del Proyecto. Luego, localiza el botón +, busca tu paquete y haz clic en el botón “Instalar Paquete”. Una vez listo, ciérralo, y en la siguiente ventana haz clic en “Aplicar” y luego en “OK”.

![Creación del proyecto](https://blog.jetbrains.com/wp-content/uploads/2024/08/image-38.png)


### 2 (En desarrollo)


## Relación con Generative AI

Estos ejercicios prácticos te permiten integrar (...)

## Conclusión

Al finalizar esta sesión práctica, habrás adquirido habilidades clave para  (...)

---