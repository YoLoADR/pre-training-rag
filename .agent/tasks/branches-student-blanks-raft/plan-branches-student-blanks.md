# Plan — Branches `student/XX-…` blank avec indices, dans `training-rag`

> **Révision 2** : intègre les findings des agents d'audit (réalisme technique, trous/régressions, pédagogie). Les corrections clés vs Rev 1 sont **balisées « ⚠️ Rev 1 disait X, on corrige »**.

## Context

La formation RAFT (HomeButler AI) a déjà un système exercice/solution **local à chaque dossier d'atelier** (`pre-training-rag/ateliers/atXX/exercice.py` + `solution.py`) — bon pour les TODOs courts, mais le **projet fil rouge complet** (le code `homebutler/`, `api/`, notebooks, scripts FT) est aujourd'hui livré sous **forme corrigée** sur les 6 branches `atelier/01-llm-baseline` → `atelier/06-finetune-vs-rag` de `/Users/yohannravino/Factory/training-rag/`.

Conséquence : l'élève ouvre une branche d'atelier, voit le code RAG/FT **déjà écrit** et n'a à compléter que le wrapper `exercice.py`. Le cœur métier (chunking, FAISS, ReAct, LoRA) lui arrive cuit — espace ouvert au vibe-coding.

**But du chantier** : produire 6 nouvelles branches `student/01-…` → `student/06-…` dans `training-rag`, dérivées des `atelier/XX-…`, où les fichiers porteurs du concept central de l'atelier en cours sont blankés (corps entiers pour concepts pivots, lignes ciblées pour détails), avec **indices guidants en docstring + commentaires inline** (jamais la réponse). Les branches `atelier/XX-…` actuelles deviennent **la version corrigée** ; la solution se récupère via `git diff student/XX atelier/XX -- <fichier>`.

**Contraintes décidées avec l'utilisateur** :
- Granularité **mixte** : `NotImplementedError` pour concepts pivots, `# TODO (indice: …)` ciblés pour paramètres.
- Indices **inline + docstring enrichie** — pas de fichier d'indices séparé.
- Solution = état des branches `atelier/XX-…` (zéro duplication).
- On ne blanke que la thématique RAG/FT de l'atelier **courant** ; ateliers passés et plomberie Python/web restent corrigés.
- Pour chaque atelier, fournir aux élèves un triplet clair : **état initial / objectif mesurable / recette de cuisine vulgarisée** (tous les termes techniques traduits avec analogie quotidienne).
- Travaux dans `/Users/yohannravino/Factory/training-rag/` uniquement (PAS dans `pre-training-rag/`).

## Approche recommandée

### 1. Cartographie atelier → fichiers à blanker (corrigée après audit)

