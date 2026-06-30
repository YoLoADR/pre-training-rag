# Plan — Ajouter AT07/AT08/AT09 à la formation RAFT HomeButler (révisé après audit 3 agents)

## Context

La formation **HomeButler AI RAFT** (6 ateliers AT01→06, fil rouge unique, local-first sans GPU) couvre déjà l'essentiel du programme officiel Ambient IT *« RAG avec LangChain et Azure AI Search »* (`Annexe-1-Fiche-descriptive-rag.pdf`). L'analyse d'écart fait ressortir **3 chapitres du PDF encore en creux**, traitables **100% CLI** et harmonisables au fil rouge. Le formateur veut **ajouter 2-3 ateliers maximum** (Azure = priorité) **sans toucher à l'existant AT01→06**.

Ce plan a été **audité par 3 agents** (réalisme, fidélité au pattern existant, faisabilité technique 2026). Leurs corrections sont intégrées ci-dessous et signalées « ⟵ audit ».

| Chapitre PDF en creux | Nouvel atelier | Réutilise / prolonge |
|---|---|---|
| ch.4 *Évaluation & Observabilité* | **AT07 — Observabilité & Évaluation** | AT05 (Langfuse), AT06 (`evaluate_pipeline.py`) |
| ch.2 *Techniques avancées / optimisation du pipeline* | **AT08 — Optimisation du pipeline RAG** | AT02 (`evaluate_rag.py`, Recall), AT03 (retriever) |
| ch.5 *RAG avec Azure AI Search* (priorité) | **AT09 — Azure AI Search** | AT02 (FAISS → vector store managé) |

### Positionnement assumé — parcours avancé optionnel ⟵ audit (must-fix)

Le PDF officiel = **14 h (2 j)**. L'existant fait déjà **~21 h (3 j)**. Ajouter 3 ateliers ≈ **+10 h → ~31 h**. Ces ateliers ne « complètent » donc **pas** la fiche Qualiopi 14 h : ce sont des **modules avancés optionnels / détachables** (« parcours industrialisation »), jouables en **Jour 4** ou **à la carte**. À refléter dans `ateliers/README.md` (mapping) sans prétendre couvrir le volume officiel.

**Honnêteté de couverture PDF** (à documenter, ne pas survendre) :
- ch.4 nomme **LangSmith** ; on enseigne **Langfuse** (déjà câblé dans le projet) — équivalent, à assumer.
- ch.2 nomme **« Deep Memory »** (feature propriétaire Activeloop Deep Lake). AT08 (reranking + multi-query) est une **substitution pédagogique légitime** de « optimisation du pipeline », **pas** une implémentation de Deep Memory. Ne pas prétendre le contraire.

### Contraintes invariantes (cf. `draft.md`, `plan-reorganisation-livraison-v3.md`)
Versioning progressif · scope strict par atelier · **zéro régression AT01→06** · dissociation blank/corrigé · pédagogie *slides → présenter le corrigé → cacher → TP blank → partage correction via `git diff`* · profils « vibe coders » (pistes 🛠️ Build / 🎮 Vibe).

---

## Doctrine de NON-RÉGRESSION (le point le plus sensible) ⟵ audit

Le « zéro régression » n'est garanti que par des règles explicites. Les nouvelles branches `atelier/07,08,09` et `student/07,08,09` partent de `atelier/06`/`student/06` et **accumulent** le code (versioning progressif). Règles strictes :

