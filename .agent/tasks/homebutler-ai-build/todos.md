# TODOs — HomeButler AI Build

> Mise à jour au fil de l'implémentation. Cocher chaque tâche dès qu'elle est terminée.

## Phase 1 — Bootstrap

- [x] Git init + push GitHub (https://github.com/YoLoADR/pre-training-rag)
- [ ] `.env.example`
- [ ] `requirements.txt`
- [ ] `README.md`
- [ ] `homebutler/__init__.py`
- [ ] `homebutler/config.py`

## Phase 2 — Données fictives

- [ ] `scripts/generate_documents.py` (6 PDFs via fpdf2)
- [ ] `scripts/generate_energy_data.py` (365j CSV + 3 anomalies)
- [ ] `scripts/generate_producers.py` (30 producteurs JSON)
- [ ] `scripts/generate_qa_dataset.py` (150 paires JSONL)
- [ ] `scripts/preload_models.py`
- [ ] **EXEC** : Générer toutes les données fictives + vérifier

## Phase 3 — Abstraction LLM

- [ ] `homebutler/llm/__init__.py`
- [ ] `homebutler/llm/provider.py` (switch Anthropic / Ollama)
- [ ] `homebutler/llm/prompts.py` (templates concierge)

## Phase 4 — Services métier

- [ ] `homebutler/services/__init__.py`
- [ ] `homebutler/services/energy.py` (z-score anomalies, résumé mensuel)
- [ ] `homebutler/services/marketplace.py` (haversine, search_producers)
- [ ] `homebutler/services/weather.py` (Open-Meteo, TTLCache)

## Phase 5 — Pipeline RAG

- [ ] `homebutler/rag/__init__.py`
- [ ] `homebutler/rag/ingestion.py` (PyMuPDF + 3 chunkers)
- [ ] `homebutler/rag/vectorstore.py` (FAISS + ChromaDB + embeddings CPU)
- [ ] `homebutler/rag/retriever.py` (EnsembleRetriever MMR)
- [ ] **EXEC** : Indexation RAG initiale + test retrieval

## Phase 6 — Agent ReAct

- [ ] `homebutler/agent/__init__.py`
- [ ] `homebutler/agent/tools.py` (4 outils LangChain)
- [ ] `homebutler/agent/react_agent.py` (AgentExecutor + LangSmith)
- [ ] **TEST** : Question complexe chaînée

## Phase 7 — API FastAPI

- [ ] `api/__init__.py`
- [ ] `api/main.py` (CORS + middleware injection + lifespan)
- [ ] `api/routers/chat.py`
- [ ] `api/routers/consumption.py`
- [ ] `api/routers/products.py`
- [ ] `api/routers/orders.py`
- [ ] `api/Dockerfile`
- [ ] **TEST** : curl /chat + /products/search + test sécurité

## Phase 8 — UI

- [ ] `ui/gradio_prototype.py` (~50 lignes)
- [ ] `ui/app.py` (Streamlit entry)
- [ ] `ui/pages/01_💬_Chat.py`
- [ ] `ui/pages/02_⚡_Energie.py` (Plotly dashboard)
- [ ] `ui/pages/03_🛒_Marketplace.py` (carte + filtres)
- [ ] `ui/pages/04_🏠_Logement.py`
- [ ] `ui/Dockerfile`

## Phase 9 — Notebooks pédagogiques

- [ ] `notebooks/01_llm_baseline.ipynb`
- [ ] `notebooks/02_ingestion_vectorisation.ipynb`

## Phase 10 — Infrastructure VPS

- [ ] `docker-compose.yml`

## Finalisation

- [ ] `git add -A && git commit` (checkpoint intermédiaire après chaque phase)
- [ ] Commit final + push