| AT | Branche source | Fichiers à blanker (corps entier) | Détails ciblés (lignes) | ⚠️ Notes Rev 2 |
|---|---|---|---|---|
| **01** LLM baseline | `atelier/01-llm-baseline` | `homebutler/llm/provider.py` (`get_llm`, `get_llm_cached`), `homebutler/llm/prompts.py` (4 `ChatPromptTemplate` : RAG_QA, BARE_LLM, REACT_SYSTEM, ENERGY_ANALYSIS) | `temperature`, `max_tokens` dans `get_llm` | — |
| **02** RAG simple | `atelier/02-rag-simple` | `homebutler/rag/ingestion.py` (`chunk_fixed_size`, `chunk_recursive`, `chunk_semantic`), **`homebutler/rag/vectorstore_faiss.py`** (`get_embeddings`, `build_faiss_index`, `load_faiss_index`) | `chunk_size`, `chunk_overlap`, `k` | ⚠️ Rev 1 disait `vectorstore.py` — c'est en fait un ré-export 17 lignes. Cible réelle = **`vectorstore_faiss.py`** (71 lignes). |
| **03** Agent + ChromaDB | `atelier/03-pipeline-agent` | `homebutler/agent/react_agent.py` (`get_agent_executor`), `homebutler/rag/retriever.py` (EnsembleRetriever) — **scope réduit** | `weights` BM25/vector, `k` retriever | ⚠️ Rev 1 incluait `tools.py` et `vectorstore_chroma.py` → calibrage 1h40 explose. On **garde `tools.py` corrigé** (l'élève voit le pattern `@tool` LangChain en lecture) ; on blanke uniquement `react_agent.py` + `retriever.py`. `vectorstore_chroma.py` reste corrigé (transposition de FAISS, faible valeur pédagogique nouvelle). |
| **04** Fine-tuning | `atelier/04-finetuning` | `notebooks/03_finetuning_lora.ipynb` (cellules code : `LoraConfig`, `TrainingArguments`, boucle `Trainer`), `scripts/generate_qa_dataset.py` (Alpaca format), `scripts/augment_qa_dataset.py` | `r`, `alpha`, `target_modules`, `learning_rate`, `num_epochs` | — |
| **05** Déploiement | `atelier/05-deploiement` | `api/routers/chat.py` (`_call_rag_only`, `_call_agent`), `api/routers/rag.py` (`/retrieve` endpoint, détection prompt injection) | — | ⚠️ Rev 1 incluait `api/limiter.py` — fichier de **5 lignes** (1 instruction), aucune valeur pédagogique à blanker. **Retiré.** |
| **06** RAG vs FT | `atelier/06-finetune-vs-rag` | **`ateliers/atelier-06-finetune-vs-rag/evaluate_pipeline.py` uniquement** (6 TODOs structurels : construire pipeline_vanilla / pipeline_rag / pipeline_ft, agrégation métriques) | — | ⚠️ Rev 1 incluait deltas `chat.py` et `rag.py` — diff réel AT05→AT06 = **4 lignes** sur `chat.py`, 0 sur `rag.py`. Trop fin. **`evaluate_pipeline.py` seul** porte le concept pédagogique d'AT06. |

**Fichiers explicitement NON blankés** (plomberie, hors-thème, déjà pédagogiques) :
- `homebutler/config.py`, `homebutler/services/{weather,energy,marketplace}.py`
- `api/main.py`, `api/routers/{consumption,orders,products}.py`, `api/limiter.py`
- `ui/*` Streamlit, `Dockerfile`, `docker-compose.yml`, `Modelfile`
- `scripts/{generate_documents,generate_energy_data,generate_producers}.py`
- Notebooks `01_llm_baseline.ipynb`, `02_ingestion_vectorisation.ipynb`
- `ateliers/atelier-0X-*/exercice.py`, `solution.py`, `checkpoints/*`, `bugs/*` (système pédagogique existant — voir §6 pour stratégie cohabitation)

### 1bis. État initial + objectif + recette par atelier

⚠️ **Rev 1 disait : créer un nouveau `MISSION.md`**. L'audit (Agent 3) montre que `ateliers/atelier-XX-*/GUIDE-ELEVE.md` (438 lignes en AT02) **contient déjà** : mission narrative PM, périmètre, carnet de bord avec mini-lexique et analogies, étapes du tronc commun, pièges, erreurs communes. Créer `MISSION.md` en parallèle = duplication + risque de désynchro.

**Décision Rev 2** : **enrichir `GUIDE-ELEVE.md`** existant avec une nouvelle section au tout début, et créer un **`QUICK-START.md` (1 page max)** comme aide-mémoire imprimable.

#### Section à ajouter en tête de chaque `GUIDE-ELEVE.md` (pattern imposé)

```markdown
## 🎯 Atelier XX en un coup d'œil

### État initial (ce qui est déjà là)
- ✅ **Acquis des ateliers précédents** : <liste compacte, ex. AT01 LLM, AT02 RAG FAISS…>
- ✅ **Plomberie fournie** : <ex. config.py, services API, génération données seed>
- 🛠️ **À toi de coder** (fichiers blancs avec indices) :
  - `<chemin>` — fonction `<nom>` (corps entier)
  - `<chemin>` — paramètres ciblés `# TODO`

### Objectif mesurable
À la fin de cet atelier, tu dois pouvoir :
- <action observable 1>
- <action observable 2>
- <action observable 3>

**Critère de succès** (chiffré, reproductible) : <métrique précise + commande pour la mesurer>

### Récupérer la solution (en dernier recours)
\`\`\`bash
git diff student/XX-<thème> atelier/XX-<thème> -- <chemin/du/fichier.py>
\`\`\`
À utiliser **après** avoir essayé les 2 niveaux d'indices et bloqué > 15 min.
```

#### Tableau cartographie état initial / objectif (à expanser dans chaque guide enrichi)

| AT | État initial (déjà là) | Objectif mesurable | Termes prioritaires du lexique |
|---|---|---|---|
| **01** | Squelette projet, `config.py`, deps installées | Lancer une question à Claude, observer hallucination, tempérer | LLM, hallucination, température, system prompt |
| **02** | LLM fonctionnel (AT01), 5 PDF dans `data/raw/` | Indexer PDFs, retrouver chunks pertinents pour 5 questions étalons. **`evaluate_rag.py` affiche Recall@5 ≥ 0.80 ET Faithfulness ≥ 0.85** | chunking récursif, embedding, vector store, FAISS, similarity search, Recall@k, Faithfulness |
| **03** | RAG FAISS (AT02), services métier opérationnels | Agent ReAct qui combine RAG + appel d'outil météo dans une conversation. Test `bugs/test_v1.py` passe vert | agent, ReAct, tool, EnsembleRetriever, BM25, hybrid retrieval |
| **04** | Dataset Q/A généré (`data/qa/`), GPU Colab T4 disponible | Fine-tuner Mistral-7B avec LoRA sur Colab, charger l'adapter, comparer vs base sur 10 questions. Loss train ≤ 1.5 après 3 epochs | LoRA, QLoRA, rank, alpha, format Alpaca, catastrophic forgetting, epoch |
| **05** | Agent fonctionnel (AT03), modèle FT optionnel (AT04) | Exposer le chatbot via FastAPI + UI Streamlit + tracing Langfuse + rate limit. `curl /chat/rag` répond en < 5s | API REST, rate limit, prompt injection, observabilité, trace, span |
| **06** | API complète (AT05) | Comparer 3 stratégies (LLM seul / RAG / RAG+FT) sur benchmark, livrer grille décision TCO. `evaluate_pipeline.py` produit tableau Markdown signé | benchmark, faithfulness, answer relevancy, TCO, RAFT |

⚠️ **Rev 1 disait Recall@3 ≥ 0.7 pour AT02** — l'audit (Agent 3) montre que le standard projet est **Recall@5 ≥ 0.80 + Faithfulness ≥ 0.85** (référence : `evaluate_rag.py` existant + `GUIDE-FORMATEUR.md` AT02 l.387). Aligné.

### 2. Convention des blanks (révisée à 2 niveaux d'indices)

⚠️ **Rev 1 demandait 3 niveaux d'indices**. L'audit (Agent 3) montre que dans 10-15 lignes de docstring, 3 niveaux deviennent redondants. **Rev 2 : 2 niveaux — léger (« quoi chercher ») et fort (« quels arguments / appels »)**.

**Pattern « corps entier »** (concept pivot) :
```python
def chunk_recursive(pages: list[Document], chunk_size: int = 512, chunk_overlap: int = 50) -> list[Document]:
    """Découpe les pages en chunks récursifs (respect des séparateurs naturels).

    Args:
        pages: documents chargés via PyPDFLoader (1 page = 1 Document).
        chunk_size: taille cible du chunk en caractères.
        chunk_overlap: chevauchement entre chunks consécutifs.

    Returns:
        Liste de Document chunkés, métadonnées préservées.

    --- Indice léger ---
    LangChain expose une classe dont le nom commence par `Recursive…Splitter`.
    Le découpage « récursif » signifie : essayer le séparateur le plus large
    (paragraphe), puis plus fin (ligne), puis plus fin encore (espace).

    --- Indice fort ---
    1. Instancie le splitter avec `chunk_size`, `chunk_overlap`, et une liste
       de séparateurs ordonnés du plus large au plus fin : ["\\n\\n", "\\n", ".", " "].
    2. Appelle sa méthode `.split_documents()` sur la liste de pages.
    """
    raise NotImplementedError(
        "Atelier 02 § 2.2 — chunking récursif. "
        "Solution finale : git diff student/02-rag-simple atelier/02-rag-simple -- homebutler/rag/ingestion.py"
    )
```

**Pattern « ligne ciblée »** (paramètre) :
```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size=...,      # TODO (indice : un chunk doit tenir dans le contexte du LLM en gardant marge pour query+answer ; vise 500-1500 caractères)
    chunk_overlap=...,   # TODO (indice : ~10-20% du chunk_size pour préserver la continuité)
    separators=["\n\n", "\n", ".", " "],
)
```

**Règles strictes** :
- Toujours conserver : imports, signatures, type hints, docstring (enrichie).
- `NotImplementedError` **toujours dans le corps de fonction, jamais au top-level** — sinon l'import casse en cascade et empêche tout test de tourner (audit Agent 1).
- Toujours terminer le message d'erreur par le pointeur git diff (l'élève sait comment récupérer la solution si vraiment bloqué).
- Ne **jamais** mentionner le nom de la classe/fonction LangChain finale dans l'indice léger ; le révéler dans l'indice fort.
- Cohérence des analogies avec lexique existant du `GUIDE-FORMATEUR.md` (validée par Agent 3 : embedding = code-barres sémantique, FAISS = bibliothèque par sens, ReAct = détective pense/agit/observe).