1. **Code neuf = fichiers neufs** quand c'est possible (séparation au niveau fichier, comme l'existant) :
   - AT07 → **nouveau** sous-module `homebutler/eval/` (n'existe pas aujourd'hui).
   - AT08 → **nouveau** fichier `homebutler/rag/reranking.py` (⟵ audit : **ne PAS éditer `homebutler/rag/retriever.py`** qui est le fichier blanké d'AT03 ; on en réutilise les fonctions par import).
   - AT09 → **nouveau** fichier `homebutler/rag/vectorstore_azure.py` (miroir de `vectorstore_faiss.py`).
2. **`homebutler/config.py`** : **aucune** modif pour AT07 (les variables `LANGFUSE_*`, `LANGCHAIN_*`, `TRACING_PROVIDER` **existent déjà** ⟵ audit) ni pour AT08 (ses params lus via `os.getenv` dans `reranking.py`). Seul **AT09** ajoute `AZURE_SEARCH_ENDPOINT/KEY/INDEX` **en additif** (mêmes conventions `os.getenv(...)`), **uniquement sur les branches AT09**, jamais re-cascadé vers 01-06.
3. **Preuve de non-régression** après chaque nouvelle branche :
   ```bash
   git diff student/06 student/09 -- homebutler/config.py   # uniquement des lignes AJOUTÉES
   # Les branches 01-06 ne doivent PAS changer de SHA :
   git rev-parse student/01 student/02 ... student/06        # identiques avant/après
   pytest ateliers/atelier-0{1..6}-*/bugs/ -q                 # 34 tests restent au vert
   for n in 01 02 03 04 05 06; do git checkout student/$n-*; python -c "import homebutler"; done
   ```
4. **Scope par fichier** : la séparation en fichiers neufs rend `scripts/verify_branch_scope.sh` fiable (pas de multi-atelier dans un même fichier).

---

## Ordre d'enseignement vs ordre de construction ⟵ audit (lever l'ambiguïté)

- **Ordre d'enseignement en salle** : **AT07 → AT08 → AT09** (*mesurer → améliorer → industrialiser*).
- **Ordre de construction par le formateur** : **AT08 → AT07 → AT09** — AT08 est le plus autonome (2-3 fonctions, 100% local) et valide la mécanique (blanking, bug hunt, pytest) avant Docker/Langfuse (AT07) et Azure (AT09). Contrainte : le `solution.py` d'AT08 ne doit **pas** dépendre de `homebutler/eval/` (il réutilise `evaluate_rag.py` d'AT02 — autonome).

---

## Apparat standard par atelier (gabarit fidèle ⟵ audit)

