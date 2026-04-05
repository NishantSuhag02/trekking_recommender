from langchain_ollama import ChatOllama
#from langchain_ollama import OllamaLLM

class ChatBot():
    def __init__(self,db_path):
        import sqlite3
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.model = ChatOllama(
            model = "llama3.2",
            temperature=0
        )

    def chat(self,user_input):

        response = self.model.invoke(user_input)
        return response.content