# Déroulé formation HomeButler AI RAFT — antisèche formateur

> **Usage** : ouvrir ce fichier sur ton 2e écran pendant la session. Une ligne par atelier, copier-coller les commandes telles quelles.
> **Repos** : tu es dans `pre-training-rag` (zone formateur). Les élèves clonent `training-rag` (zone élève).

---

## Carte des 6 ateliers

| AT | Demi-j. | Branche élève | Branche corrigée | Blanks à coder par l'élève |
|---|---|---|---|---|
| 01 | ~3h30 | `student/01-llm-baseline` | `atelier/01-llm-baseline` | `provider.py` + 4 templates |
| 02 | ~3h30 | `student/02-rag-simple` | `atelier/02-rag-simple` | `ingestion.py` (3 fn) + `vectorstore_faiss.py` (3 fn) |
| 03 | ~3h30 | `student/03-pipeline-agent` | `atelier/03-pipeline-agent` | `retriever.py` + `react_agent.py` |
| 04 | ~3h30 | `student/04-finetuning` | `atelier/04-finetuning` | 3 cellules notebook LoRA + 2 scripts dataset |
| 05 | ~3h30 | `student/05-deploiement` | `atelier/05-deploiement` | `chat.py` (2 fn) + endpoint `/retrieve` |
| 06 | ~3h30 | `student/06-finetune-vs-rag` | `atelier/06-finetune-vs-rag` | 6 TODOs dans `evaluate_pipeline.py` |

---

## Flux invariant par atelier (à appliquer 6 fois)

```
[T-15 min — préparation]
cd /Users/yohannravino/Factory/pre-training-rag
ouvrir slides/atelier-0X-corrige.md (vidéoprojeté)
ouvrir notes-formateur-vulgarisation.md sur 2e écran (local, jamais commit)

[T0 — projeter slides ~30 min]
Slides corrigées = repère pour TOI. Pas distribuées aux élèves.

[T+30 min — démo live ~20 min]
cd /Users/yohannravino/Factory/training-rag
git checkout atelier/0X-nom
# Ouvrir solution.py + montrer 1-2 fonctions clés en lecture (pas de live-typing)

[T+50 min — élèves démarrent ~1h40 Core + 30 min Bug Hunt]
# Annonce : "git checkout student/0X-nom, lisez QUICK-START.md, codez."
# Tu circules.

[T+3h — partage correction sur demande]
git diff student/0X-nom atelier/0X-nom -- <fichier>
# ou : git checkout atelier/0X-nom -- ateliers/atelier-0X-nom/solution.py
```

---

## Atelier 01 — LLM Baseline (~3h30)

| Bloc | Durée | Action |
|---|---|---|
| Slides projetées | 30 min | `slides/atelier-01-corrige.md` (énoncé + théorie temperature/system prompt/hallucination) |
| Démo live | 20 min | `git checkout atelier/01-llm-baseline` ; montrer `homebutler/llm/provider.py` (get_llm) |
| Core élève | 1h40 | Mission : 10 questions → mesurer hallucination rate ≥ 80 % sur questions privées |
| Bug Hunt | 30 min | `git apply ateliers/atelier-01-llm-baseline/bugs/v1.patch` → `pytest bugs/test_v1.py` → débugue → idem v2, v3 |
| Bonus si avance | 30 min | Voir `INDEX-EXTRAS-VIBE.md` §AT01 |

**Commande de secours élève** (à donner si bloqué > 15 min) :
```bash
git diff student/01-llm-baseline atelier/01-llm-baseline -- homebutler/llm/provider.py
```

**Tests bug-hunt attendus** : 3 tests, état initial = PASS sur exercice.py propre ; chaque patch v1/v2/v3 introduit un bug → test FAIL → élève débugue.

---

## Atelier 02 — RAG Simple FAISS (~3h30)

| Bloc | Durée | Action |
|---|---|---|
| Slides | 30 min | `slides/atelier-02-corrige.md` (chunking / embeddings / FAISS) |
| Démo live | 20 min | `git checkout atelier/02-rag-simple` ; montrer `homebutler/rag/ingestion.py` (chunk_recursive) |
| Core | 1h40 | 3 stratégies chunking + index FAISS, objectif Recall@5 ≥ 0.80 |
| Bug Hunt | 30 min | 3 patches dans `bugs/` (chunk_size aberrant, overlap=0, force_rebuild boucle) |

**Particularité Mac ARM** : préciser aux élèves que `faiss-cpu` suffit (pas de GPU).

---

## Atelier 03 — Pipeline Agent ReAct (~3h30)

| Bloc | Durée | Action |
|---|---|---|
| Slides | 30 min | `slides/atelier-03-corrige.md` (EnsembleRetriever, ReAct, mémoire) |
| Démo live | 20 min | `git checkout atelier/03-pipeline-agent` ; montrer `homebutler/agent/react_agent.py` + `tools.py` (4 outils) |
| Core | 1h40 | Retriever hybride FAISS 60% + Chroma 40%, agent ReAct avec mémoire |
| Bug Hunt | 30 min | 10 tests (duplicate tools, max_iterations, handle_parsing_errors) |