### 2bis. Recette de cuisine — exemple validé AT02

À reproduire dans chaque `GUIDE-ELEVE.md` enrichi (section « 🍳 Recette »). Modèle pour AT02 (validé par Agent 3) :

```markdown
## 🍳 Recette de cuisine — 6 étapes

1. **Charger les PDFs** — extraire le texte des notices
   - 🔧 `homebutler/rag/ingestion.py` → `load_pdf_with_metadata` (déjà fourni en lecture)
   - 📖 *metadata* = infos associées au texte (nom du fichier, numéro de page)

2. **Découper en chunks** — transformer pages longues en morceaux indexables
   - 🔧 `homebutler/rag/ingestion.py` → `chunk_recursive` (À COMPLÉTER)
   - 📖 *chunk* = morceau (~500 caractères) · *chunking récursif* = couper aux séparateurs naturels (paragraphe → ligne → phrase) au lieu de trancher brutalement
   - ⚙️ paramètres : `chunk_size=512`, `chunk_overlap=50`

3. **Vectoriser** — transformer chaque chunk en code-barres sémantique
   - 🔧 `homebutler/rag/vectorstore_faiss.py` → `get_embeddings` (À COMPLÉTER)
   - 📖 *embedding* = vecteur de 384 nombres qui résume le sens du texte

4. **Indexer avec FAISS** — bibliothèque ultra-rapide pour chercher par proximité
   - 🔧 `homebutler/rag/vectorstore_faiss.py` → `build_faiss_index` (À COMPLÉTER)
   - 📖 *FAISS* = index qui retrouve les vecteurs les plus proches en quelques ms

5. **Interroger l'index** — récupérer les k chunks les plus pertinents pour une question
   - 🔧 `ateliers/atelier-02-rag-simple/exercice.py` (déjà cadré par TODOs existants)
   - 📖 *similarity search* = calculer la proximité query↔chunks ; `k=4` = retourner 4 chunks

6. **Mesurer la qualité** — Recall@5 + Faithfulness sur 5 questions étalons
   - 🔧 `python ateliers/atelier-02-rag-simple/evaluate_rag.py`
   - 🎯 cible : Recall@5 ≥ 0.80 ET Faithfulness ≥ 0.85
```

