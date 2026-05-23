# Insights — Ateliers progressifs Formation RAFT

*Mis à jour au fur et à mesure de l'avancement*

---

## Découvertes critiques (issues détectées avant implémentation)

### 1. Import ChromaDB au niveau module dans vectorstore.py
**Problème** : `vectorstore.py` importe `from langchain_community.vectorstores import Chroma` à la ligne 9. Si chromadb n'est pas installé (atelier/02), l'import du module entier crash avec `ImportError`.  
**Solution** : Scinder en `vectorstore_faiss.py` (atelier/02) et `vectorstore_chroma.py` (atelier/03+). `vectorstore.py` en main réexporte tout.

### 2. Notebook 02 importe ChromaDB (incompatible avec atelier/02 FAISS-only)
**Problème** : `02_ingestion_vectorisation.ipynb` ligne 201 : `build_chroma_db(chunks_recursive, ...)`. Incompatible avec la règle "FAISS seul en atelier/02".  
**Solution** : Créer `02_rag_simple_faiss.ipynb` (sections 1-4 FAISS uniquement) pour atelier/02. L'original reste pour atelier/03+.

### 3. `api/routers/rag.py` existe déjà dans main avec les 3 endpoints
**Problème** : Le plan initial disait "nouveau fichier en atelier/06". FAUX — il existe déjà.  
**Solution** : En atelier/05, `/rag/retrieve` seul ; en atelier/06, ajouter `/rag/evaluate` et `/rag/compare-strategies`.

### 4. Stratégie "branche depuis commit vide" non-viable
**Problème** : Le projet a été construit en une fois (pas d'historique git chapitre par chapitre). Créer une branche vide ne donne pas un projet fonctionnel.  
**Solution** : Créer chaque branche **depuis main** puis supprimer progressivement les fichiers hors-scope. Garantit des imports fonctionnels dès le départ.

### 5. `pip install -e .` obligatoire pour Streamlit
**Problème** : Sans `pip install -e .`, Streamlit ne trouve pas le package `homebutler` (import relatif). C'est le problème le plus fréquent lors du démarrage.  
**Action** : Inclure cette commande dans CHAQUE README d'atelier, avec une vérification : `python -c "import homebutler"`.

### 6. solution.py = import depuis homebutler/ (pas de duplication de code)
**Décision** : `solution.py` **importe** depuis `homebutler/` et ajoute les commentaires pédagogiques autour des appels — pas de copie du code source. Évite le drift de maintenance.

---

## Alignement avec les slides de formation (points importants)

### Chapitre 2 — RAGAs (Slide 8)
4 métriques clés à mentionner dans atelier/02 :
- Faithfulness (le LLM invente-t-il des infos non présentes dans les chunks ?)
- Answer Relevance (la réponse répond-elle à la question ?)
- Context Precision (les chunks récupérés sont-ils pertinents ?)
- Context Recall (les bons chunks sont-ils récupérés ?)

### Chapitre 4 — 5 pièges du FT (Slide 9)
À inclure dans README atelier/04 :
1. Catastrophic forgetting → mélanger 20-30% données générales
2. Overfitting sur petit dataset → val_loss monte
3. Mauvais base model → vérifier support français
4. Learning rate trop élevé → essayer 1e-4, 2e-4, 5e-4
5. Pas de split validation → split 80/10/10 obligatoire

### Chapitre 6 — RAFT (Slide 6)
Zhang et al., 2024 : entraîner sur oracle + distracteurs = robustesse au bruit. Résultats : hybride (94%) > RAG seul (89%) > FT seul (79%) sur QA factuel.  
À mentionner dans README atelier/06 et grille_decision.md.

### Concepts présents dans slides mais hors-scope des ateliers
- **Distillation** (Slide 10 Chapitre 4) : mentionner comme perspective avancée dans README atelier/04
- **Reranking** (Slide 7 Chapitre 2) : mentionner comme extension optionnelle dans evaluate_rag.py
- **Jan.ai** (Slide 3 Chapitre 5) : expliquer le choix Ollama (LangChain natif) vs Jan.ai (GUI seulement) dans checklist atelier/05
- **Weaviate, LlamaIndex, Haystack** : tableau comparatif dans slides, pas d'implémentation — laisser dans notebook 02

---

## Décisions de conception

### Format des commentaires pédagogiques
Différent selon le type de concept :
- **Concept théorique** (atelier 01-03) : bloc `═══ CONCEPT RAG : ... ═══`
- **Concept FT** (atelier 04, Jupyter) : `# ─── FT CONCEPT : ... ───`
- **Concept sécurité/prod** (atelier 05) : `# SÉCURITÉ : ...`

### Scope strict des exercises
- L'exercice demande de **câbler** les outils existants (tools.py), pas de les réimplémenter
- 4-6 TODOs par exercice maximum (sinon trop long pour une demi-journée)
- Chaque TODO = 1 concept, 1 appel de fonction

### Requirements progressifs
Un `requirements_atelier0X.txt` par branche pour éviter que les élèves installent 47 packages dès le jour 1.

---

## À surveiller lors de l'implémentation

- Vérifier que `homebutler/__init__.py`, `homebutler/llm/__init__.py`, `homebutler/rag/__init__.py` etc. existent dans chaque branche (nécessaires pour les imports)
- Le `.env.example` de chaque branche doit être minimal (uniquement les variables utiles à ce chapitre)
- Les scripts `generate_*.py` dépendent de pandas/fpdf2 — ces packages doivent être dans les requirements de la branche correspondante
- La commande `python scripts/preload_models.py` doit être lancée UNE FOIS avant atelier/02 (télécharge le modèle d'embedding ~300MB)
