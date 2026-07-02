# Déroulé formation HomeButler AI RAFT — guide formateur

> **Lis-moi en entier la première fois.** La partie 1 explique l'architecture (sinon le reste paraît magique). La partie 2 explique chaque commande git que tu vas taper. La partie 3 est le script par atelier.
>
> **Parcours avancé optionnel (AT07/08/09) :** ce document couvre les Jours 1-3 (AT01-06). Les 3 modules avancés « industrialisation » (Observabilité & Éval, Optimisation pipeline, Azure AI Search) sont décrits dans **`_formateur/DEROULE-JOUR4-PARCOURS-AVANCE.md`**.

---

# PARTIE 1 — L'architecture en un schéma

## Les deux repos (à ne jamais confondre)

```
┌─────────────────────────────────┐         ┌─────────────────────────────────┐
│  /Factory/pre-training-rag      │         │  /Factory/training-rag          │
│  ───────────────────────        │         │  ──────────────────────         │
│  🔒 ZONE FORMATEUR (= toi)      │         │  📚 ZONE ÉLÈVE                  │
│                                 │         │                                 │
│  • slides/*-corrige.md          │         │  • homebutler/ (le code)        │
│  • slides/*-blank.md            │         │  • ateliers/atelier-0X-*/       │
│  • _formateur/DEROULE...md      │         │  • api/ ui/                     │
│  • notes-formateur-vulg...md    │         │                                 │
│  • draft.md                     │         │  GitHub : YoLoADR/training-rag  │
│                                 │         │  ← les élèves clonent CELUI-CI  │
└─────────────────────────────────┘         └─────────────────────────────────┘
```

**Tu travailles dans les deux** :
- `pre-training-rag` quand tu prépares les slides, prends des notes, écris ce déroulé
- `training-rag` quand tu démos du code en live ou récupères une correction

**Les élèves ne voient que `training-rag`.** Ils ne savent même pas que `pre-training-rag` existe.

---

## Les branches dans `training-rag` (le repo élève)

```
training-rag/
│
├── atelier/01-llm-baseline      ─┐
├── atelier/02-rag-simple         │  6 branches CORRIGÉES (formateur)
├── atelier/03-pipeline-agent     │  → toi tu y vas pour la démo live
├── atelier/04-finetuning         │  → l'élève NE BASCULE JAMAIS dessus
├── atelier/05-deploiement        │     (sauf pour récupérer une correction)
├── atelier/06-finetune-vs-rag   ─┘
│
├── student/01-llm-baseline      ─┐
├── student/02-rag-simple         │  6 branches BLANKÉES (élèves)
├── student/03-pipeline-agent     │  → les élèves codent ICI
├── student/04-finetuning         │  → toi tu y vas pour vérifier ce qu'ils voient
├── student/05-deploiement        │
└── student/06-finetune-vs-rag   ─┘
```

**La même fonction (ex: `get_llm()`) existe sur les 2 branches :**

| Branche | Contenu de `get_llm()` | Lance ? |
|---|---|---|
| `atelier/01-llm-baseline` | Code corrigé complet (~15 lignes Python) | ✅ |
| `student/01-llm-baseline` | `raise NotImplementedError("Atelier 01 § 2.1 — ...")` | ❌ crash volontaire |

L'élève lit la docstring + indices, puis remplit le corps. Quand il a fini, son `get_llm()` ressemble à celui de la branche atelier (sans être identique — chemins multiples OK).

---

## Anatomie d'une branche `student/0X`

Voici ce qu'un élève voit quand il fait `git checkout student/01-llm-baseline` :

```
training-rag/                                    ← racine du repo
│
├── STARTER.md                                   ← 1ère page que l'élève lit (8 étapes onboarding)
├── PREREQUIS-FORMATION-RAFT.md                  ← liste deps + clés API à préparer AVANT la session
├── requirements_atelier01.txt                   ← pip install -r ...
│
├── homebutler/                                  ← LE PACKAGE QUE L'ÉLÈVE FAIT TOURNER
│   ├── config.py                                ← fourni complet (ne touche pas)
│   ├── llm/
│   │   ├── provider.py    ← 🛠️ ICI L'ÉLÈVE CODE (get_llm, get_llm_cached)
│   │   └── prompts.py     ← 🛠️ ICI L'ÉLÈVE CODE (4 templates)
│   ├── rag/                                     ← fourni blanké à partir de AT02
│   ├── agent/                                   ← fourni blanké à partir de AT03
│   └── services/                                ← fourni complet (météo, énergie, marketplace)
│
└── ateliers/
    └── atelier-01-llm-baseline/
        ├── QUICK-START.md         ← recette 6 étapes "tu es perdu ? regarde ça"
        ├── GUIDE-ELEVE.md         ← brief complet : mission, carnet de bord, exercices, bonus
        │
        ├── exercice.py            ← 🎯 LE FICHIER QUE L'ÉLÈVE LANCE
        │                            (importe homebutler/, donc plante tant que homebutler/
        │                             contient des NotImplementedError)
        │
        ├── solution.py            ← ⚠️ EXPLICATION CI-DESSOUS
        │
        ├── bugs/                  ← BUG HUNT (Sprint après le Core)
        │   ├── v1.patch           ← patch qui introduit le bug v1 dans exercice.py
        │   ├── v2.patch           ← idem v2
        │   ├── v3.patch           ← idem v3
        │   ├── test_v1.py         ← test pytest qui FAIL tant que v1 pas réparé
        │   ├── test_v2.py
        │   └── test_v3.py
        │
        └── checkpoints/           ← scripts de vérif manuels (check_1.py, check_final.py)
```