Plafond imposé : **6 étapes max** par recette ; si un atelier dépasse, signal de découpage du scope (cas AT03 — voir §1 note).

### 3. Workflow git par atelier

```bash
cd /Users/yohannravino/Factory/training-rag
git checkout atelier/XX-<thème>
git checkout -b student/XX-<thème>
# 1. enrichir ateliers/atelier-XX-*/GUIDE-ELEVE.md (section "en un coup d'œil")
# 2. créer ateliers/atelier-XX-*/QUICK-START.md (1 page)
# 3. blanker les fichiers du §1 (script — voir §5)
# 4. vérifier (voir §7 Vérification)
git add -A
git commit -m "student(atXX): blank <thème> + recette pédagogique vulgarisée"
# Pas de push automatique — voir §8 décisions git
```

Ordre **impératif** : 02 d'abord (atelier pivot — validation du pattern), puis 01, 05, 06, 03, 04. Voir §Ordre d'exécution.

### 4. Outillage anti-vibe-coding sur les branches `student/XX` (nouveau)

⚠️ Audit Agent 2 : le plan Rev 1 oubliait les garde-fous techniques. L'existant `pre-training-rag` impose :
- `.claude/CLAUDE.md` local à chaque dossier d'atelier (interdit explicitement les concepts hors-scope).
- `.cursorrules` (équivalent pour Cursor).
- Hook `UserPromptSubmit` dans `.claude/settings.json` qui injecte un rappel scope-strict à chaque message élève.
- Script `scripts/verify_branch_scope.sh` (581 lignes) — valide automatiquement l'absence de code futur.

