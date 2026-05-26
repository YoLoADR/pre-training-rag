# Insights — Réorganisation livraison formation

## Architecture découverte (2026-05-26)

### Les deux repos ont des rôles distincts et non-interchangeables

- `pre-training-rag` = atelier de préparation formateur (slides, notes vulgarisation, plans .agent/tasks/, exercices corrigés en brouillon)
- `training-rag` = le repo que les élèves clonent (code HomeButler fonctionnel, branches progressives)

Le premier plan (v1) ignorait complètement `training-rag` — erreur critique.

### Les branches student/XX sont largement propres — le gros travail est déjà fait

- GUIDE-FORMATEUR.md : déjà absent de toutes les branches student
- Code blanking homebutler/ : déjà fait sur les 6 ateliers
- QUICK-START.md, STARTER.md : déjà présents
- .claude/CLAUDE.md scope guards : fonctionnels
- slides corrigées : déjà absentes

Le vrai problème restant est plus petit qu'attendu : `.agent/tasks/` + `README-formateur.md` sur student/01-05.

### La stratégie de blanking est robuste et bien conçue

- `NotImplementedError` toujours en **corps de fonction**, jamais au top-level → imports ne cassent pas en cascade
- 2 niveaux d'indices (léger → fort) dans les docstrings
- `solution.py` présent sur student/XX mais **inutilisable** (importe homebutler/ blanké → crash) → anti-fraude by design
- Lien `git diff student/XX atelier/XX` toujours dans le message d'erreur → chemin de secours clair

### Les exercices vibe-coder sont dans GUIDE-ELEVE.md §BONUS — pas de fichiers séparés (sauf gradio_demo.py en AT03)

Ce n'est pas du tout "éparpillé" : c'est structuré de façon cohérente dans le §BONUS de chaque GUIDE-ELEVE.md.
Il manquait juste un index centralisé (→ créer `_formateur/INDEX-EXTRAS-VIBE.md`).

### La progression homebutler/ est la clé de la pédagogie

Les fonctions blankées ne sont pas aléatoires : elles correspondent exactement au concept pédagogique de chaque atelier.
- AT01 = le LLM comme boîte noire → on blanke le provider et les prompts
- AT02 = la pipeline RAG → on blanke le chunking et l'indexation FAISS
- AT03 = l'orchestration agent → on blanke le retriever hybride et l'executor
- AT04 = fine-tuning → on blanke les configs LoRA et la génération dataset
- AT05 = déploiement → on blanke les endpoints API
- AT06 = comparaison → on blanke le benchmark

### La branche atelier/06-finetune-vs-rag est le HEAD courant (branche de travail active)

C'est la branche par défaut sur origin. Les modifications doivent partir de là et se propager sur les branches student.

## Risques identifiés

| Risque | Mitigation |
|---|---|
| `git rm -r .agent/tasks/` supprime des dossiers différents selon la branche | Toujours vérifier avec T0.1 avant d'agir |
| Push force sur student/XX si commits divergent | Utiliser `git push --force-with-lease` uniquement si nécessaire |
| README-formateur.md peut ne pas exister sur toutes les branches | Vérifier avant `git rm` (utiliser `git ls-tree | grep formateur`) |
| Tests bug-hunt pourraient dépendre de README-formateur.md | Vérifier (les tests ciblent exercice.py uniquement — confirmé) |

## Décisions tranchées

| Question | Décision |
|---|---|
| Supprimer ou garder solution.py sur student/XX ? | Garder — il est non-exécutable (crash NotImplementedError) et visible = feature pédagogique (l'élève comprend le pattern) |
| Slides dans student/XX ? | Absentes (déjà le cas) — le formateur les diffuse depuis pre-training-rag |
| Créer LIVRABLE.md par atelier ? | Non prioritaire — QUICK-START.md joue déjà ce rôle |
| .agent/tasks/ dans .gitignore ? | Non — .gitignore ne supprime pas les fichiers déjà trackés ; la suppression se fait par git rm sur chaque branche |
