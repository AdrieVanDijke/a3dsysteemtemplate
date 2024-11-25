import streamlit as st
from openai import OpenAI
from langchain_core.messages import AIMessage, HumanMessage


class BasisChatModule:
    def __init__( self ):
        self.client = OpenAI()
        self.model = "gpt-4o"
        self.temp = 0.4
        self.max_history = 10
        # Initialize chat history
        if "chat_history" not in st.session_state:
            st.session_state['chat_history'] = []
        # Initialize system prompt    
        if 'system_prompt' not in st.session_state:
            st.session_state['systemprompt'] = self.getSysteemPrompt()


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
        messages.insert(0, {"role": "system", "content": st.session_state['systemprompt']})

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
        prompt = """Je bent een behulpzame mentale coach. Je taak is om de gebruiker zo goed mogelijk advies te geven. 
Vraag door aan de gebruiker om dieper tot de kern door te dringen.
        """
        return prompt


