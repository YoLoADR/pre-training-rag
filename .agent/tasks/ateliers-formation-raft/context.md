# Context — Ateliers progressifs fil rouge Formation RAFT

## Objectif

Le projet final **HomeButler AI** est développé et fonctionnel (40 fichiers, 3 notebooks, 16 endpoints API, UI Streamlit + Gradio). Les slides de formation sont prêts.

Il faut maintenant créer les **6 ateliers progressifs** qui mènent à ce projet final, en remontant du projet complet vers le point de départ. Chaque atelier correspond à une demi-journée de la formation RAFT (3 jours, référence PLB v2026-0512).

## Approche pédagogique

**Fil rouge** : les ateliers construisent progressivement HomeButler AI. Un élève qui arrive au jour 2 peut `git checkout atelier/03-pipeline-agent` et retrouver un projet fonctionnel avec LLM + RAG déjà en place.

**Contraintes clés** :
1. Chaque atelier = branche git dédiée avec le projet à l'état exact de ce chapitre
2. Zéro débordement : le code d'une branche ne contient pas de features des chapitres suivants
3. Maximum de commentaires sur les concepts RAG et Fine-Tuning uniquement (pas de Python 101)
4. Chaque branche doit être autonome et démarrable (`pip install && python exercice.py`)

## Mapping formation → ateliers

| Branche | Jour | Chapitre formation | TP objectif |
|---|---|---|---|
| `atelier/01-llm-baseline` | J1 matin | Introduction LLM + concepts RAG | LLM sans contexte → hallucinations |
| `atelier/02-rag-simple` | J1 après-midi | Création d'un RAG simple | Chatbot RAG FAISS, 3 chunking, métriques RAGAs |
| `atelier/03-pipeline-agent` | J2 matin | Pipeline RAG + Agent ReAct | Agent 4 outils, trace ReAct, EnsembleRetriever |
| `atelier/04-finetuning` | J2 après-midi | Fine-tuning HuggingFace | LoRA/QLoRA Colab, dataset, 5 pièges, évaluation |
| `atelier/05-deploiement` | J3 matin | Déploiement + supervision | FastAPI + Streamlit + Langfuse + Ollama + sécurité |
| `atelier/06-finetune-vs-rag` | J3 après-midi | Fine-tuning vs RAG | Recall@k, RAFT, benchmarks, grille décision |

## Ressources disponibles

- Projet final : `/Users/yohannravino/Factory/pre-training-rag/` (branche `main`)
- Programme de formation : `formation-RAFT.pdf`
- Slides théoriques : `slides-formation-raft.md`
- Scénarios de démo : `draft.md`
- Notebooks existants : `notebooks/01_llm_baseline.ipynb`, `02_ingestion_vectorisation.ipynb`, `03_finetuning_lora.ipynb`

## Stratégie de versioning (validée)

Chaque branche créée **depuis `main`** avec suppression progressive des fichiers hors-scope — jamais depuis un commit vide (les imports croisés rendraient le projet non-fonctionnel).

Fichiers dans `ateliers/` créés d'abord sur `main` puis présents dans toutes les branches.
