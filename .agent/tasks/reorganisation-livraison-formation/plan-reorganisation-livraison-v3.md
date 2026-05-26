# Plan — Réorganisation livraison formation HomeButler AI RAG (v3 — définitif)

## Context

Deux repos distincts, un seul projet pédagogique :

| Repo | Rôle | Accès |
|---|---|---|
| `pre-training-rag` | Zone formateur : slides, notes-vulgarisation, planification | Formateur uniquement |
| `training-rag` | Zone élève : code HomeButler, exercices, branches student/ | Élèves (clone + checkout) |

**La confusion élève se passe dans `training-rag`**, pas dans `pre-training-rag`. Le plan précédent ignorait `training-rag` — erreur corrigée.

---

## Architecture de `homebutler/` (le cœur pédagogique)

`homebutler/` est le package Python central que les élèves font tourner. Il est **progressivement révélé** d'atelier en atelier. Les branches `atelier/XX` contiennent la version complète (formateur). Les branches `student/XX` ont les fonctions clés remplacées par `NotImplementedError` + indices à 2 niveaux.

```
homebutler/
├── config.py            ← 26 vars d'env. Fourni complet dès AT01 (6 vars) → AT06 (26 vars)
│
├── llm/
│   ├── provider.py      ← get_llm() + get_llm_cached()     [blanké AT01]
│   └── prompts.py       ← 4 templates ChatPromptTemplate    [blanké AT01]
│
├── rag/
│   ├── ingestion.py     ← load_pdf_with_metadata() + 3 chunking strategies  [blanké AT02]
│   ├── vectorstore_faiss.py ← get_embeddings(), build_faiss_index(), load_faiss_index()  [blanké AT02]
│   ├── vectorstore_chroma.py ← ChromaDB (fourni corrigé AT03)
│   ├── vectorstore.py   ← ré-export compat (fourni AT03+)
│   └── retriever.py     ← get_ensemble_retriever() EnsembleRetriever FAISS 60%+Chroma 40%  [blanké AT03]
│
├── agent/
│   ├── react_agent.py   ← get_agent_executor() ReAct + mémoire + tracing  [blanké AT03]
│   └── tools.py         ← 4 outils LangChain (search_docs, energy, marketplace, weather)  [fourni AT03]
│
└── services/
    ├── energy.py        ← analyse CSV consommation, détection anomalies  [fourni AT03]
    ├── marketplace.py   ← recherche producteurs JSON + filtre distance    [fourni AT03]
    └── weather.py       ← Open-Meteo API + cache                          [fourni AT03]
```

### Carte du blanking par atelier

| Atelier | Fonctions blankées (NotImplementedError) | Fournies corrigées (lecture seule) |
|---|---|---|
| **AT01 LLM** | `get_llm()`, `get_llm_cached()`, `BARE_LLM_TEMPLATE`, `RAG_QA_TEMPLATE`, `ENERGY_ANALYSIS_TEMPLATE`, `REACT_SYSTEM_TEMPLATE` | `config.py` (6 vars), `CONCIERGE_SYSTEM_PROMPT` |
| **AT02 RAG** | `chunk_fixed_size()`, `chunk_recursive()`, `chunk_semantic()`, `get_embeddings()`, `build_faiss_index()`, `load_faiss_index()` | `load_pdf()`, `load_pdf_with_metadata()`, AT01 complet |
| **AT03 Agent** | `get_ensemble_retriever()`, `get_agent_executor()` | `tools.py`, `vectorstore_chroma.py`, `services/`, AT01+02 complets |
| **AT04 FT** | Cellules `LoraConfig`, `TrainingArguments`, `Trainer` dans notebook ; `generate_qa_dataset.py`, `augment_qa_dataset.py` | Dataset base, `explore_dataset.py`, AT01+02+03 complets |
| **AT05 Deploy** | `_call_rag_only()`, `_call_agent()` dans `api/routers/chat.py` ; endpoint `/retrieve` dans `api/routers/rag.py` | `api/main.py`, `api/limiter.py`, `ui/`, AT01→04 complets |
| **AT06 RAG vs FT** | 6 TODOs dans `ateliers/atelier-06-finetune-vs-rag/evaluate_pipeline.py` | endpoints `/rag/evaluate` + `/chat/compare` fournis, AT01→05 complets |