**Action Rev 2** : sur chaque branche `student/XX-…`, **conserver à l'identique** les fichiers `.claude/CLAUDE.md`, `.cursorrules`, `.claude/settings.json` déjà présents sur `atelier/XX-…`. Ne pas les modifier sauf pour **enrichir** le CLAUDE.md d'une clause supplémentaire :

> « Si l'élève demande de remplir un `NotImplementedError` ou un `# TODO`, ne fournis JAMAIS le code complet. Réponds en posant une question socratique sur le concept (ex. : "Quel objet LangChain découpe un texte en respectant les séparateurs naturels ?") puis attends sa réponse avant d'aller plus loin. »

**Anti-skip QCM** (audit Agent 3) : enrichir `checkpoints/check_1.py` avec **une question d'explication personnelle** par blank de niveau "corps entier" :
> *« Avant de checker la solution : explique en une phrase ce que fait `RecursiveCharacterTextSplitter` et pourquoi on lui passe une liste de séparateurs. »*

Le checkpoint accepte la réponse si elle contient ≥ 2 mots-clés attendus (`séparateur`, `paragraphe`, `récursif`, `chunk`). Pas parfait, mais oblige verbalisation.

### 5. Méthode de génération des blanks (nouveau)

⚠️ Audit Agent 2 : Rev 1 ne disait pas COMMENT produire les blanks. Décision Rev 2 :

**Hybride manuel + script** :
- **Fichiers Python** (`.py`) : édition **manuelle** via l'outil `Edit`, en suivant un mini-script de validation après chaque fichier :
  ```bash
  python -c "from homebutler.<module> import <fonction>"   # import doit passer
  python -c "from homebutler.<module> import <fonction>; <fonction>(...)" # appel doit lever NotImplementedError
  ```
- **Notebooks `.ipynb`** (`03_finetuning_lora.ipynb`) : **script Python dédié** utilisant `nbformat` pour éditer cellule par cellule sans corrompre le JSON :
  ```python
  # scripts/blank_notebook.py (à créer dans training-rag, sur branche student/04)
  import nbformat
  nb = nbformat.read("notebooks/03_finetuning_lora.ipynb", as_version=4)
  # liste de (cell_index, replacement_source_with_indices)
  blanks = [(7, "# TODO LoraConfig (indice léger: ...)\nraise NotImplementedError(...)"), ...]
  for idx, new_src in blanks:
      nb.cells[idx]["source"] = new_src
      nb.cells[idx]["outputs"] = []
      nb.cells[idx]["execution_count"] = None
  nbformat.write(nb, "notebooks/03_finetuning_lora.ipynb")
  ```
  Le script reste **dans la branche `student/04` uniquement** (pas mergé sur main) — il sert de reproductibilité de la branche.

