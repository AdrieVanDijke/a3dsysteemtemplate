import streamlit as st
from a3d.utilities.u_appcore import AppCoreUtilities
import a3d.controlers.c_simple_graph as sg
from langchain_core.messages import AIMessage, HumanMessage


class SimpleGraphView:
    def __init__( self ):
        self.appcore = AppCoreUtilities()  
        self.controler = sg.SimpleGraphControler()      
        self.bouwView()


    # VIEWS =========================================
    def bouwView( self ):
        self.buildSidebarView()
        self.buildMainView()


    def buildSidebarView( self ):
        st.markdown(
            """
            <style>
                section[data-testid="stSidebar"] {
                    width: 450px !important;
                    text-align: center;
                }              
            </style>
            """,
            unsafe_allow_html=True  
        )
        with st.sidebar:
            option = st.selectbox(
                "Select a Module",
                ("🔗 Simple Graph", "🗨️ Basic AI Chatbot"),
            )
            # Als de pagina staat niet gelijk is aan de optie, zet de pagina staat en rerun
            if st.session_state['appState'] != option:
                self.controler.reset()
                self.appcore.setAppState(option)
                st.rerun()


    def buildMainView( self ):
        user_query = ''
        response = ''
        # Toon het eerste bericht van de AI als er geen chat geschiedenis is
        if len(st.session_state['chat_history']) == 0:                
            with st.chat_message("AI", avatar='🧮'):
                st.write(self.getChatIntroTekst())

        # Gebruik een invoerveld om berichten van de gebruiker te ontvangen
        user_query = st.chat_input(placeholder="Bericht naar AI") 
        if user_query is not None and user_query != "": 
            with st.spinner(f"⚙️ {user_query[:400]}..."):  
                with st.sidebar:
                    with st.spinner(f"⚙️ {user_query[:40]}..."):
                        # Run de module met de gebruikers input	                
                        response = self.controler.run()   
                        # Voeg alleen response berichten toe aan de chat geschiedenis ======================'    
                        count = response['count']  
                        antw = f"Count: {count}"        
                        st.session_state.chat_history.append(AIMessage(content = antw))

        # Toon de chat geschiedenis
        for message in st.session_state.chat_history:
            if isinstance(message, AIMessage):
                with st.chat_message("AI", avatar='🧮'):
                    st.write(message.content)
            elif isinstance(message, HumanMessage):
                with st.chat_message("Human", avatar='👤'):
                    st.write(message.content) 

    # WORKERS =======================================    
    # standaard chat intro tekst
    def getChatIntroTekst( self ):   
        intro_tekst = """        
        Dit is een hele simpele Graph module bedoeld om Graph en state functionaliteit te testen in een Class in een Streamlit omgeving.  
        🔸 Type iets in het chatvenster en klik op Enter om een teller op te laten lopen.  
        🔸 Wat je typt maakt niet uit.  
        🔸 Standaard staat de teller op 1
        """
        return intro_tekst 
