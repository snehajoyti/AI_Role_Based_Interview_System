import json
import faiss 
from sentence_transformers import SentenceTransformer 



MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)

def load_vector_store(index_path: str, metadata_path: str):
    index = faiss.read_index(index_path)

    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    return index, metadata


def retrieve_relevant_chunks(
    query: str,
    index_path: str,
    metadata_path: str,
    top_k: int = 5
): 
    # Load FAISS index and metadata
    index, metadata = load_vector_store(
        index_path,
        metadata_path 
    )

    # Convert query into embedding
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True 
    )

    # Search similar chunks 
    distances, indices = index.search(
        query_embedding,
        top_k 
    )

    results = []

    for distance, idx in zip(distances[0], indices[0]):
        if idx == -1:
            continue

        results.append({
            "text": metadata[idx]["text"],
            "page_number": metadata[idx]["page_number"],
            "distance": float(distance)
        })
    return results 
