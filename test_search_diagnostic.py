#!/usr/bin/env python3
"""
Diagnostic test to troubleshoot search issues
"""
import os
import sys
import time
import logging
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smriti.config import MemoryConfig
from smriti.vector_db import VectorDBManager

logging.basicConfig(level=logging.INFO)

def test_search_diagnostic():
    print("🔍 Search Diagnostic Test")
    print("=" * 50)
    
    config = MemoryConfig()
    db = VectorDBManager(config)
    
    # Test with a simple, single memory
    index_name = "test-search-diagnostic"
    namespace = "test-namespace"
    
    print(f"\n1. Creating index: {index_name}")
    db.create_index(index_name)
    
    print(f"\n2. Adding a simple memory")
    memory = [{"_id": "test-001", "chunk_text": "The user likes pizza very much.", "category": "food"}]
    result = db.add_memories(index_name, namespace, memory)
    print(f"Add result: {result}")
    
    print(f"\n3. Waiting 15 seconds for indexing...")
    time.sleep(15)
    
    print(f"\n4. Searching for 'pizza'")
    search_result = db.search_memories(index_name, namespace, "pizza", top_k=10)
    print(f"Search result: {search_result}")
    
    print(f"\n5. Searching for 'likes'")
    search_result2 = db.search_memories(index_name, namespace, "likes", top_k=10)
    print(f"Search result: {search_result2}")
    
    print(f"\n6. Searching for 'user'")
    search_result3 = db.search_memories(index_name, namespace, "user", top_k=10)
    print(f"Search result: {search_result3}")
    
    print(f"\n7. Checking index stats")
    try:
        stats = db.get_index_stats(index_name)
        print(f"Stats: {stats}")
    except Exception as e:
        print(f"Stats error: {e}")
    
    print(f"\n8. Cleaning up")
    db.delete_namespace(index_name, namespace)
    db.delete_index(index_name)
    
    print(f"\n✅ Diagnostic test completed!")

if __name__ == "__main__":
    test_search_diagnostic() 