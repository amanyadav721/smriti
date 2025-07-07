# Smriti Memory

An intelligent memory layer for AI applications with RAG (Retrieval-Augmented Generation) capabilities. Smriti Memory provides sophisticated memory management that can store, retrieve, and update contextual information using vector databases and LLM-powered decision making.

## 🚀 Prerequisites

Before using Smriti Memory, you'll need to obtain API keys from the following services:

### Required API Keys

1. **Pinecone API Key** - For vector database storage
2. **Groq API Key** - For LLM operations (memory decisions and chat)
3. **Gemini API Key** - For additional LLM capabilities

### Quick Setup

1. **Set Environment Variables** (recommended):
```bash
export PINECONE_API_KEY="your-pinecone-api-key"
export GROQ_API_KEY="your-groq-api-key"
export GEMINI_KEY="your-gemini-api-key"
```

2. **Or Pass Keys Directly**:
```python
from smriti import MemoryConfig, MemoryManager

config = MemoryConfig(
    pinecone_api_key="your-pinecone-key",
    groq_api_key="your-groq-key", 
    gemini_api_key="your-gemini-key"
)
memory_manager = MemoryManager(config)
```

📖 **Need help getting your API keys?** Check out our detailed [Setup Guide](SETUP_GUIDE.md) with step-by-step instructions!

## Features

- 🧠 **Intelligent Memory Management**: Uses LLM to decide what information to store, update, or ignore
- 🔍 **Semantic Search**: Find relevant memories using vector similarity search
- 🔄 **Memory Updates**: Automatically detect and update existing memories with new information
- 📊 **Memory Statistics**: Track and analyze memory usage patterns
- 🚀 **Easy Integration**: Simple API for adding to any AI application
- 🛠️ **CLI Interface**: Command-line tools for memory operations
- ⚙️ **Configurable**: Flexible configuration for different use cases

## Installation

```bash
pip install smriti-memory
```

### Development Installation

```bash
git clone https://github.com/amanyadav721/smriti.git
cd smriti-memory
pip install -e .
```

## Quick Start

### Basic Usage

```python
from smriti import MemoryManager, MemoryConfig

# Initialize with default configuration
memory_manager = MemoryManager()

# Add memory from a chat interaction
chat_thread = [
    {"user": "I like pizza and reading sci-fi books", "ai": "That's great! What's your favorite sci-fi book?"}
]

result = memory_manager.add_memory("user123", chat_thread)
print(result)
# Output: {'success': True, 'memory': [...], 'action': 'added', 'count': 1}

# Search for relevant memories
search_result = memory_manager.search_memories("user123", "pizza")
print(search_result)
# Output: {'success': True, 'results': [...], 'count': 1}

# Search with custom parameters (top_k and namespace)
search_result = memory_manager.search_memories("user123", "pizza", top_k=5, namespace="user_understanding")
print(f"Found {len(search_result['results'])} results")

# Chat with memory context
chat_result = memory_manager.chat_with_memory("user123", "What do I like?")
print(chat_result["response"])
# Output: "Based on our previous conversation, you like pizza and reading sci-fi books..."
```

### CLI Usage

```bash
# Add memory
smriti add-memory user123 --chat-thread '[{"user": "I like pizza"}]'

# Search memories
smriti search user123 --query "pizza" --verbose

# Chat with memory
smriti chat user123 --query "What do I like?"

# Get user statistics
smriti stats user123

# Delete all memories
smriti delete user123
```

## Configuration

### Environment Variables

Set these environment variables for API access:

```bash
export PINECONE_API_KEY="your-pinecone-api-key"
export GROQ_API_KEY="your-groq-api-key"
export GEMINI_KEY="your-gemini-api-key"
```

### Custom Configuration

```python
from smriti import MemoryConfig, MemoryManager

config = MemoryConfig(
    pinecone_api_key="your-key",
    groq_api_key="your-key",
    gemini_api_key="your-key",
    llm_model="llama-3.1-8b-instant",
    llm_temperature=0.3,
    default_namespace="user_understanding",
    max_memory_length=1000,
    similarity_threshold=0.7,
    max_search_results=10
)

memory_manager = MemoryManager(config)
```

## API Reference

### MemoryManager

The main class for managing memories.

#### `add_memory(user_id: str, chat_thread: List[Dict[str, Any]]) -> Dict[str, Any]`

Add memory based on a chat thread.

**Parameters:**
- `user_id`: Unique identifier for the user
- `chat_thread`: List of dictionaries with "user" and/or "ai" keys

**Returns:**
```python
{
    "success": bool,
    "memory": List[Dict],
    "action": str,  # "added" or "ignored"
    "namespace": str,
    "count": int,
    "storage_result": Dict
}
```

#### `search_memories(user_id: str, query: str, namespace: Optional[str] = None, top_k: Optional[int] = None) -> Dict[str, Any]`

Search for relevant memories.

**Parameters:**
- `user_id`: User identifier
- `query`: Search query
- `namespace`: Optional namespace to search in
- `top_k`: Number of results to return

