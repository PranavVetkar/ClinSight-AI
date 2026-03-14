from typing import List, Optional
import chromadb
from sentence_transformers import SentenceTransformer

from config import settings

# ── Model (loaded once at module import) ─────────────────────────────────────
_model: Optional[SentenceTransformer] = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        # MiniLM is lightning fast locally, avoiding Gemini API rate limits!
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


# ── ChromaDB client ───────────────────────────────────────────────────────────
_chroma_client: Optional[chromadb.PersistentClient] = None


def _get_chroma() -> chromadb.PersistentClient:
    global _chroma_client
    if _chroma_client is None:
        _chroma_client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
    return _chroma_client


def _collection_name(user_id: str) -> str:
    return f"user_{user_id.replace('-', '_')}"


# ── Public API ────────────────────────────────────────────────────────────────

def add_document_chunks(user_id: str, doc_id: str, chunks: List[str]) -> int:
    """Embed and store chunks for a document. Returns the number of chunks stored."""
    model = get_model()
    client = _get_chroma()
    collection = client.get_or_create_collection(name=_collection_name(user_id))

    embeddings = model.encode(chunks).tolist()
    ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"doc_id": doc_id, "chunk_index": i} for i in range(len(chunks))]

    collection.add(documents=chunks, embeddings=embeddings, ids=ids, metadatas=metadatas)
    return len(chunks)


def query_chunks(user_id: str, doc_id: str, query: str, top_k: int = 5) -> List[str]:
    """Return the top-k most relevant chunks for the query from a specific document."""
    model = get_model()
    client = _get_chroma()
    collection = client.get_or_create_collection(name=_collection_name(user_id))

    query_embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        where={"doc_id": doc_id},
    )
    return results["documents"][0] if results["documents"] else []


def delete_document_chunks(user_id: str, doc_id: str) -> None:
    """Remove all chunks for a given document from the vector store."""
    client = _get_chroma()
    collection = client.get_or_create_collection(name=_collection_name(user_id))
    # Get all IDs for this doc and delete them
    results = collection.get(where={"doc_id": doc_id})
    if results["ids"]:
        collection.delete(ids=results["ids"])
