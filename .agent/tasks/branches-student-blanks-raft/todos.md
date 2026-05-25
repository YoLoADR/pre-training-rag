# TODOs — Branches `student/XX-…` blanks avec indices

> Statuts : `[ ]` à faire · `[~]` en cours · `[x]` terminé · `[!]` bloqué

## Phase 0 — Audit (terminée)

- [x] Explorer `pre-training-rag/` (structure, ateliers, `.agent/tasks/` antérieures)
- [x] Explorer `training-rag/` (branches `atelier/XX-…`, mapping diffs)
- [x] Définir contraintes avec utilisateur (cible / granularité / indices / solution)
- [x] Audit Rev 1 par 3 agents en parallèle (réalisme technique + trous/régressions + pédagogie)
- [x] Réviser plan en Rev 2 intégrant les 16 findings de l'audit
- [x] Créer dossier `.agent/tasks/branches-student-blanks-raft/`

## Phase 1 — Outillage et préparation (à faire avant tout blanking)

- [x] Vérifier que `homebutler/agent/tools.py` expose `ALL_TOOLS` au top-level (risque `NameError` si construit dans fonction) — confirmé par audit Agent 1
- [x] Écrire `scripts/blank_notebook.py` (utilise `nbformat`, sera commit sur `student/04` uniquement)
- [x] Confirmer décision finale `solution.py` (Rev 2 = visible mais inopérant ; basculer en `solution/at0X` si retour terrain négatif)
- [x] Confirmer push remote `student/XX-…` (Rev 2 = oui) + CI légère GitHub Actions

## Phase 2 — Atelier 02 (pivot, en premier — validation du pattern)

- [x] `git checkout atelier/02-rag-simple && git checkout -b student/02-rag-simple`
- [x] Blanker `homebutler/rag/ingestion.py` (`chunk_fixed_size`, `chunk_recursive`, `chunk_semantic`)
- [x] Blanker `homebutler/rag/vectorstore_faiss.py` (`get_embeddings`, `build_faiss_index`, `load_faiss_index`)
- [x] Enrichir `ateliers/atelier-02-rag-simple/GUIDE-ELEVE.md` (section "Atelier 02 en un coup d'œil")
- [x] Créer `ateliers/atelier-02-rag-simple/QUICK-START.md` (1 page, recette 6 étapes)
- [x] Enrichir `ateliers/atelier-02-rag-simple/.claude/CLAUDE.md` (clause socratique anti-vibe)
- [x] Enrichir `ateliers/atelier-02-rag-simple/checkpoints/check_1.py` (QCM "explication personnelle")
- [x] Vérifications end-to-end §1-7 du plan
- [x] **Smoke test "recette suffisante"** : un dev Python sans RAG complète AT02 en ≤ 1h40 en lisant uniquement le guide enrichi + indices
- [x] Si smoke test échoue : itérer sur AT02 avant de répliquer
- [x] Commit + push `student/02-rag-simple`

## Phase 3 — Atelier 01 (le plus simple)

- [x] `git checkout atelier/01-llm-baseline && git checkout -b student/01-llm-baseline`
- [x] Blanker `homebutler/llm/provider.py` (`get_llm`, `get_llm_cached`)
- [x] Blanker `homebutler/llm/prompts.py` (4 `ChatPromptTemplate`)
- [x] Enrichir GUIDE-ELEVE + QUICK-START + CLAUDE.md + check_1.py
- [x] Vérifications end-to-end
- [x] Commit + push `student/01-llm-baseline`

## Phase 4 — Atelier 05 (déploiement)

- [x] `git checkout atelier/05-deploiement && git checkout -b student/05-deploiement`
- [x] Blanker `api/routers/chat.py` (`_call_rag_only`, `_call_agent`)
- [x] Blanker `api/routers/rag.py` (`/retrieve` + détection prompt injection)
- [x] Enrichir GUIDE-ELEVE + QUICK-START + CLAUDE.md + check_1.py
- [x] Vérifications end-to-end
- [x] Commit + push `student/05-deploiement`

## Phase 5 — Atelier 06 (comparatif)

- [x] `git checkout atelier/06-finetune-vs-rag && git checkout -b student/06-finetune-vs-rag`
- [x] Blanker `ateliers/atelier-06-finetune-vs-rag/evaluate_pipeline.py` (6 TODOs)
- [x] Enrichir GUIDE-ELEVE + QUICK-START + CLAUDE.md + check_1.py
- [x] Vérifications end-to-end
- [x] Commit + push `student/06-finetune-vs-rag`

## Phase 6 — Atelier 03 (calibrage temporel à surveiller)

- [x] `git checkout atelier/03-pipeline-agent && git checkout -b student/03-pipeline-agent`
- [x] Blanker `homebutler/agent/react_agent.py` (`get_agent_executor`)
- [x] Blanker `homebutler/rag/retriever.py` (EnsembleRetriever)
- [x] **NE PAS** blanker `homebutler/agent/tools.py` ni `homebutler/rag/vectorstore_chroma.py` (calibrage)
- [x] Enrichir GUIDE-ELEVE + QUICK-START + CLAUDE.md + check_1.py
- [x] Vérifications end-to-end
- [x] Test temporel : un dev complète AT03 en ≤ 1h40 ?
- [x] Commit + push `student/03-pipeline-agent`

## Phase 7 — Atelier 04 (notebook, outillage spécifique)

- [x] `git checkout atelier/04-finetuning && git checkout -b student/04-finetuning`
- [x] Lancer `scripts/blank_notebook.py` sur `notebooks/03_finetuning_lora.ipynb`
- [x] Blanker `scripts/generate_qa_dataset.py`
- [x] Blanker `scripts/augment_qa_dataset.py`
- [x] Enrichir GUIDE-ELEVE + QUICK-START + CLAUDE.md + check_1.py
- [x] Vérifications end-to-end (notebook : ouvrir dans Jupyter, vérifier qu'aucune cellule n'est corrompue)
- [x] Commit + push `student/04-finetuning`

## Phase 8 — Onboarding et finalisation

- [x] `git checkout main && git pull` (sur training-rag)
- [x] Créer `STARTER.md` à la racine
- [x] Commit + push main
- [x] Configurer GitHub Actions CI légère sur les branches `student/XX-…` (verify_branch_scope.sh + import smoke)
- [x] Mettre à jour `ateliers/README.md` pour mentionner le workflow `student/XX-…`

## Phase 9 — Synchronisation et clôture

- [x] Mettre à jour `pre-training-rag/.agent/tasks/branches-student-blanks-raft/insights.md` avec les apprentissages finaux
- [x] Documenter les décisions Rev 2 dans MEMORY si elles modifient la doctrine (ex. autorité de vérité, calibrage AT03)
- [x] Annoncer aux élèves : où démarrer (`STARTER.md`), comment basculer entre ateliers
