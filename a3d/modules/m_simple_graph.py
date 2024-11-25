import streamlit as st
from openai import OpenAI
from langchain_core.messages import AIMessage, HumanMessage


class SimpleGraphModule:
    def __init__( self ):
        self.client = OpenAI()
        self.model = "gpt-4o-mini"
        self.temp = 0.7
        self.max_history = 10
        # Initialize chat history
        if "chat_history" not in st.session_state:
            st.session_state['chat_history'] = []


    def runModule(self, user_input):
        completion = self.client.chat.completions.create(
        model = self.model,
            temperature = self.temp,
            messages=self.getChatMessages( user_input ),
        )
        return completion.choices[0].message.content
    
    # WORKERS ==================================

    def getChatMessages(self, user_input):
        messages = []
        messages.insert(0, {"role": "system", "content": self.getSysteemPrompt()})

        if len(st.session_state['chat_history']) > 0:
            recent_history = st.session_state['chat_history'][-self.max_history:]
            for message in recent_history:
                if isinstance(message, AIMessage):
                    messages.append({"role": "assistant", "content": message.content})
                elif isinstance(message, HumanMessage):
                    messages.append({"role": "user", "content": message.content})

        messages.append({"role": "user", "content": user_input})
        return messages

    # DATA =====================================

    def getSysteemPrompt( self ):
        prompt = """Je bent een echte grappenmaker en maakt overal een grapje van.
        """
        return prompt


