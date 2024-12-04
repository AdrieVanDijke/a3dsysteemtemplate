import os
import streamlit as st
from pinecone import Pinecone, ServerlessSpec
from langchain_community.vectorstores import Pinecone as LangChainPinecone
from langchain_openai.embeddings import OpenAIEmbeddings
import uuid


class Document:
    def __init__(self, text, metadata=None, doc_id=None):
        self.page_content = text
        self.metadata = metadata if metadata is not None else {}
        self.id = doc_id if doc_id is not None else str(uuid.uuid4())  # Uniek ID genereren


class EmbeddingControler:
    def __init__( self ):
        self.pineKey = st.secrets["PINECONE_API_KEY"]
        self.pineEnv = st.secrets["PINECONE_ENVIRONMENT"]
        self.pineInd = st.secrets["PINECONE_INDEX_NAME"]
        self.pinemod = "text-embedding-ada-002"

    
    def reset(self):
        pass


    # MAIN =====================================    
    def run(self):
        doc_db = self.embedding_db()
        print(doc_db)
        print("Bestanden weggeschreven naar PineCone DB")


    # WORKERS ==================================
    def embedding_db(self):
        embeddings = OpenAIEmbeddings(model=self.pinemod)  
        pc = Pinecone(api_key=self.pineKey)

        if self.pineInd not in pc.list_indexes().names():
            pc.create_index(
                name=self.pineInd,
                dimension=1536,  
                metric='cosine',  
                spec=ServerlessSpec(
                    cloud='gcp',  
                    region=self.pineEnv  
                )
            )

        docs_split = self.load_embeddings_from_dir()

        doc_db = LangChainPinecone.from_documents(
            docs_split, 
            embeddings, 
            index_name=self.pineInd
        )   
        return doc_db


    def load_embeddings_from_dir(self):
        directory = './files/to_db/'
        documents = []  
        for filename in os.listdir(directory):
            if filename.endswith('.txt'):
                file_path = os.path.join(directory, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    parts = content.split('\n\n')
                    for part in parts:
                        documents.append(Document(part))
        print(f"Aantal gesplitste documenten: {len(documents)}")
        return documents