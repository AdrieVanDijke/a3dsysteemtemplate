import streamlit as st
from a3d.utilities.u_appcore import AppCoreUtilities
from a3d.controlers.c_catja import CatjaControler
from langchain_core.messages import AIMessage, HumanMessage


class CatjaView:
    def __init__( self ):
        self.appcore = AppCoreUtilities()
        self.controler = CatjaControler()        
        self.buildView()


    # VIEWS =========================================
    def buildView( self ):
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
                ("😺 CATja RAG Chatbot", "🤖 Basic AI Chatbot", "🧮 Simple Graph", "♻️ ReAct Agent", "🗄️ Embedding", "👥 Multi Agents", "💶 E-boekhouden test"),
            )
            # Als de pagina staat niet gelijk is aan de optie, zet de pagina staat en rerun
            if st.session_state['appState'] != option:
                self.controler.reset()
                self.appcore.setAppState(option)
                st.rerun()

            if st.button("🆕 New Chat 🪄"):
                st.session_state['chat_history'] = []
                st.session_state['teller'] = 0


    def buildMainView( self ):
        user_query = ''
        response = ''
        # Toon het eerste bericht van de AI als er geen chat geschiedenis is
        if len(st.session_state['chat_history']) == 0:                
            with st.chat_message("AI", avatar='😺'):
                st.write(self.getChatIntroText())

        # Gebruik een invoerveld om berichten van de gebruiker te ontvangen
        user_query = st.chat_input(placeholder="Type hier je vraag aan CATja...") 
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
                with st.chat_message("AI", avatar='😺'):
                    st.write(message.content)
            elif isinstance(message, HumanMessage):
                with st.chat_message("Human", avatar='👤'):
                    st.write(message.content) 


    # WORKERS =======================================  
    # Introductie tekst voor de chat
    def getChatIntroText( self ):   
        intro_tekst = """
        **Hallo,**         
        🗨️ **Ik ben CATja**, een AI chatbot in dienst van beroepsorganisatie CAT en kwaliteitsysteem.nl.  
        🗨️ Als je een vraag aan mij wil stellen, type deze dan in het tekst veld hieronder ⤵️ en druk op **enter**.
        """
        return intro_tekst

