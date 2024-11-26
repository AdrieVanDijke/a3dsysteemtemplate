import streamlit as st
from a3d.utilities.appcore import AppCore


st.set_page_config(page_title="A3D AI Template", page_icon="🛠️")

def main():
    appcore = AppCore()
    if st.session_state['appState'] == "🗨️ Basis AI Chatbot":
        klass = appcore.loadModule("a3d.views.v_basis_chat", "BasisChatView")
        klass() 
    elif st.session_state['appState'] == "🔗 Simpele Graph":
        klass = appcore.loadModule("a3d.views.v_simple_graph", "SimpleGraphView")
        klass()



if __name__ == "__main__":
    main()