# Context — Guides élèves pour les 6 ateliers RAG HomeButler

## Objectif global

Produire **6 fichiers `GUIDE-ELEVE.md`** (un par dossier `ateliers/atelier-0X-*/`) + un **atelier 00 "Pré-vol"**, conçus comme des supports de TP **autonomes, ludiques, scope-strict, mesurables** pour des employés d'entreprise sur une demi-journée chacun (~3h30 effectifs).

## Problème à résoudre

Les guides actuels (`examples-supports/GUIDE-ELEVE.md` style tuto linéaire) ont eu de mauvais retours élèves :

1. **Calibrage flou** — soit trop court (élèves désœuvrés) soit trop dense (élèves perdus). Aucune logique 3h30 carré.
2. **Format "notice"** — l'élève suit en pilote auto sans construire de réflexe. Aucun apprentissage durable.
3. **Profils mixtes ingérés ensemble** — un même groupe contient l'élève "blank" qui code à la main et le vibe-codeur qui tape `/init` puis "fais-moi l'atelier 02". Le second produit une solution sans rien apprendre (illusion de compétence — cf. Prather ICER 2024).
4. **Scope leak** — le vibe-codeur récupère des morceaux d'ateliers suivants (agent ReAct dans At.02, fine-tuning dans At.03). Le `verify_branch_scope.sh` existant a déjà été cassé (commit `feedb98`).
5. **Pas de mesure** — l'élève ne sait pas si "ça marche bien", il n'a pas de benchmark à défendre devant un pair.
6. **Jargon non vulgarisé** — At.04 contient GPU/VRAM/lr/grid search/HF Hub/W&B/QLoRA quantization sans définition pour public non-tech. Cette critique s'étend à tous les ateliers (embedding, MMR, ReAct, p95, slowapi, etc.).

## Solution retenue

Approche pédagogique fondée sur 6 piliers validés par la littérature (Freeman PNAS 2014, Kapur Productive Failure, Bjork Desirable Difficulties, Sweller Cognitive Load, Tomlinson Differentiated Instruction, Mazur Peer Instruction) — voir Annexe A du plan pour les 12 sources clés.

**4 mécanismes anti-vibe-coding combinés** :

1. **Double piste Build/Vibe** assumée, avec prompt-guard outillé (`CLAUDE.md` local + hook `UserPromptSubmit` + `.cursorrules`) qui rend la triche vérifiable.
2. **Bug Hunt anti-cheat** : patches git + tests pytest + `solution.py` migrée sur branche séparée.
3. **Mission noire** : chaque atelier = brief client HomeButler, pas une notice.
4. **Checkpoints auto-évaluables** : QCM auto-corrigé + LLM-judge avec rubric + démo pair optionnelle.

**Calibrage en rails parallèles** (pas additif) : 20min Setup + 1h40 Core + (30min Sprint **XOR** 60min Bonus) + 10min Wrap-up = 3h30 max.

**Scope strict outillé** : tableau de concepts autorisés/interdits par atelier, feature flag `ENABLE_COMPARE_ROUTES` pour résoudre le leak At.05↔06, extension de `verify_branch_scope.sh`.

**Mesurabilité** : chaque atelier embarque une section `🔬 Mini-lab` (faire varier un paramètre, observer) et `📊 Mesure-toi` (calculer recall@k, latence, perplexité, etc.) — toutes scope-safe.

**Vulgarisation systématique** : mini-lexique jargon→analogie obligatoire en tête du Carnet de bord de chaque atelier (modèle exemplaire de 16 termes pour At.04).

## Public cible

Employés d'entreprise, formation continue. Profils mixtes :
- Niveau technique variable (de junior dev à PM curieux)
- Pas de prérequis ML — première formation RAG pour la majorité
- Outils utilisés : Mac (sans GPU), VS Code / Cursor / Claude Code, terminal zsh
- Pas d'expertise GPU/CUDA/Colab acquise

## Contraintes

- Pas de modification de `tps.md`, `examples-supports/*`, `homebutler/*` (sauf cas justifié)
- Conserver les blocs déjà rédigés dans `tps.md` (Vulgarisation, Erreurs communes, Pont projet, Critères de succès) → recyclage tel quel
- Renommer chaque `README.md` d'atelier en `README-formateur.md` (le `GUIDE-ELEVE.md` devient l'unique point d'entrée élève)
- Migrer `solution.py` sur branches `solution/at0X` (anti-cheat Bug Hunt)
- Feature flag `ENABLE_COMPARE_ROUTES` à ajouter dans `api/main.py` avant la rédaction At.05 et At.06

## Livrable

- Plan détaillé v2 dans `plan-supports-tp-autonomes-v2.md` (ce dossier)
- Suivi d'exécution dans `todos.md` (ce dossier)
- Insights itératifs dans `insights.md` (ce dossier)
- À terme : les fichiers énumérés dans §10 du plan
