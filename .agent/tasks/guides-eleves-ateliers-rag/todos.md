# TODOs — Guides élèves ateliers RAG

Checklist d'exécution du plan v2. Cocher au fur et à mesure. Référence détaillée : `plan-supports-tp-autonomes-v2.md` §10 (fichiers à créer) + §11 (stratégie d'exécution).

## Phase 0 — Outillage scope-leak + setup (à faire AVANT toute rédaction)

- [x] **Décision tranchée scope leak At.05/06** : feature flag `ENABLE_COMPARE_ROUTES` ajouté dans `api/routers/rag.py` + `api/routers/chat.py` (default `false`, `include_in_schema` conditionnel)
- [x] Vérifier que les routes `/rag/evaluate`, `/chat/compare`, `/rag/compare-strategies` sont bien conditionnées au flag
- [x] Étendre `scripts/verify_branch_scope.sh` pour vérifier la présence des fichiers `.claude/CLAUDE.md` et `.cursorrules` par atelier + fix check At.05 (adapté au feature flag)
- [x] Renommer `README.md` → `README-formateur.md` × 6 ateliers
- [x] Créer branches `solution/at01`, `solution/at02`, `solution/at03` (At.04/05/06 sans solution.py)
- [x] Créer `requirements_atelier06.txt`
- [x] Mettre à jour `.env.example` (ENABLE_COMPARE_ROUTES + ANONYMIZED_TELEMETRY)
- [x] Écrire `scripts/check_atelier_ready.sh N` (créé)
- [x] Créer le gabarit `.claude/CLAUDE.md` local atelier × 6 (créé pour At.01-06)
- [x] Créer le gabarit `.claude/settings.json` avec hook `UserPromptSubmit` × 6 (créé pour At.01-06)
- [x] Créer le gabarit `.cursorrules` × 6 (créé pour At.01-06)
- [x] Créer `ateliers/atelier-00-prevol/GUIDE-ELEVE.md` (Pré-vol)

## Phase 1 — Pilote Atelier 02 (RAG Simple FAISS) — modèle qualité

- [x] Renommer `ateliers/atelier-02-rag-simple/README.md` → `README-formateur.md`
- [x] Rédiger `ateliers/atelier-02-rag-simple/GUIDE-ELEVE.md` complet selon gabarit §7
  - [x] Section Pré-vol + mission + périmètre + choix piste
  - [x] Carnet de bord avec mini-lexique vulgarisé (chunk, embedding, FAISS, MMR, recall@k, faithfulness…)
  - [x] Étapes Core (1h40) avec indices Build + garde-fou Vibe
  - [x] Section 🔬 Mini-lab (fixed vs recursive chunking)
  - [x] Section 📊 Mesure-toi (Recall@1/3/5, latence, faithfulness)
  - [x] Section 🐛 Bug Hunt (3 bugs à brancher)
  - [x] Sprint (30min, condensé)
  - [x] Bonus (60-70min, format reflexion-challenge)
  - [x] Wrap-up + quiz oral
- [x] Créer `ateliers/atelier-02-rag-simple/bugs/v1.patch` + `test_v1.py` + `v1_explanation.md` (chunk_size=2000)
- [x] Créer `ateliers/atelier-02-rag-simple/bugs/v2.patch` + `test_v2.py` + `v2_explanation.md` (chunk_overlap=0)
- [x] Créer `ateliers/atelier-02-rag-simple/bugs/v3.patch` + `test_v3.py` + `v3_explanation.md` (reconstruction index à chaque query)
- [x] Créer `ateliers/atelier-02-rag-simple/checkpoints/check_1.py` (QCM 3 questions)
- [x] Créer `ateliers/atelier-02-rag-simple/checkpoints/check_final.py` (5 questions)
- [x] Créer `ateliers/atelier-02-rag-simple/.claude/CLAUDE.md` (scope strict)
- [x] Créer `ateliers/atelier-02-rag-simple/.claude/settings.json` (hook anti-scope-leak)
- [x] Créer `ateliers/atelier-02-rag-simple/.cursorrules`
- [ ] **Test pilote** : 2 personnes (1 Build + 1 Vibe), chrono, validation des 5 critères §12 ← HUMAIN REQUIS
- [ ] Itérer sur retours pilote avant Phase 2 ← HUMAIN REQUIS

## Phase 2 — Décliner sur les 5 autres ateliers (parallélisable)

### Atelier 01 — LLM Baseline
- [x] Renommer `README.md` → `README-formateur.md`
- [x] Rédiger `GUIDE-ELEVE.md` (scope étendu : top_p, seed, system vs user, few-shot)
- [x] Carnet de bord vulgarisé (LLM, prompt, temperature, knowledge cutoff, hallucination)
- [x] 3 bugs (T=0.9, max_tokens=50, prompt sans system)
- [x] Checkpoints + .claude/ + .cursorrules

