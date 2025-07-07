#!/usr/bin/env python3
"""
Example usage of Smriti Memory Library
This script demonstrates how to use the smriti memory system in a practical scenario.
"""

import os
import sys

# Add the current directory to Python path to import smriti
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from smriti import MemoryManager, MemoryConfig
    print("✅ Smriti Memory Library imported successfully!")
except ImportError as e:
    print(f"❌ Failed to import smriti: {e}")
    print("Please install the library first: pip install -e .")
    sys.exit(1)


def simple_chatbot_example():
    """Example of a simple chatbot with memory."""
    print("\n🤖 Simple Chatbot with Memory Example")
    print("=" * 50)
    
    # Initialize memory manager
    memory_manager = MemoryManager()
    
    # Simulate a conversation
    conversations = [
        ("user_123", "Hi, I'm John. I like pizza and reading sci-fi books."),
        ("user_123", "What do I like?"),
        ("user_123", "I also work as a software engineer at Google."),
        ("user_123", "Tell me about myself."),
        ("user_123", "I have a meeting tomorrow at 2 PM."),
        ("user_123", "When is my meeting?"),
        ("user_123", "Actually, my meeting is at 3 PM, not 2 PM."),
        ("user_123", "What time is my meeting?"),
    ]
    
    print("Starting conversation...")
    
    for user_id, message in conversations:
        print(f"\n👤 User: {message}")
        
        # Get response with memory context
        result = memory_manager.chat_with_memory(user_id, message)
        
        if result.get("success"):
            response = result.get("response", "")
            print(f"🤖 AI: {response}")
            
            # Show memory context if used
            memory_context = result.get("memory_context", {})
            context_count = len(memory_context.get("results", []))
            if context_count > 0:
                print(f"📚 (Used {context_count} memories for context)")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
    
    print("\n✅ Conversation completed!")


def memory_search_example():
    """Example of searching through memories."""
    print("\n🔍 Memory Search Example")
    print("=" * 50)
    
    memory_manager = MemoryManager()
    user_id = "user_456"
    
    # Add some sample memories
    sample_memories = [
        [{"user": "I love Italian food, especially pasta and pizza"}],
        [{"user": "I work as a data scientist at Microsoft"}],
        [{"user": "I have a dog named Max who is a golden retriever"}],
        [{"user": "I enjoy hiking in the mountains on weekends"}],
        [{"user": "My favorite programming language is Python"}],
        [{"user": "I live in Seattle, Washington"}],
    ]
    
    print("Adding sample memories...")
    for memory in sample_memories:
        result = memory_manager.add_memory(user_id, memory)
        if result.get("success"):
            print(f"✅ Added: {memory[0]['user']}")
    
    # Search for different types of information
    search_queries = [
        "food preferences",
        "work and career",
        "pets and animals",
        "hobbies and activities",
        "programming and technology",
        "location and residence"
    ]
    
    print("\nSearching memories...")
    for query in search_queries:
        print(f"\n🔍 Searching for: '{query}'")
        result = memory_manager.search_memories(user_id, query)
        
        if result.get("success"):
            results = result.get("results", [])
            if results:
                print(f"Found {len(results)} relevant memories:")
                for i, memory in enumerate(results[:3], 1):  # Show top 3
                    print(f"  {i}. {memory.get('text', 'N/A')}")
            else:
                print("No relevant memories found.")
        else:
            print(f"❌ Search failed: {result.get('error', 'Unknown error')}")
    
    print("\n✅ Memory search completed!")


def memory_update_example():
    """Example of memory updates and corrections."""
    print("\n🔄 Memory Update Example")
    print("=" * 50)
    
    memory_manager = MemoryManager()
    user_id = "user_789"
    
    # Initial information
    print("Adding initial information...")
    initial_memories = [
        [{"user": "My name is Alice"}],
        [{"user": "I have a meeting on Monday at 10 AM"}],
        [{"user": "I live in New York"}],
        [{"user": "My phone number is 555-1234"}],
    ]
    
    for memory in initial_memories:
        memory_manager.add_memory(user_id, memory)
    
    # Search to see initial state
    print("\nInitial memories:")
    result = memory_manager.search_memories(user_id, "meeting phone name location")
    if result.get("success"):
        for memory in result.get("results", []):
            print(f"  - {memory.get('text', 'N/A')}")
    
    # Update information
    print("\nUpdating information...")
    updates = [
        [{"user": "Actually, my name is Alice Johnson"}],
        [{"user": "My meeting is on Monday at 2 PM, not 10 AM"}],
        [{"user": "I moved to Boston, not New York"}],
        [{"user": "My new phone number is 555-5678"}],
    ]
    
    for update in updates:
        result = memory_manager.add_memory(user_id, update)
        if result.get("success"):
            print(f"✅ Updated: {update[0]['user']}")
    
    # Search again to see updated state
    print("\nUpdated memories:")
    result = memory_manager.search_memories(user_id, "meeting phone name location")
    if result.get("success"):
        for memory in result.get("results", []):
            print(f"  - {memory.get('text', 'N/A')}")
    
    print("\n✅ Memory updates completed!")


def user_statistics_example():
    """Example of getting user statistics."""
    print("\n📊 User Statistics Example")
    print("=" * 50)
    
    memory_manager = MemoryManager()
    user_id = "user_stats"
    
    # Add some memories to get statistics
    memories = [
        [{"user": "I like coffee"}],
        [{"user": "I work from home"}],
        [{"user": "I have two cats"}],
    ]
    
    for memory in memories:
        memory_manager.add_memory(user_id, memory)
    
    # Get user statistics
    print("Getting user statistics...")
    stats = memory_manager.get_user_stats(user_id)
    
    if stats.get("success"):
        if stats.get("exists"):
            stats_data = stats.get("stats", {})
            total_vectors = stats_data.get("total_vector_count", "N/A")
            namespaces = list(stats_data.get("namespaces", {}).keys())
            
            print(f"📊 User: {user_id}")
            print(f"   Total memories: {total_vectors}")
            print(f"   Namespaces: {namespaces}")
        else:
            print(f"ℹ️  User {user_id} has no memories yet.")
    else:
        print(f"❌ Failed to get stats: {stats.get('error', 'Unknown error')}")
    
    print("\n✅ Statistics retrieved!")


def main():
    """Run all examples."""
    print("🚀 Smriti Memory Library Examples")
    print("=" * 60)
    
    # Check if API keys are set
    required_keys = ["PINECONE_API_KEY", "GROQ_API_KEY", "GEMINI_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        print("⚠️  Warning: Missing API keys!")
        print("Set these environment variables to run the examples:")
        for key in missing_keys:
            print(f"  export {key}='your-api-key'")
        print("\nSome examples may fail without proper API keys.")
        print("Continuing with examples anyway...\n")
    
    try:
        # Run examples
        simple_chatbot_example()
        memory_search_example()
        memory_update_example()
        user_statistics_example()
        
        print("\n🎉 All examples completed successfully!")
        print("\n💡 Tips:")
        print("  - Use the CLI: smriti --help")
        print("  - Check the README for more advanced usage")
        print("  - Set up proper API keys for production use")
        
    except Exception as e:
        print(f"\n❌ Example failed: {e}")
        print("This might be due to missing API keys or network issues.")


if __name__ == "__main__":
    main() 