Chaque `ateliers/atelier-0X-nom/` reproduit l'arborescence exacte de l'existant :
`GUIDE-ELEVE.md` (15 sections canoniques, ton tutoiement, 🚦 pré-vol → 🎯 mission chiffrée → 🚧 périmètre → 🛠️/🎮 pistes → 🧠 carnet → 🎯 tronc → 🐛 bug hunt → 📊 mesure → ✋ checkpoints → ⚡ sprint / 🏆 bonus → 🎓 wrap-up) · `GUIDE-FORMATEUR.md` (modèle riche d'`atelier-05`) · `README-formateur.md` · `.claude/CLAUDE.md` + `.claude/settings.json` (hook `UserPromptSubmit` dont le `matcher` regex bloque les mots-clés des **autres** nouveaux ateliers) + `.cursorrules` · `bugs/` (`vN.patch` format `git diff --git` + `test_vN.py` + `vN_explanation.md` QCM V/F + `__init__.py`) · `checkpoints/check_1.py` (QCM A/B/C/D) + `check_final.py` (routage Bonus/Sprint) · `requirements_atelier0X.txt` (hérité via `-r`) · slides `slides/atelier-0X-corrige.md` + `-blank.md` (indices **2 niveaux** léger/fort) · entrée dans `_formateur/INDEX-EXTRAS-VIBE.md`.

**Type d'atelier** (⟵ audit, déterminant) :
- **AT07 = type « évaluation/synthèse » comme AT06** : **pas** de `exercice.py`/`solution.py` ; les TODO vivent **inline** dans un fichier `evaluate_observability.py` (style `evaluate_pipeline.py`). `homebutler/eval/` est **fourni corrigé** (la bibliothèque), l'élève **câble** les appels.
- **AT08 = type « construction » comme AT02** : `exercice.py` (TODO) + `solution.py` (corrigé commenté `═══ CONCEPT RAG ═══`), blanks dans `homebutler/rag/reranking.py`.
- **AT09 = type « construction/déploiement » comme AT05/AT02** : `exercice.py` + `solution.py`, blanks dans `homebutler/rag/vectorstore_azure.py`, + scripts infra fournis.

**Branches `solution/at07-09`** : **NON créées** ⟵ audit (cohérence avec la décision tranchée du `plan-v3` de skip `solution/at04-06`) ; la correction se partage via `git diff student/0X atelier/0X -- <fichier>`.

**Seuils chiffrés** : les valeurs ci-dessous sont des **ordres de grandeur indicatifs**. ⟵ audit : **figer chaque seuil par un run réel de `solution.py`** avant de le graver dans `GUIDE-ELEVE.md`/checkpoints (sinon mission « échouée » à code correct).

---

## AT07 — Observabilité & Évaluation

**Mission (critères à figer par run) :** instrumenter l'agent HomeButler, produire un **rapport d'évaluation RAGAS** sur un petit jeu de validation, et faire remonter des **scores LLM-as-judge** dans Langfuse. Succès ≈ traces visibles + rapport généré + `faithfulness` au-dessus du seuil mesuré.

**Décisions issues de l'audit :**
- **Observabilité = Langfuse Cloud par défaut** (déjà configuré : `.env.example` + usage AT05), **self-host Docker en bonus** (v3 = **6 conteneurs** web/worker/postgres/clickhouse/redis/minio, ≥ 8 Go RAM, timezone UTC — trop lourd comme chemin obligatoire en salle).
- **CallbackHandler** : SDK **`langfuse==2.57.1`** (hérité), import **`from langfuse.callback import CallbackHandler`** (v2). **Ne PAS** utiliser `from langfuse.langchain import CallbackHandler` (= v3, casse en v2).
- **RAGAS** : ⟵ audit **épingler `ragas==0.2.x`** (le `>=0.1.0` actuel installerait une API incompatible). Nouveau schéma **`EvaluationDataset` / `SingleTurnSample`** avec colonnes **`user_input`, `response`, `retrieved_contexts`, `reference`** (≠ ancien `question/answer/contexts/ground_truth`). Juge configuré explicitement (jamais OpenAI implicite) :
  ```python
  from ragas import evaluate, EvaluationDataset
  from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
  from ragas.llms import LangchainLLMWrapper
  from ragas.embeddings import LangchainEmbeddingsWrapper
  judge = LangchainLLMWrapper(get_llm(temperature=0))            # Claude ou Ollama
  emb   = LangchainEmbeddingsWrapper(get_embeddings())           # fastembed 384d
  result = evaluate(dataset, metrics=[...], llm=judge, embeddings=emb)
  ```
- **Garde-fous salle** ⟵ audit : RAGAS = dizaines d'appels LLM × N élèves → **rate-limit 429**. Mitigations : **dataset réduit à 5-8 questions en Core** (20 en bonus), `LLM_PROVIDER=ollama` pour la phase éval, vérifier que le jeu de validation (`data/qa_dataset/`, présent dès AT06) contient bien des **`reference` (ground_truth)** — sinon `context_recall`/`context_precision` = NaN (c'est justement le bug v2, donc le happy-path doit fournir les références).

**L'élève câble (TODO inline dans `evaluate_observability.py`, style AT06) :**
1. instancier `get_langfuse_handler()` et le passer en `config={"callbacks": [handler]}` à l'agent ; `flush_traces()` en fin.
2. construire l'`EvaluationDataset` (mapping correct des 4 colonnes + `reference`).
3. appeler `run_ragas_eval()` et afficher le tableau de métriques.
4. scorer chaque réponse via `llm_as_judge()` (température 0) et pousser le score dans Langfuse (`score_trace`).

**Fourni corrigé (lecture seule) :** `homebutler/eval/__init__.py`, `tracing.py` (`get_langfuse_handler`, `flush_traces`, `score_trace`), `ragas_eval.py` (`run_ragas_eval`), `judge.py` (`llm_as_judge`) ; le jeu de validation d'AT06 ; l'agent AT03.

**Bug Hunt (tests style « analyse statique » comme AT06 → pas de Langfuse live requis) :**
- v1 : handler non passé aux `callbacks` (ou `flush_traces()` oublié) → 0 trace. `test_v1` (mock du client / assert callbacks non vide).
- v2 : `reference` absent du dataset → `context_recall` = NaN. `test_v2` (assert mapping présent / `not isnan`).
- v3 : juge à `temperature != 0` → scores non reproductibles. `test_v3` = **assert statique** `temperature=0` dans le source (évite un test flaky). ⟵ audit (bug réel mais rendu déterministe).

**Dépendances** (`requirements_atelier07.txt`) : `-r requirements_atelier06.txt` + `ragas==0.2.*` (override du pin lâche), `datasets`. `langfuse==2.57.1` déjà hérité.

