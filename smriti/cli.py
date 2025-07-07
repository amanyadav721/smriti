"""
Command-line interface for Smriti Memory.
"""

import argparse
import json
import sys
from typing import Dict, Any
from .memory_manager import MemoryManager
from .config import MemoryConfig
from .exceptions import SmritiError


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Smriti Memory - Intelligent memory layer for AI applications",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add memory from a chat thread
  smriti add-memory user123 --chat-thread '[{"user": "I like pizza"}]'
  
  # Search for memories
  smriti search user123 --query "pizza"
  
  # Chat with memory context
  smriti chat user123 --query "What do I like?"
  
  # Delete all memories for a user
  smriti delete user123
  
  # Get user statistics
  smriti stats user123
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Add memory command
    add_parser = subparsers.add_parser("add-memory", help="Add memory from chat thread")
    add_parser.add_argument("user_id", help="User identifier")
    add_parser.add_argument("--chat-thread", required=True, help="JSON string of chat thread")
    add_parser.add_argument("--config", help="Path to config file (optional)")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search for memories")
    search_parser.add_argument("user_id", help="User identifier")
    search_parser.add_argument("--query", required=True, help="Search query")
    search_parser.add_argument("--namespace", help="Namespace to search in")
    search_parser.add_argument("--top-k", type=int, help="Number of results to return")
    search_parser.add_argument("--config", help="Path to config file (optional)")
    
    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Chat with memory context")
    chat_parser.add_argument("user_id", help="User identifier")
    chat_parser.add_argument("--query", required=True, help="User query")
    chat_parser.add_argument("--no-memory", action="store_true", help="Don't add to memory")
    chat_parser.add_argument("--config", help="Path to config file (optional)")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete all memories for a user")
    delete_parser.add_argument("user_id", help="User identifier")
    delete_parser.add_argument("--config", help="Path to config file (optional)")
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Get user memory statistics")
    stats_parser.add_argument("user_id", help="User identifier")
    stats_parser.add_argument("--config", help="Path to config file (optional)")
    
    # Global options
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        # Load configuration
        config = load_config(args.config)
        
        # Initialize memory manager
        memory_manager = MemoryManager(config)
        
        # Execute command
        result = execute_command(memory_manager, args)
        
        # Output result
        output_result(result, args)
        
    except SmritiError as e:
        print_error(f"Smriti Error: {e.message}", args)
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}", args)
        sys.exit(1)


def load_config(config_path: str = None) -> MemoryConfig:
    """Load configuration from file or environment."""
    if config_path:
        # TODO: Implement config file loading
        pass
    
    return MemoryConfig()


def execute_command(memory_manager: MemoryManager, args: argparse.Namespace) -> Dict[str, Any]:
    """Execute the specified command."""
    if args.command == "add-memory":
        return execute_add_memory(memory_manager, args)
    elif args.command == "search":
        return execute_search(memory_manager, args)
    elif args.command == "chat":
        return execute_chat(memory_manager, args)
    elif args.command == "delete":
        return execute_delete(memory_manager, args)
    elif args.command == "stats":
        return execute_stats(memory_manager, args)
    else:
        raise ValueError(f"Unknown command: {args.command}")


def execute_add_memory(memory_manager: MemoryManager, args: argparse.Namespace) -> Dict[str, Any]:
    """Execute add-memory command."""
    try:
        chat_thread = json.loads(args.chat_thread)
    except json.JSONDecodeError as e:
        raise SmritiError(f"Invalid JSON in chat-thread: {str(e)}")
    
    return memory_manager.add_memory(args.user_id, chat_thread)


def execute_search(memory_manager: MemoryManager, args: argparse.Namespace) -> Dict[str, Any]:
    """Execute search command."""
    return memory_manager.search_memories(
        args.user_id,
        args.query,
        namespace=args.namespace,
        top_k=args.top_k
    )


def execute_chat(memory_manager: MemoryManager, args: argparse.Namespace) -> Dict[str, Any]:
    """Execute chat command."""
    return memory_manager.chat_with_memory(
        args.user_id,
        args.query,
        add_to_memory=not args.no_memory
    )


def execute_delete(memory_manager: MemoryManager, args: argparse.Namespace) -> Dict[str, Any]:
    """Execute delete command."""
    return memory_manager.delete_user_memories(args.user_id)


def execute_stats(memory_manager: MemoryManager, args: argparse.Namespace) -> Dict[str, Any]:
    """Execute stats command."""
    return memory_manager.get_user_stats(args.user_id)


def output_result(result: Dict[str, Any], args: argparse.Namespace):
    """Output the result in the specified format."""
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_human_readable(result, args)


def print_human_readable(result: Dict[str, Any], args: argparse.Namespace):
    """Print result in human-readable format."""
    if not result.get("success", False):
        print(f"❌ Error: {result.get('error', 'Unknown error')}")
        return
    
    if args.command == "add-memory":
        action = result.get("action", "unknown")
        count = result.get("count", 0)
        if action == "ignored":
            print(f"ℹ️  Memory ignored: {result.get('reason', 'No reason provided')}")
        else:
            print(f"✅ Added {count} memory(ies) successfully")
            if args.verbose:
                print(f"Namespace: {result.get('namespace', 'N/A')}")
    
    elif args.command == "search":
        count = result.get("count", 0)
        print(f"🔍 Found {count} memory(ies)")
        if count > 0 and args.verbose:
            for i, memory in enumerate(result.get("results", []), 1):
                print(f"\n{i}. Score: {memory.get('score', 'N/A')}")
                print(f"   Category: {memory.get('category', 'N/A')}")
                print(f"   Text: {memory.get('text', 'N/A')}")
    
    elif args.command == "chat":
        response = result.get("response", "")
        print(f"🤖 AI Response: {response}")
        if args.verbose:
            context_count = len(result.get("memory_context", {}).get("results", []))
            print(f"📚 Used {context_count} memory(ies) for context")
    
    elif args.command == "delete":
        print(f"🗑️  {result.get('message', 'Memories deleted')}")
    
    elif args.command == "stats":
        if result.get("exists", False):
            stats = result.get("stats", {})
            print(f"📊 Memory statistics for user {result.get('user_id')}:")
            print(f"   Total vectors: {stats.get('total_vector_count', 'N/A')}")
            print(f"   Namespaces: {list(stats.get('namespaces', {}).keys())}")
        else:
            print(f"ℹ️  {result.get('message', 'No memories found')}")


def print_error(message: str, args: argparse.Namespace):
    """Print error message."""
    if args.json:
        error_result = {"success": False, "error": message}
        print(json.dumps(error_result, indent=2))
    else:
        print(f"❌ {message}", file=sys.stderr)


if __name__ == "__main__":
    main() 