### Stratégie de blanking (pattern uniforme)

```python
def chunk_recursive(documents: list[Document], chunk_size: int = 512, chunk_overlap: int = 50) -> list[Document]:
    """
    Stratégie 2 — Récursif par séparateurs (recommandée).
    
    --- Indice léger ---
    LangChain expose RecursiveCharacterTextSplitter.
    Découpage récursif = essaie \\n\\n, puis \\n, puis ., puis espace.
    
    --- Indice fort ---
    1. Instancie RecursiveCharacterTextSplitter(chunk_size, chunk_overlap, separators=[...])
    2. Appelle .split_documents(documents)
    """
    raise NotImplementedError(
        "Atelier 02 § 2.2 — chunking récursif.\\n"
        "Solution : git diff student/02-rag-simple atelier/02-rag-simple -- homebutler/rag/ingestion.py"
    )
```

**Règles strictes :**
- `NotImplementedError` toujours **en corps de fonction**, jamais au top-level (sinon import cascade bloqué)
- Imports, signatures, type hints, docstrings toujours préservés
- Lien `git diff student/XX atelier/XX` toujours présent dans le message d'erreur

---

## État réel des branches `student/XX` (audit du 2026-05-26)

### Ce qui est déjà fait ✅

| Élément | État |
|---|---|
| `GUIDE-FORMATEUR.md` | Supprimé de tous student/01-06 |
| Code blanking homebutler/ | Fait pour tous les 6 ateliers |
| `QUICK-START.md` per atelier | Présent sur tous student/XX |
| `STARTER.md` (racine) | Présent sur tous student/XX |
| `.github/workflows/student-branches.yml` | Présent (CI légère) |
| `slides/atelier-0X-corrige.md` | Absents de tous student/XX |
| `.claude/CLAUDE.md` local par atelier | Présent et fonctionnel (scope strict) |

### Ce qui reste à nettoyer ❌

| Élément | Branches concernées | Impact |
|---|---|---|
| `.agent/tasks/` (5 dossiers planning formateur) | student/01, 02, 03, 04, 05 | Élèves voient les plans de conception interne |
| `README-formateur.md` | student/01, 02, 03, 04, 05, 06 | Guide animateur visible par les élèves |
| Branches `solution/at04`, `at05`, `at06` | Local uniquement | Correction non disponible pour ces ateliers |

---

## Le flux pédagogique par atelier

### Flux invariant

```
[Formateur]  git checkout atelier/0X-nom
             → Projeter slides/atelier-0X-corrige.md (depuis pre-training-rag/slides/)
             → Live coding : montrer solution.py (résultat attendu)

[Élèves]     git checkout student/0X-nom
             → Reçoivent GUIDE-ELEVE.md + QUICK-START.md + exercice.py (blanké)
             → Codent dans homebutler/ via exercice.py

[Fin de session] git checkout atelier/0X-nom -- ateliers/atelier-0X-nom/solution.py
                 OU: git diff student/0X atelier/0X -- <fichier>
```

### Contenu exact de chaque branche `student/0X`

