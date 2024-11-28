import streamlit as st
from typing import Annotated
from typing import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START
from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from openai import OpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import tools_condition # this is the checker for the if you got a tool back
from langgraph.prebuilt import ToolNode


# Define state
class GraphState(TypedDict):
    #messages: list
    messages:Annotated[list, add_messages]


class ReActAgentControler:
    def __init__( self ):
         # Initialize chat history
        if "chat_history" not in st.session_state:
            st.session_state['chat_history'] = []

        self.llm = ChatOpenAI(model="gpt-4o") 
        self.sys_msg = SystemMessage( content = self.getSystePrompt() )
        self.search = DuckDuckGoSearchRun()
        self.builder = StateGraph(GraphState)

        self.setTools()
        self.buildGraph()


    # Cache legen geheugen wissen ========================
    def reset(self):
        del st.session_state['chat_history'] 


    # Tools ==============================================
    def search(self, query: str) -> str:
        """Search the internet for query.

        Args:
            query: search query
        """
        return self.search.invoke(query)

    def multiply(self, a: int, b: int) -> int:
        """Multiply a and b.

        Args:
            a: first int
            b: second int
        """
        return a * b

    def add(self, a: int, b: int) -> int:
        """Adds a and b.

        Args:
            a: first int
            b: second int
        """
        return a + b

    def subtract(self, a: int, b: int) -> int:
        """Subtract b from a.

        Args:
            a: first int
            b: second int
        """
        return a - b
    
    def divide(self, a: int, b: int) -> float:
        """Divide a and b.

        Args:
            a: first int
            b: second int
        """
        return a / b   


    # Tools aan llm koppelen =============================
    def setTools(self):
        self.tools = [self.add, self.multiply, self.divide, self.subtract, self.search]
        self.llmWithTools = self.llm.bind_tools(self.tools)


    # Maak Nodes =========================================
    def reasoner(self, state: MessagesState):
        return {"messages": [self.llmWithTools.invoke([self.sys_msg] + state["messages"])]}


    # Maak de graph ======================================  
    def buildGraph(self):
        # Add nodes
        self.builder.add_node("reasoner", self.reasoner)
        self.builder.add_node("tools", ToolNode(self.tools)) # for the tools

        # Add edges
        self.builder.add_edge(START, "reasoner")
        self.builder.add_conditional_edges(
            "reasoner",
            # If the latest message (result) from node reasoner is a tool call -> tools_condition routes to tools
            # If the latest message (result) from node reasoner is a not a tool call -> tools_condition routes to END
            tools_condition,
        )
        self.builder.add_edge("tools", "reasoner")
        self.react_graph = self.builder.compile()


    # Run de module ======================================= 
    def run(self, user_query):
        if len(st.session_state['chat_history']) > 0:
            user_query = self.summarizeHistory(user_query)

        # Zorg dat het bericht correct wordt ingepakt
        messages = MessagesState(messages=[HumanMessage(content=user_query)])
        response = self.react_graph.invoke(messages)

        # Print the messages xxxxxxxxx
        for m in response['messages']:
            m.pretty_print()

        # Bericht terug naar de view
        last_message = response['messages'][-1] 
        last_content = last_message.content
        return last_content
    

    # WORKERS =============================================
    def summarizeHistory(self, user_query):
        summclient = OpenAI()
        summmodel = "gpt-4o-mini"
        summtemp = 0.4
        messages1 = []
        messages1.insert(0, {"role": "system", "content": self.getSummerizePrompt()})

        recent_history = st.session_state['chat_history'][-2:]
        for message in recent_history:
            if isinstance(message, AIMessage):
                messages1.append({"role": "assistant", "content": message.content})
            elif isinstance(message, HumanMessage):
                messages1.append({"role": "user", "content": message.content})
        messages1.append({"role": "user", "content": user_query})
        completion = summclient.chat.completions.create(
        model = summmodel,
            temperature = summtemp,
            messages = messages1,
        )
        return completion.choices[0].message.content


    # DATA ===============================================
    def getSystePrompt(self):
        prompt = """
        You are a helpful assistant tasked with using search and performing arithmetic on a set of inputs. 
Always answer in Dutch.
        """
        return prompt


    def getSummerizePrompt(self):
        prompt = """
        If the new question is a follow-up question, 
make a summary of the first question and the answer as a string and add the new question to it so that it becomes a logical whole. 
If the question is not a follow-up question, only return the last question. 
The result should be a Dutch sentence.
        """
        return prompt





