# Todos — Ateliers progressifs Formation RAFT

## Phase 0 — Préparation (sur main)

- [ ] Scinder `homebutler/rag/vectorstore.py` en `vectorstore_faiss.py` + `vectorstore_chroma.py` (correction import ChromaDB au niveau module → crash atelier/02)
- [ ] Créer `notebooks/02_rag_simple_faiss.ipynb` (version sans ChromaDB, sections 1-4 FAISS uniquement)
- [ ] Créer `requirements_atelier01.txt` (~8 packages : LLM seul)
- [ ] Créer `requirements_atelier02.txt` (+7 packages : RAG FAISS)
- [ ] Créer `requirements_atelier03.txt` (+3 packages : ChromaDB, agent)
- [ ] Créer `requirements_atelier04.txt` (note Colab pour packages FT)
- [ ] Créer `requirements_atelier05.txt` (+10 packages : API, Streamlit, Langfuse)
- [ ] Créer `scripts/verify_branch_scope.sh` (vérification anti-débordement + notebooks)
- [ ] Créer `ateliers/README.md` (guide "comment démarrer un atelier")

---

## Phase 1 — Créer les fichiers d'exercices (sur main)

### Atelier 01 — LLM Baseline
- [ ] `ateliers/atelier-01-llm-baseline/README.md` (installation, questions réflexion, contexte HomeButler)
- [ ] `ateliers/atelier-01-llm-baseline/exercice.py` (5 TODOs : instancier LLM, 5 questions logement, température, switch Ollama, noter hallucinations)
- [ ] `ateliers/atelier-01-llm-baseline/solution.py` (commentaires : hallucination, knowledge cutoff, température, Anthropic vs Ollama)

### Atelier 02 — RAG Simple
- [ ] `ateliers/atelier-02-rag-simple/README.md` (installation, 3 questions réflexion sur chunking/embedding/FAISS)
- [ ] `ateliers/atelier-02-rag-simple/exercice.py` (6 TODOs : génération PDFs, load_pdf, 3 stratégies chunking, FAISS index, LCEL chain, Recall@k évaluation)
- [ ] `ateliers/atelier-02-rag-simple/solution.py` (commentaires : embedding, FAISS similarité cosinus, 3 stratégies, Recall@k)
- [ ] `ateliers/atelier-02-rag-simple/evaluate_rag.py` (4 métriques RAGAs optionnel : Faithfulness, Answer Relevance, Context Precision, Context Recall)

### Atelier 03 — Pipeline Agent ReAct
- [ ] `ateliers/atelier-03-pipeline-agent/README.md` (pré-requis scripts, question multi-outils fil rouge, questions réflexion)
- [ ] `ateliers/atelier-03-pipeline-agent/exercice.py` (5 TODOs : EnsembleRetriever, 4 outils à câbler, AgentExecutor, return_intermediate_steps, question multi-outils)
- [ ] `ateliers/atelier-03-pipeline-agent/solution.py` (commentaires : ReAct loop, EnsembleRetriever hybride dense/sparse, mémoire conversationnelle)
- [ ] `ateliers/atelier-03-pipeline-agent/gradio_demo.py` (interface Gradio avec affichage steps ReAct)

### Atelier 04 — Fine-tuning
- [ ] `ateliers/atelier-04-finetuning/README.md` (3 parcours GPU/CPU/pair-sharing, checklist 5 pièges FT, instructions Colab)
- [ ] `ateliers/atelier-04-finetuning/prepare_dataset.py` (génère dataset, affiche distribution catégories, format Alpaca, split 80/10/10)
- [ ] `ateliers/atelier-04-finetuning/explore_dataset.py` (stats longueur, détection paires courtes/longues, distribution équilibre)
- [ ] Enrichir `notebooks/03_finetuning_lora.ipynb` sections 1, 2, 3, 5, 7, 8 (commentaires LoRA, QLoRA, hyperparamètres, métriques, 5 pièges)

