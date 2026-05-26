# Todos — Réorganisation livraison formation

## Phase 0 — Vérification (avant toute action)

- [ ] **T0.1** Vérifier l'état exact des branches student/01-06 dans training-rag
  ```bash
  for b in student/01-llm-baseline student/02-rag-simple student/03-pipeline-agent student/04-finetuning student/05-deploiement student/06-finetune-vs-rag; do
    echo "=== $b ==="; git -C /Users/yohannravino/Factory/training-rag ls-tree -r $b --name-only | grep -E "\.agent|formateur"
  done
  ```
- [ ] **T0.2** Confirmer que les 15 tests passent sur la branche courante de training-rag
  ```bash
  git -C /Users/yohannravino/Factory/training-rag checkout atelier/06-finetune-vs-rag
  pytest --tb=short -q
  ```

---

## Phase 1 — Nettoyage branches student dans training-rag

### AT02 en premier (atelier pivot — valide le pattern)

- [ ] **T1.1** `git checkout student/02-rag-simple`
- [ ] **T1.2** `git rm -r .agent/tasks/` (si présent confirmé par T0.1)
- [ ] **T1.3** `git rm ateliers/atelier-02-rag-simple/README-formateur.md`
- [ ] **T1.4** Vérifier imports : `python -c "import homebutler; print('OK')"`
- [ ] **T1.5** Vérifier exercice.py se lance : `python ateliers/atelier-02-rag-simple/exercice.py`
- [ ] **T1.6** `git commit -m "clean(student/02): retirer .agent/tasks/ et README-formateur.md"`
- [ ] **T1.7** Vérifier : `git ls-tree -r HEAD --name-only | grep -E "\.agent|formateur"` → vide

### AT01

- [ ] **T1.8** Même séquence sur `student/01-llm-baseline`

### AT03

- [ ] **T1.9** Même séquence sur `student/03-pipeline-agent`

### AT04

- [ ] **T1.10** Même séquence sur `student/04-finetuning`

### AT05

- [ ] **T1.11** Même séquence sur `student/05-deploiement`

### AT06

- [ ] **T1.12** Sur `student/06-finetune-vs-rag` : vérifier .agent/ résiduel + README-formateur.md, même séquence

---

## Phase 2 — Branches solution manquantes

- [ ] **T2.1** Créer `solution/at04` en suivant le pattern de `solution/at01` (~30 fichiers : exercice + solution + README minimal)
- [ ] **T2.2** Créer `solution/at05`
- [ ] **T2.3** Créer `solution/at06`

---

## Phase 3 — Push remote

- [ ] **T3.1** Push toutes les branches student nettoyées :
  ```bash
  git -C /Users/yohannravino/Factory/training-rag push origin \
    student/01-llm-baseline student/02-rag-simple student/03-pipeline-agent \
    student/04-finetuning student/05-deploiement student/06-finetune-vs-rag
  ```
- [ ] **T3.2** Push branches solution nouvelles

---

## Phase 4 — Documentation formateur dans pre-training-rag

- [ ] **P1** Ajouter `notes-formateur-vulgarisation.md` au `.gitignore` racine de pre-training-rag
- [ ] **P2** Créer `_formateur/DEROULE-FORMATION.md` : antisèche per-atelier (slides à projeter, commandes git, timing Core/Sprint/Bonus)
- [ ] **P3** Créer `_formateur/INDEX-EXTRAS-VIBE.md` : index des exercices bonus par atelier

---

## Phase 5 — Vérification finale

- [ ] **V1** Sur chaque student/XX : `git ls-tree -r HEAD --name-only | grep -E "\.agent|formateur"` → vide
- [ ] **V2** Sur student/02 : `pytest ateliers/atelier-02-rag-simple/bugs/ -v` → 3 tests dans état attendu
- [ ] **V3** Sur atelier/06 (main ref) : `pytest --tb=short -q` → 15 tests PASS
