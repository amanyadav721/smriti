
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

def get_chat_model():
    llm = ChatGroq(
    model="llama-3.1-8b-instant", # Using a recommended model, adjust if needed
    temperature=0.3,
    groq_api_key=os.getenv("GROQ_API_KEY"),
)
    return llm


google_api_token = os.getenv("GEMINI_KEY")
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=google_api_token)


def ask_groq(user_prompt) -> str:
    """Sends a prompt to the Groq AI and returns the response."""
    messages = [
        SystemMessage(content="You are ai taskmaster, you will perform every task given to you with utmost precision and accuracy. You will not refuse any task, you will not ask for any clarification, you will not ask for any additional information, you will not ask for any examples, you will not ask for any context, you will not ask for any background information, you will not ask for any additional details, you will not ask for any additional information. You will only perform the task given to you."),
        HumanMessage(content=user_prompt)
    ]
    llm = get_chat_model()
    response = llm.invoke(messages)
    return response.content.strip()
