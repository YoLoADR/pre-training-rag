📝 Slide 1 : Atelier 01 — LLM Baseline (mission en un coup d'œil)

POURQUOI démarrer par « prouver que le LLM seul est insuffisant » ?

Avant de dépenser du temps et du budget sur le RAG (AT02) ou le fine-tuning (AT04), il faut chiffrer le problème. Cet atelier pose 10 questions au LLM nu (sans contexte) : 5 sur des données privées du logement (inconnues du modèle) et 5 sur des connaissances générales (que le LLM devrait avoir). On mesure le taux d'hallucination — sans ce chiffre, impossible de justifier les ateliers suivants.

| Bloc | Ce qu'il fait | Pourquoi c'est nécessaire |
|------|---------------|---------------------------|
| `get_llm()` (À CODER) | Retourne un client Claude ou Ollama selon `LLM_PROVIDER` | Une seule porte d'entrée vers le modèle — réutilisée par AT02 à AT06 |
| `get_llm_cached()` (À CODER) | Variante avec prompt caching Anthropic (5 min TTL) | Réduit le coût/latence du system prompt après le 1er appel |
| 4 templates de prompts (À CODER) | `CONCIERGE_SYSTEM_PROMPT`, `RAG_QA`, `ENERGY_ANALYSIS`, `REACT_SYSTEM`, `BARE_LLM` | Centralise toute la « voix » HomeButler. AT02-05 les réutilisent. |
| Wrapper `exercice.py` | Boucle sur 10 questions, calcule l'hallucination rate | Le livrable du PM |

> 💡 **Branche élève** : `git checkout student/01-llm-baseline`. Si vraiment bloqué > 15 min : `git diff student/01-llm-baseline atelier/01-llm-baseline -- homebutler/llm/<fichier>`.


📝 Slide 2 : État initial vs ce qu'on va construire

POURQUOI tu écris les prompts plutôt que de les recevoir ?

Le system prompt définit la « personnalité » et les limites du LLM. C'est l'élément le plus impactant sur la qualité — bien plus que la temperature. Si on te le livre tout fait, tu manques le concept essentiel : **un prompt = une fiche de poste**. L'écrire force à expliciter chaque rôle, chaque limite, chaque ton.

| Fichier | État | Pourquoi |
|---------|------|----------|
| `homebutler/config.py` | ✅ Plomberie | Variables d'env (clés API, modèle, hôte Ollama) |
| `homebutler/llm/__init__.py` | ✅ Vide (juste exports) | |
| `homebutler/llm/provider.py` → `get_llm`, `get_llm_cached` | 🛠️ **À CODER** | Concept central : abstraction du provider + paramètres de génération |
| `homebutler/llm/prompts.py` → 4 templates + system prompt | 🛠️ **À CODER** | Concept central : prompt = fiche de poste, variables, templates LangChain |
| `ateliers/atelier-01-llm-baseline/exercice.py` | ✅ Cadré par TODOs | Boucle d'éval des 10 questions |

> 💡 Granularité MIXTE : les corps de fonctions lèvent `NotImplementedError`. Les paramètres clés (`temperature`, `max_tokens`) sont en `# TODO` ciblés avec `Ellipsis` pour forcer un choix éclairé.


📝 Slide 3 : Concept #1 — Le provider LLM unifié

POURQUOI une seule fonction `get_llm()` qui retourne Claude OU Ollama ?

Le projet doit pouvoir tourner cloud (Claude via API) ou local (Ollama sur Mac/VPS). Sans cette abstraction, chaque appel au LLM dans AT02-06 devrait gérer les deux cas — c'est explosif. Une fonction unique, un seul point de bascule (`config.LLM_PROVIDER`), et tout le reste du code consomme l'objet retourné.

**Signature à compléter** :

```python
def get_llm(
    temperature: float = ...,   # TODO (indice : 0.0 = déterministe / 1.0 = créatif)
    max_tokens: int = ...,      # TODO (indice : ~750 mots ≈ ? tokens)
    streaming: bool = False,
):
    """Retourne un LLM Claude (Anthropic) ou Mistral (Ollama) selon config.LLM_PROVIDER."""
    raise NotImplementedError(
        "Atelier 01 § Provider — implémente la sélection Anthropic/Ollama"
    )
```

**Indice léger** — `config.LLM_PROVIDER` vaut `"anthropic"` ou `"ollama"`. LangChain fournit deux classes `Chat...` qui exposent une API identique. Tu testes la valeur, tu instancies la bonne, tu retournes l'objet.

**Indice fort** — Pour Anthropic : `ChatAnthropic(model=config.ANTHROPIC_MODEL, api_key=config.ANTHROPIC_API_KEY, temperature=..., max_tokens=..., streaming=...)`. Pour Ollama : `ChatOllama(base_url=config.OLLAMA_HOST, model=config.OLLAMA_MODEL, temperature=..., num_predict=..., ...)`. ⚠️ Le paramètre s'appelle **`num_predict`** chez Ollama, pas `max_tokens` — c'est un piège fréquent.

> 💡 **Analogie** : `get_llm()` = la PRISE ÉLECTRIQUE universelle de ton projet. Le reste du code ne sait pas si derrière il y a EDF (Claude) ou des panneaux solaires (Ollama).

⚠️ **Piège** — si tu oublies de tester `config.ANTHROPIC_API_KEY` avant d'instancier ChatAnthropic, le crash arrive 2 secondes plus tard avec un message obscur. Un `if not key: raise ValueError(...)` explicite te fait gagner du debug.


📝 Slide 4 : Concept #2 — Le system prompt (fiche de poste du LLM)

POURQUOI le system prompt impacte plus que la temperature ?

Sans system prompt, le LLM répond en « par défaut » : généraliste, parfois familier, parfois jargonneux. Un bon system prompt force le rôle, le ton, le domaine, ET les limites. Pour HomeButler : chaleureux, vocabulaire accessible, actions concrètes, source citée, refus d'inventer. Ces 5 lignes peuvent réduire l'hallucination de 40 % sans aucune autre intervention.

**À écrire** :

```python
CONCIERGE_SYSTEM_PROMPT = """TODO — rédige une fiche de poste pour HomeButler.
Indices ci-dessous.
"""
```

**Indice léger** — Pense à 5 sections : (1) qui est l'assistant, (2) ses domaines, (3) son ton, (4) ce qu'il fait toujours, (5) ce qu'il ne fait jamais.

**Indice fort** — La dernière clause est la plus importante : « Si tu ne sais pas, dis-le clairement plutôt que d'inventer. » Sans elle, le LLM préfère inventer une réponse plausible plutôt que d'admettre son ignorance. Ajoute aussi « Cite tes sources entre crochets [nom_du_document] » pour rendre les réponses traçables.

| Variantes courantes | Effet observé |
|--------------------|---------------|
| Sans clause anti-hallucination | 80 % d'inventions plausibles sur questions privées |
| Avec « réponds 'je ne sais pas' si tu n'es pas sûr » | 30 % d'inventions |
| Avec en plus « indique tes sources entre crochets » | 15 % d'inventions, sources traçables |

> 💡 **Analogie** : embaucher un assistant SANS fiche de poste = il improvise. AVEC fiche de poste claire = il sait ce qu'il doit faire ET ce qu'il ne doit pas faire.


📝 Slide 5 : Concept #3 — Les 4 templates LangChain

POURQUOI on a 4 templates différents et pas un seul ?

Chaque mode d'utilisation a une structure de prompt différente. RAG injecte un `{context}`. ENERGY injecte `{monthly_summary}` + `{anomalies}`. REACT a la mécanique Thought/Action/Observation avec `{tools}` et `{agent_scratchpad}`. BARE_LLM ne prend que `{question}`. Un seul template monolithique serait illisible et fragile.

**Signature à compléter** (exemple `RAG_QA_TEMPLATE`) :

```python
RAG_QA_TEMPLATE = ChatPromptTemplate.from_messages([
    # TODO 1 — message "system" : qui injecte CONCIERGE_SYSTEM_PROMPT
    # TODO 2 — message "human" : qui place {context} et {question} aux bons endroits
    #          + consigne de citer la source entre crochets
])
```

**Indice léger** — `ChatPromptTemplate.from_messages([...])` prend une liste de tuples `(role, contenu)`. Les rôles valides : `"system"`, `"human"`, `"ai"`. Les variables substituées au runtime sont entourées d'accolades simples `{nom_variable}`.

**Indice fort** — Pour le human message, structure typique : *« Voici des extraits pertinents :\n\n{context}\n\n---\nQuestion : {question}\n\nRéponds en te basant sur les documents. Cite la source entre crochets [nom_du_document]. »* — La citation explicite ramène le taux de citation effective de ~30 % à >95 %.

**Pattern d'usage** (déjà géré dans `exercice.py`) :
```python
chain = RAG_QA_TEMPLATE | llm                                # LCEL "pipe"
result = chain.invoke({"context": chunks_str, "question": user_input})
```

> 💡 **Analogie** : un template = un FORMULAIRE à trous. `RAG_QA_TEMPLATE` = formulaire « question avec dossier joint », `BARE_LLM_TEMPLATE` = formulaire « question simple ». Tu remplis les trous au moment d'envoyer.


📝 Slide 6 : Récap — démarrer sur la branche `student/01-llm-baseline`

POURQUOI cet ordre de travail ?

L'ordre est imposé par les dépendances : `get_llm()` doit exister AVANT que tu puisses tester un template. Le system prompt doit être écrit AVANT les 4 templates (ils l'importent). Suis la recette QUICK-START dans cet ordre.

