"""
Compatibilité : réexporte les helpers FAISS + Chroma depuis les modules dédiés.

Historique : ce fichier monolithique importait Chroma au niveau module, ce qui
crashait l'import dès que chromadb n'était pas installé (atelier/02 = FAISS only).
Solution : un module par backend.
  - vectorstore_faiss.py  → FAISS + embeddings (atelier/02+)
  - vectorstore_chroma.py → ChromaDB (atelier/03+)
"""

from homebutler.rag.vectorstore_faiss import (
    EMBEDDING_MODEL,
    get_embeddings,
    build_faiss_index,
    load_faiss_index,
)
from homebutler.rag.vectorstore_chroma import (
    build_chroma_db,
    load_chroma_db,
)

__all__ = [
    "EMBEDDING_MODEL",
    "get_embeddings",
    "build_faiss_index",
    "load_faiss_index",
    "build_chroma_db",
    "load_chroma_db",
]
