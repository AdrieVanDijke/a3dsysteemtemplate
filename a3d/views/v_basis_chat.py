import streamlit as st
from a3d.utilities.appcore import AppCore
from a3d.modules.m_basis_chat import BasisChatModule
from langchain_core.messages import AIMessage, HumanMessage


class BasisChatView:
    def __init__( self ):
        self.appcore = AppCore()
        self.module = BasisChatModule()        
        self.bouwView()


    # VIEWS =========================================
    def bouwView( self ):
        self.bouwSidebarView()
        self.bouwMainView()


    def bouwSidebarView( self ):
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
            if st.button("🆕 Nieuwe Chat 🪄"):
                st.session_state['chat_history'] = []

            option = st.selectbox(
                "Selecteer een Module",
                ("🗨️ Basis AI Chatbot", "🔗 Simpele Graph", "⛓️ Graph met Tools Test"),
            )
            # Als de pagina staat niet gelijk is aan de optie, zet de pagina staat en rerun
            if st.session_state['paginaStaat'] != option:
                st.session_state['chat_history'] = []
                st.session_state['systemprompt'] = ""
                self.appcore.zetPaginaStaat(option)
                st.rerun()

            # Systeemprompt gedeelte       
            st.text_area(
                "Systeemprompt:",
                key = "input_area",  # Koppel het tekstgebied aan st.session_state
                value = st.session_state['systemprompt'],  # Vul het tekstveld met de opgeslagen waarde
                height = 200,
            )
            st.button(
                "🔁 Systeemprompt Instellen ✅",
                on_click = self.save_systeem_prompt  # Roep de save_systeem_prompt-functie aan bij een klik op de knop
            )


    def bouwMainView( self ):
        user_query = ''
        response = ''
        # Toon het eerste bericht van de AI als er geen chat geschiedenis is
        if len(st.session_state['chat_history']) == 0:                
            with st.chat_message("AI", avatar='🤖'):
                st.write(self.getChatIntroTekst())

        # Gebruik een invoerveld om berichten van de gebruiker te ontvangen
        user_query = st.chat_input(placeholder="Bericht naar AI") 
        if user_query is not None and user_query != "": 
            with st.spinner(f"⚙️ {user_query[:400]}..."):  
                with st.sidebar:
                    with st.spinner(f"⚙️ {user_query[:40]}..."):
                        # Run de module met de gebruikers input	                
                        response = self.module.runModule(user_query)   
                        # Voeg de berichten toe aan de chat geschiedenis                      
                        st.session_state.chat_history.append(HumanMessage(content=user_query))                
                        st.session_state.chat_history.append(AIMessage(content=response))
        # Toon de chat geschiedenis
        for message in st.session_state.chat_history:
            if isinstance(message, AIMessage):
                with st.chat_message("AI", avatar='🤖'):
                    st.write(message.content)
            elif isinstance(message, HumanMessage):
                with st.chat_message("Human", avatar='👤'):
                    st.write(message.content) 

    # WORKERS ======================================= 
 
    # Systeem prompt opslaan 
    def save_systeem_prompt(self):
        st.session_state['systemprompt'] = st.session_state['input_area']


    # Introductie tekst voor de chat
    def getChatIntroTekst( self ):   
        intro_tekst = """        
        **Hallo**, Ik ben een basis OpenAI Chatbot met een Systeemprompt en geheugen van 10 berichten.  
        Waar kan ik je mee van dienst zijn?  
        """
        return intro_tekst 
