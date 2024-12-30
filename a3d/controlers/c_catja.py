import streamlit as st
import openai
from openai import OpenAI
import pinecone
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.vectorstores import Pinecone
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import Tool



class CatjaControler:
    def __init__( self ):
        # Initialize chat history
        if "chat_history" not in st.session_state:
            st.session_state['chat_history'] = []               
        # AI model voor RAG chain ed.    
        if "ragmodel" not in st.session_state:
            st.session_state['ragmodel'] = "gpt-4o-mini"
        # AI model voor zoekmachine.    
        if "zoektermmodel" not in st.session_state:
            st.session_state['zoektermmodel'] = "gpt-3.5-turbo"
        # AI model voor Embedding.    
        if "embeddingmmodel" not in st.session_state:
            st.session_state['embeddingmmodel'] = "text-embedding-3-small"

    
    # Cache legen geheugen wissen ===============
    def reset(self):
        del st.session_state['chat_history'] 
        del st.session_state['ragmodel']
        del st.session_state['zoektermmodel']
        del st.session_state['embeddingmmodel']


    # MAIN =====================================    
    def run(self, user_input):
        # 1e run als st.session_state['show_loader'] leeg is dan andere llm aanroepen
        if len(st.session_state['chat_history']) == 0:
            # maak een zoekterm met kernwoorden voor Pinecone
            new_query = self.get_optimized_search_term(user_input)
             # Hyde zoekterm maken
            hyde_query = self.get_db_hyde_search_term(user_input) 
            # Pinecone ophalen + retrievers maken
            vector_store = self.get_pinecone()
            retriever = vector_store.as_retriever(search_kwargs={"k": 2})
            retriever_2 = vector_store.as_retriever(search_kwargs={"k": 1})

            # gehele input zoeken in Pinecone
            docs_1 = retriever.invoke(user_input)
            # kernwoorden zoeken in Pinecone
            docs_2 = retriever.invoke(new_query)  
            # hyde zoekterm zoeken in Pinecone
            docs_3 = retriever_2.invoke(hyde_query)  

            # Resultaat beide zoekvormen combineren / samenvoegen tot een documenten
            docs = self.combineer_documenten(docs_1, docs_2, docs_3)

            # AI model aanroepen
            llm = ChatOpenAI (model=st.session_state['ragmodel'], temperature=0.2)
            # documenten en vraag naar AI sturen voor antwoord
            prompt = ChatPromptTemplate.from_messages([
            ("system", self.getSysteemPrompt()),
                ("user", "{context}"),
                ("user", "{input}"),               
            ])        
            stuff_documents_chain = create_stuff_documents_chain(llm,prompt)
            # 1e run -> RAG zonder geschiedenis
            vraag = user_input
            response = stuff_documents_chain.invoke({"input": vraag, "context": docs})
            return response
        # 2e run -> RAG met geschiedenis
        else:
            retriever_chain = self.get_context_retriever_chain(self.get_pinecone())
            conversation_rag_chain = self.get_conversational_rag_chain(retriever_chain)      
            response = conversation_rag_chain.invoke({
                "chat_history": st.session_state.chat_history[-6:],
                "input": user_input
            })   
            return response['answer']


    # WORKERS ==================================
    # RAG ------------------------------------------------------
    # 1e run: zoekterm optimaliseren (kernwoorden) voor Pinecone -> voor eerste call van gebruiker
    def get_optimized_search_term(self, user_query):
        llm = ChatOpenAI(model=st.session_state['ragmodel'], temperature = 0.2)
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.get_eerste_vraag_prompt()),
            ("user", "{input}")
        ])
        output_parser = StrOutputParser()
        chain = prompt | llm | output_parser
        new_query = chain.invoke({"input": user_query})
        return new_query


    # 1e run: een hypothetische passage/zoekterm maken voor de database
    def get_db_hyde_search_term(self, user_query):
        llm = ChatOpenAI(model=st.session_state['ragmodel'], temperature = 0.3)
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.get_db_hyde_prompt_template()),
            ("user", "{input}")
        ])
        output_parser = StrOutputParser()
        chain = prompt | llm | output_parser
        new_query = chain.invoke({"input": user_query})
        return new_query


    # 1e run: voeg documenten samen
    def combineer_documenten(self, document1, document2, document3):
        gecombineerd = []
        # Voeg documenten uit document1 toe
        for document in document1:
            gecombineerd.append(document)
        # Voeg documenten uit document2 toe, mits uniek
        for document in document2:
            if document not in gecombineerd:
                gecombineerd.append(document)
        # Voeg documenten uit document3 toe, mits uniek
        for document in document3:
            gecombineerd.append(document)
                              
        return gecombineerd


    # 2e run: RAG met geschiedenis 1: context retriever chain
    def get_context_retriever_chain(self, vector_store):
        llm = ChatOpenAI(model=st.session_state['ragmodel'], temperature=0)       
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})  
        prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", self.get_db_prompt_template())
        ])       
        retriever_chain = create_history_aware_retriever(llm, retriever, prompt)      
        return retriever_chain
    

    # 2e run: RAG met geschiedenis 2: conversational rag chain
    def get_conversational_rag_chain(self, retriever_chain):        
        llm = ChatOpenAI (model=st.session_state['ragmodel'], temperature=0.2)       
        prompt = ChatPromptTemplate.from_messages([
        ("system", self.getSysteemPrompt()),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
        ])        
        stuff_documents_chain = create_stuff_documents_chain(llm,prompt)               
        return create_retrieval_chain(retriever_chain, stuff_documents_chain)


    # DATA =====================================
    @st.cache_resource
    def get_pinecone( _self ):
        pc = pinecone.Pinecone(api_key=st.secrets["PINECONE_API_KEY"], environment=st.secrets["PINECONE_ENVIRONMENT"])
        embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["OPENAI_API_KEY"]) # oude versie standaard waarde
        #embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["OPENAI_API_KEY"], model=st.session_state['embeddingmmodel']) # nieuwe versie met model parameter text-embedding-3-small
        vectorstore = Pinecone.from_existing_index(st.secrets["PINECONE_INDEX_NAME"], embeddings, "text")
        return vectorstore 
    

    def getSysteemPrompt( self ):
        prompt = """Je bent een AI assistent in dienst van beroepsorganisatie CAT en account systeem kwaliteitsysteem.nl. Je bent de CATviseur. Je naam is CATja.  
Gebruik de onderstaande context om de vraag van de gebruiker zo ter zake doende mogelijk te beantwoorden. Vermijd het vermelden van de context zoals b.v. in: 'In de context staat...'. 
**Verzin geen URL's, websitenamen, e-mailadressen, paginanamen of vensternamen die niet direct uit de context gehaald kunnen worden. Geef nooit URLs/links die niet in de context staan! Geef geen fictieve voorbeelden!** 
Concentreer je op de vraag en het beantwoorden daarop zonder overbodige informatie te geven dat niet direct met de vraag te maken heeft.  
Als de vraag te onduidelijk is of als je geen goed antwoord uit de context kunt halen en je zelf ook het antwoord niet zeker weet geef dan aan dat de vraag onduidelijk is en vraag om verduidelijking.  
Als er gevraagd wordt of een bepaald diploma, opleiding of beroep/vak erkend of toegestaan is, of voldoende is om toegelaten te worden tot een beroepsorganisatie, antwoord dan niet met ja maar geef aan dat de screeningcommissie daarover beslist. 
Als er door de gebruiker wordt aangegeven dat deze gegevens in het account heeft aangevuld/geüpload/opgevoerd/bijgewerkt geef dan aan dat de CATviseur niet in staat bent dit door te geven!!! 
Geef aan dat ze dit door kunnen geven door een van de formulieren op de Servise + Contact pagina in te vullen voor een snellere afhandeling.  
Ter verduidelijking: CAT-collectief, CAT-vergoedbaar en Complementaire Kwaliteitstherapeuten zijn beroepsorganisaties, BAT is een verzekeringsmaatschappij en GAT is een geschilleninstantie.  
Verwerk zo veel mogelijk URLs die in de context staan als klikbare links in het antwoord.  
Afsluiten van het antwoord: Vraag of er nog vragen zijn.
\n\n<context>{context}</context>"""
        return prompt
    

    def get_eerste_vraag_prompt(self):
        prompt = """Je bent een Nederlandstalige taalprofessor gespecialiseerd in het filteren van kernwoorden uit de door de gebruiker gegeven input. 
Je maakt van de input effectieve zoekwoorden om een antwoord op de kern van de vraag te verkrijgen. Voeg maximaal 1 synoniem per kernwoord toe aan je zoekwoorden maar vergeet niet het originele kernwoord ook te gebruiken.
Output: Alleen de zoekwoorden en geen beschrijving. Gebruik geen aanhalingstekens."""
        return prompt
    

    def get_db_hyde_prompt_template(self):
        prompt = """Schrijf een passage om de vraag te beantwoorden 
in de wetenschap dat de vraag gesteld wordt door een zorgverlener of student in de alternatieve zorg die lid is of lid wil worden van een beroepsorganisatie in die zelfde sector. 
Deze therapeuten hebben een account op kwaliteitsyteem.nl dat controle uitvoert op de verplichtingen die de zorgverleners hebben.\n
Probeer zoveel mogelijk belangrijke details op te nemen."""
        return prompt
    

    def get_db_prompt_template(self):
        prompt_template = """Genereer, gezien het bovenstaande gesprek, een zoekopdracht om informatie te verkrijgen die relevant is voor het gesprek. 
Retourneert altijd alleen de zoekopdracht en geen beschrijving."""
        return prompt_template


