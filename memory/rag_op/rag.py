# Import the Pinecone library
import os
import re
from pinecone import Pinecone
from dotenv import load_dotenv
load_dotenv()
# Initialize a Pinecone client with your API key
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

#namespace : here we can distinguish  type of memory

def sanitize_index_name(name: str) -> str:
    # Convert to lowercase
    name = name.lower()
    # Replace all non-alphanumeric characters with dashes
    name = re.sub(r'[^a-z0-9\-]', '-', name)
    # Optional: truncate to 45 characters if necessary
    return name[:45]

def create_index(user_id: str):
    index_name = sanitize_index_name(user_id)
    if not pc.has_index(index_name):
        pc.create_index_for_model(
            name=index_name,
            cloud="aws",
            region="us-east-1",
            embed={
                "model":"llama-text-embed-v2",
                "field_map":{"text": "chunk_text"}
            }
        )

def add_text_to_index(user_id: str, thread: list, namespace: str ):
    user_id = sanitize_index_name(user_id)
    dense_index = pc.Index(user_id)
    dense_index.upsert_records(namespace, thread)


def search_index(user_id: str, query: str ,top_k: int = 10):
    user_id = sanitize_index_name(user_id)
    query = query.strip()
    dense_index = pc.Index(user_id)

    if not pc.has_index(user_id):
        return {"error": "No memory exist."}

    # Search the dense index
    results = dense_index.search(
        namespace="user_understanding",
        query={
            "top_k": top_k,
            "inputs": {
                'text': query
            }
        }
    )

    # Convert results to JSON format
    formatted_results = []
    for hit in results['result']['hits']:
        formatted_results.append({
            "id": hit['_id'],
            "score": round(hit['_score'], 2),
            "category": hit['fields'].get('category', ''),
            "text": hit['fields'].get('chunk_text', '')
        })

    return {"results": formatted_results}


def delete_memory(user_id: str):
    # Delete the index
    user_id = sanitize_index_name(user_id)
    pc.delete_index(user_id)

    if pc:
        return {"message": "Memory deleted successfully."}
    else:
        return {"error": "Failed to delete memory."}
