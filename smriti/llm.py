"""
LLM integration for Smriti Memory.
"""

import json
import logging
import time
from typing import Dict, Any, Optional, List
from langchain_groq import ChatGroq
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage
from .exceptions import LLMError, ValidationError
from .config import MemoryConfig


logger = logging.getLogger(__name__)


class LLMManager:
    """Manages LLM operations for Smriti Memory."""
    
    def __init__(self, config: MemoryConfig):
        """Initialize the LLM manager."""
        self.config = config
        self.chat_model = self._initialize_chat_model()
        self.embedding_model = self._initialize_embedding_model()
        
        if config.enable_logging:
            logging.basicConfig(level=getattr(logging, config.log_level))
    
    def _initialize_chat_model(self) -> ChatGroq:
        """Initialize the chat model."""
        try:
            return ChatGroq(
                model=self.config.llm_model,
                temperature=self.config.llm_temperature,
                groq_api_key=self.config.groq_api_key,
            )
        except Exception as e:
            raise LLMError(f"Failed to initialize chat model: {str(e)}")
    
    def _initialize_embedding_model(self) -> GoogleGenerativeAIEmbeddings:
        """Initialize the embedding model."""
        try:
            return GoogleGenerativeAIEmbeddings(
                model=self.config.embedding_model,
                google_api_key=self.config.gemini_api_key
            )
        except Exception as e:
            raise LLMError(f"Failed to initialize embedding model: {str(e)}")
    
    def _retry_with_backoff(self, func, max_retries: int = 3, base_delay: float = 1.0):
        """Retry function with exponential backoff."""
        for attempt in range(max_retries):
            try:
                return func()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                
                delay = base_delay * (2 ** attempt)
                logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay}s: {str(e)}")
                time.sleep(delay)
    
    def ask_llm(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        max_retries: int = 3
    ) -> str:
        """Send a prompt to the LLM and return the response."""
        try:
            if not prompt or not prompt.strip():
                raise ValidationError("Prompt cannot be empty")
            
            default_system = "You are a helpful AI assistant that follows instructions precisely."
            system_content = system_prompt or default_system
            
            messages = [
                SystemMessage(content=system_content),
                HumanMessage(content=prompt)
            ]
            
            def _call_llm():
                response = self.chat_model.invoke(messages)
                return response.content.strip()
            
            result = self._retry_with_backoff(_call_llm, max_retries)
            
            logger.info(f"LLM response generated successfully (length: {len(result)})")
            return result
            
        except Exception as e:
            error_msg = f"Failed to get LLM response: {str(e)}"
            logger.error(error_msg)
            raise LLMError(error_msg, {"prompt_length": len(prompt), "system_prompt": system_prompt})
    
    def decide_memory_action(
        self, 
        user_id: str, 
        chat_thread: List[Dict[str, Any]], 
        existing_memories: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Use LLM to decide what memory action to take."""
        try:
            if not chat_thread:
                raise ValidationError("Chat thread cannot be empty")
            
            # Create the decision prompt
            system_prompt = self._create_memory_decision_prompt(user_id)
            
            # Format the data for the LLM
            prompt_data = {
                "chat_thread": chat_thread,
                "searched_result": existing_memories,
                "user_id": user_id
            }
            
            # Get LLM decision
            response = self.ask_llm(
                prompt=str(prompt_data),
                system_prompt=system_prompt
            )
            
            # Parse the response
            try:
                decision = json.loads(response)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse LLM response as JSON: {response}")
                raise LLMError(f"Invalid JSON response from LLM: {str(e)}")
            
            # Validate the decision format
            self._validate_memory_decision(decision)
            
            logger.info(f"Memory decision made: {decision.get('memory', False)}")
            return decision
            
        except Exception as e:
            error_msg = f"Failed to decide memory action: {str(e)}"
            logger.error(error_msg)
            raise LLMError(error_msg, {
                "user_id": user_id,
                "chat_thread_length": len(chat_thread),
                "existing_memories_count": len(existing_memories.get("results", []))
            })
    
    def _create_memory_decision_prompt(self, user_id: str) -> str:
        """Create the system prompt for memory decision making."""
        return f"""You are a human brain's thinking process. Your job is to decide what is important to remember from a conversation.

You will be given the current `chat_thread` and a `searched_result` of existing memories. Your goal is to create a concise memory point.

Crucially, you must decide if the new information is an **UPDATE** to an existing memory or if it is completely **NEW** information.

---
**Rules for Deciding:**

1. **UPDATE:** If the new information directly corrects, modifies, or makes an existing memory from `searched_result` obsolete (e.g., changing a name, rescheduling a meeting, updating a preference), you MUST identify it as an update and provide the `id` of the memory to be updated.

2. **NEW:** If the information is on a new topic not present in the `searched_result`, it is new information.

3. **IGNORE:** Ignore casual conversation, greetings, or information that is already perfectly stored in the memory. If the `searched_result` already says "User has a meeting on Saturday" and the chat says the same, there is nothing to do.

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
`chat_thread`: {{chat_thread}}
`searched_result`: {{searched_result}}
`user_id`: {user_id}"""
    
    def _validate_memory_decision(self, decision: Dict[str, Any]) -> None:
        """Validate the memory decision format."""
        if not isinstance(decision, dict):
            raise ValidationError("Decision must be a dictionary")
        
        if "memory" not in decision:
            raise ValidationError("Decision must contain 'memory' field")
        
        if not isinstance(decision["memory"], bool):
            raise ValidationError("'memory' field must be a boolean")
        
        if decision["memory"]:
            if "type_of_memory" not in decision:
                raise ValidationError("Decision must contain 'type_of_memory' when memory is True")
            
            if "memory_data" not in decision:
                raise ValidationError("Decision must contain 'memory_data' when memory is True")
            
            if not isinstance(decision["memory_data"], list):
                raise ValidationError("'memory_data' must be a list")
            
            for memory_item in decision["memory_data"]:
                if not isinstance(memory_item, dict):
                    raise ValidationError("Each memory item must be a dictionary")
                
                required_fields = ["user_id", "text"]
                for field in required_fields:
                    if field not in memory_item:
                        raise ValidationError(f"Memory item missing required field: {field}")
    
    def generate_response_with_context(
        self, 
        query: str, 
        context: Dict[str, Any]
    ) -> str:
        """Generate a response using context from memory."""
        try:
            if not query or not query.strip():
                raise ValidationError("Query cannot be empty")
            
            system_prompt = """You are a helpful AI assistant. Use the provided context from your memory to give personalized and relevant responses. 
            If the context is empty or doesn't contain relevant information, respond based on your general knowledge."""
            
            prompt = f"""Context from memory: {context}

User query: {query}

Please provide a helpful response using the context when relevant."""
            
            return self.ask_llm(prompt, system_prompt)
            
        except Exception as e:
            error_msg = f"Failed to generate response with context: {str(e)}"
            logger.error(error_msg)
            raise LLMError(error_msg, {"query": query, "context_keys": list(context.keys())}) 