---

## "Pourquoi `solution.py` est sur student/0X ? Ça ne triche pas ?"

C'est la question qui m'a embrouillé dans le doc précédent. Réponse claire :

```
solution.py présent sur student/01-llm-baseline
  │
  ├── Il existe physiquement (~50 lignes Python)
  │
  ├── Si l'élève fait `python solution.py` →
  │     ImportError ou NotImplementedError car solution.py
  │     IMPORTE depuis homebutler/llm/provider.py
  │     qui contient encore `raise NotImplementedError(...)`
  │
  └── Donc : visible mais INUTILISABLE tant que l'élève
             n'a pas rempli ses blanks dans homebutler/
```

**Conséquence pédagogique :**
- L'élève PEUT lire `solution.py` (c'est moins de 50 lignes, c'est une orchestration)
- L'élève NE PEUT PAS s'en servir comme béquille pour sauter le travail
- Tu n'as pas à le supprimer ni à le cacher → feature, pas bug

**Quand l'élève va-t-il s'en servir ?** Jamais directement. Il sert juste à montrer le pattern attendu (boucler sur 10 questions, mesurer hallucination rate, etc.) — c'est de la doc exécutable.

---

# PARTIE 2 — Les 5 commandes git que tu vas taper (et pourquoi)

## Commande 1 : basculer sur la version corrigée pour la démo

```bash
cd /Users/yohannravino/Factory/training-rag
git checkout atelier/01-llm-baseline
```

**Quand ?** Juste avant la démo live (T+30 min). Tu projettes ton terminal, tu tapes ça.

**Pourquoi ?** Pour avoir le code complet sous les yeux. Ouvrir `homebutler/llm/provider.py` et `homebutler/llm/prompts.py` → voir les fonctions remplies. Tu vas montrer aux élèves "voici à quoi ça ressemble une fois fini" — sans coder en live (= sans risque de bug à 9h du matin devant 15 personnes).

**Ce que je voulais dire par "Ouvrir solution.py + montrer 1-2 fonctions clés en lecture (pas de live-typing)" :**
- Tu OUVRES le fichier (cmd+P → solution.py)
- Tu SCROLLES jusqu'à la fonction principale
- Tu LIS à voix haute en pointant les lignes
- Tu NE TYPES PAS du code à la volée (= live-coding = risqué, lent, distrait)

## Commande 2 : voir ce que les élèves voient

```bash
git checkout student/01-llm-baseline
```

**Quand ?** Quand un élève t'appelle "j'ai un message d'erreur bizarre" — tu basules sur student/0X pour voir EXACTEMENT le même code que lui.

**Pourquoi ?** Si tu restes sur `atelier/01-llm-baseline` (la version corrigée), tu ne vois pas son problème : chez lui `get_llm()` est blanké, chez toi non.

## Commande 3 : montrer la correction à un élève bloqué

```bash
git diff student/01-llm-baseline atelier/01-llm-baseline -- homebutler/llm/provider.py
```

**Quand ?** Un élève a essayé 20 min, lu les 2 niveaux d'indices, et il est toujours bloqué. Tu lui montres CETTE commande à taper sur son terminal.

**Ce que ça fait :** affiche les différences entre sa version (blanké) et la version corrigée — donc le code qu'il aurait dû écrire. C'est mieux que `cat solution.py` parce que :
- Ça pointe exactement les lignes manquantes
- Ça respecte le format que tu lui as enseigné
- Ça lui apprend `git diff`, une compétence pro

**Important :** ne tape PAS cette commande sur ton terminal pour lui montrer — tape-la sur LE SIEN, en t'asseyant à côté. Sinon les autres élèves voient la correction projetée.

## Commande 4 : récupérer le fichier corrigé d'un coup (rare)

```bash
git checkout atelier/01-llm-baseline -- ateliers/atelier-01-llm-baseline/solution.py
```

**Quand ?** Fin de session, tu veux distribuer la correction à toute la classe. Mais en pratique on s'en sert peu — `git diff` (Commande 3) suffit dans 95% des cas.

## Commande 5 : pour les élèves au démarrage de chaque atelier

```bash
git checkout student/01-llm-baseline
cat ateliers/atelier-01-llm-baseline/QUICK-START.md
```

**Ce que tu annonces au passage de relais (= quand tu rends la main aux élèves) :**

> « Pour démarrer l'atelier 1, vous tapez ces deux commandes : `git checkout student/01-llm-baseline`, puis vous lisez `QUICK-START.md`. Si vous restez bloqués 15 minutes, vous levez la main. »

Tu les écris au tableau ou dans le chat de session. Ce sont les SEULES commandes qu'un élève a besoin de retenir pour démarrer.

---

# PARTIE 3 — Le déroulé par atelier (~3h30 chacun)

## Structure invariante de toute demi-journée