**Attention Anthropic rate limit** : Tier 1 = 50 req/min. Si toute la classe code en même temps, basculer sur Ollama local (`LLM_PROVIDER=ollama`).

---

## Atelier 04 — Fine-tuning LoRA / QLoRA (~3h30)

| Bloc | Durée | Action |
|---|---|---|
| Slides | 30 min | `slides/atelier-04-corrige.md` (LoRA, QLoRA, SFTTrainer, perplexité) |
| Démo Colab | 20 min | Ouvrir `notebooks/03_finetuning_lora.ipynb` (Google Colab T4 obligatoire — pas de GPU local Mac) |
| Core | 1h40 | Compléter 3 cellules (BitsAndBytesConfig, LoraConfig, TrainingArguments) + `generate_qa_dataset.py` + `augment_qa_dataset.py` |
| Bug Hunt | 30 min | 3 tests (categorize, learning_rate, n_val) |

**⚠️ Particularité** : pas de `exercice.py` à la racine de l'atelier — le code vit dans le notebook Colab. Bien le préciser dès le début.

---

## Atelier 05 — Déploiement FastAPI (~3h30)

| Bloc | Durée | Action |
|---|---|---|
| Slides | 30 min | `slides/atelier-05-corrige.md` (FastAPI, CORS, rate limit, Langfuse tracing) |
| Démo live | 20 min | `git checkout atelier/05-deploiement` ; `uvicorn api.main:app --reload` puis `curl /chat` |
| Core | 1h40 | Compléter `api/routers/chat.py` (`_call_rag_only`, `_call_agent`) + endpoint `/rag/retrieve` |
| Bug Hunt | 30 min | 7 tests (CORS origins explicites, timeout numeric, wait_for present) |

**⚠️ Particularité** : pas d'`exercice.py` — le code modifié est dans `api/routers/`. Lancement : `uvicorn api.main:app --reload --port 8000` ; UI Streamlit : `streamlit run ui/app.py`.

---

## Atelier 06 — RAG vs FT vs RAFT (~3h30)

| Bloc | Durée | Action |
|---|---|---|
| Slides | 30 min | `slides/atelier-06-corrige.md` (benchmark 3 modes, RAFT 2024) |
| Démo live | 20 min | `git checkout atelier/06-finetune-vs-rag` ; lancer `python ateliers/atelier-06-finetune-vs-rag/evaluate_pipeline.py` |
| Core | 1h40 | Compléter 6 TODOs dans `evaluate_pipeline.py` (3 NotImplementedError + 11 # TODO) |
| Bug Hunt | 30 min | 8 tests (no sentence_bleu, no single question, latencies append) |

**⚠️ Particularité** : pas d'`exercice.py` — TODOs parsemés dans `evaluate_pipeline.py`. Donner aux élèves au début la liste explicite des lignes à compléter : `grep -n "TODO\|NotImplementedError" ateliers/atelier-06-finetune-vs-rag/evaluate_pipeline.py`.

---

## Checklist pré-session (15 min avant chaque atelier)

```bash
cd /Users/yohannravino/Factory/training-rag

# 1. Vérifier que tu es bien sur la branche corrigée (pour la démo)
git checkout atelier/0X-nom
git status   # → clean, à jour

# 2. Tester la solution UNE FOIS
.venv/bin/python ateliers/atelier-0X-nom/exercice.py   # (sauf AT04/05/06)
# Pour AT04 : ouvrir notebook
# Pour AT05 : uvicorn api.main:app --reload
# Pour AT06 : .venv/bin/python ateliers/atelier-06-finetune-vs-rag/evaluate_pipeline.py

# 3. Vérifier qu'on peut basculer rapidement sur student/XX pour montrer le blanking
git checkout student/0X-nom
grep -n NotImplementedError homebutler/ -r | head -5
git checkout atelier/0X-nom   # revenir avant démo
```

---

## Cas pannes typiques (à anticiper)

| Symptôme | Cause probable | Réponse |
|---|---|---|
| `ANTHROPIC_API_KEY missing` | `.env` pas copié depuis `.env.example` | `cp .env.example .env` + remplir |
| `ModuleNotFoundError: homebutler` | venv pas activé | `source .venv/bin/activate` |
| `faiss.IndexFlatL2 segfault` | macOS ARM avec faiss-gpu installé | Forcer `pip install faiss-cpu` |
| Rate limit Anthropic | 50 req/min Tier 1 | Basculer `LLM_PROVIDER=ollama` |
| Bug-hunt patch refuse à appliquer | Élève a modifié exercice.py différemment | `git checkout student/0X-nom -- ateliers/atelier-0X-nom/exercice.py` puis réappliquer |
| Notebook Colab plante (AT04) | Pas de GPU sélectionné | Runtime → Change runtime type → T4 GPU |

---

## Ressources formateur (locales, jamais distribuées)

- `notes-formateur-vulgarisation.md` (racine) — analogies grand public, vulgarisation des concepts
- `_formateur/INDEX-EXTRAS-VIBE.md` — index des exercices bonus vibe-coders
- `slides/atelier-0X-corrige.md` — slides projetées
- `slides/atelier-0X-blank.md` — version élève des slides (si distribution PDF)
