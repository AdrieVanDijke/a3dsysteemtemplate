import streamlit as st
from openai import OpenAI
from langchain_core.messages import AIMessage, HumanMessage


class MultiAgentsControler:
    def __init__( self ):
        self.client = OpenAI()
        self.model = "gpt-4o"
        self.temp = 0.4
        self.max_history = 10
        # Initialize chat history
        if "chat_history" not in st.session_state:
            st.session_state['chat_history'] = []

    
    # Cache legen geheugen wissen ===============
    def reset(self):
        del st.session_state['chat_history'] 


    # MAIN =====================================    
    def run(self, user_input):
        testReturn = "IETS OM TERUG TE STUREN"
        return testReturn


    # WORKERS ==================================

    # DATA =====================================



