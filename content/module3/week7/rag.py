from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import os
from dotenv import load_dotenv
import sys

# Cargar variables de entorno AL INICIO
load_dotenv()

# Verificar que la API key de OpenAI esté configurada correctamente
if not os.getenv("OPENAI_API_KEY"):
    print("\n❌ Error: La API key de OpenAI no está configurada.")
    print("\nPor favor sigue estos pasos:")
    print("1. Crea un archivo .env en este directorio (copia .env.example si existe)")
    print("2. Añade tu API key de OpenAI: OPENAI_API_KEY=tu_api_key_aquí")
    print("3. Asegúrate de que la API key sea válida y esté activa")
    print("\nPuedes obtener tu API key en: https://platform.openai.com/account/api-keys\n")
    sys.exit(1)

try:
    # Verificar si el archivo existe
    file_path = "tu_archivo.txt"
    if not os.path.exists(file_path):
        print(f"\n❌ Error: El archivo '{file_path}' no existe.")
        print(f"Directorio actual: {os.getcwd()}")
        print(f"Ruta completa buscada: {os.path.abspath(file_path)}")
        print("\nPor favor asegúrate de que el archivo existe en este directorio.")
        sys.exit(1)
        
    # 1. Cargar documentos (ejemplo)
    print(f"Cargando archivo: {file_path}...")
    loader = TextLoader(file_path)  # Reemplaza con tu fuente de datos
    documents = loader.load()
    print(f"✅ Archivo cargado correctamente. Encontrados {len(documents)} documentos.")

    # 2. Dividir documentos en chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    print(f"✅ Textos divididos en {len(texts)} fragmentos.")

    # 3. Crear base vectorial y retriever
    print("Generando embeddings con OpenAI...")
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(texts, embeddings)
    retriever = vectorstore.as_retriever()
    print("✅ Base vectorial y retriever creados correctamente.")

    # Sistema de pregunta-respuesta mejorado
    system_prompt = """Eres un experto en sistemas de Retrieval Augmented Generation (RAG).
    Responde a las preguntas de manera detallada y técnica, utilizando la información del contexto.
    Si no encuentras información suficiente en el contexto proporcionado, indícalo claramente.
    Cita secciones específicas del contexto cuando sea relevante.
    
    Contexto: {context}"""

    # Lista de preguntas interesantes - elegimos una
    questions = [
        "¿Cuáles son las principales ventajas de usar RAG frente a LLMs tradicionales?",
        "¿Qué componentes principales conforman un sistema RAG avanzado?",
        "¿Cuáles son los principales desafíos y limitaciones de los sistemas RAG?",
        "¿Cómo se evalúa la efectividad de un sistema RAG?",
        "¿Qué arquitecturas de RAG existen y cuáles son sus diferencias?"
    ]
    
    # Seleccionamos una pregunta (puedes cambiar el índice para probar diferentes preguntas)
    question = questions[1]  # Pregunta sobre componentes de RAG
    
    print(f"\nPregunta: {question}")

    # Recuperar documentos relevantes
    print("Recuperando documentos relevantes...")
    docs = retriever.invoke(question)
    docs_text = "\n".join(d.page_content for d in docs)

    # Formatear prompt
    formatted_prompt = system_prompt.format(context=docs_text)

    # Crear y ejecutar modelo
    print("Generando respuesta con el modelo...")
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    response = model.invoke([
        SystemMessage(content=formatted_prompt),
        HumanMessage(content=question)
    ])

    print("\n✅ Respuesta del modelo:")
    print("-" * 50)
    print(response.content)
    print("-" * 50)

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    print(f"\nDetalles del error:\n{traceback.format_exc()}")
    print("\nSi es un error de autenticación, verifica que tu API key sea correcta.")
    print("Si es un error de archivo, asegúrate de que tu_archivo.txt exista y sea legible.")
    print("Si necesitas ayuda, consulta el README.md para instrucciones detalladas.")
    sys.exit(1) 