```
00:00 ─┬─ Slides projetées (30 min)
       │  Tu projettes slides/atelier-0X-corrige.md
       │  Tu poses les concepts (temperature, RAG, agent, etc.)
       │
00:30 ─┼─ Démo live (20 min)
       │  Tu es sur git checkout atelier/0X-nom
       │  Tu OUVRES (pas live-code) 1-2 fonctions clés
       │  Tu lances la solution une fois, tu pointes le résultat
       │
00:50 ─┼─ Passage de relais (5 min)
       │  Tu écris au tableau les 2 commandes (git checkout student/0X + cat QUICK-START)
       │  Tu rappelles le critère de succès chiffré
       │  Tu rappelles la règle "15 min bloqué → main levée"
       │
00:55 ─┼─ Élèves codent : Core (1h40)
       │  Tu circules. Tu réponds aux mains levées.
       │  Tu utilises Commande 2 (basculer student/0X) + Commande 3 (git diff) pour débloquer.
       │
02:35 ─┼─ Bug Hunt (30 min)
       │  Voir détail spécifique en bas de cet atelier.
       │
03:05 ─┼─ Bonus (optionnel, 25 min)
       │  Tu pointes _formateur/INDEX-EXTRAS-VIBE.md §AT0X
       │
03:30 ── Fin
```

---

## AT01 — LLM Baseline

**Mission élève :** poser 10 questions à un LLM, mesurer un `hallucination_rate ≥ 80 %` sur les 5 questions privées.

**Fichiers que l'élève complète :**
- `homebutler/llm/provider.py` → `get_llm()`, `get_llm_cached()`
- `homebutler/llm/prompts.py` → 4 templates ChatPromptTemplate

### T+0 — Slides (30 min)
- Projeter `slides/atelier-01-corrige.md` (depuis `pre-training-rag/slides/`)
- Concepts à enfoncer : `temperature`, `system prompt`, `hallucination`, différence Claude/Ollama

### T+30 — Démo live (20 min)
```bash
git checkout atelier/01-llm-baseline
```
- Ouvre `homebutler/llm/provider.py` → montre `get_llm()` (15 lignes). Pointe `temperature=0` et `max_tokens=1024`.
- Ouvre `homebutler/llm/prompts.py` → montre `CONCIERGE_SYSTEM_PROMPT` (déjà fourni). Pointe le "tu n'inventes JAMAIS de données privées".
- Lance :
  ```bash
  python ateliers/atelier-01-llm-baseline/exercice.py
  ```
- Quand l'output sort, pointe `hallucination_rate: 0.85`. Dis : « On a chiffré l'échec, c'est ça la mission de l'atelier. »

### T+50 — Passage de relais (5 min)
Écris au tableau :
```bash
git checkout student/01-llm-baseline
cat ateliers/atelier-01-llm-baseline/QUICK-START.md
python ateliers/atelier-01-llm-baseline/exercice.py   # va crash, c'est normal
```
Annonce : **« 1h40 pour Core. Critère : hallucination rate ≥ 80 %. Bloqué 15 min → main levée. »**

### T+55 — Core élève (1h40)
Tu circules. Signaux à guetter :
- Élève figé sur `get_llm()` > 10 min → lui dire « relis l'indice léger dans la docstring, c'est `ChatAnthropic` ou `ChatOllama` selon `config.LLM_PROVIDER` »
- Élève qui ouvre `solution.py` pour copier-coller → « ferme ça, tu n'apprends rien. Lis l'indice fort d'abord. »
- Élève qui a fini en < 1h → pointe `GUIDE-ELEVE.md §BONUS` (benchmark Sonnet vs Haiku ou few-shot)

### T+2h35 — Bug Hunt (30 min)
**Tu annonces oralement :**
> « Maintenant Bug Hunt. Vous allez appliquer 3 patches qui introduisent des bugs réalistes dans votre `exercice.py`. Pour chacun : `git apply bugs/v1.patch`, vous lancez `pytest bugs/test_v1.py`, le test va FAIL, vous lisez l'erreur et vous corrigez. »

Tu écris au tableau :
```bash
git apply ateliers/atelier-01-llm-baseline/bugs/v1.patch
pytest ateliers/atelier-01-llm-baseline/bugs/test_v1.py -v
# débugue jusqu'à PASS
git checkout ateliers/atelier-01-llm-baseline/exercice.py   # reset pour v2
git apply ateliers/atelier-01-llm-baseline/bugs/v2.patch
# etc.
```

Bugs introduits sur AT01 :
- v1 : `temperature=2.0` (au lieu de 0) — output devient incohérent
- v2 : `max_tokens=50` (au lieu de 1024) — réponses tronquées
- v3 : pas de `system message` — le LLM oublie qu'il est concierge

**Si un élève n'arrive pas à débugger v1 après 8 min** : tape sur SON terminal `git diff` entre son exercice patché et la version pre-patch. La diff lui montre où regarder.

---

## AT02 — RAG Simple FAISS

**Mission élève :** indexer le corpus HomeButler dans FAISS, mesurer `Recall@5 ≥ 0.80`.

---

### Carte des blancs — `student/02-rag-simple`

> **Comment s'y retrouver :** `git checkout student/02-rag-simple` puis ouvre les fichiers ci-dessous. Les `raise NotImplementedError` sont dans `homebutler/` (la bibliothèque), PAS dans `exercice.py`.

#### `homebutler/rag/ingestion.py`