**Pas de script AST automatique** : trop fragile pour le ROI (6 ateliers, ~15 fichiers au total).

### 6. Cohabitation Bug Hunt + blanks (nouveau, résolution explicite)

⚠️ Audit Agent 2 : Rev 1 reconnaissait le problème sans le résoudre. Le Bug Hunt utilise `bugs/v*.patch` appliqués sur `solution.py`, qui importe depuis `homebutler/*.py`. Si `homebutler/rag/ingestion.py` lève `NotImplementedError`, l'import de `solution.py` réussit mais l'exécution crashe au premier appel.

**Décision Rev 2** : workflow séquentiel **explicite** documenté dans `GUIDE-ELEVE.md` enrichi :

```
ÉTAPE 1 — Remplir les blanks (Tronc commun, ~1h40)
  → Compléter tous les NotImplementedError + # TODO en suivant les indices
  → Validation : `pytest ateliers/atelier-XX-*/` passe vert
  → Tu as maintenant une version fonctionnelle équivalente à atelier/XX-…

ÉTAPE 2 — Bug Hunt (Sprint, ~30min)
  → Appliquer bugs/v1.patch sur ton code complété
  → Lancer test_v1.py (il échoue intentionnellement)
  → Diagnostiquer le bug, répondre au QCM v1_explanation.md
  → Recommencer pour v2, v3
```

**Important** : le `solution.py` du dossier d'atelier (qui sert de cible aux `bugs/v*.patch`) **fonctionnera** uniquement après que l'élève a complété les blanks de `homebutler/*` — par conception, on force l'ordre pédagogique.

### 7. `solution.py` et anti-fraude — décision

⚠️ Audit Agent 2 : `solution.py` reste visible sur `student/XX` → `cat solution.py` = solution livrée gratuitement.

**Décision Rev 2** : **garder `solution.py` visible** sur `student/XX` (cohérent avec branches `atelier/XX` ET la convention existante de `pre-training-rag` qui ne déplace `solution.py` que pour AT01-03 sur des branches `solution/at0X` séparées — pas généralisé). Le risque de fraude est **mitigé pédagogiquement** par :
1. Le QCM "explication personnelle" du `check_1.py` enrichi (§4).
2. Le fait que `solution.py` **importe depuis `homebutler/`** : sur `student/XX`, lancer `solution.py` crashe sur `NotImplementedError` tant que les blanks ne sont pas remplis dans `homebutler/`. L'élève qui `cat solution.py` voit du code qui appelle des fonctions vides — il doit quand même comprendre quoi remplir.
3. Les `checkpoints/check_final.py` LLM-judge évaluent la **qualité explicative** des réponses, pas juste l'output.

Si retour terrain montre que c'est insuffisant, basculer en Rev 3 vers la convention `solution/at0X` (branches séparées).

### 8. Décisions git (nouveau)

| Question | Décision Rev 2 | Raison |
|---|---|---|
| Tags `student-vX.Y` ? | **Non.** Les branches `student/XX-…` sont des branches de référence, pas des releases. | Évite l'inflation de tags ; les `atelier/XX-…` et `v1.X-atelier-0X` portent déjà l'historique. |
| Push sur remote ? | **Oui**, pour que les élèves puissent `git clone && git checkout student/02-…`. | Sans push, distribution = `.zip` ou `.tar.gz` — moins ergonomique. |
| CI sur `student/XX` ? | **Légère** : un workflow GitHub Actions qui lance `scripts/verify_branch_scope.sh` + `python -c "import homebutler"` pour détecter les imports cassés. Pas de `pytest` (qui doit échouer par conception sur les blanks). | Garde la branche démarrable, sans bloquer les `NotImplementedError` attendus. |
| Synchronisation `pre-training-rag` ↔ `training-rag` ? | **Autorité = `training-rag`** pour le code projet (`homebutler/`, `api/`, etc.). `pre-training-rag` reste autorité pour les supports formateur (`docs/`, slides, `.agent/tasks/`). Pas de sync automatique ; PR croisée si correction critique. | Évite la confusion de deux sources de vérité. |

