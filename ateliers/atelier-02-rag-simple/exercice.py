"""
═══════════════════════════════════════════════════════════════════════════
Atelier 02 — RAG Simple FAISS (exercice à compléter)
═══════════════════════════════════════════════════════════════════════════

Objectif : construire un pipeline RAG complet sur les PDFs du logement.

6 TODOs :
  1. Générer les PDFs (commande shell, ou via os.system)
  2. Charger les PDFs avec load_pdf_with_metadata
  3. Chunker avec les 3 stratégies, comparer le nombre de chunks
  4. Construire l'index FAISS (build_faiss_index)
  5. Assembler la chaîne RAG avec LCEL
  6. Mesurer le Recall@5 sur 5 questions étalons

Lancer :  python ateliers/atelier-02-rag-simple/exercice.py
═══════════════════════════════════════════════════════════════════════════
"""

import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from homebutler import config
from homebutler.llm.prompts import RAG_QA_TEMPLATE

# TODO 1 — importer les fonctions nécessaires depuis homebutler
# from homebutler.llm.provider import ...
# from homebutler.rag.ingestion import (load_pdf_with_metadata, chunk_fixed_size,
#                                       chunk_recursive)
# from homebutler.rag.vectorstore_faiss import build_faiss_index


# ─── 5 questions étalons (Recall@k) ──────────────────────────────────────
BENCHMARK_QUESTIONS = [
    ("Quelle est la marque de ma chaudière ?",      "notice_chaudiere.pdf"),
    ("Code erreur F4 chaudière",                    "notice_chaudiere.pdf"),
    ("Comment purger les radiateurs ?",             "notice_chaudiere.pdf"),
    ("Quel est le filtre de la VMC à nettoyer ?",   "notice_vmc.pdf"),
    ("Quelle est la durée du bail ?",               "bail.pdf"),
]


def format_docs(docs: list) -> str:
    """Formate les documents récupérés pour le prompt."""
    return "\n\n".join(
        f"[{d.metadata.get('source')} p.{d.metadata.get('page')}]\n{d.page_content}"
        for d in docs
    )


def main() -> None:
    # ─── TODO 1 — Générer les PDFs si absents ───────────────────────────
    docs_dir = config.DOCUMENTS_DIR
    if not os.path.exists(docs_dir) or not os.listdir(docs_dir):
        print("→ Lancer d'abord : python scripts/generate_documents.py")
        # os.system("python scripts/generate_documents.py")
        return

    # ─── TODO 2 — Charger toutes les pages PDF avec métadonnées ─────────
    # pages = []
    # for f in sorted(os.listdir(docs_dir)):
    #     if f.endswith('.pdf'):
    #         pages.extend(load_pdf_with_metadata(os.path.join(docs_dir, f)))
    # print(f"Pages chargées : {len(pages)}")
    raise NotImplementedError("TODO 2 — charger les PDFs")

    # ─── TODO 3 — Chunker avec 3 stratégies (fixed, recursive) ──────────
    # chunks_fixed = chunk_fixed_size(pages, chunk_size=512, chunk_overlap=50)
    # chunks_rec   = chunk_recursive(pages, chunk_size=512, chunk_overlap=50)
    # print(f"chunks_fixed     : {len(chunks_fixed)}")
    # print(f"chunks_recursive : {len(chunks_rec)}")

    # ─── TODO 4 — Construire l'index FAISS sur les chunks récursifs ─────
    # faiss_store = build_faiss_index(chunks_rec, force_rebuild=True)

    # ─── TODO 5 — Assembler la chaîne RAG (LCEL) ────────────────────────
    # retriever = faiss_store.as_retriever(search_type="mmr",
    #                                      search_kwargs={"k": 4})
    # llm = get_llm(temperature=0.1)
    # rag_chain = (
    #     {"context": retriever | format_docs, "question": RunnablePassthrough()}
    #     | RAG_QA_TEMPLATE | llm | StrOutputParser()
    # )
    # print("\n", rag_chain.invoke("Quelle est la marque de ma chaudière ?"))

    # ─── TODO 6 — Recall@5 sur les 5 questions étalons ─────────────────
    # hits = 0
    # for q, expected in BENCHMARK_QUESTIONS:
    #     results = faiss_store.similarity_search(q, k=5)
    #     if any(r.metadata.get("source") == expected for r in results):
    #         hits += 1
    # print(f"\nRecall@5 = {hits/len(BENCHMARK_QUESTIONS):.0%}")


if __name__ == "__main__":
    main()
