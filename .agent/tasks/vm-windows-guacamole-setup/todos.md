# Todos — Setup VM Windows Guacamole

> Légende : `[ ]` à faire · `[~]` en cours · `[x]` terminé · `[!]` bloqué/dépendance externe

---

## Phase 0 — Pré-vérification

- [ ] **0.1** Double-cliquer sur `Install-Formati...` sur le bureau → noter ce qui est installé
- [ ] **0.2** Ouvrir CMD → `python --version` et `git --version` → noter les versions ou "non trouvé"
- [ ] **0.3** Vérifier génération HyperV : `systeminfo | findstr /i "BIOS"` → UEFI ou Legacy ?

---

## Phase 1 — Environnement système

### Voie A — WSL2 (si UEFI confirmé)
- [ ] **1A.1** Confirmer avec admin que nested virtualization est activée sur la VM HyperV
- [ ] **1A.2** `wsl --install` dans PowerShell admin → redémarrer
- [ ] **1A.3** Créer user Unix dans Ubuntu (`formateur` / `raft2026`)
- [ ] **1A.4** `sudo apt update && apt upgrade -y`
- [ ] **1A.5** `sudo add-apt-repository ppa:deadsnakes/ppa && apt install python3.13 python3.13-venv python3.13-dev git curl`
- [ ] **1A.6** `python3.13 --version` → confirmer Python 3.13.x
- [ ] **1A.7** `hostname -I` → noter l'IP WSL2 (ex: 172.x.x.x) — utilisée pour tous les accès browser

### Voie B — Fallback Python natif Windows (si Legacy ou WSL2 échoue)
- [ ] **1B.1** `winget install Git.Git` dans PowerShell admin
- [ ] **1B.2** Télécharger Python 3.13 depuis python.org → installer avec "Add to PATH"
- [ ] **1B.3** `python --version` dans Git Bash → confirmer 3.13.x
- [ ] **1B.4** Noter : remplacer `source .venv/bin/activate` par `.venv/Scripts/activate` dans toutes les commandes

---

## Phase 2 — Projet

- [ ] **2.1** `git clone https://github.com/YoLoADR/pre-training-rag.git ~/formation`
- [ ] **2.2** `cd ~/formation && python3.13 -m venv .venv && source .venv/bin/activate`
- [ ] **2.3** `pip install --upgrade pip && pip install -r requirements.txt`
- [ ] **2.4** `pip install -e .` ← obligatoire sinon Streamlit ne trouve pas `homebutler`
- [ ] **2.5** Vérification imports critiques (langchain, chromadb, fastembed, fitz, fastapi, streamlit)

---

## Phase 3 — Configuration .env

- [ ] **3.1** `cp .env.example .env`
- [ ] **3.2** Renseigner `ANTHROPIC_API_KEY=sk-ant-...` ← seule variable obligatoire au démarrage
- [ ] **3.3** Renseigner `OLLAMA_MODEL=qwen2.5:7b-instruct`
- [ ] **3.4** Renseigner clés Langfuse si disponibles (optionnel — J2/J3)

---

## Phase 4 — Ollama + modèles

- [ ] **4.1** Télécharger et installer OllamaSetup.exe depuis ollama.com/download/windows
- [ ] **4.2** `ollama pull qwen2.5:7b-instruct` (~4.7 Go)
- [ ] **4.3** `ollama pull phi4-mini` (~2.8 Go)
- [ ] **4.4** `ollama pull mistral:7b-instruct` (~4.1 Go)
- [ ] **4.5** Test démo live : `ollama run qwen2.5:7b-instruct "Explique RAG en 3 phrases en français"`
- [ ] **4.6** `ollama ps` → noter PROCESSOR (100% CPU ou 100% GPU)
- [ ] **4.7** Consigner le verdict GPU dans `insights.md`

---

## Phase 5 — Validation API Anthropic

- [ ] **5.1** Test clé API avant indexation :
  ```bash
  python -c "from homebutler.llm.provider import get_llm; llm=get_llm(temperature=0.1,max_tokens=50); resp=llm.invoke('OK'); print(resp.content)"
  ```
- [ ] **5.2** Confirmer réponse sans erreur 401

---

## Phase 6 — Données et indexation RAG

- [ ] **6.1** `python scripts/preload_models.py` → modèle ONNX fastembed (~100 Mo)
- [ ] **6.2** `python scripts/generate_documents.py` → 6 PDFs
- [ ] **6.3** `python scripts/generate_energy_data.py` → CSV 365 jours
- [ ] **6.4** `python scripts/generate_producers.py` → JSON 30 producteurs
- [ ] **6.5** `python scripts/generate_qa_dataset.py` → JSONL 150 Q/A
- [ ] **6.6** Indexation FAISS + ChromaDB + test retrieval
- [ ] **6.7** Confirmer N chunks indexés + test retrieval "chaudière nuit"

---

## Phase 7 — Services

- [ ] **7.1** Lancer FastAPI : `uvicorn api.main:app --reload --port 8000 --host 0.0.0.0`
- [ ] **7.2** Vérifier `http://<IP-WSL2>:8000/docs` accessible depuis Firefox Windows
- [ ] **7.3** Lancer Streamlit : `streamlit run ui/app.py --server.port 8501 --server.address 0.0.0.0`
- [ ] **7.4** Vérifier `http://<IP-WSL2>:8501` accessible
- [ ] **7.5** Lancer Gradio : `python ui/gradio_prototype.py`
- [ ] **7.6** Vérifier `http://<IP-WSL2>:7860` accessible

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

- [ ] **9.1** Test RAG : `curl -X POST http://localhost:8000/rag/retrieve -d '{"query":"chaudière","k":3}'`
- [ ] **9.2** Test Chat agent : `curl -X POST http://localhost:8000/chat -d '{"message":"temp chaudière nuit?"}'`
- [ ] **9.3** Test énergie : `curl -X GET http://localhost:8000/consumption`
- [ ] **9.4** Switcher `LLM_PROVIDER=ollama` dans `.env` → relancer API → re-tester `/chat`
- [ ] **9.5** Comparer qualité réponse Anthropic vs Ollama qwen2.5 → consigner dans `insights.md`

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

## Statut global

- [ ] Phase 0 complète
- [ ] Phase 1 complète
- [ ] Phase 2 complète
- [ ] Phase 3 complète
- [ ] Phase 4 complète
- [ ] Phase 5 complète
- [ ] Phase 6 complète
- [ ] Phase 7 complète
- [ ] Phase 8 complète
- [ ] Phase 9 complète
- [ ] Phase 10 complète
- [ ] Phase 11 complète
