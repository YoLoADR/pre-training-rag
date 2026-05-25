# Insights — Branches `student/XX-…` blanks avec indices

> Apprentissages itératifs accumulés au fil de l'exécution. Pré-rempli des 16 findings issus de la Phase 0 d'audit (3 agents en parallèle).

## I. Découvertes de l'audit initial (Phase 0)

### I.1 — Réalisme technique du blanking (Agent 1)

- **AT02 : la vraie cible n'est pas `vectorstore.py`** mais `homebutler/rag/vectorstore_faiss.py` (71 lignes, 3 fonctions). `vectorstore.py` est un ré-export de 17 lignes — trop fin pour blanker.
- **AT06 : les deltas API sont anémiques.** `git diff atelier/05..atelier/06 -- api/routers/chat.py` = **4 lignes** seulement (removal timeout) ; `rag.py` = 0 ligne. Conclusion : `evaluate_pipeline.py` est le **seul** vrai porteur pédagogique d'AT06.
- **`api/limiter.py` = 5 lignes, 1 instruction.** Aucune valeur à blanker — c'est de la plomberie sans concept.
- **Risque `NameError` AT03 :** si `homebutler/agent/tools.py` construit `ALL_TOOLS` dynamiquement (vs constante top-level), blanker `tools.py` casse l'import de `react_agent.py` qui fait `from homebutler.agent.tools import ALL_TOOLS`. Vérification préalable nécessaire (cf. todos.md Phase 1).
- **Notebooks bas-risque si on respecte la règle :** remplacer le contenu de la cellule code par `raise NotImplementedError(...)` ne touche pas aux UUID des cellules. Mais édition JSON manuelle = corruption garantie. Toujours passer par `nbformat`.

### I.2 — Trous et risques de régression (Agent 2)

