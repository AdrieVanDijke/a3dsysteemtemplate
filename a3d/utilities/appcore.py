import streamlit as st
import os
import importlib

# OPENAI API KEY ===========================
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# LANGSMITH ================================================================================

#os.environ["LANGCHAIN_TRACING_V2"] = "true"
#os.environ["LANGCHAIN_PROJECT"] = st.secrets["LANGCHAIN_PROJECT"]
#os.environ["LANGCHAIN_ENDPOINT"] = st.secrets["LANGCHAIN_ENDPOINT"]
#os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]

# LANGSMITH ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

class AppCore:
    def __init__(self):        
        # Pagina Staat zetten als deze nog niet bestaat
        if "paginaStaat" not in st.session_state:
            self.zetPaginaStaat("🗨️ Basis AI Chatbot")       


    # Pagina Staat zetten
    def zetPaginaStaat( self, staat ):
        st.session_state['paginaStaat'] = staat


    # Dynamisch modules laden 
    def laadModule(self, module_name, class_name):
        module = importlib.import_module(module_name)
        # Dynamisch een class ophalen uit de module
        klass = getattr(module, class_name)
        return klass


    # Log functionaliteit
    def log( self, boodschap, locatie="N.v.t." ):
        if locatie:
            print(f"[LOCATIE]: {locatie}") 

        print(f"[LOG]: {boodschap}")   
        print("-----------------------------------") 

            
