# Context — HomeButler AI Build

## Objectif

Construire l'application complète **HomeButler AI** — un assistant conciergerie domestique intelligent servant de projet fil rouge pour une formation RAFT (RAG + Fine-Tuning, 3 jours).

Le formateur (Yohann) veut le "corrigé" complet de l'application avant de préparer les supports pédagogiques pour les stagiaires.

## Périmètre

**In scope :**
- Structure complète du projet (40 fichiers)
- Génération des données fictives (6 PDFs, CSV énergie 365j, JSON 30 producteurs, JSONL 150 paires Q/A)
- Pipeline RAG (FAISS + ChromaDB, 3 stratégies chunking, embeddings multilingues CPU)
- Agent ReAct LangChain avec 4 outils (search_docs, analyze_energy, find_products, weather)
- API FastAPI (4 endpoints + middleware sécurité)
- UI Streamlit multi-pages + prototype Gradio
- Notebooks pédagogiques (01_llm_baseline, 02_ingestion_vectorisation)
- Docker Compose pour déploiement VPS

**Out of scope :**
- Fine-tuning QLoRA (sera fait sur Google Colab séparément)
- MLFlow (tracking fine-tuning)
- Tests de charge Locust
- Supports pédagogiques (énoncés de TP)

## Contraintes techniques

- **Machine** : Mac sans GPU/CUDA, sans Conda → venv Python standard
- **LLM** : switch configurable — `LLM_PROVIDER=anthropic` (Claude API) en dev, `ollama` sur VPS
- **Observabilité** : LangSmith (curriculum RAFT) + Langfuse optionnel (pattern pbn/amplifiire)
- **Versions** : LangChain 0.3.x, Pydantic v2, FastAPI 0.115.x

## Repo GitHub

https://github.com/YoLoADR/pre-training-rag

## Répertoire projet

`/Users/yohannravino/Factory/pre-training-rag/`

## Plan de référence

`.agent/tasks/homebutler-ai-build/plan.md`

---

## État au 2026-05-19 (soir)

**Setup local validé end-to-end sur Mac Intel.**

- Venv : Python 3.13.5 (`.venv/`) — **pas 3.14** sur Mac Intel (cf. insights.md pour la raison onnxruntime).
- Package `homebutler` installé en editable (`pip install -e .`).
- Données générées + indexation FAISS/ChromaDB faites.
- API FastAPI + Streamlit + Gradio testés.

Ce qui reste à faire pour préparer la formation est essentiellement pédagogique (énoncés de TP) et non technique sur l'app elle-même.