```
training-rag/ (branche student/0X)
├── STARTER.md                              ← onboarding 8 étapes
├── PREREQUIS-FORMATION-RAFT.md
├── homebutler/
│   ├── llm/provider.py                    ← [AT01 blanké / AT02+ corrigé]
│   ├── llm/prompts.py                     ← [AT01 blanké / AT02+ corrigé]
│   ├── rag/ingestion.py                   ← [AT02 blanké / AT03+ corrigé]
│   ├── rag/vectorstore_faiss.py           ← [AT02 blanké / AT03+ corrigé]
│   ├── rag/retriever.py                   ← [AT03 blanké / AT04+ corrigé]
│   ├── agent/react_agent.py               ← [AT03 blanké / AT04+ corrigé]
│   └── ...                               ← reste fourni corrigé
├── ateliers/
│   └── atelier-0X-nom/
│       ├── QUICK-START.md                 ← recette 6 étapes avec analogies
│       ├── GUIDE-ELEVE.md                 ← mission + carnet + tronc + bug hunt + bonus
│       ├── exercice.py                    ← TP blank (importe depuis homebutler/ blanké)
│       ├── solution.py                    ← présent MAIS inutilisable (crash NotImplementedError)
│       ├── .claude/CLAUDE.md              ← garde-fou scope strict par atelier
│       ├── .cursorrules
│       ├── bugs/                          ← v1/v2/v3 patches + tests pytest + QCM explication
│       └── checkpoints/                   ← check_1.py + check_final.py
│
└── [ABSENT] GUIDE-FORMATEUR.md
    [ABSENT] README-formateur.md           ← après nettoyage
    [ABSENT] .agent/tasks/                 ← après nettoyage
```

### Table des livrables par atelier

| Atelier | Élève code (blanks) | Fourni corrigé (lecture) | Extras Bonus (vibe-coders) |
|---|---|---|---|
| **AT01 LLM** | `provider.py`, `prompts.py` | `config.py`, `CONCIERGE_SYSTEM_PROMPT` | Sonnet vs Haiku, few-shot prompting |
| **AT02 RAG** | `ingestion.py` (3 fonctions), `vectorstore_faiss.py` (3 fonctions) | `load_pdf_with_metadata()`, AT01 complet | chunk_size sweep {200/600/1500}, MMR vs similarity |
| **AT03 Agent** | `retriever.py` (ensemble), `react_agent.py` (executor) | `tools.py`, `services/`, AT01+02 complets | Ajouter 1 outil custom, mémoire ON/OFF via `gradio_demo.py` |
| **AT04 FT** | Cellules notebook LoRA (Colab), `generate_qa_dataset.py`, `augment_qa_dataset.py` | Dataset base, `explore_dataset.py` | Sur-échantillonnage minorité, LoRA training Colab |
| **AT05 Deploy** | `api/routers/chat.py` (2 fonctions), `api/routers/rag.py` (endpoint) | `api/main.py`, `ui/`, `api/limiter.py` | SSE streaming endpoint, PII scrubbing Langfuse |
| **AT06 RAG vs FT** | `evaluate_pipeline.py` (6 TODOs) | endpoints /rag/evaluate + /chat/compare | Benchmark RAFT, mini-débat FT/RAG/hybride |

---

## Localisation des exercices vibe-coder (index complet)

### Dans GUIDE-ELEVE.md §BONUS de chaque atelier

| Atelier | Défi Bonus 1 | Défi Bonus 2 |
|---|---|---|
| AT01 | Benchmark Sonnet vs Haiku (coût + latence + qualité) | Few-shot prompting (3 exemples → mesure baisse hallucination) |
| AT02 | Sweep chunk_size ∈ {200, 600, 1500} → Recall@5 max | MMR vs similarity sur questions dispersées |
| AT03 | Ajouter `get_indoor_temperature` (outil custom scope-safe) | Mémoire ON vs OFF sur dialogue 3 tours |
| AT04 | Sur-échantillonnage catégorie minoritaire (marketplace) | LoRA training Colab + comparaison avant/après |
| AT05 | SSE streaming `POST /chat/stream` + intégration Streamlit | PII scrubbing avant log Langfuse (RGPD) |
| AT06 | RAFT : argumentaire 5 min adoption/rejet pour HomeButler | Mini-débat en duo FT/RAG/hybride |

