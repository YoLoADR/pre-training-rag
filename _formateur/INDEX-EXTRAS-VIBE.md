# Index des exercices Bonus (vibe-coders) — HomeButler AI RAFT

> **Usage formateur** : à présenter aux élèves rapides (Core + Bug Hunt terminé en < 2h30) pour qu'ils ne s'ennuient pas.
> **Localisation** : chaque défi est dans la section §BONUS du `GUIDE-ELEVE.md` de la branche `student/0X` correspondante.

---

## AT01 — LLM Baseline

| # | Défi | Fichier de référence | Objectif mesurable |
|---|---|---|---|
| 1 | Benchmark Sonnet vs Haiku | `ateliers/atelier-01-llm-baseline/exercice.py` (boucler sur 2 modèles) | Coût €/1k tokens + latence p50/p95 + qualité (LLM-judge) |
| 2 | Few-shot prompting | `homebutler/llm/prompts.py` (ajouter 3 exemples dans `CONCIERGE_SYSTEM_PROMPT`) | Baisse mesurée de l'hallucination rate (-10pts minimum) |

---

## AT02 — RAG Simple FAISS

| # | Défi | Fichier de référence | Objectif mesurable |
|---|---|---|---|
| 1 | Sweep chunk_size | `homebutler/rag/ingestion.py` ; lancer `evaluate_rag.py` | Recall@5 max sur {200, 600, 1500} → courbe à présenter |
| 2 | MMR vs similarity | `homebutler/rag/retriever.py` (search_type) | Diversité vs précision sur questions dispersées |

**Fichier extra** : `ateliers/atelier-02-rag-simple/evaluate_rag.py` — LLM-judge faithfulness + Recall@k

---

## AT03 — Pipeline Agent ReAct

| # | Défi | Fichier de référence | Objectif mesurable |
|---|---|---|---|
| 1 | Ajouter outil custom | `homebutler/agent/tools.py` (créer `get_indoor_temperature`) | Outil scope-safe + appelé par l'agent sur question pertinente |
| 2 | Mémoire ON vs OFF | `ateliers/atelier-03-pipeline-agent/gradio_demo.py` | Dialogue 3 tours : cohérence référentielle mesurée |

**Fichier extra** : `ateliers/atelier-03-pipeline-agent/gradio_demo.py` — interface Gradio pour tester mémoire

---

## AT04 — Fine-tuning LoRA

| # | Défi | Fichier de référence | Objectif mesurable |
|---|---|---|---|
| 1 | Sur-échantillonnage minorité | `scripts/augment_qa_dataset.py` (forcer catégorie marketplace ×3) | Distribution équilibrée + perplexité baisse sur cette catégorie |
| 2 | LoRA training complet Colab | `notebooks/03_finetuning_lora.ipynb` | Modèle fine-tuné poussé sur HuggingFace, comparé avant/après |

**⚠️ Pré-requis** : compte Google Colab + ~30 min de quota T4.

---

## AT05 — Déploiement FastAPI

| # | Défi | Fichier de référence | Objectif mesurable |
|---|---|---|---|
| 1 | SSE streaming endpoint | `api/routers/chat.py` (ajouter `POST /chat/stream`) | Streamlit reçoit les tokens en streaming (effet "machine à écrire") |
| 2 | PII scrubbing Langfuse | `api/main.py` (hook avant log) | Masquage emails/tel avant ingestion Langfuse (RGPD) |

---

## AT06 — RAG vs FT vs RAFT

| # | Défi | Fichier de référence | Objectif mesurable |
|---|---|---|---|
| 1 | Argumentaire RAFT 5 min | aucun code | Présentation orale : "adopter ou rejeter RAFT pour HomeButler — pourquoi" |
| 2 | Mini-débat duo FT/RAG/hybride | aucun code | 2 élèves défendent des positions opposées sur un cas client réel |

---

## Fichiers standalone hors §BONUS (utilisables comme extras isolés)

| Fichier | Atelier | Usage formateur |
|---|---|---|
| `notebooks/01_llm_baseline.ipynb` | AT01 | Comparatif 3 modèles open-source en Colab (alternative à l'exercice.py) |
| `notebooks/03_finetuning_lora.ipynb` | AT04 | Notebook principal — pas un bonus, c'est le Core |
| `ateliers/atelier-02-rag-simple/evaluate_rag.py` | AT02 | Évaluation Recall@k + faithfulness — peut être Core étendu |
| `ateliers/atelier-03-pipeline-agent/gradio_demo.py` | AT03 | Interface visuelle pour démo client (ou bonus) |
| `ateliers/atelier-06-finetune-vs-rag/evaluate_pipeline.py` | AT06 | Benchmark 3 modes (llm_only / rag / agent) — c'est le Core |

---

## Comment piocher dans cet index pendant une session

**Cas 1 — élève rapide** : "Tu as fini Core + Bug Hunt en 2h ? Va voir §BONUS dans ton GUIDE-ELEVE.md, défi #1 (présenté ici)."

**Cas 2 — groupe avancé** : annoncer le Bonus en début d'atelier comme objectif ambitieux pour ceux qui terminent Core en 1h.

**Cas 3 — formation prolongée (+1 jour)** : enchaîner 2 bonus consécutifs par atelier = ~1h supplémentaire par atelier = format 7 jours au lieu de 6.

---

## Tableau récap couverture pédagogique des bonus

| Compétence visée | Atelier(s) couvrant |
|---|---|
| Mesure coût/latence LLM | AT01.1 |
| Prompt engineering avancé | AT01.2 |
| Évaluation RAG quantitative | AT02.1, AT02.2 |
| Personnalisation agent | AT03.1 |
| Conversations multi-tours | AT03.2 |
| Data engineering dataset | AT04.1 |
| Fine-tuning hands-on | AT04.2 |
| API production-ready | AT05.1 |
| Conformité RGPD | AT05.2 |
| Synthèse pédagogique | AT06.1, AT06.2 |