**Returns:**
```python
{
    "success": bool,
    "results": List[Dict],
    "query": str,
    "namespace": str,
    "count": int
}
```

#### `chat_with_memory(user_id: str, query: str, add_to_memory: bool = True) -> Dict[str, Any]`

Generate a chat response using memory context.

**Parameters:**
- `user_id`: User identifier
- `query`: User's query
- `add_to_memory`: Whether to add the interaction to memory

**Returns:**
```python
{
    "success": bool,
    "response": str,
    "memory_context": Dict,
    "memory_result": Dict
}
```

#### `delete_user_memories(user_id: str) -> Dict[str, Any]`

Delete all memories for a user.

#### `get_user_stats(user_id: str) -> Dict[str, Any]`

Get statistics about a user's memories.

### MemoryConfig

Configuration class for customizing behavior.

**Attributes:**
- `pinecone_api_key`: Pinecone API key
- `groq_api_key`: Groq API key
- `gemini_api_key`: Gemini API key
- `llm_model`: LLM model name
- `llm_temperature`: LLM temperature
- `default_namespace`: Default namespace for memories
- `max_memory_length`: Maximum length of memory text
- `similarity_threshold`: Similarity threshold for search
- `max_search_results`: Maximum number of search results

## Advanced Usage

### Custom Memory Types

```python
# Add memory with custom namespace
chat_thread = [{"user": "I have a meeting on Friday"}]
result = memory_manager.add_memory("user123", chat_thread)

# Search in specific namespace
search_result = memory_manager.search_memories(
    "user123", 
    "meeting", 
    namespace="facts"
)

# Search with custom top_k parameter
search_result = memory_manager.search_memories(
    "user123", 
    "pizza", 
    top_k=3  # Get only top 3 results
)

# Search with both namespace and top_k
search_result = memory_manager.search_memories(
    "user123", 
    "work", 
    namespace="professional",
    top_k=10  # Get top 10 results from professional namespace
)
```

### Batch Operations

```python
# Add multiple memories
chat_threads = [
    [{"user": "I like pizza"}],
    [{"user": "I work at Google"}],
    [{"user": "I have a dog named Max"}]
]

for thread in chat_threads:
    memory_manager.add_memory("user123", thread)
```

### Error Handling

```python
from smriti import SmritiError, MemoryError

try:
    result = memory_manager.add_memory("user123", chat_thread)
    if not result["success"]:
        print(f"Error: {result['error']}")
except SmritiError as e:
    print(f"Smriti error: {e.message}")
    print(f"Details: {e.details}")
```

## CLI Commands

### `smriti add-memory`

Add memory from a chat thread.

```bash
smriti add-memory user123 --chat-thread '[{"user": "I like pizza"}]'
```

### `smriti search`

Search for memories.

```bash
smriti search user123 --query "pizza" --namespace "user_understanding" --top-k 5
```

### `smriti chat`

Chat with memory context.

```bash
smriti chat user123 --query "What do I like?" --no-memory
```

### `smriti delete`

Delete all memories for a user.

```bash
smriti delete user123
```

### `smriti stats`

Get user memory statistics.

```bash
smriti stats user123 --verbose
```

## Examples

### Chatbot Integration

```python
from smriti import MemoryManager

class Chatbot:
    def __init__(self):
        self.memory_manager = MemoryManager()
    
    def respond(self, user_id: str, message: str) -> str:
        # Get response with memory context
        result = self.memory_manager.chat_with_memory(user_id, message)
        
        if result["success"]:
            return result["response"]
        else:
            return "I'm sorry, I encountered an error. Please try again."
    
    def add_memory(self, user_id: str, user_message: str, ai_response: str):
        chat_thread = [{"user": user_message, "ai": ai_response}]
        self.memory_manager.add_memory(user_id, chat_thread)

# Usage
chatbot = Chatbot()
response = chatbot.respond("user123", "What do I like?")
print(response)
```

### Web Application Integration

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from smriti import MemoryManager

app = FastAPI()
memory_manager = MemoryManager()

class ChatRequest(BaseModel):
    user_id: str
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    result = memory_manager.chat_with_memory(request.user_id, request.message)
    
    if result["success"]:
        return {"response": result["response"]}
    else:
        raise HTTPException(status_code=500, detail=result["error"])

@app.get("/memories/{user_id}")
async def get_memories(user_id: str, query: str):
    result = memory_manager.search_memories(user_id, query)
    return result
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development

### Setup Development Environment

```bash
git clone https://github.com/amanyadav721/smriti.git
cd smriti-memory
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black smriti/
flake8 smriti/
mypy smriti/
```

### Building Documentation

```bash
pip install -e ".[docs]"
cd docs
make html
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Pinecone](https://www.pinecone.io/) for vector storage
- Powered by [Groq](https://groq.com/) for fast LLM inference
- Uses [Google Gemini](https://ai.google.dev/) for embeddings
- Inspired by research in memory-augmented neural networks

## Support

- 📧 Email: ad721603@gmail.com
