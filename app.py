import streamlit as st
from a3d.utilities.appcore import AppCore


st.set_page_config(page_title="A3D AI Template", page_icon="🛠️")

def main():
    appcore = AppCore()
    if st.session_state['paginaStaat'] == "🗨️ Basis AI Chatbot":
        klass = appcore.laadModule("a3d.views.v_basis_chat", "BasisChatView")
        klass() 
    elif st.session_state['paginaStaat'] == "🔗 Simpele Graph":
        klass = appcore.laadModule("a3d.views.v_simple_graph", "SimpleGraphView")
        klass()
    elif st.session_state['paginaStaat'] == "⛓️ Graph met Tools Test":
        klass = appcore.laadModule("a3d.views.v_graph_tools", "GraphToolsView")
        klass()


if __name__ == "__main__":
    main()