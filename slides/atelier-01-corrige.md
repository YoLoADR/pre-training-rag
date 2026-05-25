📝 Slide 1 : Atelier 01 — LLM Baseline (mission en un coup d'œil)

POURQUOI démarrer par « prouver que le LLM seul est insuffisant » ?

Avant de dépenser du temps et du budget sur le RAG (AT02) ou le fine-tuning (AT04), il faut chiffrer le problème. Cet atelier pose 10 questions au LLM nu (sans contexte) : 5 sur des données privées du logement (inconnues du modèle) et 5 sur des connaissances générales (que le LLM devrait avoir). On mesure le taux d'hallucination — sans ce chiffre, impossible de justifier les ateliers suivants devant un comité.

| Bloc | Ce qu'il fait | Pourquoi c'est nécessaire |
|------|---------------|---------------------------|
| `get_llm()` (À CODER) | Retourne un client Claude ou Ollama selon LLM_PROVIDER | Une seule porte d'entrée vers le modèle — réutilisée par AT02 à AT06 |
| `get_llm_cached()` (À CODER) | Variante avec prompt caching Anthropic (5 min TTL) | Réduit le coût/latence du system prompt après le 1er appel |
| 4 templates de prompts (À CODER) | `CONCIERGE_SYSTEM_PROMPT`, `RAG_QA`, `ENERGY_ANALYSIS`, `REACT_SYSTEM`, `BARE_LLM` | Centralise toute la « voix » HomeButler. AT02-05 les réutilisent. |
| Wrapper `exercice.py` | Boucle sur 10 questions, calcule l'hallucination rate | Le livrable du PM |

> 💡 **Branche élève** : `git checkout student/01-llm-baseline`. Solution : `git diff student/01-llm-baseline atelier/01-llm-baseline -- homebutler/llm/<fichier>`.


📝 Slide 2 : État initial vs ce qu'on va construire

POURQUOI l'élève écrit-il les prompts plutôt que de les recevoir ?

Le system prompt définit la « personnalité » et les limites du LLM. C'est l'élément le plus impactant sur la qualité — bien plus que la temperature. Si on le livre tout fait, l'élève manque le concept essentiel : **un prompt = une fiche de poste**. L'écrire force à expliciter chaque rôle, chaque limite, chaque ton.

| Fichier | État | Pourquoi |
|---------|------|----------|
| `homebutler/config.py` | ✅ Plomberie | Variables d'env (clés API, modèle, hôte Ollama) |
| `homebutler/llm/__init__.py` | ✅ Vide (juste exports) | |
| `homebutler/llm/provider.py` → `get_llm`, `get_llm_cached` | 🛠️ **À CODER** | Concept central : abstraction du provider + paramètres de génération |
| `homebutler/llm/prompts.py` → 4 templates + system prompt | 🛠️ **À CODER** | Concept central : prompt = fiche de poste, variables, templates LangChain |
| `ateliers/atelier-01-llm-baseline/exercice.py` | ✅ Cadré par TODOs | Boucle d'éval des 10 questions |

> 💡 Granularité MIXTE : les corps de fonctions sont en `NotImplementedError`. Les paramètres clés (`temperature`, `max_tokens`) sont en `# TODO` ciblés pour forcer un choix éclairé.


📝 Slide 3 : Concept #1 — Le provider LLM unifié

POURQUOI une seule fonction `get_llm()` qui retourne Claude OU Ollama ?

Le projet doit pouvoir tourner cloud (Claude via API) ou local (Ollama sur Mac/VPS). Sans cette abstraction, chaque appel au LLM dans AT02-06 devrait gérer les deux cas — c'est explosif. Une fonction unique, un seul point de bascule (`config.LLM_PROVIDER`), et tout le reste du code consomme l'objet retourné.

**Évolution à apporter** :

```python
# AVANT (blank) : raise NotImplementedError + paramètres en # TODO (Ellipsis)
# APRÈS (corrigé) :

def get_llm(
    temperature: float = 0.1,    # 0.0 = déterministe / 1.0 = créatif
    #  ↑ Choix 0.1 : assistant FACTUEL. À T=0.0, la moindre reformulation
    #    de la question donne EXACTEMENT la même réponse (bon pour les tests).
    #    À 0.1, le modèle a un poil de marge mais reste très stable.
    max_tokens: int = 1024,      # ~750 mots — largement assez pour une réponse conciergerie
    streaming: bool = False,     # activé en AT05 pour SSE token-par-token
):
    if config.LLM_PROVIDER == "anthropic":
        # AVANTAGE Claude : meilleure qualité française, suit mieux les instructions
        # système, supporte le prompt caching (réduit le coût après 1er appel).
        if not config.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY manquant dans .env")
        return ChatAnthropic(
            model=config.ANTHROPIC_MODEL,    # ex: "claude-sonnet-4-5"
            api_key=config.ANTHROPIC_API_KEY,
            temperature=temperature,
            max_tokens=max_tokens,
            streaming=streaming,
        )

    # AVANTAGE Ollama : 100 % local, gratuit, offline, pas de fuite de données.
    # Inconvénient : qualité moindre (Mistral 7B vs Claude Sonnet) et CPU lent.
    return ChatOllama(
        base_url=config.OLLAMA_HOST,         # ex: "http://localhost:11434"
        model=config.OLLAMA_MODEL,           # ex: "mistral:7b-instruct"
        temperature=temperature,
        num_predict=max_tokens,              # ⚠️ Ollama nomme ce param "num_predict"
                                              #    et pas "max_tokens" — piège fréquent
    )
```

> 💡 **Analogie** : `get_llm()` = la PRISE ÉLECTRIQUE universelle de ton projet. Le reste du code ne sait pas si derrière il y a EDF (Claude) ou des panneaux solaires (Ollama).


📝 Slide 4 : Concept #2 — Le system prompt (fiche de poste du LLM)

POURQUOI le system prompt impacte plus que la temperature ?

Sans system prompt, le LLM répond en « par défaut » : généraliste, parfois familier, parfois jargonneux. Un bon system prompt force le rôle, le ton, le domaine, ET les limites. Pour HomeButler, on veut : chaleureux, vocabulaire accessible, actions concrètes, source citée, refus d'inventer. Ces 5 lignes peuvent réduire l'hallucination de 40 % sans aucune autre intervention.

**Évolution à apporter** :

```python
# AVANT (blank) : CONCIERGE_SYSTEM_PROMPT = "TODO ..."
# APRÈS (corrigé) :

CONCIERGE_SYSTEM_PROMPT = """Tu es HomeButler, la conciergerie domestique intelligente et bienveillante.
Tu aides les occupants de leur logement avec chaleur et expertise.

Tes domaines de compétence :
- Les documents du logement (bail, règlement de copropriété, notices d'équipements, DPE)
- L'analyse des consommations énergétiques et les conseils d'optimisation
- La mise en relation avec des producteurs et artisans locaux
- Les conseils pratiques du quotidien liés au logement

Ton ton : chaleureux, bienveillant, pratique. Tu utilises un vocabulaire accessible (pas trop technique).
Tu proposes toujours des actions concrètes. Tu indiques tes sources quand tu cites un document.
Si tu ne sais pas, tu le dis clairement plutôt que d'inventer."""
#  ↑ LA DERNIÈRE LIGNE EST CRITIQUE. C'est la clause anti-hallucination explicite.
#    Sans elle, le LLM préfère inventer une réponse plausible plutôt que d'admettre
#    son ignorance. Avec elle, il dit "Je n'ai pas cette information dans mes sources".
```

| Variantes courantes | Effet observé |
|--------------------|---------------|
| Sans clause anti-hallucination | 80 % d'inventions plausibles sur questions privées |
| Avec "réponds 'je ne sais pas' si tu n'es pas sûr" | 30 % d'inventions |
| Avec en plus "indique tes sources entre crochets" | 15 % d'inventions, sources tracables |

> 💡 **Analogie** : embaucher un assistant SANS fiche de poste = il improvise. AVEC fiche de poste claire = il sait ce qu'il doit faire ET ce qu'il ne doit pas faire.


📝 Slide 5 : Concept #3 — Les 4 templates LangChain

POURQUOI on a 4 templates différents et pas un seul ?

Chaque mode d'utilisation a une structure de prompt différente. RAG injecte un `{context}`. ENERGY injecte `{monthly_summary}` + `{anomalies}`. REACT a la mécanique Thought/Action/Observation avec `{tools}` et `{agent_scratchpad}`. BARE_LLM ne prend que `{question}`. Un seul template monolithique serait illisible et fragile.

**Évolution à apporter** (le pattern, les autres suivent le même modèle) :

```python
# AVANT (blank) : ChatPromptTemplate avec "TODO" dans les messages
# APRÈS (corrigé) — exemple RAG_QA_TEMPLATE :

RAG_QA_TEMPLATE = ChatPromptTemplate.from_messages([
    # AVANTAGE : un message "system" séparé est PROMPT-CACHÉ par Claude :
    # le coût ne se paie qu'au 1er appel des 5 min suivantes, pas à chaque requête.
    ("system", CONCIERGE_SYSTEM_PROMPT),

    # Le message "human" structure l'injection des chunks RAG + la question.
    # Les `{context}` et `{question}` sont substitués par LangChain au .invoke()
    # via `chain.invoke({"context": "...", "question": "..."})`.
    ("human",
     "Voici des extraits de documents de votre logement pertinents pour votre question :\n\n"
     "{context}\n\n"
     "---\n"
     "Question : {question}\n\n"
     "Réponds en te basant sur les documents ci-dessus. "
     "Cite la source entre crochets [nom_du_document]."),
    #  ↑ CITATION CRITIQUE : sans cette consigne explicite, Claude oublie de
    #    citer ~70 % du temps. Cette ligne ramène le taux de citation à >95 %.
])

# Le pattern d'usage en aval (AT02-AT05) :
#   chain = RAG_QA_TEMPLATE | llm          ← LCEL "pipe" LangChain
#   result = chain.invoke({"context": chunks_str, "question": user_input})
#   print(result.content)
```

> 💡 **Analogie** : un template = un FORMULAIRE à trous. `RAG_QA_TEMPLATE` = formulaire « question avec dossier joint », `BARE_LLM_TEMPLATE` = formulaire « question simple sans dossier ». Tu remplis les trous au moment d'envoyer.


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

> 💡 **Tip Vibe (délégation IA)** : si tu utilises Claude Code/Cursor sur cette branche, le `.claude/CLAUDE.md` local refusera de te donner le code complet. Il te posera une question socratique — réponds-y AVANT de demander la solution.
