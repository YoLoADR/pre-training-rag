# Checklist déploiement HomeButler — Atelier 05

## 1. Local (poste développeur)

- [ ] `python -m venv .venv && source .venv/bin/activate`
- [ ] `pip install -r requirements_atelier05.txt`
- [ ] `pip install -e .`     ← **OBLIGATOIRE** pour Streamlit (imports croisés)
- [ ] `.env` complété : `ANTHROPIC_API_KEY`, `OLLAMA_MODEL`, ...
- [ ] Index vectoriels construits (FAISS + Chroma)
- [ ] `uvicorn api.main:app --reload --port 8000` → vérifier `/docs`
- [ ] `streamlit run ui/app.py` → 4 pages chargent
- [ ] `bash ateliers/atelier-05-deploiement/test_securite.sh` → tous tests OK

## 2. VPS (Ubuntu / Debian)

- [ ] Python 3.11+ installé (`python3 --version`)
- [ ] `git clone ...` + créer un venv dédié
- [ ] Variables d'env dans `/etc/systemd/system/homebutler.service`
- [ ] Reverse-proxy nginx → uvicorn (port 8000 interne)
- [ ] HTTPS via certbot (let's encrypt gratuit)
- [ ] Firewall : ouvrir 80/443, fermer 8000/8501
- [ ] Logs centralisés (journalctl ou Loki)
- [ ] Backup quotidien de `data/` et `data/chroma_db/`

## 3. Docker (`docker-compose.yml` fourni)

```bash
docker compose build
docker compose up -d
docker compose logs -f api
```

Services :
- `api` : FastAPI + uvicorn (port 8000)
- `ui`  : Streamlit (port 8501)
- `ollama` : modèle local (optionnel, gros volume disque ~5 Go)
- `langfuse` : self-hosted observability (optionnel)

## 4. Pourquoi Ollama plutôt que Jan.ai ?

| Critère                 | Ollama                          | Jan.ai                    |
|-------------------------|---------------------------------|---------------------------|
| API HTTP REST           | ✓ native (`/api/generate`)      | ✓ (compat OpenAI)         |
| Intégration LangChain   | ✓ `ChatOllama` officiel         | partielle (via OpenAI API) |
| Mode GUI desktop        | ✗ (CLI seulement)               | ✓ (Electron)              |
| Headless server         | ✓ optimal pour VPS              | ✗ pensé desktop           |
| Modelfile (custom prompts) | ✓ format propre              | ✗ moins flexible          |
| Communauté + plugins    | très active                     | grandit                   |

→ **Ollama gagne pour la prod headless**. Jan.ai reste utile pour tester
en local sur un poste développeur sans terminal.

## 5. Pièges Streamlit fréquents

- **`@st.cache_resource`** sur la fonction qui charge le vectorstore /
  l'agent → sinon ils sont rechargés à CHAQUE refresh = lent + coûteux.
- **`pip install -e .`** absolument requis : Streamlit ne trouve pas
  `homebutler` sinon (import absolu nécessaire, pas relatif).
- **`API_URL`** dans `.env` doit pointer vers l'API publique en prod
  (ex : `https://api.homebutler.example.com`).

## 6. Monitoring en prod (Langfuse / LangSmith)

- Traces par requête (latence, tokens, coût)
- Erreurs LLM (rate limit, timeouts, hallucinations détectées)
- Sessions utilisateur (multi-tours conversationnels)
- Dashboard : qualité retriever (Recall@5 moyen sur 7j)