---

## AT08 — Optimisation du pipeline RAG

**Mission (critères à figer par run) :** ajouter **reranking + multi-query** au retriever hybride d'AT03 et **prouver** le gain de `Recall@5` (baseline ensemble ≈ 0.83) avec `evaluate_rag.py` d'AT02. 100% local CPU.

**Décisions issues de l'audit :**
- **Reranker = `flashrank`** (cross-encoder ONNX `ms-marco-MiniLM-L-12-v2`, ~**34 Mo**, CPU, OK Mac ARM). Import **`from langchain_community.document_compressors import FlashrankRerank`** + `ContextualCompressionRetriever`. Ajouter le download à `scripts/preload_models.py` (pré-vol) ⟵ audit.
- **MultiQuery** : `from langchain.retrievers.multi_query import MultiQueryRetriever` ; `MultiQueryRetriever.from_llm(retriever=..., llm=get_llm())` (un seul appel LLM → N reformulations).
- **HyDE** (bonus avancé) : composé en **LCEL** (`prompt | llm | StrOutputParser` → embed → `similarity_search`), pas l'ancien `HypotheticalDocumentEmbedder`.

**L'élève code (nouveau `homebutler/rag/reranking.py`, blanké sur `student/08`) :**
- `get_reranked_retriever(base_k=20, top_n=5)` → `ContextualCompressionRetriever(base_compressor=FlashrankRerank(top_n=...), base_retriever=get_ensemble_retriever(...))` (importe les fonctions AT03, ne les modifie pas). Concept clé : **entonnoir `base_k ≫ top_n`**.
- `get_multiquery_retriever()` → `MultiQueryRetriever.from_llm(...)`.
- (bonus) `get_hyde_retriever()`.
- `exercice.py`/`solution.py` → mesurent Recall@5 avant/après via `evaluate_rag.py`.

**Bug Hunt (tests comportementaux Recall, style AT02) :**
- v1 : `base_k == top_n` → le reranker **ne filtre plus** (il ne fait que réordonner) → bénéfice précision/coût perdu. ⟵ audit : formuler « perte du filtrage entonnoir », **pas** « aucun effet ». `test_v1` (Recall@5 inchangé vs baseline).
- v2 : ⟵ audit **bug original « temperature=0 ne diversifie pas » = FAUX, RETIRÉ** (les variantes sortent d'un seul appel piloté par le prompt). **Remplacé** par : prompt multi-query demandant **1 seule** reformulation (ou `LineListOutputParser` mal câblé) → 1 requête, aucune diversité → Recall non amélioré. `test_v2` (compter les requêtes générées / Recall).
- v3 : résultats non triés par score / `top_n` ignoré → ordre incohérent. `test_v3`.

**Dépendances** (`requirements_atelier08.txt`) : `-r requirements_atelier02.txt` + `flashrank`. Aucun GPU, aucune API tierce.

---

## AT09 — Azure AI Search (priorité)

**Concept central (le « aha ») ⟵ recherche Azure 2026 :** **control plane (CLI `az search` = service + clés) vs data plane (SDK/REST = index, vecteurs, ingestion, requêtes)**. C'est ce qui rend l'atelier réalisable au terminal. Seul le wizard portail « Import and vectorize data » est portail-only (et remplaçable par SDK).

**Mission (critères à figer par run) :** (1) comprendre/observer le provisioning CLI ; (2) créer un index vectoriel + ingérer le corpus HomeButler via SDK ; (3) requêter en hybrid/semantic et comparer à FAISS ; (4) **teardown**. Succès = une requête hybride cite les bonnes sources + l'élève sait dire ce qui est CLI vs portail.

**Décisions issues de l'audit (risque salle = bloquant sinon) :**
- **Quota Free tier = 1 service de recherche par souscription** → 15 élèves sur une souscription partagée = **un seul** `create` réussit. **Mitigation retenue : le formateur pré-provisionne UN service `Basic` partagé** (semantic ranker dispo), **chaque élève crée SON index** dessus (`index_name = <trigramme>-homebutler`). 1 service, N index, pas de quota Free. `az login` interactif validé **au pré-vol la veille**, pas en live ×15.
- **Embeddings = `fastembed all-MiniLM-L6-v2` (384 dims)** déjà installé → **0 dépendance Azure OpenAI, 0 coût token**. Schéma fixé à `vector_search_dimensions=384`.
- **Index créé à la main via SDK** (`SearchIndexClient`, `azure-search-documents>=11.5.1`) — c'est le cœur data-plane **et** ça rend le bug v1 réel (LangChain auto-créerait l'index en inférant 384, masquant le bug). Requêtes via `from langchain_community.vectorstores.azuresearch import AzureSearch` (`search_type ∈ {similarity, hybrid, semantic_hybrid}` ; `semantic_hybrid` exige tier Basic+ et une **semantic configuration**).

