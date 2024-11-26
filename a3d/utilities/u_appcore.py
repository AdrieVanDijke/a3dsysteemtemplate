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

class AppCoreUtilities:
    def __init__(self):        
        # Pagina Staat zetten als deze nog niet bestaat
        if "appState" not in st.session_state:
            self.setAppState("🗨️ Basic AI Chatbot")       


    # Pagina Staat zetten
    def setAppState( self, state ):
        st.session_state['appState'] = state


    # Dynamisch modules laden 
    def loadModule( self, module_name, class_name=None ):
        # Class terug als class naam is opgegeven
        if class_name is not None:
            module = importlib.import_module(module_name)
            klass = getattr(module, class_name)
            return klass
        # Module terug als class naam niet is opgegeven
        else:
            return importlib.import_module(module_name)
        


    # Log functionaliteit
    def log( self, text, location="N.v.t." ):
        if location:
            print(f"[LOCATIE]: {location}") 

        print(f"[LOG]: {text}")   
        print("-----------------------------------") 

            
