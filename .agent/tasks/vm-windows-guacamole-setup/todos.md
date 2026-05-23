# Todos — Setup VM Windows Guacamole

> Légende : `[ ]` à faire · `[~]` en cours · `[x]` terminé · `[!]` bloqué/dépendance externe

---

## Phase 0 — Pré-vérification

- [x] **0.1** Double-cliquer sur `Install-Formati...` sur le bureau → script `Install-FormationRAFT.ps1` déjà exécuté
- [x] **0.2** `python --version` → **Python 3.13.13** ✅ — installé en natif Windows
- [x] **0.3** HyperV Gen 2 confirmé implicitement (script a tourné, pas de WSL2 utilisé — installation 100% native Windows)
- [x] **0.4** Architecture choisie : **Python natif Windows** (pas WSL2) → `localhost` fonctionne directement dans Firefox
- [x] **0.5** Projet cloné à `C:\Formation_RAFT\pre-training-rag` (chemin défini dans le script)
- [x] **0.6** Claude Code CLI absent : `claude --version` → commande non reconnue

---

## Phase 1 — Environnement système

### Voie retenue — Python natif Windows (script Install-FormationRAFT.ps1 déjà exécuté)
- [x] **1.1** Python 3.13.13 installé (`C:\Users\PLB\AppData\Local\Programs\Python\Python313\`)
- [x] **1.2** Git : `git version 2.54.0.windows.1` ✅
- [x] **1.3** Ollama : `ollama version 0.24.0` ✅
- [x] **1.4** Projet cloné : ❌ `C:\Formation_RAFT` existe mais `pre-training-rag` absent — clone a échoué (git pas dans PATH au moment du script)
- [x] **1.5** Venv : ❌ absent (clone manquant)
- [x] **1.6** .env : ❌ absent (clone manquant)
- [x] **1.7** Modèle Ollama `mistral:7b-instruct` : ✅ présent (4.4 GB, il y a 41h)

---

## Phase 2 — Projet (à faire dans PowerShell)

- [ ] **2.1** `git clone https://github.com/YoLoADR/pre-training-rag.git C:\Formation_RAFT\pre-training-rag`
- [ ] **2.2** `cd C:\Formation_RAFT\pre-training-rag`
- [ ] **2.3** `python -m venv .venv`
- [ ] **2.4** `.\.venv\Scripts\Activate.ps1` (ou `Activate.bat` dans CMD)
- [ ] **2.5** `pip install --upgrade pip`
- [~] **2.6** `pip install -r requirements.txt` — BLOQUÉ sur `chroma-hnswlib` (pas de wheel cp313)
  - [x] Fix slowapi : `slowapi>=0.5.7` → `>=0.1.0` (corrigé dans le repo)
  - [x] VS Build Tools → ABANDONNÉ (inacceptable sur chaque machine)
  - [x] chromadb 1.5.9 → INCOMPATIBLE avec langchain-community 0.3.14
  - [x] **FIX RETENU** : VS Build Tools 2022 installés via winget (version 17.14.33) ✅
    - [x] **2.6a** `winget install Microsoft.VisualStudio.2022.BuildTools` → téléchargé et installé
    - [ ] **2.6b** **REDÉMARRER la VM** (requis pour finaliser l'installation du compilateur)
    - [ ] **2.6c** Après reboot : rouvrir PowerShell, `cd C:\Formation_RAFT\pre-training-rag`, `.\.venv\Scripts\Activate.ps1`
    - [x] **2.6d** `pip install -r requirements.txt` → ✅ SUCCÈS (chroma-hnswlib compilé, slowapi 0.1.9 installé)
  - [ ] **TODO script** : Ajouter VS Build Tools dans `Install-FormationRAFT.ps1` (avant le pip install)
- [x] **2.7** `pip install -e .` → homebutler-1.0.0 installé ✅
- [x] **2.8** Vérification imports → `=== Tous les imports OK ===` ✅

---

## Phase 3 — Configuration .env

- [x] **3.1** `.env` créé à partir de `.env.example` ✅
- [x] **3.2** `ANTHROPIC_API_KEY` renseignée ✅
- [x] **3.3** `OLLAMA_MODEL=homebutler` (nom custom du projet — Modelfile basé sur mistral:7b-instruct)
- [x] **3.4** Clés Langfuse renseignées (`TRACING_PROVIDER=langfuse`) ✅
- [x] **3.5** Anthropic API OK : réponse `OK` reçue ✅

---

## Phase 4 — Ollama + modèles

- [x] **4.1** Ollama 0.24.0 installé (par Install-FormationRAFT.ps1) ✅
- [ ] **4.2** `ollama pull qwen2.5:7b-instruct` (~4.7 Go) — optionnel, mistral suffit pour la formation
- [ ] **4.3** `ollama pull phi4-mini` (~2.8 Go) — optionnel, backup démo rapide
- [x] **4.4** `ollama pull mistral:7b-instruct` → 4.4 GB présent ✅
- [x] **4.5** Test démo live : `ollama run mistral:7b-instruct` → répond en français ✅
- [x] **4.6** `ollama ps` → **PROCESSOR : 100% CPU** (pas de GPU sur VM HyperV) ✅
- [x] **4.7** Verdict GPU consigné dans `insights.md` ✅

---

## Phase 5 — Validation API Anthropic

- [ ] **5.1** Test clé API avant indexation :
  ```bash
  python -c "from homebutler.llm.provider import get_llm; llm=get_llm(temperature=0.1,max_tokens=50); resp=llm.invoke('OK'); print(resp.content)"
  ```
- [ ] **5.2** Confirmer réponse sans erreur 401

---

## Phase 6 — Données et indexation RAG

- [x] **6.1** `python scripts/preload_models.py` → modèle ONNX 384 dim, cache Windows ✅
- [x] **6.2** `python scripts/generate_documents.py` → 6 PDFs ✅
- [x] **6.3** `python scripts/generate_energy_data.py` → 365 lignes CSV ✅
- [x] **6.4** `python scripts/generate_producers.py` → 30 producteurs JSON ✅
- [x] **6.5** `python scripts/generate_qa_dataset.py` → 150 paires Q/A JSONL ✅
- [x] **6.6** Indexation FAISS + ChromaDB ✅
- [x] **6.7** 49 chunks indexés (6 PDFs → 12 pages → 49 chunks) ✅ — telemetry errors inoffensifs

---

## Phase 7 — Services

- [x] **7.1** FastAPI lancé → POST /chat 200 OK ✅
- [ ] **7.2** Ouvrir `http://localhost:8000/docs` dans Firefox → tester Swagger
- [x] **7.3** Streamlit lancé → `http://localhost:8501` ✅
- [ ] **7.4** Ouvrir `http://localhost:8501` dans Firefox → tester l'UI
- [x] **7.5** Gradio lancé → `http://127.0.0.1:7860` ✅
- [ ] **7.6** Ouvrir `http://localhost:7860` dans Firefox → tester le prototype

---

## Phase 8 — Jupyter + Notebooks

- [ ] **8.1** `jupyter notebook --no-browser --port=8888 --ip=0.0.0.0`
- [ ] **8.2** Copier le token depuis les logs → accéder à `http://<IP-WSL2>:8888/?token=...`
- [ ] **8.3** Ouvrir `01_llm_baseline.ipynb` → exécuter cellule par cellule
- [ ] **8.4** Ouvrir `02_ingestion_vectorisation.ipynb` → exécuter cellule par cellule
- [ ] **8.5** Confirmer notebook 03 → **Colab uniquement** (pas d'exécution locale)
- [ ] **8.6** Tester notebook 03 sur https://colab.research.google.com avec GPU T4

---

## Phase 9 — Tests end-to-end

- [x] **9.1** Test FastAPI `/chat` (Swagger) → réponse RAG Anthropic 200 OK ✅
      Agent a retrouvé notice Viessmann Vitodens 100-W et généré réponse structurée (tables, markdown)
- [ ] **9.2** Vérifier Streamlit UI `http://localhost:8501` dans Firefox
- [ ] **9.3** Vérifier Gradio `http://localhost:7860` dans Firefox
- [x] **9.4** Ollama homebutler testé → 200 OK ~3 min, qualité dégradée (comportement attendu CPU) ✅
- [x] **9.5** Comparaison Anthropic vs Ollama consignée dans insights.md ✅

---

## Phase 10 — Claude Code CLI

- [ ] **10.1** `irm https://claude.ai/install.ps1 | iex` dans PowerShell Windows
- [ ] **10.2** `claude --version`
- [ ] **10.3** `cd ~/formation && claude` → confirmer que Claude Code se lance sur le projet

---

## Phase 11 — Vérification globale finale

- [ ] **11.1** Script de vérification complet (Python + imports + Ollama + données + index)
- [ ] **11.2** Remplir le tableau de verdict GPU dans `insights.md`
- [ ] **11.3** Documenter les éventuels workarounds trouvés pendant le setup

---

## Phase 10 — Claude Code CLI

- [ ] **10.1** `winget install Anthropic.ClaudeCode` dans PowerShell admin
- [ ] **10.2** `claude --version` → confirmer installation
- [ ] **10.3** `cd C:\Formation_RAFT\pre-training-rag && claude` → lancer Claude Code sur le projet

## Phase 11 — Documentation mise à jour

- [x] **11.1** `PREREQUIS-FORMATION-RAFT.md` section 6 ajoutée (débogage Windows) ✅
- [x] **11.2** `Modelfile` ajouté au repo ✅
- [x] `requirements.txt` fix slowapi ✅
- [ ] **11.3** Commit final + push

## Statut global

- [x] Phase 0 complète ✅
- [x] Phase 1 complète ✅ (Python 3.13.13 natif Windows)
- [x] Phase 2 complète ✅ (clone + venv + pip install + pip install -e .)
- [x] Phase 3 complète ✅ (.env configuré, Anthropic + Langfuse)
- [x] Phase 4 complète ✅ (Ollama 0.24.0, mistral:7b-instruct, homebutler créé)
- [x] Phase 5 complète ✅ (Anthropic API validée)
- [x] Phase 6 complète ✅ (données générées, 49 chunks indexés FAISS + ChromaDB)
- [x] Phase 7 complète ✅ (FastAPI + Streamlit + Gradio lancés)
- [ ] Phase 8 — Jupyter (optionnel, à faire si besoin)
- [x] Phase 9 complète ✅ (tests end-to-end Anthropic + Ollama)
- [ ] Phase 10 — Claude Code CLI
- [x] Phase 11 partielle ✅ (doc mise à jour)