**Cartographie CLI vs Portail (à enseigner, table issue de la doc Azure 2026) :**

| Tâche | CLI / SDK | Portail obligatoire ? | Choix atelier |
|---|---|---|---|
| Groupe + service + clés | ✅ `az group create`, `az search service create`, `az search admin-key` | Non | **CLI** (démo formateur) |
| **Créer l'index vectoriel** | ✅ **SDK `azure-search-documents`** (pas de `az search` pour le contenu) | Non | **SDK Python (élève)** |
| Ingérer (push API) | ✅ `SearchClient.upload_documents` / `AzureSearch.add_documents` | Non | SDK |
| Vectorisation intégrée (skillset+indexer+vectorizer) | ✅ REST/SDK (`api-version=2026-04-01` GA) | Non | démo optionnelle |
| Wizard « Import and vectorize data » | ❌ no-code | **Oui (portail)** | démo visuelle facultative |
| Semantic ranker | ✅ `SemanticConfiguration` via SDK (tier Basic+) | Non | SDK |
| Requêter vector/hybrid/semantic | ✅ SDK + **LangChain `AzureSearch`** | Non | LangChain |
| Monitoring (latence, QPS) | ⚠️ Azure Monitor scriptable, lisible surtout au portail | Non strict | **Portail** (démo monitoring) |

**L'élève code (nouveau `homebutler/rag/vectorstore_azure.py`, blanké sur `student/09`) :**
- `build_azure_index(documents)` → schéma explicite via `SearchIndexClient` (`vector_search_dimensions=384`, champ `content` `searchable=True`, `HnswAlgorithmConfiguration`) puis upload.
- `get_azure_store()` → `AzureSearch(endpoint, key, index_name, embedding_function=get_embeddings().embed_query, search_type="hybrid")`.
- `azure_search(query, k, search_type)`.
- `exercice.py`/`solution.py` → ingèrent, requêtent en 3 modes, comparent à FAISS.

**Fourni (lecture seule, partie infra CLI) :** `azure_provision.sh` (`az login`, création service/groupe — **lancé par le formateur**), `azure_teardown.sh` (`az group delete --yes --no-wait`), `CLI-VS-PORTAIL.md` (la table + captures portail monitoring).

