import streamlit as st
from a3d.utilities.u_appcore import AppCoreUtilities
import a3d.controlers.c_embedding as ec



class EmbeddingView:
    def __init__( self ):
        self.appcore = AppCoreUtilities()  
        self.controler = ec.EmbeddingControler()      
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
                ("🗄️ Embedding", "🤖 Basic AI Chatbot", "🧮 Simple Graph", "♻️ ReAct Agent", "😺 CATja RAG Chatbot", "👥 Multi Agents", "💶 E-boekhouden test"),
            )
            # Als de pagina staat niet gelijk is aan de optie, zet de pagina staat en rerun
            if st.session_state['appState'] != option:
                self.controler.reset()
                self.appcore.setAppState(option)
                st.rerun()

            info = """This module stores the data from the text files located in the "files/to_db" folder in a Pincone database.  
            Click the button below to start the embedding process.
            """

            st.info(info)


            if st.button("➡️ Embed Content 🗄️"):
                self.controler.run()


    def buildMainView( self ):
        st.subheader("🗄️ Embedding")
        

    # WORKERS =======================================    

