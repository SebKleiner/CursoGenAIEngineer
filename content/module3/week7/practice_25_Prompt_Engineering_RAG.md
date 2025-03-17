# Clase 25: Prompt Engineering RAG
Retrieval-augmented generation (RAG) es una arquitectura de software que combina la inteligencia artificial (IA) con fuentes de información externas.

![Arquitectura RAG](https://docs.aws.amazon.com/images/sagemaker/latest/dg/images/jumpstart/jumpstart-fm-rag.jpg)

Una aplicación RAG típica tiene dos componentes principales:

- Indexación: Una canalización para ingerir datos desde una fuente e indexarlos. Esto normalmente ocurre en modo offline (sin conexión).

![Indexación](https://python.langchain.com/assets/images/rag_indexing-8160f90a90a33253d0154659cf7d453f.png)

- Recuperación y generación: La cadena RAG propiamente dicha, que toma la consulta del usuario en tiempo de ejecución, recupera los datos relevantes del índice, y luego los envía al modelo para generar la respuesta.

![Recuperación y generación](https://python.langchain.com/assets/images/rag_retrieval_generation-1046a4668d6bb08786ef73c56d4f228a.png)

## Ejercicio 1: Incorporación de conocimiento externo

Con un sistema de recuperación implementado, necesitamos transferir el conocimiento de este sistema al modelo. Un pipeline RAG típicamente logra esto siguiendo estos pasos:

1. Recibir una consulta de entrada.
2. Utilizar el sistema de recuperación para buscar información relevante basada en la consulta.
3. Incorporar la información recuperada en el prompt enviado al LLM.
4. Generar una respuesta que aproveche el contexto recuperado.

1. Instalar las dependencias
``` bash
pip install langchain-openai faiss-cpu langchain-text-splitters langchain-community python-dotenv
```

2. Generar un script (rag.py)
``` python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import os
from dotenv import load_dotenv

# Cargar variables de entorno AL INICIO
load_dotenv()

# 1. Cargar documentos (ejemplo)
loader = TextLoader("tu_archivo.txt")  # Reemplaza con tu fuente de datos
documents = loader.load()

# 2. Dividir documentos en chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

# 3. Crear base vectorial y retriever
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(texts, embeddings)
retriever = vectorstore.as_retriever()

# Resto del código original (modificado para mejor práctica)
system_prompt = """Eres un asistente para tareas de pregunta-respuesta. 
Usa los siguientes fragmentos de contexto recuperado para responder. 
Si no sabes la respuesta, di que no lo sabes. 
Usa máximo tres oraciones y mantén la respuesta concisa.
Contexto: {context}"""

question = "¿Cuáles son los componentes principales de un sistema de agente autónomo impulsado por LLM?"

# Recuperar documentos relevantes
docs = retriever.invoke(question)  # Ahora funciona
docs_text = "\n".join(d.page_content for d in docs)

# Formatear prompt
formatted_prompt = system_prompt.format(context=docs_text)

# Crear y ejecutar modelo
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
response = model.invoke([
    SystemMessage(content=formatted_prompt),
    HumanMessage(content=question)
])

print(response.content)
```

3. Generar un archivo que se llame tu_archivo.txt y que contanga
```bash
Los componentes principales de un agente autónomo con LLM son:
- Módulo de planificación
- Memoria a largo plazo
- Sistema de recuperación (RAG)
- Modelo de lenguaje (LLM)
- Módulo de ejecución de tareas
```

3. Ejecutar el script
```bash
python rag.py
```

Explicación breve de los pasos:
- Paso 1: El usuario realiza una pregunta (ej: "¿Cómo optimizar consultas SQL?").
- Paso 2: Se buscan fragmentos de documentos relevantes (ej: guías técnicas sobre SQL).
- Paso 3: El contexto recuperado se inserta en el prompt (ej: "Responde usando esta información: [contexto]...").
- Paso 4: El LLM genera una respuesta precisa y contextualizada (ej: pasos específicos para optimización).

** Ejercicio Extra**:
1. Ingresa nueva información a "tu_archivo.txt" y cambia la pregunta para que se pueda responder con la información nueva
2. Cambia la pregunta por una que no se pueda responder con la información que hay en  "tu_archivo.txt"

## Ejercicio 2: RAG con LangChain (Flujo Completo)

1. Instalar las dependencias
``` bash
pip install fastapi uvicorn langchain langchain-openai langchain-community python-dotenv langchain-huggingface langchain-pinecone
```

2. Estructura de archivos
```bash
├── .env            # Clave de OpenAI
├── main.py         # API con FastAPI
└── documents/      # Archivos subidos (opcional)
```

3. Lógica RAG (rag_handler.py)
``` python
import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

class OpenAIRAGHandler:
    def __init__(self):
        # Configurar embeddings y LLM de OpenAI
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)
        self.vector_store = None
        
        # Plantilla de prompt
        self.prompt_template = PromptTemplate(
            template="""
            Eres un asistente experto. Responde la pregunta usando SOLO el contexto proporcionado.
            Si no hay información relevante, di 'No tengo datos suficientes'.
            
            Contexto: {context}
            
            Pregunta: {question}
            
            Respuesta:
            """,
            input_variables=["context", "question"]
        )

    def add_text(self, text: str):
        # Dividir texto en chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.split_text(text)
        
        # Crear o actualizar FAISS
        if self.vector_store is None:
            self.vector_store = FAISS.from_texts(texts, self.embeddings)
        else:
            self.vector_store.add_texts(texts)

    def add_file(self, file_path: str):
        # Cargar documento según tipo
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path)
        
        documents = loader.load()
        
        # Dividir y añadir
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.split_documents(documents)
        
        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(texts, self.embeddings)
        else:
            self.vector_store.add_documents(texts)

    def ask(self, question: str) -> str:
        if self.vector_store is None:
            return "Error: No hay documentos cargados."
        
        # Crear cadena QA
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
            chain_type_kwargs={"prompt": self.prompt_template}
        )
        
        result = qa_chain.invoke({"query": question})
        return result["result"]
```

4. API con FastAPI (main.py)

```python
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from rag_handler import OpenAIRAGHandler
import os

app = FastAPI()
rag = OpenAIRAGHandler()

class QueryRequest(BaseModel):
    question: str

class AddTextRequest(BaseModel):
    text: str

@app.post("/add-text")
async def add_text(request: AddTextRequest):
    try:
        rag.add_text(request.text)
        return {"status": "Texto añadido exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/add-file")
async def add_file(file: UploadFile = File(...)):
    try:
        # Guardar archivo temporalmente
        file_path = f"documents/{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Procesar archivo
        rag.add_file(file_path)
        return {"status": f"Archivo {file.filename} procesado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Limpiar archivo temporal
        if os.path.exists(file_path):
            os.remove(file_path)

@app.post("/ask")
async def ask_question(request: QueryRequest):
    try:
        answer = rag.ask(request.question)
        return {"question": request.question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

5. Ejecutar la API
```bash
uvicorn main:app --reload
```

# ¿Por qué usar RAG en lugar de "poner un documento" directamente al LLM?

## Ejemplo: Pregunta sobre un Documento Largo
Imagina que tienes un **manual técnico de 200 páginas** y quieres hacer preguntas específicas sobre su contenido.

---

### **Opción 1: Enviar el documento "tal cual" al LLM (sin RAG)**
- **Proceso**:  
  Pegas todo el texto del manual en el prompt del LLM y preguntas:  
  `"¿Cómo reiniciar el servidor según el manual?"`

- **Problemas**:  
  - 🚫 **Límite de tokens**: Modelos como GPT-4 soportan ~8k-128k tokens. Un manual largo excede este límite.  
  - 💸 **Costo alto**: Enviar 200 páginas en cada consulta es caro (ej: 200k tokens cuestan ~$20 en GPT-4).  
  - 📢 **Ruido contextual**: El LLM se distrae con texto irrelevante y puede dar respuestas incorrectas.

---

### **Opción 2: Usar RAG**
- **Proceso**:  
  1. **Divides el manual** en chunks pequeños (ej: párrafos).  
  2. **Indexas los chunks** en una base vectorial (ej: FAISS) usando embeddings.  
  3. Cuando llega una pregunta, **recuperas solo los chunks relevantes** (ej: 3 párrafos sobre "reinicio").  
  4. **Envías solo esos chunks + la pregunta** al LLM.  

- **Resultado**:  
  - ✅ **Eficiencia**: Trabajas con 1% del texto original.  
  - 🎯 **Precisión**: El LLM se enfoca en contexto relevante.  
  - 💰 **Menor costo**: Pagas por ~1k tokens en lugar de 200k.

---

## Analogía: Biblioteca vs. Libro Abierto
- **Sin RAG**:  
  Es como buscar una cita específica en una biblioteca **sin índice ni catálogo**.  
  - Debes leer **todos los libros** cada vez que tienes una pregunta.  

- **Con RAG**:  
  Es como usar un **bibliotecario inteligente** que:  
  1. **Indexa todos los libros** por temas (embeddings).  
  2. Cuando preguntas, te trae **solo las páginas relevantes**.  
  3. Luego, un experto (LLM) **resume la respuesta** usando esas páginas.

---

## Comparación Clave: RAG vs. "Pegar el Documento"

| **Aspecto**         | **Sin RAG**                                  | **Con RAG**                                  |
|----------------------|---------------------------------------------|---------------------------------------------|
| **Límite de tokens** | Falla con documentos grandes.              | Usa solo chunks relevantes (escalable).     |
| **Costo**            | Muy alto (pagos por todo el documento).     | Bajo (pagos por chunks útiles).             |
| **Velocidad**        | Lenta (procesa texto masivo).              | Rápida (procesa solo lo relevante).         |
| **Precisión**        | Riesgo de alucinaciones por ruido.         | Respuestas enfocadas en contexto real.      |
| **Actualizaciones**  | Reenviar todo el documento cada vez.       | Añadir/eliminar chunks dinámicamente.       |

---

## Ejemplo Real: Respuestas con y sin RAG
**Documento**:  
`"El protocolo X requiere 3 pasos: (1) Verificar conexión, (2) Ejecutar `sudo service restart`, (3) Validar logs en /var/logs."`

**Pregunta**:  
`"¿Cómo reiniciar el servicio según el protocolo X?"`

- **Sin RAG**:  
  ❌ `"Para reiniciar un servicio en Linux, usa `systemctl restart nombre-del-servicio`..."`  
  *(Alucinación: el LLM no sabe del protocolo X).*

- **Con RAG**:  
  ✅ `"Según el protocolo X, ejecute: (1) Verifique la conexión, (2) Ejecute `sudo service restart`, (3) Valide logs en /var/logs."`

---

## ¿Cuándo NO usar RAG?
- 📄 **Documentos muy cortos** (ej: 1 página).  
- ❓ **Preguntas generales** que no requieren contexto específico (ej: "¿Qué es un servidor?").  
- ⚙️ **Recursos limitados**: Si no puedes gestionar una base vectorial.

---



## Ejercicio 3: Ejemplo de Código con Pinecone

1. Instalar las dependencias
``` bash
pip install fastapi uvicorn pinecone-client sentence-transformers python-dotenv pinecone
```

2. Generar una api key en Pinecone

Pinecone es una base de datos vectorial que permite almacenar y recuperar datos de manera eficiente. Pinecone convierte los documentos en vectores de alta dimensión (embeddings) utilizando un modelo de lenguaje (como el modelo de embeddings SentenceTransformer) y luego permite realizar búsquedas rápidas para recuperar los documentos más similares a una consulta.

En el caso de RAG, Pinecone se utiliza para:

- Almacenar documentos: Convierte los documentos a embeddings y los guarda en un índice. Luego, cuando se realiza una consulta, puede buscar rápidamente los documentos más relevantes basados en su similitud con la consulta.
- Recuperación de documentos: Al recibir una consulta, Pinecone busca los documentos más similares en el índice y devuelve los más relevantes. Esta información se utiliza para crear un contexto relevante para la generación de respuestas.

3. API con FastAPI (main.py)

```python
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import os

from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

if not PINECONE_API_KEY:
    raise ValueError("Falta la API Key de Pinecone en el archivo .env")

INDEX_NAME = "rag-demo"

pc = Pinecone(api_key=PINECONE_API_KEY)
EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2')

# Crear índice si no existe
if INDEX_NAME not in [i["name"] for i in pc.list_indexes()]:
    pc.create_index(INDEX_NAME, dimension=EMBEDDING_MODEL.get_sentence_embedding_dimension())

index = pc.Index(INDEX_NAME)

app = FastAPI()

# Modelo para agregar documentos
class Document(BaseModel):
    doc_id: str
    text: str

# Modelo para consultas
class Query(BaseModel):
    text: str

@app.post("/add_document")
async def add_document(doc: Document):
    embedding = EMBEDDING_MODEL.encode(doc.text).tolist()
    index.upsert([(doc.doc_id, embedding, {"text": doc.text})])
    return {"message": "Documento agregado"}

@app.post("/query")
async def rag_query(query: Query):
    query_embedding = EMBEDDING_MODEL.encode(query.text).tolist()
    results = index.query(vector=query_embedding, top_k=3, include_metadata=True)

    context = " ".join([match["metadata"]["text"] for match in results["matches"] if "metadata" in match])

    return {"answer": f"Respuesta basada en: {context}", "context": context}
```

4. Ejecutar la API
```bash
uvicorn main:app --reload
```

Este endpoint está diseñado para agregar un documento de texto a Pinecone desde un JSON en el cual se envía el texto del documento junto con un ID único.

¿Cómo funciona?

Recibes un objeto JSON con:
- doc_id: El identificador único para el documento.
- text: El texto del documento que quieres agregar.

El texto se convierte en un embedding (vector numérico) usando el modelo de SentenceTransformer.
El documento con su doc_id, el embedding y el texto original se agrega al índice de Pinecone.

### Ejemplo de uso:

Si tienes un documento con información sobre un tema y quieres agregarlo a tu base de datos de Pinecone para que esté disponible para consultas posteriores, usarías este endpoint.


También se puede ingresar un documento desde un archivo .txt y agregar su contenido a Pinecone.

¿Cómo funciona?

Recibes un archivo .txt.
El contenido del archivo se lee y se convierte a un embedding (vector numérico).
El documento se agrega al índice de Pinecone con el nombre del archivo como ID.
Ejemplo de uso:

Si tienes un archivo de texto (por ejemplo, un archivo con una receta o un artículo) y quieres cargarlo en Pinecone para su posterior búsqueda, usarías este endpoint.

Código de ejemplo:
```python
@app.on_event("startup")
async def startup_event():
    print("Cargando documentación técnica en Pinecone...")
    # Cargar documentos desde un directorio de archivos de texto o base de datos
    documents = load_documents_from_directory("docs/")  # Cargar todos los documentos del directorio
    embeddings = EMBEDDING_MODEL.encode(documents).tolist()
    index = pc.Index(INDEX_NAME)
    vectors = [{"id": str(i), "values": embedding, "metadata": {"text": doc}} 
               for i, (embedding, doc) in enumerate(zip(embeddings, documents))]
    index.upsert(vectors)
    print("Documentos cargados con éxito.")
```

### ¿Para qué sirve usar RAG con Pinecone?
1. Mejorar la capacidad de respuesta:
Los modelos de lenguaje como GPT-3 o T5 tienen una capacidad limitada de conocimiento en función de su tamaño y de los datos con los que fueron entrenados. RAG permite acceder a información más actualizada o específica al buscar en bases de datos externas, como Pinecone. 

Esto es útil cuando:
- El modelo necesita acceder a una gran cantidad de información no contenida en sus parámetros.
La información es muy específica o técnica (por ejemplo, documentos científicos, manuales, datos de productos, etc.).
- El conocimiento es dinámico, como en el caso de noticias, documentos recientes, o bases de datos que cambian con frecuencia.

2. Sistema de preguntas y respuestas (QA):
Imagina que tienes un sistema de QA que responde a preguntas complejas sobre temas técnicos, como documentación de productos o información de soporte técnico. Sin RAG, el modelo solo podría generar respuestas basadas en lo que ha aprendido durante su entrenamiento, lo que no siempre es suficiente ni preciso.

Con RAG y Pinecone, cuando un usuario hace una pregunta, el sistema primero recupera los documentos más relevantes de la base de datos (Pinecone). Luego, el modelo usa esa información para generar una respuesta más precisa y detallada. Por ejemplo, si alguien pregunta sobre un aspecto técnico específico de un producto, el sistema puede acceder a los manuales de usuario y guías de producto más relevantes y generar una respuesta a partir de ahí.

3. Sistemas de recomendación de contenido:
En aplicaciones donde los usuarios necesitan recomendaciones personalizadas (por ejemplo, recomendación de artículos o contenidos en línea), RAG puede mejorar el proceso de búsqueda de contenido. Pinecone puede almacenar los artículos o páginas de contenido, y el modelo puede usar las consultas de los usuarios para buscar el contenido más relevante y generar recomendaciones de manera más precisa.

4. Asistentes virtuales o chatbots avanzados:
Un asistente virtual o chatbot entrenado con RAG puede acceder a una base de datos específica (por ejemplo, una base de datos de clientes, productos, o preguntas frecuentes) y recuperar información relevante para responder a las consultas de los usuarios. Esto permite que el asistente se base en datos actualizados y específicos, mejorando la calidad de las respuestas.

5. Búsqueda semántica:
Si tienes una base de datos grande con documentos, como artículos científicos, artículos de blog, libros, o cualquier tipo de contenido textual, RAG y Pinecone pueden mejorar significativamente la búsqueda. La búsqueda tradicional basada en palabras clave no siempre es efectiva, ya que no tiene en cuenta la semántica o el significado real detrás de las palabras. Pinecone permite realizar búsquedas semánticas donde los documentos más relevantes se recuperan no solo por coincidencias exactas de palabras, sino por similitud semántica (es decir, significado).