| Ligne | Fonction | Ce que l'élève doit écrire | Pourquoi c'est important |
|-------|----------|---------------------------|--------------------------|
| ~85 | `chunk_fixed_size()` | Instancier `CharacterTextSplitter(chunk_size=..., chunk_overlap=..., separator="\n", length_function=len)` puis `.split_documents(documents)` | Découpage naïf : ignore la structure du texte. Sert de baseline pour montrer que le chunking a un impact sur le Recall. |
| ~122 | `chunk_recursive()` | Instancier `RecursiveCharacterTextSplitter(chunk_size=..., chunk_overlap=..., separators=["\n\n", "\n", ".", "!", "?", " ", ""])` | **La stratégie recommandée.** L'ordre des séparateurs est critique : on coupe d'abord aux paragraphes, puis aux phrases — on préserve le sens. |
| ~166 | `chunk_semantic()` | Importer `SemanticChunker` depuis `langchain_experimental`, appeler `.create_documents(texts, metadatas=metadatas)` | Coupe selon la rupture sémantique (embedding distance). Plus lent mais pertinent pour des docs hétérogènes. Bonus niveau avancé. |

#### `homebutler/rag/vectorstore_faiss.py`

| Ligne | Fonction | Ce que l'élève doit écrire | Pourquoi c'est important |
|-------|----------|---------------------------|--------------------------|
| ~51 | `get_embeddings()` | `return FastEmbedEmbeddings(model_name=EMBEDDING_MODEL)` (1 ligne) | L'embedding transforme le texte en vecteur numérique. On utilise `fastembed` local (0 GPU, 0 API). Sans ça, FAISS ne peut pas indexer. |
| ~98 | `build_faiss_index()` | Vérifier si l'index existe déjà (`force_rebuild`), sinon : `FAISS.from_documents(documents, embeddings)` puis `.save_local(path)` | Persiste l'index sur disque — sinon il faut reconstruire à chaque démarrage (lent, coûteux). |
| ~125 | `load_faiss_index()` | `FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)` | `allow_dangerous_deserialization=True` est obligatoire avec FAISS ≥ 1.7. C'est un choix délibéré (environnement maîtrisé). |

---

### Démo live (T+30)

```bash
git checkout atelier/02-rag-simple
# Sur atelier/02, homebutler/ est complet → solution.py tourne
python scripts/generate_documents.py          # génère les 6 PDFs (fpdf2, 0 API)
python ateliers/atelier-02-rag-simple/solution.py
```

- Ouvre `homebutler/rag/ingestion.py` → montre `chunk_recursive()` (lignes ~100-130). Insiste sur l'ordre des séparateurs `["\n\n", "\n", ". ", " "]` → coupe aux paragraphes d'abord, jamais en plein mot.
- Quand `solution.py` tourne, pointe le tableau comparatif chunks_fixed vs chunks_recursive + le `Recall@5: 0.83` final.

> **Note :** c'est `solution.py` que tu lances, pas `exercice.py`. `exercice.py` contient les TODOs de l'élève avec `raise NotImplementedError` — il ne tourne jamais tel quel, même sur les branches atelier/.

### Passage de relais

```bash
git checkout student/02-rag-simple
cat ateliers/atelier-02-rag-simple/QUICK-START.md
python ateliers/atelier-02-rag-simple/exercice.py    # va crash → normal, c'est leur point de départ
```

### Pièges à anticiper

