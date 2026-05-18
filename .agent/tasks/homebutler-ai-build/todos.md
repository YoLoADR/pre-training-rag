# TODOs — HomeButler AI Build

> Mise à jour au fil de l'implémentation. Cocher chaque tâche dès qu'elle est terminée.

## Phase 1 — Bootstrap ✅

- [x] Git init + push GitHub (https://github.com/YoLoADR/pre-training-rag)
- [x] `.env.example`
- [x] `requirements.txt`
- [x] `README.md`
- [x] `homebutler/__init__.py`
- [x] `homebutler/config.py`

## Phase 2 — Données fictives ✅

- [x] `scripts/generate_documents.py` (6 PDFs via fpdf2) — CORRIGÉ: remplacé em-dash/→ latin-1
- [x] `scripts/generate_energy_data.py` (365j CSV + 3 anomalies)
- [x] `scripts/generate_producers.py` (30 producteurs JSON)
- [x] `scripts/generate_qa_dataset.py` (150 paires JSONL)
- [x] `scripts/preload_models.py`
- [x] **EXEC** : Données générées et validées (365 lignes, 30 producteurs, 150 paires, 6 PDFs)

## Phase 3 — Abstraction LLM ✅

- [x] `homebutler/llm/__init__.py`
- [x] `homebutler/llm/provider.py` (switch Anthropic / Ollama)
- [x] `homebutler/llm/prompts.py` (templates concierge)

## Phase 4 — Services métier ✅

- [x] `homebutler/services/__init__.py`
- [x] `homebutler/services/energy.py` (z-score anomalies, résumé mensuel) — VALIDÉ: 32 anomalies détectées
- [x] `homebutler/services/marketplace.py` (haversine, search_producers) — VALIDÉ: 7 producteurs < 15km
- [x] `homebutler/services/weather.py` (Open-Meteo, TTLCache)

## Phase 5 — Pipeline RAG ✅

- [x] `homebutler/rag/__init__.py`
- [x] `homebutler/rag/ingestion.py` (PyMuPDF + 3 chunkers)
- [x] `homebutler/rag/vectorstore.py` (FAISS + ChromaDB + embeddings CPU)
- [x] `homebutler/rag/retriever.py` (EnsembleRetriever MMR)
- [ ] **TODO** : Indexation RAG (nécessite sentence-transformers installé)

## Phase 6 — Agent ReAct ✅

- [x] `homebutler/agent/__init__.py`
- [x] `homebutler/agent/tools.py` (4 outils LangChain)
- [x] `homebutler/agent/react_agent.py` (AgentExecutor + LangSmith/Langfuse)
- [ ] **TODO** : Test question complexe (nécessite ANTHROPIC_API_KEY + index RAG)

## Phase 7 — API FastAPI ✅

- [x] `api/__init__.py`
- [x] `api/main.py` (CORS + middleware injection + lifespan)
- [x] `api/routers/chat.py`
- [x] `api/routers/consumption.py`
- [x] `api/routers/products.py`
- [x] `api/routers/orders.py`
- [x] `api/Dockerfile`

## Phase 8 — UI ✅

- [x] `ui/gradio_prototype.py` (~50 lignes)
- [x] `ui/app.py` (Streamlit entry)
- [x] `ui/pages/01_💬_Chat.py`
- [x] `ui/pages/02_⚡_Energie.py` (Plotly dashboard)
- [x] `ui/pages/03_🛒_Marketplace.py` (carte + filtres)
- [x] `ui/pages/04_🏠_Logement.py`
- [x] `ui/Dockerfile`

## Phase 9 — Notebooks pédagogiques ✅

- [x] `notebooks/01_llm_baseline.ipynb`
- [x] `notebooks/02_ingestion_vectorisation.ipynb`

## Phase 10 — Infrastructure VPS ✅

- [x] `docker-compose.yml`
- [x] `.gitignore`

## Finalisation ✅

- [x] Commit final + push (commit: 6efc690)
- [x] Données générées validées

## Prochaines étapes (pour l'utilisateur)

- [ ] Ajouter `ANTHROPIC_API_KEY` dans `.env`
- [ ] `pip install -r requirements.txt` (complet — attention Python 3.14 vs 3.11)
- [ ] `python scripts/preload_models.py` (télécharger le modèle embeddings ~470Mo)
- [ ] Indexation RAG : `python -c "from homebutler.rag.ingestion import ingest_all_documents; ..."`
- [ ] Tester l'API : `uvicorn api.main:app --reload --port 8000`