```bash
# 1. Cloner et basculer
git clone <repo> && cd training-rag
git checkout student/01-llm-baseline
python -m venv .venv && source .venv/bin/activate
pip install -e .

# 2. Configurer le provider
cp .env.example .env
# choix A — Claude :  LLM_PROVIDER=anthropic + ANTHROPIC_API_KEY=sk-ant-...
# choix B — Ollama :  LLM_PROVIDER=ollama   + ollama pull mistral:7b-instruct

# 3. Lire la recette
cat ateliers/atelier-01-llm-baseline/QUICK-START.md

# 4. Coder dans l'ordre
#    a) homebutler/llm/provider.py  → get_llm  + paramètres temperature/max_tokens
#    b) homebutler/llm/prompts.py   → CONCIERGE_SYSTEM_PROMPT (le plus important)
#    c) puis les 4 templates qui s'appuient dessus
#    d) homebutler/llm/provider.py  → get_llm_cached (optionnel, pour AT05)

# 5. Tester
python ateliers/atelier-01-llm-baseline/exercice.py
# 🎯 cible : hallucination rate ≥ 80 % sur les 5 questions privées
#            (preuve qu'on a besoin du RAG en AT02)

# 6. Checkpoint
python ateliers/atelier-01-llm-baseline/checkpoints/check_1.py
#    → QCM 3 questions + verbalisation pourquoi T=0.1 vs T=0.8

# 7. Bloqué > 15 min : en dernier recours
git diff student/01-llm-baseline atelier/01-llm-baseline -- homebutler/llm/provider.py
```

> 💡 **Tip Vibe (délégation IA)** : si tu utilises Claude Code / Cursor sur cette branche, le `.claude/CLAUDE.md` local refusera de te donner le code complet. Il te posera une question socratique — réponds-y AVANT de demander la solution.
