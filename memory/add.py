import json
import uuid
from model.chat_completion import ask_groq
from memory.rag_op.rag import create_index, add_text_to_index, search_index, delete_memory




def add_memory(user_id, chat_thread):
    """
    Adds a memory based on chat_thread.
    
    Args:
        chat_thred (list): The chat thread to which the memory will be added.
        
    Returns:
        list: The updated chat thread with the new memory added.
    """

    # index creation
    create_index(user_id)
    user_text = chat_thread[0].get("user")
    searched_result = search_index(user_id,user_text)
    print(searched_result)
    if searched_result.get("error"):
        searched_result = "No memory exist till now for this user."
    



    system_prompt = f"""You are a human brain's thinking process. Your job is to decide what is important to remember from a conversation.

                    You will be given the current `chat_thread` and a `searched_result` of existing memories. Your goal is to create a concise memory point.

                    Crucially, you must decide if the new information is an **UPDATE** to an existing memory or if it is completely **NEW** information.

                    ---
                    **Rules for Deciding:**

                    1.  **UPDATE:** If the new information directly corrects, modifies, or makes an existing memory from `searched_result` obsolete (e.g., changing a name, rescheduling a meeting, updating a preference), you MUST identify it as an update and provide the `id` of the memory to be updated.

                    2.  **NEW:** If the information is on a new topic not present in the `searched_result`, it is new information.

                    3.  **IGNORE:** Ignore casual conversation, greetings, or information that is already perfectly stored in the memory. If the `searched_result` already says "User has a meeting on Saturday" and the chat says the same, there is nothing to do.

                    ---
                    **Examples of How to Behave:**

                    **Example 1: Updating a Fact**
                    * `chat_thread`: [{{"user": "oh sorry, my meeting is actually on saturday"}}]
                    * `searched_result`: {{ "results": [{{ "id": "uuid-123", "text": "User has a meeting on Friday."}}] }}
                    * **Your Correct Output:**
                        {{
                            "memory": true,
                            "type_of_memory": "facts",
                            "memory_data": [
                                {{
                                    "user_id": "{user_id}",
                                    "text": "User's meeting is on Saturday.",
                                    "update_id": "uuid-123"
                                }}
                            ]
                        }}

                    **Example 2: Adding a New Fact**
                    * `chat_thread`: [{{"user": "i like to read sci-fi books"}}]
                    * `searched_result`: {{ "results": [{{ "id": "uuid-456", "text": "User's meeting is on Saturday."}}] }}
                    * **Your Correct Output:**
                        {{
                            "memory": true,
                            "type_of_memory": "user_understanding",
                            "memory_data": [
                                {{
                                    "user_id": "{user_id}",
                                    "text": "User enjoys reading science fiction books.",
                                    "update_id": null
                                }}
                            ]
                        }}

                    **Example 3: Ignoring a Duplicate**
                    * `chat_thread`: [{{"user": "yes my name is aman"}}]
                    * `searched_result`: {{ "results": [{{ "id": "uuid-789", "text": "User introduced himself as Aman."}}] }}
                    * **Your Correct Output:**
                        {{
                            "memory": false
                        }}

                    ---
                    **Output format:**

                    * If you decide an update or a new memory is needed, return:
                        `{{ "memory": true, "type_of_memory": "...", "memory_data": [{{ "user_id": "...", "text": "...", "update_id": "..." }}] }}`
                    * If you decide nothing needs to be remembered, return:
                        `{{ "memory": false }}`

                    **Strict Guidelines:**
                    1. No markdown. 2. Response must be valid JSON starting with `{{` and ending with `}}`. 3. The `update_id` MUST be a string from the `searched_result` if it's an update, otherwise it MUST be `null`.

                    ---
                    **Here is the data, please make your decision:**
                    `chat_thread`: {chat_thread}
                    `searched_result`: {searched_result}
                    `user_id`: {user_id}
                    """

    response = ask_groq(system_prompt)

    response = json.loads(response)
    print(response)

    if response["memory"] is False:
        return {"memory": []}

    if response.get("memory") is True:
        memory_data = response.get("memory_data", [])
        if not memory_data:
            return {"memory": []}

        namespace = response.get("type_of_memory")

        formatted_data = []
        for item in memory_data:
            # Check if this is an update
            update_id = item.get("update_id")
            record_id = update_id if update_id else str(uuid.uuid4())

            formatted_data.append({
                "_id": record_id,
                "chunk_text": item["text"],
                "category": namespace
            })

        # Upsert to Pinecone
        added_data = add_text_to_index(user_id, formatted_data, namespace)
        return response

    return {"error": "something went wrong while adding memory."}
