"""
Pipeline d'ingestion des documents PDF.
Expose 3 stratégies de chunking pour la comparaison pédagogique :
  1. chunk_fixed_size  — taille fixe (512 tokens)
  2. chunk_recursive   — récursif par séparateurs (§, \n, .)
  3. chunk_semantic    — rupture sur similarité sémantique (langchain_experimental)
"""

import os
import fitz  # pymupdf — s'installe `pip install pymupdf` mais s'importe `import fitz`
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from homebutler import config


# ── Chargement PDF ────────────────────────────────────────────────────────────

def load_pdf(path: str) -> str:
    """Extrait le texte brut d'un PDF (toutes pages)."""
    doc = fitz.open(path)
    pages = []
    for page in doc:
        pages.append(page.get_text())
    doc.close()
    return "\n".join(pages)


def load_pdf_with_metadata(path: str) -> list[Document]:
    """Extrait le texte page par page avec métadonnées (source, page)."""
    doc = fitz.open(path)
    documents = []
    filename = os.path.basename(path)
    for i, page in enumerate(doc):
        text = page.get_text().strip()
        if text:
            documents.append(
                Document(
                    page_content=text,
                    metadata={"source": filename, "page": i + 1, "total_pages": len(doc)},
                )
            )
    doc.close()
    return documents


# ── Stratégies de chunking ────────────────────────────────────────────────────

def chunk_fixed_size(
    documents: list[Document],
    chunk_size: int = 512,
    chunk_overlap: int = 50,
) -> list[Document]:
    """
    Stratégie 1 — Taille fixe.
    Simple et rapide, mais peut couper au milieu d'une phrase ou d'un concept.
    Bon pour les documents uniformes (logs, tableaux).
    """
    splitter = CharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separator="\n",
        length_function=len,
    )
    return splitter.split_documents(documents)


def chunk_recursive(
    documents: list[Document],
    chunk_size: int = 512,
    chunk_overlap: int = 50,
) -> list[Document]:
    """
    Stratégie 2 — Récursif par séparateurs (recommandée pour la plupart des docs).
    Essaie de couper sur \n\n, puis \n, puis ., puis espace.
    Préserve mieux la cohérence sémantique des paragraphes.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", "!", "?", " ", ""],
        length_function=len,
    )
    return splitter.split_documents(documents)


def chunk_semantic(
    documents: list[Document],
    embeddings=None,
    breakpoint_threshold_type: str = "percentile",
) -> list[Document]:
    """
    Stratégie 3 — Sémantique (rupture sur similarité cosinus).
    Nécessite le modèle d'embeddings chargé.
    Plus lent mais produit des chunks thématiquement cohérents.
    Utilise langchain_experimental.SemanticChunker.
    """
    from langchain_experimental.text_splitter import SemanticChunker

    if embeddings is None:
        from homebutler.rag.vectorstore import get_embeddings
        embeddings = get_embeddings()

    splitter = SemanticChunker(
        embeddings,
        breakpoint_threshold_type=breakpoint_threshold_type,
    )
    texts = [d.page_content for d in documents]
    metadatas = [d.metadata for d in documents]
    return splitter.create_documents(texts, metadatas=metadatas)


# ── Pipeline d'ingestion complète ────────────────────────────────────────────

def ingest_all_documents(
    docs_dir: str | None = None,
    strategy: str = "recursive",
    chunk_size: int = 512,
    chunk_overlap: int = 50,
) -> list[Document]:
    """
    Charge tous les PDFs du dossier et les chunke.
    strategy : "fixed" | "recursive" | "semantic"
    """
    docs_dir = docs_dir or config.DOCUMENTS_DIR

    if not os.path.exists(docs_dir):
        raise FileNotFoundError(
            f"Dossier documents introuvable : {docs_dir}\n"
            "Lancez d'abord : python scripts/generate_documents.py"
        )

    all_documents: list[Document] = []
    pdf_files = [f for f in os.listdir(docs_dir) if f.endswith(".pdf")]

    if not pdf_files:
        raise ValueError(f"Aucun PDF trouvé dans {docs_dir}")

    for filename in sorted(pdf_files):
        path = os.path.join(docs_dir, filename)
        pages = load_pdf_with_metadata(path)
        all_documents.extend(pages)

    print(f"  {len(pdf_files)} PDFs chargés → {len(all_documents)} pages")

    if strategy == "fixed":
        chunks = chunk_fixed_size(all_documents, chunk_size, chunk_overlap)
    elif strategy == "semantic":
        chunks = chunk_semantic(all_documents)
    else:  # recursive (défaut)
        chunks = chunk_recursive(all_documents, chunk_size, chunk_overlap)

    print(f"  Stratégie '{strategy}' → {len(chunks)} chunks")
    return chunks