### 9. Onboarding élève (nouveau)

⚠️ Audit Agent 2 : pas de document de démarrage pour l'élève. Action Rev 2 :

Créer **`training-rag/STARTER.md`** (à la racine, sur main et sur toutes les branches) :

```markdown
# Démarrer un atelier (élève)

1. `git clone <repo>`
2. `cd training-rag && python -m venv .venv && source .venv/bin/activate`
3. `git checkout student/01-llm-baseline`  # ou 02, 03, …
4. `pip install -e .`
5. `bash scripts/check_atelier_ready.sh 01`  # vérifie env (clés, modèles, deps)
6. Ouvre `ateliers/atelier-01-llm-baseline/QUICK-START.md` (1 page) puis `GUIDE-ELEVE.md` (complet)
7. Code dans les fichiers marqués 🛠️ "À toi de coder" (cf. section "En un coup d'œil" du guide)
8. Quand bloqué > 15 min : `git diff student/01-llm-baseline atelier/01-llm-baseline -- <fichier>`
```

## Fichiers critiques à modifier

Chemins relatifs à `/Users/yohannravino/Factory/training-rag/`.

**Par branche `student/XX-…`** (code blanks + pédagogie) :

- **student/01** : `homebutler/llm/provider.py`, `homebutler/llm/prompts.py`, `ateliers/atelier-01-llm-baseline/GUIDE-ELEVE.md` (enrichi), `ateliers/atelier-01-llm-baseline/QUICK-START.md` (nouveau), `ateliers/atelier-01-llm-baseline/.claude/CLAUDE.md` (clause socratique ajoutée), `ateliers/atelier-01-llm-baseline/checkpoints/check_1.py` (QCM "explication personnelle")
- **student/02** : `homebutler/rag/ingestion.py`, `homebutler/rag/vectorstore_faiss.py`, + pédagogie idem AT01
- **student/03** : `homebutler/agent/react_agent.py`, `homebutler/rag/retriever.py`, + pédagogie idem AT01
- **student/04** : `notebooks/03_finetuning_lora.ipynb` (via `scripts/blank_notebook.py`), `scripts/generate_qa_dataset.py`, `scripts/augment_qa_dataset.py`, + pédagogie idem AT01
- **student/05** : `api/routers/chat.py`, `api/routers/rag.py`, + pédagogie idem AT01
- **student/06** : `ateliers/atelier-06-finetune-vs-rag/evaluate_pipeline.py`, + pédagogie idem AT01

**Une seule fois sur `main`** :
- `STARTER.md` (nouveau, racine)

