# Insights — Ateliers avancés AT07 / AT08 / AT09

> Mis à jour au fil de l'eau. Findings techniques, pièges, décisions.

## Architecture repos (confirmé)
- Code + ateliers vivent dans `training-rag` (repo élève). Branches `atelier/0X` (corrigé) et `student/0X` (blanké).
- Branche courante au départ : `student/04-finetuning`. Untracked : `ateliers/atelier-02-rag-simple.zip`, `scripts.zip` → NE PAS committer.
- Remotes : `github` (YoLoADR/training-rag) + `origin`. Branches 01-06 déjà push sur les deux = backup existant.
- `solution/at01-03` existent seulement sur `origin` (pas github). Décision plan : pas de solution/at07-09.

## Faisabilité technique (audit 2026)
### AT08
- `pip install flashrank` ; `from langchain_community.document_compressors import FlashrankRerank`. Modèle ms-marco-MiniLM-L-12-v2 ~34 Mo ONNX CPU, OK Mac ARM.
- `ContextualCompressionRetriever(base_compressor=FlashrankRerank(top_n=...), base_retriever=...)`.
- `from langchain.retrievers.multi_query import MultiQueryRetriever` ; `.from_llm(retriever, llm)`.
- Bug "temperature=0 ne diversifie pas multi-query" = FAUX (variantes issues d'un seul appel piloté par prompt) → remplacé par "prompt demande 1 seule reformulation".
- Bug base_k==top_n : reformuler "perte du filtrage entonnoir" (pas annulation totale).

### AT07
- RAGAS : épingler `ragas==0.2.*`. Schéma EvaluationDataset/SingleTurnSample colonnes user_input/response/retrieved_contexts/reference. Juge via LangchainLLMWrapper(get_llm(temperature=0)), embeddings LangchainEmbeddingsWrapper(get_embeddings()).
- `reference` obligatoire pour context_recall ET context_precision (variantes with-reference). Pas pour faithfulness/answer_relevancy.
- Langfuse : SDK v2 (langfuse==2.57.1), import `from langfuse.callback import CallbackHandler`. PAS `langfuse.langchain` (=v3). Self-host = 6 conteneurs (web/worker/postgres/clickhouse/redis/minio), dashboard :3000, lourd → Cloud par défaut, Docker en bonus.
- config.py a DÉJÀ LANGFUSE_*/LANGCHAIN_*/TRACING_PROVIDER → zéro delta config AT07.

### AT09
- `from langchain_community.vectorstores.azuresearch import AzureSearch`. embedding_function accepte Callable/Embeddings. add_documents auto-crée l'index en inférant la dim → pour rendre le bug dim réel, créer le schéma À LA MAIN via SearchIndexClient (azure-search-documents>=11.5.1).
- search_type ∈ {similarity, hybrid, semantic_hybrid}. semantic_hybrid exige tier Basic+ + semantic configuration.
- Free tier = 1 service/souscription → service Basic partagé + 1 index/élève (index_name = trigramme).
- `az search` = control plane (service+clés). Tout le RAG (index/ingest/query) = SDK/REST. Wizard "Import and vectorize" = seul portail-only (remplaçable SDK).

## Gabarits existants (à copier fidèlement)
- AT07 = type éval/synthèse (pas exercice/solution, TODO inline dans evaluate_*.py) comme AT06.
- AT08/AT09 = type construction (exercice.py + solution.py) comme AT02/AT05.
- evaluate_rag.py (AT02) : LLM-judge maison, QUESTIONS_ETALONS avec ground_truth, format_docs, parse_score, 4 métriques.
- evaluate_pipeline.py (AT06) : benchmark via API HTTP, TODO inline.
- requirements : héritage `-r requirements_atelierXX.txt` + delta.
- check_atelier_ready.sh : regex ^0[1-6]$ → ^0[1-9]$, + branche case import-test.
- Slides : slides/atelier-0X-corrige.md + -blank.md à la racine pre-training-rag, indices 2 niveaux.

## AT08 — TERMINÉ (atelier/08 + student/08)
- **Seuils figés (run réel, corpus HomeButler, questions en langage NATUREL)** :
  baseline FAISS k=5 → Recall@1=40% Recall@3=90% Recall@5=90% MRR=0.617 ;
  + reranking (base_k=20→top_n=5) → Recall@1=70% Recall@3=100% Recall@5=100% MRR=0.833.
  GAIN = ΔRecall@1 +30pts, ΔMRR +0.22.
- **Piège T2 confirmé & résolu** : sur questions "mot pour mot" du doc, baseline déjà
  Recall@5=100% → AUCUN gain visible. Solution = benchmark de 10 questions en langage
  naturel/indirect (vocabulaire usager ≠ doc) + métriques-phares Recall@1 et MRR (pas Recall@5).
- **Patches Bug Hunt** : générés par `git diff` après `git add` du fichier (sinon untracked
  → diff vide + checkout échoue). Cible = homebutler/rag/reranking.py. v1=base_k 20→5,
  v2=prompt 3→1 reformulation, v3=FlashrankRerank sans top_n (défaut flashrank=3).
  Tests robustes (pas flaky) : v1 base>final, v2 analyse statique prompt, v3 len==top_n.
- **Bug "multiquery temp=0 ne diversifie pas" = FAUX** (audit) → retiré, remplacé par
  "prompt demande 1 reformulation". Confirmé en pratique.
- FlashrankRerank import : `from langchain_community.document_compressors import FlashrankRerank`.
  Modèle ms-marco-MiniLM-L-12-v2 ~34Mo, OK Mac/CPU. flashrank>=0.2.9.
- Venv de test : `.venv_at08test` (Python 3.12.13 — le `.venv` repo est en 3.14, sans deps).
  3.12 a les wheels pour faiss-cpu==1.13.2 / onnxruntime==1.23.2.
- Commits : atelier/08 = c423d29 (+ scope), student/08 = 6e117b0 (+ scope). Diff atelier↔student
  = uniquement reranking.py (blank). verify_branch_scope conforme sur les 2.
- check_atelier_ready : regex ^0[1-9]$ + cases 07/08/09. preload_models : flashrank (try/except).
