# Context — Branches `student/XX-…` blanks avec indices

## Objectif

Produire, dans `/Users/yohannravino/Factory/training-rag/`, **6 nouvelles branches `student/01-…` → `student/06-…`** dérivées des 6 branches `atelier/XX-…` existantes (corrigées et fonctionnelles), qui livrent aux élèves :

1. Une version **blank** des fichiers porteurs du concept central RAG/fine-tuning de l'atelier en cours (corps de fonctions remplacés par `NotImplementedError`, paramètres remplacés par `# TODO (indice : …)`).
2. Des **indices guidants** progressifs en docstring + commentaires inline (jamais la réponse complète).
3. Pour chaque atelier, un triplet pédagogique clair (intégré dans `GUIDE-ELEVE.md` existant + un `QUICK-START.md` 1 page) :
   - **État initial** : ce qui est déjà là (ateliers passés + plomberie), ce qui reste à coder.
   - **Objectif mesurable** : actions observables + métrique chiffrée + commande pour la vérifier.
   - **Recette de cuisine vulgarisée** : checklist ≤ 6 étapes avec **tous les termes techniques traduits** en français courant + analogie quotidienne.

La **version corrigée** = état actuel des branches `atelier/XX-…`. L'élève récupère la solution via :
```bash
git diff student/XX-<thème> atelier/XX-<thème> -- <fichier>
```

## Pourquoi ce chantier

État actuel : l'élève qui clone `training-rag` et fait `git checkout atelier/02-rag-simple` reçoit le code RAG **déjà écrit** (`homebutler/rag/ingestion.py`, `vectorstore_faiss.py` complets). Son seul travail = compléter le wrapper `exercice.py` du dossier d'atelier — espace ouvert au vibe-coding sur le cœur du projet.

But : que le projet **fil rouge lui-même** (HomeButler AI) soit blank côté RAG/FT à l'atelier courant, pour forcer l'élève à implémenter chunking, FAISS, ReAct, LoRA, etc., en suivant la recette vulgarisée et les indices structurés.

## Périmètre — ce qui est dans le scope

- 6 branches `student/XX-…` dans `training-rag`, créées séquentiellement (AT02 en premier, atelier pivot).
- Blanks sur le code projet (`homebutler/`, `api/`, notebooks, `scripts/`) **uniquement** pour la thématique RAG/FT de l'atelier courant.
- Enrichissement du `GUIDE-ELEVE.md` existant (pas de nouveau fichier `MISSION.md` qui dupliquerait).
- Création de `QUICK-START.md` (1 page) par atelier.
- Mise à jour `.claude/CLAUDE.md` avec clause socratique anti-vibe.
- Enrichissement `checkpoints/check_1.py` avec QCM "explication personnelle".
- Création d'un `STARTER.md` racine sur main pour onboarding élève.
- Pour le notebook AT04 : script `nbformat` dédié.

## Périmètre — ce qui est HORS scope

- Aucune modification dans `/Users/yohannravino/Factory/pre-training-rag/` (autorité de vérité : `training-rag` pour le code, `pre-training-rag` pour supports formateur).
- Aucune modification des `exercice.py`, `solution.py`, `bugs/v*.patch`, `bugs/test_v*.py`, `checkpoints/check_final.py` existants (système Bug Hunt préservé à l'identique — voir cohabitation §6 du plan).
- Aucun fichier plomberie (`config.py`, `services/*`, `api/main.py`, `api/routers/{consumption,orders,products}.py`, `ui/*`, Dockerfile, etc.).
- Pas de tags `student-vX.Y` (les branches `student/XX` sont des branches de référence, pas des releases).

## Livrables attendus

À la fin de l'exécution du plan :

1. 6 branches `student/01-llm-baseline` → `student/06-finetune-vs-rag` poussées sur le remote de `training-rag`.
2. Chaque branche valide les 7 critères de vérification end-to-end (cf. plan §Vérification).
3. Un test "recette suffisante" sur AT02 passé : un dev Python sans expérience RAG complète l'atelier en ≤ 1h40 en suivant uniquement le guide enrichi + indices inline.
4. `STARTER.md` racine sur main.
5. CI légère GitHub Actions sur `student/XX` : `verify_branch_scope.sh` + `python -c "import homebutler"` (pas de pytest qui doit échouer par conception).

## Source de vérité

- **Plan détaillé** : `./plan-branches-student-blanks.md` (Rev 2 — intègre findings de 3 agents d'audit).
- **Plan original mode-claude** : `/Users/yohannravino/.claude/plans/dans-cette-formation-il-delegated-deer.md` (identique au plan détaillé local).
- **Progression** : `./todos.md`.
- **Apprentissages itératifs** : `./insights.md` (déjà pré-rempli des 16 trous identifiés par les agents d'audit en Phase 0).

## Contraintes pédagogiques héritées (à respecter impérativement)

- Calibrage 3h30/atelier (20min Setup + 1h40 Core + 30/60min Sprint XOR Bonus + 10min Wrap).
- Approche pédagogique v2 (cf. `../guides-eleves-ateliers-rag/`) : 6 piliers + 4 mécanismes anti-vibe-coding.
- Standard de qualité AT02 : `Recall@5 ≥ 0.80 ET Faithfulness ≥ 0.85` (référence : `evaluate_rag.py` + `GUIDE-FORMATEUR.md` AT02 l.387).
- Cohabitation avec Bug Hunt existant : ordre séquentiel imposé (remplir blanks d'abord, puis appliquer `bugs/v*.patch`).
- Cohérence des analogies avec lexique `GUIDE-FORMATEUR.md` existant (embedding = code-barres sémantique, FAISS = bibliothèque par sens, ReAct = détective pense/agit/observe, LoRA = notes adhésives sur le cerveau, etc.).
