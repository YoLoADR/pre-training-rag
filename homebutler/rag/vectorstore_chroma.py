"""
Vectorstore ChromaDB — FAQ dynamiques, métadonnées riches, filtres.

Concept RAG : Pourquoi un second vectorstore ?
  - FAISS  → optimisé recherche dense, immuable (rebuild = coûteux)
  - Chroma → supporte les filtres sur métadonnées (where={"source":"X"}),
             la suppression/MAJ de documents à la volée, le multi-collections.
ChromaDB sert pour les FAQ qui changent souvent, ou quand on a besoin
de filtrer par source/page/date avant la recherche sémantique.
"""

import os
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from homebutler import config
from homebutler.rag.vectorstore_faiss import get_embeddings


def build_chroma_db(
    documents: list[Document],
    collection: str = "homebutler_docs",
    persist_dir: str | None = None,
) -> Chroma:
    """
    Crée ou met à jour une collection ChromaDB persistante.
    ChromaDB >= 0.4.x : utiliser PersistentClient (géré par le wrapper LangChain).
    """
    persist_dir = persist_dir or config.CHROMA_PATH
    print(f"  Construction ChromaDB ({len(documents)} chunks) → {persist_dir}")
    embeddings = get_embeddings()
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name=collection,
        persist_directory=persist_dir,
    )
    print(f"  ✓ ChromaDB sauvegardé dans {persist_dir}")
    return vectorstore


def load_chroma_db(
    collection: str = "homebutler_docs",
    persist_dir: str | None = None,
) -> Chroma:
    """Charge une collection ChromaDB existante."""
    persist_dir = persist_dir or config.CHROMA_PATH
    embeddings = get_embeddings()
    return Chroma(
        collection_name=collection,
        embedding_function=embeddings,
        persist_directory=persist_dir,
    )