### Atelier 05 — Déploiement
- [ ] `ateliers/atelier-05-deploiement/README.md` (3 terminaux, switch Ollama, Langfuse, Ollama vs Jan.ai justification)
- [ ] `ateliers/atelier-05-deploiement/test_securite.sh` (4 tests curl avec commentaires sur les 19 patterns injection + OWASP LLM01)
- [ ] `ateliers/atelier-05-deploiement/checklist.md` (local → VPS → Docker, `pip install -e .`, `@st.cache_resource`)

### Atelier 06 — Fine-tuning vs RAG
- [ ] `ateliers/atelier-06-finetune-vs-rag/README.md` (RAFT Zhang et al. 2024, benchmarks 89%/94%/96%, section TCO)
- [ ] `ateliers/atelier-06-finetune-vs-rag/evaluate_pipeline.py` (6 TODOs : dataset test, /rag/evaluate, /chat/compare, latence, tableau Recall@k, grille décision)
- [ ] `ateliers/atelier-06-finetune-vs-rag/grille_decision.md` (arbre décision 4 questions, 8 critères, exemples métier)

---

## Phase 2 — Enrichir les commentaires pédagogiques dans le code source

- [ ] `homebutler/llm/provider.py` — commentaires sur hallucination, switch provider, prompt caching
- [ ] `homebutler/llm/prompts.py` — commentaires sur rôle du system prompt
- [ ] `homebutler/rag/ingestion.py` — commentaires sur les 3 stratégies de chunking (pourquoi pas de Python, juste concept)
- [ ] `homebutler/rag/vectorstore_faiss.py` — commentaires sur FAISS, similarité cosinus, embedding
- [ ] `homebutler/rag/vectorstore_chroma.py` — commentaires sur ChromaDB, filtres métadonnées
- [ ] `homebutler/rag/retriever.py` — commentaires sur EnsembleRetriever, dense vs sparse
- [ ] `homebutler/agent/tools.py` — commentaires sur Tool Chains, quand utiliser quel outil
- [ ] `homebutler/agent/react_agent.py` — commentaires ReAct loop complet (Thought → Action → Observation)

---

## Phase 3 — Créer les branches git

- [ ] Créer branche `atelier/01-llm-baseline` depuis main, supprimer homebutler/rag/, homebutler/agent/, homebutler/services/, api/, ui/, scripts non-nécessaires, notebooks 02 et 03 — adapter config.py (6 vars), requirements.txt
- [ ] Créer branche `atelier/02-rag-simple` depuis atelier/01, ajouter rag/ingestion.py + vectorstore_faiss.py + scripts generate + preload + notebook 02 FAISS
- [ ] Créer branche `atelier/03-pipeline-agent` depuis atelier/02, ajouter vectorstore_chroma.py + retriever.py + agent/ + services/ + Gradio + api/routers/chat.py basique + notebook 02 complet
- [ ] Créer branche `atelier/04-finetuning` depuis atelier/03, ajouter scripts dataset + notebook 03
- [ ] Créer branche `atelier/05-deploiement` depuis atelier/04, ajouter API complète (5 routers + limiter) + Streamlit (4 pages) + Modelfile + docker-compose.yml + api/routers/rag.py (retrieve only)
- [ ] Créer branche `atelier/06-finetune-vs-rag` depuis atelier/05, ajouter /rag/evaluate + /rag/compare-strategies + /chat/compare

---

## Phase 4 — Tags et vérifications

- [ ] Tagger `v1.1-atelier-01` à `v1.6-atelier-06`
- [ ] Lancer `scripts/verify_branch_scope.sh` sur chaque branche
- [ ] Test fonctionnel atelier/01 : `python exercice.py` → LLM répond sans context, hallucine
- [ ] Test fonctionnel atelier/02 : `python solution.py` → "Viessmann Vitodens 100-W" + sources
- [ ] Test fonctionnel atelier/03 : question multi-outils → 3+ outils appelés en trace ReAct
- [ ] Test fonctionnel atelier/04 : `python prepare_dataset.py` → stats dataset affichées
- [ ] Test fonctionnel atelier/05 : `test_securite.sh` → HTTP 400 sur injection
- [ ] Test fonctionnel atelier/06 : `evaluate_pipeline.py` → tableau Recall@k affiché