### Atelier 03 — Pipeline Agent ReAct
- [x] Renommer `README.md` → `README-formateur.md`
- [x] Rédiger `GUIDE-ELEVE.md` (densité forte, prévoir 4h pour test pilote)
- [x] Carnet de bord vulgarisé (EnsembleRetriever, ReAct, tool, mémoire)
- [x] 3 bugs (description tool bâclée, 15 tools, sans max_iterations)
- [x] Checkpoints + .claude/ + .cursorrules
- [x] **Vérifier que ChromaDB démarre proprement** (telemetry errors tps.md 266-267) — ajouter `ANONYMIZED_TELEMETRY=False` au Pré-vol At.03

### Atelier 04 — Fine-tuning LoRA/QLoRA
- [x] **Tableau jargon→analogie obligatoire** (16 termes, §8 At.04 du plan)
- [x] Vérifier existence `notebooks/at04_finetuning_lora.ipynb`, créer si absent
- [x] Renommer `README.md` → `README-formateur.md`
- [x] Rédiger `GUIDE-ELEVE.md` (Core Mac + Bonus Colab)
- [x] 3 bugs (dataset 100% "autres", lr=1e-2, sans val set)
- [x] **Reformuler chaque "🐛 erreurs communes" en langage non-tech**
- [x] Sur-échantillonnage = manip Core (pas Bonus)
- [x] Section "📦 Garde une trace" (HF Hub gratuit, simplifié)
- [x] Checkpoints + .claude/ + .cursorrules
- [x] Quiz vérifie 3 termes au hasard du lexique

### Atelier 05 — Déploiement
- [x] Renommer `README.md` → `README-formateur.md`
- [x] Rédiger `GUIDE-ELEVE.md` (scope étendu : CORS, auth API key, streaming SSE en Bonus)
- [x] Carnet de bord vulgarisé (FastAPI, prompt injection, rate limit, Langfuse, CORS)
- [x] Vérifier feature flag `ENABLE_COMPARE_ROUTES=false` actif
- [x] 3 bugs (clé API exposée, CORS *, sans timeout)
- [x] Checkpoints + .claude/ + .cursorrules
- [x] Intégrer `checklist.md` + `test_securite.sh` existants en vérification finale

### Atelier 06 — Fine-tuning vs RAG / RAFT
- [x] Renommer `README.md` → `README-formateur.md`
- [x] Rédiger `GUIDE-ELEVE.md` (atelier de synthèse + soutenance 5 min)
- [x] Vérifier feature flag `ENABLE_COMPARE_ROUTES=true` activé ici
- [x] Réutiliser `evaluate_pipeline.py` + `grille_decision.md` existants
- [x] 3 bugs (eval sur train set, BLEU sur ton, latence sans warm-up)
- [x] Présentation RAFT (tableau Zhang 2024) en Bonus
- [x] Checkpoints + .claude/ + .cursorrules
- [x] Format wrap-up = soutenance + reco écrite 1 page

## Phase 3 — Atelier 00 Pré-vol + cohérence finale

- [x] Créer `ateliers/atelier-00-prevol/GUIDE-ELEVE.md`
  - [x] Clone, venv, deps par atelier
  - [x] Pré-téléchargement modèles (multilingual MiniLM, tokenizer Mistral)
  - [x] Vérif clés (Anthropic, Langfuse, Colab)
  - [x] Génération données (`generate_documents.py`, `generate_energy_data.py`, `generate_producers.py`)
  - [x] Pré-construction index
  - [x] Détection conflits ports (8000, 8501, 3300)
- [x] **Passe finale de cohérence** : lecture croisée des "🚧 Périmètre" pour anti-leak entre ateliers
- [ ] **Test anti-scope-leak Vibe** : tenter prompts hors-scope sur chaque atelier, vérifier que le hook bloque ← HUMAIN REQUIS
- [ ] **Test anti-cheat Bug Hunt** : tenter `cat bugs/v1.patch | claude` → si trop facile, raffiner ← HUMAIN REQUIS
- [ ] **Test coût Anthropic** : estimer < 5€/stagiaire pour At.03 (le plus cher). Sinon Haiku. ← HUMAIN REQUIS
- [ ] **Relecture employé non-formateur** sur At.02 + At.04 (vulgarisation OK ?) ← HUMAIN REQUIS

## Décisions à valider avec le formateur avant de coder

- [x] OK pour renommer `README.md` → `README-formateur.md` × 6 ?
- [x] OK pour migrer `solution.py` sur branches `solution/at0X` ?
- [x] OK pour le feature flag `ENABLE_COMPARE_ROUTES` (modification `api/routers/`) ?
- [ ] OK pour créer `notebooks/at04_finetuning_lora.ipynb` si absent ? ← À confirmer
- [x] Quel format de Bug Hunt préféré : patches git (recommandé) ou branches dédiées ? → patches git
- [ ] Quel outil LLM-judge pour les checkpoints : Claude direct, prompt-template, ou intégration Langfuse ? ← À confirmer
