# Context — Réorganisation livraison formation HomeButler AI

## Problème à résoudre

Les élèves sont perdus car :
1. **Notes formateur visibles dans leur projet** : `.agent/tasks/` (planning interne) et `README-formateur.md` (guide animateur) sont encore trackés sur les branches `student/XX` de `training-rag`
2. **Contrat de livraison flou** : aucun document ne dit explicitement "à cette étape, l'élève reçoit EXACTEMENT ces fichiers"
3. **Exercices vibe-coder introuvables** : ils existent (dans GUIDE-ELEVE.md §Bonus + fichiers standalone) mais pas d'index centralisé
4. **Architecture homebutler/ jamais documentée** : les élèves ne comprennent pas pourquoi certains fichiers sont blankés et d'autres non

## Périmètre

**Deux repos distincts :**

| Repo | Rôle | Accès |
|---|---|---|
| `pre-training-rag` | Zone formateur : slides, notes, planification (CE repo) | Formateur uniquement |
| `training-rag` | Zone élève : code HomeButler, exercices, branches student/ | Élèves (clone + checkout) |

**L'action se passe principalement dans `training-rag`** (nettoyage branches student).
**Ce repo (`pre-training-rag`) reçoit la documentation formateur** (DEROULE, INDEX-EXTRAS).

## Méthodologie pédagogique à respecter

```
1. Formateur projette slides/atelier-0X-corrige.md (depuis pre-training-rag)
2. Formateur démo live : git checkout atelier/0X → montrer solution.py
3. Élèves sur git checkout student/0X → exercice.py (blanké) + GUIDE-ELEVE.md
4. Fin session : git checkout atelier/0X -- .../solution.py (partage correction)
```

**Contraintes absolues :**
- Zéro régression : 15 tests PASS + 18 tests bug-hunt dans état attendu
- Ne pas toucher à homebutler/, api/, ui/ (code fonctionnel)
- Garder le versionning progressif (branches atelier/XX intactes)
- Blank et corrigé restent séparés (student/XX ≠ atelier/XX)

## Architecture homebutler/ (package central)

Le package est **progressivement révélé** d'atelier en atelier :

| Atelier | Fonctions blankées (NotImplementedError) | Fournies corrigées |
|---|---|---|
| AT01 | `get_llm()`, `get_llm_cached()`, 4 templates prompts | `config.py` (6 vars), `CONCIERGE_SYSTEM_PROMPT` |
| AT02 | `chunk_fixed_size/recursive/semantic()`, `get_embeddings()`, `build/load_faiss_index()` | `load_pdf_with_metadata()`, AT01 complet |
| AT03 | `get_ensemble_retriever()`, `get_agent_executor()` | `tools.py`, `services/`, AT01+02 complets |
| AT04 | Cellules LoRA notebook, `generate_qa_dataset.py`, `augment_qa_dataset.py` | `explore_dataset.py`, AT01+02+03 complets |
| AT05 | `_call_rag_only()`, `_call_agent()`, endpoint `/retrieve` | `api/main.py`, `ui/`, `api/limiter.py` |
| AT06 | 6 TODOs dans `evaluate_pipeline.py` | endpoints /rag/evaluate + /chat/compare |

## État connu des branches student (audit 2026-05-26)

**Déjà fait ✅** : GUIDE-FORMATEUR.md absent, code blanké, QUICK-START.md, STARTER.md, .claude/CLAUDE.md scope guards, slides corrigées absentes

**Reste à faire ❌** :
- `.agent/tasks/` encore présent sur student/01 à student/05
- `README-formateur.md` encore présent sur student/01 à student/06
- Branches solution/at04, at05, at06 absentes en local
