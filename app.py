import streamlit as st
from a3d.utilities.u_appcore import AppCoreUtilities


st.set_page_config(page_title="A3D AI Template", page_icon="🛠️")

def main():
    appcore = AppCoreUtilities()
    if st.session_state['appState'] == "🤖 Basic AI Chatbot":
        klass = appcore.loadModule("a3d.views.v_basic_chat", "BasicChatView")
        klass() 
    elif st.session_state['appState'] == "🧮 Simple Graph":
        klass = appcore.loadModule("a3d.views.v_simple_graph", "SimpleGraphView")
        klass()
    elif st.session_state['appState'] == "♻️ ReAct Agent":
        klass = appcore.loadModule("a3d.views.v_react_agent", "ReActAgentView")
        klass()
    elif st.session_state['appState'] == "🗄️ Embedding":
        klass = appcore.loadModule("a3d.views.v_embedding", "EmbeddingView")
        klass()
    elif st.session_state['appState'] == "😺 CATja RAG Chatbot":
        klass = appcore.loadModule("a3d.views.v_catja", "CatjaView")
        klass()
    elif st.session_state['appState'] == "👥 Multi Agents":
        klass = appcore.loadModule("a3d.views.v_multi_agents", "MultiAgentsView")
        klass()
    elif st.session_state['appState'] == "💶 E-boekhouden test":
        klass = appcore.loadModule("a3d.views.v_e_boekhouden", "E_BoekhoudenView")
        klass()


if __name__ == "__main__":
    main()