### Fichiers standalone

| Fichier | Atelier | Usage |
|---|---|---|
| `ateliers/atelier-03-pipeline-agent/gradio_demo.py` | AT03 | Interface Gradio pour tester mémoire ON/OFF |
| `ateliers/atelier-02-rag-simple/evaluate_rag.py` | AT02 | LLM-judge faithfulness + Recall@k |
| `notebooks/01_llm_baseline.ipynb` | AT01 | Comparatif 3 modèles open-source (Colab uniquement) |
| `notebooks/03_finetuning_lora.ipynb` | AT04 | LoRA training Colab |
| `ateliers/atelier-06-finetune-vs-rag/evaluate_pipeline.py` | AT06 | Benchmark 3 modes (llm_only/rag/agent) |

---

## Actions à effectuer

### Phase 0 — Vérification (avant toute action)

```bash
# Confirmer état réel de chaque branche
for b in student/01-llm-baseline student/02-rag-simple student/03-pipeline-agent student/04-finetuning student/05-deploiement student/06-finetune-vs-rag; do
  echo "=== $b ==="; git -C /Users/yohannravino/Factory/training-rag ls-tree -r $b --name-only | grep -E "\.agent|formateur"
done
```

### Phase 1 — Nettoyage branches student dans training-rag

Pattern par branche (commencer par AT02) :
```bash
git -C /Users/yohannravino/Factory/training-rag checkout student/0X-nom

# Supprimer .agent/tasks/ (si présent confirmé)
git rm -r .agent/tasks/

# Supprimer README-formateur.md
git rm ateliers/atelier-0X-nom/README-formateur.md

# Vérifier avant commit
python -c "import homebutler; print('OK')"
python ateliers/atelier-0X-nom/exercice.py  # doit afficher TODOs, pas d'ImportError

git commit -m "clean(student/0X): retirer .agent/tasks/ et README-formateur.md formateur"
```

Ordre : AT02 → AT01 → AT03 → AT04 → AT05 → AT06

### Phase 2 — Branches solution manquantes

Créer `solution/at04`, `solution/at05`, `solution/at06` en suivant le pattern de `solution/at01` (~30 fichiers).

### Phase 3 — Push remote

```bash
git -C /Users/yohannravino/Factory/training-rag push origin \
  student/01-llm-baseline student/02-rag-simple student/03-pipeline-agent \
  student/04-finetuning student/05-deploiement student/06-finetune-vs-rag
```

### Phase 4 — Documentation formateur (pre-training-rag)

- Ajouter `notes-formateur-vulgarisation.md` au `.gitignore` racine
- Créer `_formateur/DEROULE-FORMATION.md` : antisèche per-atelier
- Créer `_formateur/INDEX-EXTRAS-VIBE.md` : index des exercices bonus

---

## Ce qui ne change PAS (zéro régression)

- `homebutler/`, `api/`, `ui/` — aucun fichier Python modifié
- Les 18 tests bug-hunt (`bugs/test_v1/v2/v3.py`) — intacts (ciblent exclusivement `exercice.py`)
- Les branches `atelier/XX` — le formateur voit tout, non touchées
- `GUIDE-ELEVE.md`, `QUICK-START.md`, `STARTER.md` — conservés tels quels
- `.claude/CLAUDE.md` local + `.cursorrules` par atelier — conservés

---

## Vérification end-to-end

Après nettoyage de chaque branche `student/0X` :

```bash
git -C training-rag checkout student/0X-nom

# 1. Aucun fichier formateur
git ls-tree -r HEAD --name-only | grep -E "\.agent|formateur"
# → vide

# 2. Import package OK
python -c "import homebutler; print('OK')"

# 3. exercice.py se lance
python ateliers/atelier-0X-nom/exercice.py

# 4. Tests bug-hunt dans état attendu
pytest ateliers/atelier-0X-nom/bugs/ -v 2>&1 | head -20
```
