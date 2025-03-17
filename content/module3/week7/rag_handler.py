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