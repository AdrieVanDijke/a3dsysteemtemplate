import streamlit as st
from a3d.utilities.u_appcore import AppCoreUtilities
from a3d.controlers.c_e_boekhouden import E_BoekhoudenControler
from langchain_core.messages import AIMessage, HumanMessage


class E_BoekhoudenView:
    def __init__( self ):
        self.appcore = AppCoreUtilities()
        self.controler = E_BoekhoudenControler()        
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
                ("💶 E-boekhouden test", "🤖 Basic AI Chatbot", "🧮 Simple Graph", "♻️ ReAct Agent", "🗄️ Embedding", "😺 CATja RAG Chatbot", "👥 Multi Agents"),
            )
            # Als de pagina staat niet gelijk is aan de optie, zet de pagina staat en rerun
            if st.session_state['appState'] != option:
                self.controler.reset()
                self.appcore.setAppState(option)
                st.rerun()

            

            
    def buildMainView( self ):
        st.subheader("💶 E-boekhouden testruimte")

        if st.button("Haal facturen van testpersoon op"):
            response = self.controler.run(st.secrets["RELATIECODE"])
            response = self.format_response(response)
            response = self.display_response(response)

            st.markdown(response, unsafe_allow_html=True)
        

    # WORKERS =======================================  

    def format_response(self, response):
        """
        Format de response van de facturen naar een leesbaar formaat.
        """
        if hasattr(response, "Facturen") and response.Facturen is not None:
            # Controleer of het een lijst van factuurobjecten bevat
            facturen_list = getattr(response.Facturen, "cFactuurList", response.Facturen)
            if isinstance(facturen_list, list):
                return [
                    {
                        "Factuurnummer": f.Factuurnummer,
                        "Datum": f.Datum,
                        "TotaalInclBTW": f.TotaalInclBTW,
                        "Relatiecode": f.Relatiecode,
                        "URLPDF": f.URLPDFBestand
                    } for f in facturen_list
                ]
            elif isinstance(facturen_list, object):  # Enkelvoudig object
                return [
                    {
                        "Factuurnummer": facturen_list.Factuurnummer,
                        "Datum": facturen_list.Datum,
                        "TotaalInclBTW": facturen_list.TotaalInclBTW,
                        "Relatiecode": facturen_list.Relatiecode,
                        "URLPDF": facturen_list.URLPDFBestand
                    }
                ]
        return "Geen facturen gevonden."

    def display_response(self, formatted_response):
        """
        Toon de response in een mooi opgemaakte Markdown-weergave met emoji's.
        """
        if isinstance(formatted_response, list):
            markdown_output = ""
            for factuur in formatted_response:
                markdown_output += (
                    f"### 📄 Factuur {factuur['Factuurnummer']}\n"
                    f"- **Datum**: {factuur['Datum']}\n"
                    f"- **Totaal (incl. BTW)**: €{factuur['TotaalInclBTW']}\n"
                    f"- **Relatiecode**: {factuur['Relatiecode']}\n"
                    f"- [🔗 Download PDF]({factuur['URLPDF']})\n\n"
                )
            return markdown_output
        else:
            return f"### ❌ {formatted_response}"