**Patterns réutilisés** (depuis l'existant) : analogies du `GUIDE-FORMATEUR.md` AT02 (validées Agent 3), structure `check_1.py` / `check_final.py`, format `bugs/v*.patch`, hook `UserPromptSubmit`, `verify_branch_scope.sh`.

## Vérification end-to-end

Pour chaque branche `student/XX-…` produite, **séquence stricte** :

1. **Imports intacts** (signature des fonctions préservée) :
   ```bash
   python -c "import homebutler; from homebutler.rag import ingestion, vectorstore_faiss; from homebutler.agent import react_agent"
   ```
   Doit charger sans `ImportError`/`NameError`.

2. **Scope strict** :
   ```bash
   bash scripts/verify_branch_scope.sh
   git diff atelier/XX-<thème> student/XX-<thème> --name-only
   ```
   Le diff doit lister **uniquement** les fichiers du §1 + les 4 fichiers pédagogiques (GUIDE-ELEVE, QUICK-START, CLAUDE.md, check_1.py). Rien d'autre.

3. **Tests échouent proprement** :
   ```bash
   pytest -x 2>&1 | tail -20
   ```
   Échecs attendus = `NotImplementedError` sur les fonctions blankées. Pas d'autre type d'erreur.

4. **Récupération solution fonctionne** :
   ```bash
   git diff student/02-rag-simple atelier/02-rag-simple -- homebutler/rag/vectorstore_faiss.py
   ```
   Doit afficher exactement le code attendu côté solution.

5. **Wrapper pédagogique préservé** :
   ```bash
   git diff atelier/XX student/XX -- ateliers/atelier-XX-*/exercice.py ateliers/atelier-XX-*/solution.py ateliers/atelier-XX-*/bugs/
   ```
   Doit être **vide** (zéro modification du système exercice/solution/bug-hunt existant).

6. **Test "recette suffisante" sur AT02** (atelier pivot, avant de répliquer le pattern) :
   - Un dev Python qui n'a jamais fait de RAG, ne connaissant que `GUIDE-ELEVE.md` enrichi + `QUICK-START.md` + indices inline, doit pouvoir compléter `homebutler/rag/ingestion.py` et `vectorstore_faiss.py` en ≤ 1h40 et faire passer `pytest ateliers/atelier-02-rag-simple/`.
   - Si test échoue (concept manquant au lexique, indice fort trop vague) : **réviser AT02 d'abord, puis seulement répliquer sur AT01/03-06**.

7. **Sanity check `solution.py`** (cohabitation §6) :
   ```bash
   python ateliers/atelier-02-rag-simple/solution.py
   ```
   Doit crasher avec `NotImplementedError` (preuve que `solution.py` n'est pas une cheat-sheet exécutable tant que les blanks ne sont pas remplis).

## Risques identifiés et mitigations (consolidés)

| Risque | Mitigation Rev 2 |
|---|---|
| Bug Hunt cassé par blanks | §6 : ordre séquentiel imposé (remplir blanks → puis Bug Hunt). Documenté en tête de `GUIDE-ELEVE.md`. |
| Notebooks JSON corrompus | §5 : script `nbformat` dédié, pas d'`Edit` direct. |
| Effet cascade imports | `NotImplementedError` **toujours en corps de fonction**, jamais au top-level. Vérification §1 du end-to-end. |
| Fraude `cat solution.py` | §7 : `solution.py` importe depuis `homebutler/` blanké donc inutile à copier-coller ; QCM "explication personnelle" dans `check_1.py`. |
| Vibe-coder qui demande à Claude "remplis les TODO" | §4 : CLAUDE.md enrichi avec clause socratique ; hook `UserPromptSubmit` existant. |
| Calibrage AT03 déborde 1h40 | §1 note : scope AT03 réduit à `react_agent.py` + `retriever.py` (tools.py et vectorstore_chroma.py restent corrigés). |
| Désynchro `pre-training-rag` ↔ `training-rag` | §8 : autorité = `training-rag` pour le code projet ; PR croisée manuelle pour corrections. |
| Confusion `MISSION.md` vs `GUIDE-ELEVE.md` | §1bis : Rev 2 abandonne `MISSION.md`, enrichit le `GUIDE-ELEVE.md` existant + `QUICK-START.md` 1 page. Une seule source de vérité. |

## Ordre d'exécution recommandé

1. **AT02 d'abord** (atelier pivot, validation du pattern). Stop si test "recette suffisante" §7.6 échoue.
2. AT01 (le plus simple, valide le pattern sur petit volume).
3. AT05 puis AT06 (continuum déploiement/évaluation).
4. AT03 (calibrage temporel à surveiller).
5. AT04 en dernier (notebook, outillage `nbformat` spécifique).

Sur main : créer `STARTER.md` après que toutes les branches `student/XX-…` existent.
