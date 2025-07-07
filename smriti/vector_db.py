"""
Vector Database Manager for Smriti Memory.
"""

import os
import re
import logging
from typing import List, Dict, Any, Optional
from pinecone import Pinecone
from .config import MemoryConfig
from .exceptions import VectorDBError, ValidationError, SmritiError

logger = logging.getLogger(__name__)

def sanitize_index_name(name: str) -> str:
    name = name.lower()
    name = re.sub(r'[^a-z0-9\-]', '-', name)
    return name[:45]

class VectorDBManager:
    """Manages vector database operations using Pinecone."""
    
    def __init__(self, config: MemoryConfig):
        """Initialize the vector database manager."""
        self.config = config
        self.pinecone = Pinecone(api_key=config.pinecone_api_key)
    
    def create_index(self, index_name: Optional[str] = None):
        index_name = sanitize_index_name(index_name)
        if not self.pinecone.has_index(index_name):
            self.pinecone.create_index_for_model(
                name=index_name,
                cloud=self.config.pinecone_cloud,
                region=self.config.pinecone_environment,
                embed={
                    "model": "llama-text-embed-v2",
                    "field_map": {"text": "chunk_text"}
                }
            )
            logger.info(f"Created index {index_name}")
        else:
            logger.info(f"Index {index_name} already exists")
        return index_name
    
    def add_memories(self, index_name: Optional[str], namespace: Optional[str], memories: List[Dict[str, Any]]):
        index_name = sanitize_index_name(index_name)
        namespace = namespace
        self.create_index(index_name)
        index = self.pinecone.Index(index_name)
        index.upsert_records(namespace, memories)
        logger.info(f"Added {len(memories)} memories to index {index_name}, namespace {namespace}")
        return {"success": True, "count": len(memories)}
    
    def search_memories(self, index_name: Optional[str], namespace: Optional[str], query: str, top_k: int = 3):
        index_name = sanitize_index_name(index_name)
        namespace = namespace
        if not self.pinecone.has_index(index_name):
            return {"results": []}
        index = self.pinecone.Index(index_name)
        results = index.search(
            namespace=namespace,
            query={
                "top_k": top_k,
                "inputs": {"text": query}
            }
        )
        formatted_results = []
        for hit in results['result']['hits']:
            formatted_results.append({
                "id": hit['_id'],
                "score": round(hit['_score'], 2),
                "category": hit['fields'].get('category', ''),
                "text": hit['fields'].get('chunk_text', '')
            })
        logger.info(f"Found {len(formatted_results)} memories for query '{query}' in index {index_name}, namespace {namespace}")
        return {"results": formatted_results}
    
    def delete_namespace(self, index_name: Optional[str], namespace: Optional[str]):
        index_name = sanitize_index_name(index_name)
        namespace = namespace
        if not self.pinecone.has_index(index_name):
            return {"success": False, "message": "Index does not exist"}
        try:
            index = self.pinecone.Index(index_name)
            index.delete(delete_all=True, namespace=namespace)
            logger.info(f"Deleted namespace {namespace} from index {index_name}")
            return {"success": True}
        except Exception as e:
            # Handle case where namespace doesn't exist
            if "Namespace not found" in str(e) or "NotFoundException" in str(e):
                logger.info(f"Namespace {namespace} does not exist in index {index_name}")
                return {"success": True, "message": "Namespace does not exist"}
            else:
                logger.error(f"Error deleting namespace {namespace} from index {index_name}: {str(e)}")
                return {"success": False, "message": f"Error deleting namespace: {str(e)}"}
    
    def delete_index(self, index_name: Optional[str]):
        index_name = sanitize_index_name(index_name)
        if not self.pinecone.has_index(index_name):
            return {"success": False, "message": "Index does not exist"}
        self.pinecone.delete_index(index_name)
        logger.info(f"Deleted index {index_name}")
        return {"success": True}
    
    def get_index_stats(self, user_id: str) -> Dict[str, Any]:
        """Get statistics about a user's memory index."""
        try:
            index_name = sanitize_index_name(user_id)
            
            if not self.pinecone.has_index(index_name):
                return {
                    "success": True,
                    "exists": False,
                    "message": "No index exists for this user"
                }
            
            index = self.pinecone.Index(index_name)
            stats = index.describe_index_stats()
            
            return {
                "success": True,
                "exists": True,
                "stats": stats,
                "user_id": user_id,
                "index_name": index_name
            }
            
        except Exception as e:
            error_msg = f"Failed to get index stats for user {user_id}: {str(e)}"
            logger.error(error_msg)
            raise VectorDBError(error_msg, {
                "user_id": user_id,
                "operation": "get_index_stats"
            }) 