**Bug Hunt :**
- v1 : `vector_search_dimensions=1536` (copié d'un exemple OpenAI) ≠ embedding 384 → **upload rejeté**. `test_v1` (exception dimension). Excellent, réel **car** schéma créé à la main ⟵ audit.
- v2 : `search_type="similarity"` au lieu de `"hybrid"` → Recall dégradé sur vocabulaire divergent. `test_v2`.
- v3 : ⟵ audit **remplacé** (l'ancien « clé en dur + teardown » n'est pas pytest-able) par : champ `content` **sans** `searchable=True` (ou mauvais champ) → BM25/hybrid renvoie **0 résultat** malgré upload OK. `test_v3` (assert résultats non vides). La **clé en dur + teardown oublié** deviennent un item du `v3_explanation.md` (sécurité/coût) + une ligne de la checklist, pas un pytest.

**Dépendances** (`requirements_atelier09.txt`) : `-r requirements_atelier05.txt` + `azure-search-documents>=11.5.1`, `azure-identity>=1.16`. Système : **Azure CLI** (`az`) + **compte Azure** (pré-requis PDF « Maîtriser Azure » → valider à l'inscription). `az login` interactif → `! az login` en session.

---

## Fichiers à créer / modifier (récap)

**Repo élève `training-rag`** (versioning progressif) :
- Branches **`atelier/07-observabilite`, `atelier/08-optimisation`, `atelier/09-azure-search`** (corrigées, depuis `atelier/06`) + **`student/07,08,09`** (blankées).
- Code applicatif neuf : `homebutler/eval/{__init__,tracing,ragas_eval,judge}.py` (AT07) ; `homebutler/rag/reranking.py` (AT08) ; `homebutler/rag/vectorstore_azure.py` (AT09).
- `homebutler/config.py` : **+ `AZURE_SEARCH_*` additif (AT09 uniquement)** ; `.env.example` idem. Rien pour AT07/AT08.
- Dossiers ateliers complets (apparat standard ci-dessus) + `requirements_atelier0{7,8,9}.txt` (hérités `-r`).
- `scripts/check_atelier_ready.sh` : regex `^0[1-6]$` → **`^0[1-9]$`** + branches `case` import-test (07 `import langfuse, ragas` ; 08 `import flashrank` ; 09 `import azure.search.documents`). `scripts/preload_models.py` : + modèle flashrank. `scripts/verify_branch_scope.sh` : couvrir 07/08/09.

**Zone formateur `pre-training-rag`** :
- `slides/atelier-0{7,8,9}-corrige.md` + `-blank.md` (indices 2 niveaux).
- `_formateur/DEROULE-FORMATION.md` : section « Jour 4 / parcours avancé » + déroulé minuté AT07/08/09 + pannes typiques (Docker, rate-limit RAGAS, quota Azure, `az login`).
- `_formateur/INDEX-EXTRAS-VIBE.md` : `## AT07/08/09` (2 défis chiffrés chacun) + ligne couverture.
- `ateliers/README.md` : étendre le mapping en marquant AT07-09 « module avancé optionnel ».

---

## Vérification end-to-end

**Non-régression AT01→06** (avant ET après — cf. Doctrine ci-dessus) : SHA des branches 01-06 inchangés, `git diff student/06 student/09 -- config.py` additif only, 34 tests bug-hunt verts, imports OK.

**Par atelier :**
```bash
# AT08 (construire en 1er)
python ateliers/atelier-08-optimisation/solution.py     # Recall@5 avant/après (gain reranking)
pytest ateliers/atelier-08-optimisation/bugs/ -v

# AT07
python ateliers/atelier-07-observabilite/evaluate_observability.py   # rapport RAGAS + traces Langfuse (cloud)
pytest ateliers/atelier-07-observabilite/bugs/ -v
# bonus: docker compose -f docker-compose.langfuse.yml up -d  (self-host, dashboard :3000)

# AT09 (compte Azure requis)
! az login
bash ateliers/atelier-09-azure-search/azure_provision.sh   # formateur: service Basic partagé
python ateliers/atelier-09-azure-search/solution.py        # index 384d + ingestion + hybrid query vs FAISS
pytest ateliers/atelier-09-azure-search/bugs/ -v
bash ateliers/atelier-09-azure-search/azure_teardown.sh    # garde-fou coût
```
**Scope strict :** `bash scripts/verify_branch_scope.sh` ; sur chaque `student/0X`, `grep -rn "raise NotImplementedError"` ne remonte que les nouvelles fonctions, message contenant le lien `git diff`.

---

## Ordre d'implémentation & checklist par atelier

Construire **AT08 → AT07 → AT09**. Pour chacun : (a) écrire le corrigé (`homebutler/` neuf + fichier atelier), (b) **run réel → figer les seuils chiffrés**, (c) blanker → branche `student/`, (d) bugs v1/v2/v3 + tests + explanations + checkpoints, (e) GUIDE-ELEVE + GUIDE-FORMATEUR + slides corrige/blank + `.claude`/`.cursorrules`, (f) requirements `-r` + `check_atelier_ready.sh`/`preload_models.py`, (g) doc formateur (DEROULE + INDEX-EXTRAS + README), (h) **re-jouer la non-régression 01-06**.

## Décisions ouvertes (à confirmer en début d'implémentation)
- AT09 : souscription Azure **partagée Basic** (retenu) vs une souscription par élève — dépend des comptes réels en salle.
- AT07 : dataset RAGAS réduit (5-8 Q) en Core — valider que `data/qa_dataset/` contient des `reference`.
- Positionnement final : « Jour 4 » bloc vs 3 modules « à la carte ».
