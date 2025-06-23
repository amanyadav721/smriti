from model.chat_completion import ask_groq
from memory.rag_op.rag import search_index
from memory.add import add_memory


def chat_bot(user_id: str, query) -> str:
    """
    Processes a chat thread and returns a response from the AI model.

    Args:
        user_id (str): The ID of the user.
        chat_thread (list): The chat thread to process.

    Returns:
        str: The AI's response to the chat thread.
    """
    # Convert the chat thread to a string format
    
    searched_result = search_index(user_id, query)
    print(searched_result)
    if searched_result.get("error"):
        searched_result = "No memory exist till now for this user."
    

    # Prepare the prompt for the AI model
    prompt = f"You are helpful ai assistnat, you will help user with their queries. for better understanding of user, you will use the following information from your memory: {searched_result}. Now answer the user query: {query}"

   
    # Get the AI's response
    response = ask_groq(prompt)
    chat_thread = [{"user": query, "ai": response}]

    add_memory(user_id,chat_thread)

    return response