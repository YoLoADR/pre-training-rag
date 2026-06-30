# Contexte — Ajout des ateliers avancés AT07 / AT08 / AT09

## Objectif

Ajouter **3 ateliers complets** à la formation RAFT HomeButler (existant : AT01→06, 3 jours, fil rouge unique, local-first sans GPU), pour combler 3 chapitres du programme officiel Ambient IT (`Annexe-1-Fiche-descriptive-rag.pdf`) encore en creux, **tout en restant 100% réalisable depuis le terminal/CLI** et **sans toucher à l'existant AT01→06** :

- **AT07 — Observabilité & Évaluation** (chapitre PDF « Évaluation & observabilité ») : Langfuse + RAGAS + LLM-as-judge.
- **AT08 — Optimisation du pipeline RAG** (chapitre PDF « techniques avancées / optimisation pipeline ») : reranking cross-encoder CPU (flashrank), multi-query, HyDE.
- **AT09 — Azure AI Search** (chapitre PDF « RAG avec Azure AI Search », **priorité**) : control plane CLI `az search` vs data plane SDK ; index vectoriel 384d (fastembed) ; hybrid/semantic search.

## Contraintes (non négociables)

- **Zéro régression AT01→06** : code neuf = fichiers neufs (`homebutler/eval/`, `homebutler/rag/reranking.py`, `homebutler/rag/vectorstore_azure.py`) ; `config.py` modifié seulement par AT09 en additif, jamais re-cascadé.
- **Versioning progressif** : branches `atelier/07,08,09` + `student/07,08,09` depuis `atelier/06`/`student/06`, accumulant le code.
- **Scope strict par atelier** + dissociation blank/corrigé.
- **Pédagogie** : slides → présenter le corrigé → cacher → TP blank → partage correction via `git diff`. Pistes 🛠️ Build / 🎮 Vibe.
- **Apparat standard** identique à l'existant (GUIDE-ELEVE/FORMATEUR, bugs v1/v2/v3 + tests pytest, checkpoints, .claude/CLAUDE.md scope-strict, slides corrige/blank, requirements `-r`).
- **Tout fonctionnel, aucune régression** (cf. draft.md du formateur).

## Repos

- `/Users/yohannravino/Factory/training-rag` : repo ÉLÈVE (branches atelier/ + student/), c'est là que vit le code + les ateliers. Remotes : `github` (YoLoADR/training-rag) + `origin`.
- `/Users/yohannravino/Factory/pre-training-rag` : zone FORMATEUR (slides, _formateur/, ce dossier .agent/).

## Ordre

Construction : **AT08 → AT07 → AT09**. Enseignement : AT07 → AT08 → AT09.

## Plan détaillé

Voir `plan-ateliers-avances.md` (copie du plan approuvé) dans ce dossier.
Plan canonique : `~/.claude/plans/je-dois-ajouter-des-glowing-gizmo.md`.
