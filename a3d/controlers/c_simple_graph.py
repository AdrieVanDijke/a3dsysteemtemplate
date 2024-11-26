import streamlit as st
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver


# Define state
class GraphState(TypedDict):
    count: int


class SimpleGraphControler:
    def __init__( self ):
        # Initialize chat history
        if "chat_history" not in st.session_state:
            st.session_state['chat_history'] = []
        # config voor geheugen    
        if "config" not in st.session_state:
            st.session_state['config'] = {"configurable": {"thread_id": 1234}}
        # geheugen    
        if "memory" not in st.session_state:
            st.session_state['memory'] = MemorySaver()
        # Graph builder
        if "builder" not in st.session_state:
            st.session_state['builder'] = StateGraph(GraphState)
            # Graph
        if "graph" not in st.session_state:
            st.session_state['graph'] = None
        # Vlag voor initialisatie (om te voorkomen dat de graph meerdere keren wordt gemaakt)   
        if "initflag" not in st.session_state:
            st.session_state['initflag'] = False
        # Maak de graph als deze nog niet is gemaakt
        if st.session_state['initflag'] == False:
            self.buildGraph()


    # Cache legen geheugen wissen ========================
    def reset(self):
        del st.session_state['chat_history'] 
        del st.session_state['config']       
        del st.session_state['memory']
        del st.session_state['builder']
        del st.session_state['graph']
        del st.session_state['initflag']


    # Maak Nodes =========================================
    # Create developer (test) node
    def developer(self, state):
        state['count'] += 1  # Getal verhogen
        return state  # Aangepaste state teruggeven


    # Maak de graph ======================================  
    def buildGraph(self):
        st.session_state['initflag'] = True
        # Node aan graph toevoegen
        st.session_state['builder'].add_node("developer", self.developer)

        # Zet beginpunt en eindpunt (eges)
        st.session_state['builder'].add_edge(START, "developer")
        st.session_state['builder'].add_edge('developer', END)

        # Maak en gebruik de bouwer
        st.session_state['graph'] = st.session_state['builder'].compile(checkpointer=st.session_state['memory'])
        inputs = {"count": 0}  # begin staat
        result = st.session_state['graph'].invoke(inputs, st.session_state['config'])
        return result
    
    # Run de module ======================================= 
    def run(self):
        # Run de graph
        count = st.session_state['graph'].get_state(st.session_state['config']).values["count"]
        result = st.session_state['graph'].invoke({"count": count}, st.session_state['config'])
        return result