- `ModuleNotFoundError: No module named 'fitz'` → `pip install pymupdf==1.25.1` (s'importe `import fitz`)
- Mac ARM : il faut `faiss-cpu` (pas `faiss-gpu`). Si erreur segfault → `pip uninstall faiss-gpu && pip install faiss-cpu`
- Embeddings : `fastembed` (`all-MiniLM-L6-v2` local, ~300 Mo DL au premier lancement dans `~/.cache/fastembed/`)

---

### Bug Hunt AT02 — script complet formateur

**Contexte :** les patches sont dans `ateliers/atelier-02-rag-simple/bugs/`. Ils modifient **`solution.py`** (pas `exercice.py`). L'élève applique chaque patch sur la solution complète, observe le symptôme, corrige.

**Tu écris au tableau :**

```bash
# ─── Bug v1 ───────────────────────────────────────────────────────────
git apply ateliers/atelier-02-rag-simple/bugs/v1.patch
pytest ateliers/atelier-02-rag-simple/bugs/test_v1.py -v     # FAIL → trouve pourquoi
# Correction trouvée ? Reset :
git checkout ateliers/atelier-02-rag-simple/solution.py

# ─── Bug v2 ───────────────────────────────────────────────────────────
git apply ateliers/atelier-02-rag-simple/bugs/v2.patch
pytest ateliers/atelier-02-rag-simple/bugs/test_v2.py -v
git checkout ateliers/atelier-02-rag-simple/solution.py

# ─── Bug v3 ───────────────────────────────────────────────────────────
git apply ateliers/atelier-02-rag-simple/bugs/v3.patch
pytest ateliers/atelier-02-rag-simple/bugs/test_v3.py -v
git checkout ateliers/atelier-02-rag-simple/solution.py
```

| Patch | Fichier modifié | Ligne modifiée | Bug introduit | Symptôme observable | Ce que l'élève doit trouver |
|-------|----------------|----------------|---------------|---------------------|-----------------------------|
| v1 | `solution.py` | ~72-73 | `chunk_size=2000` au lieu de `512` | Recall@5 chute (chunks trop gros → mauvaise granularité) | Remettre `chunk_size=512` |
| v2 | `solution.py` | ~72-73 | `chunk_overlap=0` au lieu de `50` | Perte d'info aux frontières de chunk → Recall@5 < 0.80 | Remettre `chunk_overlap=50` |
| v3 | `solution.py` | ~133 | `force_rebuild=True` dans la boucle benchmark | Le script tourne mais est 5x plus lent (reconstruction à chaque question) | Sortir `build_faiss_index(...)` de la boucle |

**Pourquoi ces 3 bugs :** ce sont des erreurs de configuration réelles. En prod, chunk_size trop grand est l'erreur #1 des juniors. chunk_overlap=0 est un oubli fréquent. force_rebuild en boucle est un anti-pattern performance classique.

---

## AT03 — Pipeline Agent ReAct

**Mission élève :** agent ReAct avec 4 outils + retriever hybride FAISS 60% / Chroma 40% + mémoire conversationnelle.

---

### Carte des blancs — `student/03-pipeline-agent`

> **Pré-requis pour que l'élève puisse tester :** les deux index doivent exister (`data/faiss_index/` et `data/chroma_db/`). L'index FAISS vient d'AT02. Pour Chroma, lancer avant de donner la main :
> ```bash
> python -c "
> import os; from homebutler import config
> from homebutler.rag.ingestion import load_pdf_with_metadata, chunk_recursive
> from homebutler.rag.vectorstore_chroma import build_chroma_db
> pages = []
> [pages.extend(load_pdf_with_metadata(os.path.join(config.DOCUMENTS_DIR, f)))
>  for f in sorted(os.listdir(config.DOCUMENTS_DIR)) if f.endswith('.pdf')]
> build_chroma_db(chunk_recursive(pages)); print('ChromaDB OK')
> "
> ```

#### `homebutler/rag/retriever.py`

| Ligne | Fonction | Ce que l'élève doit écrire | Pourquoi c'est important |
|-------|----------|---------------------------|--------------------------|
| ~80 | `get_ensemble_retriever()` | Récupérer `faiss_retriever` (via `load_faiss_index().as_retriever(k=faiss_k)`) + `chroma_retriever` (via `get_chroma_retriever(k=chroma_k)`), puis `EnsembleRetriever(retrievers=[faiss_r, chroma_r], weights=[0.6, 0.4])` | FAISS seul rate les questions où le vocabulaire diverge des chunks. Chroma compense. L'EnsembleRetriever avec poids 60/40 améliore le Recall@5 de ~8 points. |

#### `homebutler/agent/react_agent.py`

| Ligne | Fonction | Ce que l'élève doit écrire | Pourquoi c'est important |
|-------|----------|---------------------------|--------------------------|
| ~126 | `get_agent_executor()` | `llm = get_llm()`, `prompt = hub.pull("hwchase17/react")`, `agent = create_react_agent(llm, tools, prompt)`, `AgentExecutor(agent=agent, tools=tools, max_iterations=8, handle_parsing_errors=True, verbose=True)` | `max_iterations=8` est le garde-fou : sans lui, l'agent boucle indéfiniment sur une question difficile. `handle_parsing_errors=True` évite le crash si le LLM produit un output ReAct mal formé. |

**Fichiers fournis (PAS à coder) :**
- `homebutler/agent/tools.py` → les 4 outils (`search_home_docs`, `analyze_energy_consumption`, `find_local_products`, `get_weather_forecast`). **Montre-les en démo, ne les fais pas coder.**

---

### Démo live (T+30)

```bash
git checkout atelier/03-pipeline-agent
ANONYMIZED_TELEMETRY=false python ateliers/atelier-03-pipeline-agent/solution.py
```

- Ouvre `homebutler/agent/tools.py` → montre les 4 fonctions décorées `@tool`. Insiste sur **la description** : c'est ce que le LLM lit pour décider quel outil appeler. Une description floue = outil ignoré.
- Ouvre `homebutler/agent/react_agent.py` → montre `get_agent_executor()` complet. Pointe `max_iterations=8` et `handle_parsing_errors=True`.
- Quand `solution.py` tourne, pointe la **trace ReAct** : `Step 1 → Action: get_weather_forecast`, `Step 2 → Action: search_home_docs`, etc. Dis : « L'agent décide lui-même de l'ordre. »

> **Note :** c'est `solution.py` que tu lances, pas `exercice.py`.

### ⚠️ Piège typique AT03 : rate limit Anthropic

- Tier 1 : 50 req/min. L'agent fait 5-10 appels par question. Une classe de 15 → blocage massif.
- **Solution préemptive :** avant de donner la main, demande aux élèves : `LLM_PROVIDER=ollama` dans `.env`. Ollama local = 0 rate limit.
- Si déjà bloqué : attendre 60 s ou switcher. Message d'erreur : `RateLimitError: 429`.

---

### Bug Hunt AT03 — script complet formateur

**Contexte :** les patches modifient des fichiers dans `homebutler/` (pas `solution.py`). Reset après chaque bug : `git checkout homebutler/agent/tools.py` ou `homebutler/agent/react_agent.py`.

**Tu écris au tableau :**

```bash
# ─── Bug v1 ───────────────────────────────────────────────────────────
git apply ateliers/atelier-03-pipeline-agent/bugs/v1.patch
# Lance solution.py et observe la qualité de la réponse (dégradation visible)
pytest ateliers/atelier-03-pipeline-agent/bugs/test_v1.py -v     # FAIL
# Reset :
git checkout homebutler/agent/tools.py

# ─── Bug v2 ───────────────────────────────────────────────────────────
git apply ateliers/atelier-03-pipeline-agent/bugs/v2.patch
pytest ateliers/atelier-03-pipeline-agent/bugs/test_v2.py -v
git checkout homebutler/agent/tools.py

# ─── Bug v3 ───────────────────────────────────────────────────────────
git apply ateliers/atelier-03-pipeline-agent/bugs/v3.patch
pytest ateliers/atelier-03-pipeline-agent/bugs/test_v3.py -v
git checkout homebutler/agent/react_agent.py
```

| Patch | Fichier modifié | Ligne modifiée | Bug introduit | Symptôme observable | Ce que l'élève doit trouver |
|-------|----------------|----------------|---------------|---------------------|-----------------------------|
| v1 | `homebutler/agent/tools.py` | ~26-32 | Description de `search_home_docs` remplacée par `"cherche des documents"` | L'agent n'appelle plus l'outil RAG sur les questions logement → réponses inventées | Restaurer la vraie description (`search_home_docs : ...`) |
| v2 | `homebutler/agent/tools.py` | ~131-148 | 10 outils inutiles ajoutés à `ALL_TOOLS` (14 outils au lieu de 4) | Latence x3, trace ReAct incohérente, l'agent hésite entre les outils | Retirer les 10 outils fantômes de `ALL_TOOLS` |
| v3 | `homebutler/agent/react_agent.py` | ~94 | `max_iterations=8` supprimé de `AgentExecutor` | Sur une question complexe, l'agent boucle indéfiniment (timeout ou crash) | Rajouter `max_iterations=8` |

**Pourquoi ces 3 bugs :** v1 = la description d'outil est la seule interface entre le LLM et le code — c'est du prompt engineering. v2 = le "tool explosion" est un vrai problème de scaling. v3 = oublier max_iterations est l'erreur #1 en prod avec les agents.

---

## AT04 — Fine-tuning LoRA / QLoRA

**⚠️ Particularité majeure AT04 :** **PAS d'`exercice.py`**. Les scripts locaux (`prepare_dataset.py`, `explore_dataset.py`) testent la préparation des données. Le fine-tuning lui-même se fait dans un notebook Google Colab (GPU T4 gratuit obligatoire).

**Mission élève :** fine-tuner Mistral-7B sur dataset HomeButler via LoRA, comparer perplexité avant/après.

---

### Carte des blancs — `student/04-finetuning`

> Les `NotImplementedError` sont dans `scripts/` (PAS dans le notebook). Le notebook `03_finetuning_lora.ipynb` est fourni complet — l'élève doit seulement le lire et le lancer cellule par cellule.

#### `scripts/generate_qa_dataset.py`

| Ligne | Fonction | Ce que l'élève doit écrire | Pourquoi c'est important |
|-------|----------|---------------------------|--------------------------|
| ~338 | `generate()` | Créer le dossier `OUTPUT_DIR`, itérer sur `ALL_PAIRS`, classifier chaque paire via `_classify()`, écrire chaque ligne en JSON (format Alpaca : `{"instruction": "...", "input": "...", "output": "...", "category": "..."}`) dans `OUTPUT_FILE`, afficher le résumé par catégorie | Le dataset est le carburant du fine-tuning. Format Alpaca = convention instruction-tuning : le modèle apprend `instruction + input → output`. Sans catégories, pas de diagnostic déséquilibre. |

#### `scripts/augment_qa_dataset.py`

| Ligne | Fonction | Ce que l'élève doit écrire | Pourquoi c'est important |
|-------|----------|---------------------------|--------------------------|
| ~137 | `paraphrase_question()` | Générer 0-2 variantes de la question : variante 1 via `_apply_first_matching_rewrite(q)`, variante 2 en ajoutant un préfixe "locataire" + suffixe formel. Utiliser `random.Random(seed)` pour la reproductibilité. Retourner `variants[:2]` (jamais l'original, pas de doublons) | L'augmentation multiplie la diversité sans API. Un dataset augmenté 2x améliore la généralisation du modèle. Le seed garantit la reproductibilité entre runs. |

**Fichiers fournis (PAS à coder) :**
- `notebooks/03_finetuning_lora.ipynb` → le notebook Colab complet. L'élève le lit et l'exécute, il ne le modifie pas.
- `ateliers/atelier-04-finetuning/prepare_dataset.py` → script d'analyse du dataset (split 80/10/10, stats). Fourni complet.
- `ateliers/atelier-04-finetuning/explore_dataset.py` → exploration visuelle. Fourni complet.

---

### Démo live (T+30)

```bash
git checkout atelier/04-finetuning

# ─── Montrer les scripts dataset (local, 0 GPU) ───────────────────────
python scripts/generate_qa_dataset.py    # génère data/qa_dataset/concierge_qa.jsonl
python ateliers/atelier-04-finetuning/prepare_dataset.py   # montre le split + stats catégories

# ─── Montrer le notebook (Colab) ─────────────────────────────────────
# Ouvre Google Colab → upload notebooks/03_finetuning_lora.ipynb
# Runtime → Change runtime type → T4 GPU
```

- Ouvre `scripts/generate_qa_dataset.py` → montre les 150 paires Q/R + la fonction `_classify()`. Dis : « Ce dataset simule ce qu'un vrai HomeButler saurait répondre. »
- Dans le notebook : montre `BitsAndBytesConfig(load_in_4bit=True, ...)` → explique QLoRA = quantization 4-bit (Mistral tient en RAM) + LoRA = adapters (on n'entraîne que ~1% des paramètres).
- Montre `LoraConfig(r=8, lora_alpha=16, ...)` → explique `r` = rang = taille de l'adapter. Plus grand = plus expressif, mais plus lent.
- Lance **UNE seule cellule** training (10 steps) pour montrer que ça avance. **Ne pas lancer le training complet** (20 min).

### Passage de relais — différent ici

> « Vous ouvrez `notebooks/03_finetuning_lora.ipynb` dans Google Colab. Runtime → Change runtime type → T4 GPU. Lancez cellule par cellule. Les 2 seules choses à coder : `scripts/generate_qa_dataset.py` → fonction `generate()`, et `scripts/augment_qa_dataset.py` → fonction `paraphrase_question()`. Le training prend ~20 min sur T4. »

---

### Bug Hunt AT04 — script complet formateur

**Contexte :** les patches modifient `ateliers/atelier-04-finetuning/prepare_dataset.py`. Reset : `git checkout ateliers/atelier-04-finetuning/prepare_dataset.py`.

```bash
# ─── Bug v1 ───────────────────────────────────────────────────────────
git apply ateliers/atelier-04-finetuning/bugs/v1.patch
python ateliers/atelier-04-finetuning/prepare_dataset.py
pytest ateliers/atelier-04-finetuning/bugs/test_v1.py -v     # FAIL
git checkout ateliers/atelier-04-finetuning/prepare_dataset.py

# ─── Bug v2 ───────────────────────────────────────────────────────────
git apply ateliers/atelier-04-finetuning/bugs/v2.patch
python ateliers/atelier-04-finetuning/prepare_dataset.py
pytest ateliers/atelier-04-finetuning/bugs/test_v2.py -v
git checkout ateliers/atelier-04-finetuning/prepare_dataset.py

# ─── Bug v3 ───────────────────────────────────────────────────────────
git apply ateliers/atelier-04-finetuning/bugs/v3.patch
python ateliers/atelier-04-finetuning/prepare_dataset.py
pytest ateliers/atelier-04-finetuning/bugs/test_v3.py -v
git checkout ateliers/atelier-04-finetuning/prepare_dataset.py
```

| Patch | Fichier modifié | Ligne modifiée | Bug introduit | Symptôme observable | Ce que l'élève doit trouver |
|-------|----------------|----------------|---------------|---------------------|-----------------------------|
| v1 | `prepare_dataset.py` | ~43-52 | `categorize()` retourne `"autres"` pour toutes les catégories | 100% des paires classées "autres", 0 dans les vraies catégories | Rétablir les 4 `return "équipements"/"droits"/"énergie"/"marketplace"` |
| v2 | `prepare_dataset.py` | ~8 (top) | `LEARNING_RATE = 1e-2` ajouté au module | Le script tourne mais le LR affiché est 100x trop grand (divergence garantie) | Supprimer la ligne `LEARNING_RATE = 1e-2` (valeur réelle : 1e-4 à 1e-5) |
| v3 | `prepare_dataset.py` | ~79-80 | `n_train = n`, `n_val = 0` (100/0/0 au lieu de 80/10/10) | Split : train=150, val=0, test=0 → impossible d'évaluer le modèle | Rétablir `n_train = int(n * 0.8)`, `n_val = int(n * 0.1)` |

**Pourquoi ces 3 bugs :** v1 = catégorisation incorrecte → dataset déséquilibré, le modèle ne généralise pas sur certains sujets. v2 = learning_rate trop élevé est l'erreur #1 en fine-tuning (convergence chaotique). v3 = pas de validation set = overfitting invisible.

---

## AT05 — Déploiement FastAPI

**⚠️ Particularité AT05 :** **PAS d'`exercice.py`**. L'élève modifie des fichiers de l'API (`api/routers/chat.py`, `api/routers/rag.py`) puis lance un serveur.

**Mission élève :** déployer l'API HomeButler avec rate limit, CORS, et 3 endpoints (`/chat`, `/rag/retrieve`, `/health`).

**Fichiers que l'élève complète :**
- `api/routers/chat.py` → `_call_rag_only()`, `_call_agent()`
- `api/routers/rag.py` → endpoint `POST /rag/retrieve`

### Démo live (T+30)
```bash
git checkout atelier/05-deploiement
uvicorn api.main:app --reload --port 8000
```
- Dans un 2e terminal :
  ```bash
  curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message":"Quelle est ma chaudière?"}'
  ```
- Ouvre Streamlit :
  ```bash
  streamlit run ui/app.py
  ```
- Montre la conversation en UI.

### Passage de relais — différent
> « Vous lancez `uvicorn api.main:app --reload` dans un terminal. Vous éditez `api/routers/chat.py` (les fonctions `_call_rag_only` et `_call_agent`). À chaque sauvegarde, uvicorn rechargera tout seul. Vous testez avec `curl` ou avec l'UI Streamlit. »

### Bug Hunt AT05
- v1 : (pas de v1 sur AT05 — démarrer à v2)
- v2 : `allow_origins=["*"]` (CORS trop permissif → fail tests sécurité)
- v3 : `asyncio.wait_for` sans timeout numérique

---

## AT06 — RAG vs FT vs RAFT

**⚠️ Particularité AT06 :** **PAS d'`exercice.py`**. L'élève complète `evaluate_pipeline.py` avec 6 TODOs.

**Mission élève :** benchmark 3 modes (`llm_only`, `rag`, `agent`) sur 20 questions de validation, choisir le meilleur avec arguments.

**Fichier que l'élève complète :**
- `ateliers/atelier-06-finetune-vs-rag/evaluate_pipeline.py` (3 `NotImplementedError` + 11 `# TODO`)

### Démo live (T+30)
```bash
git checkout atelier/06-finetune-vs-rag
grep -n "TODO\|NotImplementedError" ateliers/atelier-06-finetune-vs-rag/evaluate_pipeline.py
```
- Donne la liste des lignes à compléter dès le début (sinon les élèves cherchent partout).
- Lance :
  ```bash
  python ateliers/atelier-06-finetune-vs-rag/evaluate_pipeline.py
  ```
- Pointe le tableau de scores final + la décision argumentée.

### Passage de relais
> « Vous ouvrez `ateliers/atelier-06-finetune-vs-rag/evaluate_pipeline.py`. Lancez `grep -n "TODO\|NotImplementedError"` pour avoir la liste des 6 endroits à compléter. Critère de succès : le script tourne jusqu'au bout et affiche les 3 scores. »

### Bug Hunt AT06
- v1 : (n/a)
- v2 : usage de `sentence_bleu` (déprécié, à remplacer par `corpus_bleu`)
- v3 : sélection d'une seule question (au lieu du dataset complet) + latencies écrasées (au lieu d'append)

---

# PARTIE 4 — Checklist pré-session (15 min avant d'arriver)

```bash
cd /Users/yohannravino/Factory/training-rag

# 1. Vérifier que tu es bien sur la branche corrigée de l'atelier du jour
git checkout atelier/01-llm-baseline
git status      # → clean, à jour

# 2. Vérifier que la solution tourne (sauf AT04/05/06)
.venv/bin/python ateliers/atelier-01-llm-baseline/exercice.py
# Pour AT04 : ouvrir Colab + tester 1 cellule
# Pour AT05 : uvicorn api.main:app --reload + curl
# Pour AT06 : .venv/bin/python ateliers/atelier-06-finetune-vs-rag/evaluate_pipeline.py

# 3. Vérifier la version élève en parallèle pour anticiper leurs questions
git checkout student/01-llm-baseline
grep -rn NotImplementedError homebutler/llm/   # voir où ils vont bloquer
git checkout atelier/01-llm-baseline           # revenir pour la démo

# 4. Confirmer .env
cat .env | grep -E "ANTHROPIC_API_KEY|LLM_PROVIDER"
```

---

# PARTIE 5 — Pannes typiques pendant la session

| Symptôme élève | Cause probable | Réponse |
|---|---|---|
| `ANTHROPIC_API_KEY missing` | `.env` pas créé | `cp .env.example .env` + remplir |
| `ModuleNotFoundError: homebutler` | venv pas activé | `source .venv/bin/activate` puis `pip install -e .` |
| `faiss segfault` (AT02) | Mac ARM + faiss-gpu | `pip uninstall faiss-gpu && pip install faiss-cpu` |
| Rate limit 429 (AT01-03) | Tier 1 Anthropic, classe entière | Basculer `LLM_PROVIDER=ollama` dans `.env` |
| `git apply` refuse le patch | Élève a modifié exercice.py de façon incompatible | `git checkout student/0X-nom -- ateliers/atelier-0X-nom/exercice.py` puis ré-`git apply` |
| Notebook Colab plante (AT04) | Pas de GPU | Runtime → Change runtime type → T4 GPU |
| uvicorn ne reload pas (AT05) | `--reload` oublié ou fichier hors watch | Relancer `uvicorn api.main:app --reload` |

---

# PARTIE 6 — Ressources formateur (jamais distribuées aux élèves)

| Fichier | Où | Usage |
|---|---|---|
| `_formateur/DEROULE-FORMATION.md` | pre-training-rag | Ce document |
| `_formateur/INDEX-EXTRAS-VIBE.md` | pre-training-rag | Catalogue des 12 défis bonus per-atelier |
| `notes-formateur-vulgarisation.md` | pre-training-rag (local, gitignored) | Tes analogies grand public à recycler |
| `slides/atelier-0X-corrige.md` | pre-training-rag | Slides à projeter |
| `slides/atelier-0X-blank.md` | pre-training-rag | Si tu distribues des slides PDF aux élèves (rare) |
| `draft.md` | pre-training-rag (local, gitignored) | Brouillon perso |