- **Bug Hunt cassé par les blanks (résolu en Rev 2) :** les `bugs/v*.patch` s'appliquent sur `solution.py` qui importe `homebutler/*`. Si `homebutler` est blanké, `solution.py` crashe à l'exécution. Solution Rev 2 = ordre séquentiel imposé (remplir blanks → puis Bug Hunt).
- **`.claude/CLAUDE.md` + hook `UserPromptSubmit` étaient absents du plan Rev 1.** Sans eux, un élève demande à Claude/Cursor "remplis ce NotImplementedError" et obtient la solution. Rev 2 enrichit le CLAUDE.md avec clause socratique explicite.
- **`solution.py` reste visible** sur `student/XX` (cohérent avec l'existant). Le risque `cat solution.py` est mitigé par le fait que `solution.py` importe depuis `homebutler/` blanké — il devient inutilisable comme cheat-sheet.
- **Synchronisation `pre-training-rag` ↔ `training-rag` non triviale.** Décision Rev 2 : autorité = `training-rag` pour le code projet, `pre-training-rag` pour supports formateur. PR croisée manuelle si correction critique.
- **Onboarding élève flou en Rev 1 (résolu).** Création de `STARTER.md` à la racine de `training-rag` pour pointer vers `git checkout student/XX-…` + `check_atelier_ready.sh`.
- **Décisions git arrêtées en Rev 2 :** pas de tags student, push remote oui, CI légère (verify_branch_scope + import smoke uniquement — pas de pytest qui doit échouer par conception).

### I.3 — Cohérence pédagogique (Agent 3)

- **`MISSION.md` était une duplication.** Le `GUIDE-ELEVE.md` existant d'AT02 fait 438 lignes et contient déjà mission narrative PM, périmètre, carnet de bord avec mini-lexique, étapes du tronc commun, pièges, erreurs communes. Rev 2 abandonne `MISSION.md` et enrichit le `GUIDE-ELEVE.md` existant + `QUICK-START.md` 1 page.
- **3 niveaux d'indices = redondance cognitive** dans 10-15 lignes de docstring. Rev 2 = **2 niveaux uniquement** : léger (« quel objet chercher ») et fort (« quels arguments / quelle méthode appeler »).
- **Cohérence des analogies confirmée** avec lexique `GUIDE-FORMATEUR.md` existant. Chunking = découper interview/fiches révision ; embedding = code-barres sémantique / coordonnées GPS sémantiques ; FAISS = bibliothèque organisée par sens ; ReAct = détective qui pense/agit/observe ; LoRA = notes adhésives sur quelques zones du cerveau ; prompt injection = lettre piégée.
- **Objectif AT02 corrigé :** Rev 1 disait Recall@3 ≥ 0.7 (arbitraire). Standard projet = **Recall@5 ≥ 0.80 ET Faithfulness ≥ 0.85** (référence : `evaluate_rag.py` + `GUIDE-FORMATEUR.md` AT02 l.387). Aligné en Rev 2.
- **Calibrage AT03 à risque.** Blanker à la fois `react_agent.py`, `tools.py`, `retriever.py`, `vectorstore_chroma.py` ferait exploser le budget 1h40. Rev 2 = scope réduit à `react_agent.py` + `retriever.py` uniquement. Les autres restent corrigés (lecture pour l'élève — le pattern `@tool` LangChain n'est pas pivot pédagogique).
- **Anti-vibe insuffisant en Rev 1.** Ajout en Rev 2 d'un QCM "explication personnelle" dans `check_1.py` qui force la verbalisation avant de récupérer la solution via git diff.

## II. Apprentissages au fil de l'exécution

### Phase 0 — Audit prep
**Date** : 2026-05-25
**Découvert** : `homebutler/agent/tools.py:131` expose bien `ALL_TOOLS` au top-level (constante directe, pas construction dynamique). Aucun risque `NameError` à craindre quand on blank `react_agent.py` qui fait `from homebutler.agent.tools import ALL_TOOLS`.
**Impact** : Phase A peut blanker `react_agent.py` sans précaution supplémentaire.
**Décision** : aucun garde-fou complémentaire requis.

### Phase A — Code blanks (6 branches)
**Date** : 2026-05-25
**Découvert** :
- L'environnement Python du venv `training-rag/.venv` est cassé (python 3.14 binary qui charge depuis 3.13 site-packages). Conséquence : `import fitz` échoue malgré `pip install pymupdf` réussi. **Workaround** : on s'est rabattu sur `python3 -m py_compile` (syntax-check seulement, pas d'import réel) pour valider chaque blanking. Suffisant pour la signature pédagogique.
- Le pattern « blank avec `Ellipsis` (`...`) comme valeur de défaut dans la signature + `# TODO (indice…)` en commentaire » fonctionne bien pour les paramètres ciblés (cas AT01 `temperature: float = ...`). Pas d'erreur de syntaxe, l'élève voit clairement qu'il doit remplir une vraie valeur.
- AT05 : la « détection prompt injection » mentionnée dans le plan vit en réalité dans `api/main.py` (middleware + `_INJECTION_PATTERNS`), pas dans `api/routers/rag.py`. Comme `main.py` est listé HORS-scope du blanking (plomberie), on l'a laissé corrigé. Décision pragmatique : le concept se voit en LECTURE pour les élèves AT05.
- AT06 : les TODOs étaient déjà dans le code corrigé (commentaires `─── TODO N — …`). Il a suffi de blanker 3 fonctions (TODO 2/3/5) ; les 3 autres (1, 4, 6) sont utilitaires/placeholders.
- AT04 notebook : `scripts/blank_notebook.py` avec nbformat fonctionne parfaitement (3 cellules réécrites, structure JSON préservée). À garder dans la branche student/04 pour reproductibilité.
**Impact** : pattern de blanking validé, signatures préservées, imports OK.
**Décision** : aucune correction nécessaire pour Phase B/C.

### Phase B — Pédagogie (GUIDE + QUICK-START + CLAUDE + check_1)
**Date** : 2026-05-25
**Découvert** :
- Les `GUIDE-ELEVE.md` existants sont longs (200-500 lignes) mais bien structurés. L'ajout de la section « 🎯 Atelier XX en un coup d'œil » EN TÊTE (avant « Pré-vol ») fonctionne très bien : l'élève voit immédiatement l'état initial / objectif / récupération solution sans devoir scroller.
- Pour `check_1.py`, on a 2 styles existants : (a) QCM A/B/C/D avec `input()` simple (AT01, AT02, AT03), (b) verbalisation par mots-clés (AT04, AT05, AT06). Notre ajout « explication personnelle » s'intègre bien sans casser le style.
- Les `.claude/CLAUDE.md` existaient déjà avec une partie « anti-vibe » générique. On a ajouté une CLAUSE SPÉCIFIQUE au blanking (NotImplementedError + # TODO + git diff) avec une question socratique calibrée par atelier (chunking récursif, temperature, ensemble retriever, LoRA target_modules, async executor, HTTP vs imports).
**Impact** : 4 livrables/atelier × 6 = 24 fichiers modifiés, cohérence pédagogique préservée.
**Décision** : pattern stabilisé.

### Phase C — Slides (6 decks)
**Date** : 2026-05-25
**Découvert** :
- Format imposé par `slides-formation-raft.md` : header `📝 Slide N : Titre`, puis « POURQUOI … » en italique, puis contenu (tables / code blocks / analogies / pièges).
- Le pattern le plus efficace pour montrer une évolution = bloc « AVANT (blank) … APRÈS (corrigé) » avec des commentaires inline qui expliquent l'AVANTAGE et vulgarisent les termes (LCEL, NF4, RRF, etc.). C'est ce qu'a demandé l'utilisateur.
- 6 decks × ~200-290 lignes = ~1500 lignes de slides au total. Suffisant pour 30-45 min de présentation par atelier.
**Impact** : decks stockés dans `pre-training-rag/slides/atelier-XX-student.md` (autorité support formateur).
**Décision** : prêt pour présentation.

### Phase D — Finalisation
**Date** : 2026-05-25
**Découvert** :
- Les 6 branches `student/XX-…` descendent de `atelier/XX-…`, pas de `main`. Pour propager `STARTER.md` + workflow CI à toutes les branches, le `cherry-pick` du commit main fonctionne sans conflit (les fichiers `.github/workflows/student-branches.yml` et `STARTER.md` sont nouveaux).
- Pas de push remote effectué — décision à valider avec l'utilisateur (action sensible).
**Impact** : 6 branches student locales prêtes pour push.
**Décision** : demander confirmation push à l'utilisateur.

## III. Risques résiduels à surveiller en exécution

- **Si le smoke test "recette suffisante" sur AT02 échoue** : ne PAS répliquer le pattern sur les autres ateliers. Itérer sur AT02 (recette trop floue, indices trop vagues, lexique incomplet) avant de continuer.
- **Si le calibrage AT03 reste > 1h40 même avec scope réduit** : envisager de blanker uniquement `retriever.py` (concept EnsembleRetriever) et laisser `react_agent.py` entièrement corrigé.
- **Si un élève contourne les indices via LLM externe (ChatGPT, etc.)** : nos garde-fous (`.claude/CLAUDE.md`, hook) ne couvrent que Claude Code et Cursor. Risque résiduel accepté en formation supervisée.
- **Si `pre-training-rag` et `training-rag` divergent sur `homebutler/`** : autorité = `training-rag`, mais aucun mécanisme automatique de détection. Audit manuel recommandé en fin de chantier.

## IV. Choix architecturaux délibérément non retenus

- **Branches `solution/at0X` séparées** (pour cacher `solution.py`) : non retenu en Rev 2 car incohérent avec l'existant (pre-training-rag ne le fait que pour AT01-03). Basculement possible en Rev 3 si retour terrain.
- **Script AST automatique pour les blanks Python** : non retenu (trop fragile pour 6 ateliers × ~15 fichiers). Edit manuel via Claude Code reste le bon ROI.
- **Tags `student-vX.Y`** : non retenus (les branches `student/XX-…` ne sont pas des releases).
- **Fichier `MISSION.md` séparé** : non retenu (duplication avec `GUIDE-ELEVE.md` existant — voir I.3).
- **3 niveaux d'indices** : non retenus (redondance cognitive — voir I.3).
