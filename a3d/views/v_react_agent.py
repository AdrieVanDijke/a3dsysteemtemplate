import streamlit as st
from a3d.utilities.u_appcore import AppCoreUtilities
import a3d.controlers.c_react_agent as ra
from langchain_core.messages import AIMessage, HumanMessage


class ReActAgentView:
    def __init__( self ):
        self.appcore = AppCoreUtilities()  
        self.controler = ra.ReActAgentControler()      
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
                ("♻️ ReAct Agent", "🤖 Basic AI Chatbot", "🧮 Simple Graph", "🗄️ Embedding", "😺 CATja RAG Chatbot", "👥 Multi Agents", "💶 E-boekhouden test"),
            )
            # Als de pagina staat niet gelijk is aan de optie, zet de pagina staat en rerun
            if st.session_state['appState'] != option:
                self.controler.reset()
                self.appcore.setAppState(option)
                st.rerun()
            
            if st.button("🆕 New Chat 🪄"):
                st.session_state['chat_history'] = []


    def buildMainView( self ):
        user_query = ''
        response = ''                    
        with st.chat_message("AI", avatar='♻️'):
            st.write(self.getChatIntroTekst())

        # Gebruik een invoerveld om berichten van de gebruiker te ontvangen
        user_query = st.chat_input(placeholder="Bericht naar AI") 
        if user_query is not None and user_query != "": 
            with st.spinner(f"⚙️ {user_query[:400]}..."):  
                with st.sidebar:
                    with st.spinner(f"⚙️ {user_query[:40]}..."):
                        # Run de module met de gebruikers input	                
                        response = self.controler.run(user_query)
                        # Voeg de berichten toe aan de chat geschiedenis                                             
                        st.session_state.chat_history.append(HumanMessage(content=user_query))                
                        st.session_state.chat_history.append(AIMessage(content=response))    

        # Toon de chat geschiedenis
        for message in st.session_state.chat_history:
            if isinstance(message, AIMessage):
                with st.chat_message("AI", avatar='♻️'):
                    st.write(message.content)
            elif isinstance(message, HumanMessage):
                with st.chat_message("Human", avatar='👤'):
                    st.write(message.content) 


    # WORKERS =======================================    
    # standaard chat intro tekst
    def getChatIntroTekst( self ):   
        intro_tekst = """        
        **Hallo**, Ik ben een V/A ReAct Agent met Tools *(een zoekfunctie (zoeken op internet) en diverse rekengereedschap)*. 
        Ik heb geen *echt* geheugen maar van de vorige vraag en het antwoord daarop wordt *(bij een vervolgvraag)* een samenvatting gemaakt.  
        Waar kan ik je mee van dienst zijn?
        """
        return intro_tekst 
