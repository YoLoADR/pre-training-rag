# TODOs — Ateliers avancés AT07 / AT08 / AT09

> Mise à jour itérative. Ordre de construction : **AT08 → AT07 → AT09**.
> Légende : [ ] à faire · [~] en cours · [x] fait

## Phase 0 — Setup & backup
- [x] Créer `.agent/tasks/ateliers-avances-07-08-09/` (context/todos/insights/plan)
- [x] Backup git : tags datés des 12 branches existantes (atelier+student 01-06) + push tags
- [x] Vérifier état repo training-rag (untracked zips à ignorer, pas committer)
- [x] Capturer SHA des branches student/01-06 (preuve non-régression)

## Phase 1 — AT08 Optimisation pipeline RAG (construire en 1er)
- [x] Brancher `atelier/08-optimisation` depuis `atelier/06`
- [x] Code corrigé `homebutler/rag/reranking.py` (get_reranked_retriever, get_multiquery_retriever, get_hyde_retriever)
- [x] Ajouter flashrank à `scripts/preload_models.py`
- [x] `ateliers/atelier-08-optimisation/solution.py` + `exercice.py` (mesure Recall@5 avant/après via evaluate_rag.py)
- [x] **RUN réel → figer seuils chiffrés** (baseline ensemble vs reranké)
- [x] `requirements_atelier08.txt` (`-r requirements_atelier02.txt` + flashrank)
- [x] Bugs v1/v2/v3 (.patch + test_*.py + *_explanation.md) + bugs/__init__.py
- [x] checkpoints/check_1.py + check_final.py
- [x] GUIDE-ELEVE.md (15 sections) + GUIDE-FORMATEUR.md + README-formateur.md
- [x] .claude/CLAUDE.md + .claude/settings.json + .cursorrules (scope strict)
- [x] Slides `slides/atelier-08-corrige.md` + `-blank.md` (pre-training-rag)
- [x] Brancher `student/08-optimisation` : blanker reranking.py + exercice.py
- [x] Vérif : solution tourne, exercice crash propre, pytest bugs OK
- [x] `check_atelier_ready.sh` (regex ^0[1-9]$ + case 08) + verify_branch_scope.sh

## Phase 2 — AT07 Observabilité & Évaluation
- [ ] Brancher `atelier/07-observabilite` depuis `atelier/06`
- [ ] Sous-module `homebutler/eval/` : __init__, tracing.py, ragas_eval.py, judge.py (fourni corrigé)
- [ ] `ateliers/atelier-07-observabilite/evaluate_observability.py` (TODO inline style AT06)
- [ ] docker-compose.langfuse.yml (bonus self-host)
- [ ] **RUN réel → figer seuils** (faithfulness, etc.) + valider data/qa_dataset a des `reference`
- [ ] `requirements_atelier07.txt` (`-r requirements_atelier06.txt` + ragas==0.2.* + datasets)
- [ ] Bugs v1/v2/v3 (tests style analyse statique) + explanations
- [ ] checkpoints check_1 (QCM) + check_final (mots-clés)
- [ ] GUIDE-ELEVE + GUIDE-FORMATEUR + README-formateur
- [ ] .claude/CLAUDE.md + settings.json + .cursorrules
- [ ] Slides corrige/blank
- [ ] Brancher `student/07-observabilite` : blanker les TODO de evaluate_observability.py
- [ ] Vérif + check_atelier_ready case 07

## Phase 3 — AT09 Azure AI Search (priorité)
- [ ] Brancher `atelier/09-azure-search` depuis `atelier/06`
- [ ] `homebutler/rag/vectorstore_azure.py` (build_azure_index schéma manuel 384d, get_azure_store, azure_search)
- [ ] config.py + .env.example : AZURE_SEARCH_* (additif AT09 uniquement)
- [ ] Scripts fournis : azure_provision.sh, azure_teardown.sh, CLI-VS-PORTAIL.md
- [ ] solution.py + exercice.py (ingest + 3 modes + comparaison FAISS)
- [ ] `requirements_atelier09.txt` (`-r requirements_atelier05.txt` + azure-search-documents + azure-identity)
- [ ] Bugs v1 (dim 1536≠384) / v2 (similarity vs hybrid) / v3 (searchable=True manquant) + explanations
- [ ] checkpoints
- [ ] GUIDE-ELEVE + GUIDE-FORMATEUR + README-formateur + table CLI/portail
- [ ] .claude/CLAUDE.md + settings.json + .cursorrules
- [ ] Slides corrige/blank
- [ ] Brancher `student/09-azure-search` : blanker vectorstore_azure.py + exercice.py
- [ ] Vérif (run conditionnel compte Azure) + check_atelier_ready case 09

## Phase 4 — Doc formateur (pre-training-rag)
- [ ] DEROULE-FORMATION.md : section Jour 4 / parcours avancé + déroulé minuté AT07/08/09 + pannes
- [ ] INDEX-EXTRAS-VIBE.md : ## AT07/08/09 (2 défis chiffrés chacun)
- [ ] ateliers/README.md : mapping étendu (modules avancés optionnels)

## Phase 5 — Non-régression & push
- [ ] SHA student/01-06 inchangés ; git diff config.py additif only
- [ ] pytest ateliers/atelier-0{1..6}-*/bugs/ verts
- [ ] imports homebutler OK sur 01-06
- [ ] Push branches atelier/07-09 + student/07-09 sur remote github
- [ ] Mettre à jour insights.md + memory
