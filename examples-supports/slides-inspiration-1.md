Leçon 1.2 : Claude Code Setup — MCP & Agents — Théorie

🎯 Objectif de la leçon

Comprendre **pourquoi** MCP existe, **où vivent les configs** Claude Code (5 emplacements), **quels MCPs brancher** en 2026 (top 6) et **comment ne pas exposer un secret ni une faille** au passage. À la fin, vous saurez ajouter un MCP en 30 secondes (CLI ou JSON), arbitrer entre config globale et config projet, et lire `/mcp` + `/context` pour surveiller le coût.



📝 Slide 1 : MCP — l'USB-C des agents IA

POURQUOI un protocole et pas une extension par éditeur ?

Avant 2024, chaque éditeur IA avait son propre format de plugin : extensions Cursor, ChatGPT plugins, Copilot extensions. Conséquence : **le même outil** (un connecteur GitHub, par exemple) devait être codé plusieurs fois pour fonctionner partout.

MCP (Model Context Protocol) standardise tout ça. **Un serveur écrit une fois fonctionne partout** : Claude Code, Cursor, Continue, ChatGPT desktop, Gemini-CLI, GitHub Copilot.

Avant MCP Avec MCP (2025+)
Une extension par éditeur Un serveur, tous les clients
Format propriétaire (Cursor, Copilot…) Standard ouvert (JSON-RPC)
Chaque éditeur réinvente la connectique Tu codes 1× pour tous les clients

État de l'écosystème (mai 2026)

- **9 400+ MCP servers** dans le registry public (vs 1 200 il y a 18 mois)
- Standard passé sous **Linux Foundation** → consortium multi-vendor (OpenAI, Google, Microsoft, Amazon, Anthropic)
- **78 % des équipes IA d'entreprise** ont au moins un MCP en prod

> 💡 **Linux Foundation** = consortium open-source neutre (Linux, Kubernetes, Node.js…). Ça veut dire que MCP n'est plus piloté par Anthropic seul → garantie de pérennité pour vos choix techniques.

L'analogie cuisine

Claude Code de base = un cuisinier avec **17 ustensiles** (Read, Edit, Bash, Task, etc. — vu en 1.1). Vous lui livrez une **mallette MCP GitHub** → il a 15 nouveaux outils (`list_issues`, `create_pr`…). Une **mallette Sentry** → 8 outils de debug prod. Pour Claude, ces tools sont indistinguables des tools natifs : il décide quand les appeler.



📝 Slide 2 : 17 tools natifs + MCP = boîte à outils extensible

POURQUOI distinguer les deux ?

Parce que les **17 tools natifs** sont **non-modifiables** (ils sont câblés dans Claude Code). MCP est le **seul mécanisme officiel** pour ajouter de nouveaux tools — votre DB, votre API interne, un service externe.

Tools natifs (1.1) Tools MCP (1.2)
17 outils fixes : `Read`, `Edit`, `Bash`, `Task`, `Glob`, `Grep`, `WebFetch`… Tous les outils ajoutés via MCP servers
Câblés dans Claude Code Branchés via `~/.claude.json` ou `.mcp.json`
Pas de personnalisation Vous décidez ce que vous branchez
Pas de secrets, pas d'IO réseau Souvent : tokens, IO réseau, état distant

Préfixe visible dans le terminal

Quand Claude appelle un tool MCP, vous voyez dans le journal :

```
mcp__context7__resolve-library-id
mcp__github__list_issues
mcp__playwright__navigate
```

Le préfixe `mcp__<server>__` vous dit **quel serveur** est appelé. Utile pour le debug : un tool inattendu = vous savez tout de suite quel MCP l'a injecté.

Vous consommez, vous ne codez (presque) pas

Dans 95 % des cas, vous **branchez un MCP existant** (Context7, GitHub, Linear, Sentry, Postgres, Playwright…). Coder son propre MCP server n'est utile que pour exposer une API maison spécifique — ~50 lignes en Python/TS, sujet d'un module avancé. **Cette leçon = consommateur, pas producteur.**



📝 Slide 3 : stdio vs http — 2 transports, 1 protocole

POURQUOI deux types de transport ?

Parce que les besoins sont différents :
- **stdio** (process local lancé par Claude Code) → outil sans réseau, secrets en local
- **http** (URL distante) → service hébergé, mises à jour gérées par le provider

Comparatif

Critère stdio http
Localisation Process **local** lancé par Claude Distant (URL)
Communication stdin/stdout (JSON-RPC) Requêtes HTTP
Install Node, Python, Docker… selon serveur Aucune (juste l'URL)
Latence Très faible (process local) Dépend du provider
Secrets Restent sur votre machine Token envoyé en `Authorization: Bearer …`
Mise à jour À votre charge Gérée par le provider
Exemple `npx @playwright/mcp@latest` `https://mcp.context7.com/mcp`

Anatomie d'une config stdio

```json
"shadcn-components": {
  "type": "stdio",
  "command": "npx",
  "args": ["@jpisnice/shadcn-ui-mcp-server"],
  "env": {
    "API_KEY": "${API_KEY_FROM_SHELL}"
  }
}
```

Anatomie d'une config http

```json
"context7": {
  "type": "http",
  "url": "https://mcp.context7.com/mcp"
}
```

Avec auth bearer (Linear, Sentry…) :

```json
"linear": {
  "type": "http",
  "url": "https://mcp.linear.app/sse",
  "headers": {
    "Authorization": "Bearer ${LINEAR_API_KEY}"
  }
}
```

⚠️ Piège — ne pas mélanger

Si vous mettez `"type": "stdio"` mais que vous donnez une `url` (ou inversement), Claude ne se connectera pas. **Règle** : stdio → `command + args` ; http → `url`. Pas d'hybride.



📝 Slide 4 : Cartographie des 5 emplacements de config

POURQUOI 5 fichiers et pas un seul ?

Parce que Claude Code distingue **3 dimensions** :
- **Portée** (global vs projet)
- **Versionnage** (partagé en équipe vs perso)
- **Type** (MCP servers vs hooks vs commands vs agents)

La table à mémoriser

Fichier Portée Versionné ? Contenu typique
**`~/.claude.json`** Globale (toutes vos sessions) ❌ perso machine MCP servers persistants, préférences user
**`.mcp.json`** (racine projet) Projet ✅ commité MCP servers spécifiques au projet, partagés équipe
**`.claude/settings.json`** Projet ✅ commité Permissions, hooks **partagés équipe**
**`.claude/settings.local.json`** Projet ❌ gitignored Permissions, hooks **personnels**, secrets éventuels
**`.claude/{commands,hooks,agents,tasks}/`** Projet ✅ commité Slash commands, scripts hooks, sub-agents, plans

Règle d'or pour décider où poser quoi

> *Versionne tout ce qui aide quelqu'un d'autre à bosser sur le projet. Garde local tout ce qui ne concerne que toi.*

En pratique :

Vous voulez… Allez dans…
Un MCP utile à toute l'équipe sur ce projet `.mcp.json` (commité)
Un MCP que vous utilisez partout (Context7, GitHub) `~/.claude.json` (global, perso)
Un hook `tsc --noEmit` que tout le monde doit avoir `.claude/settings.json` (commité)
Un hook `afplay` macOS-only (son perso) `.claude/settings.local.json` (perso)
Une commande `/recap` utile à toute l'équipe `.claude/commands/recap.md` (commité)

Raccourci pratique

```bash
code .claude       # ouvre le dossier projet (commands, hooks, settings…)
code ~/.claude.json # ouvre la config globale
```

⚠️ Piège — `code` pas dans le PATH

Si la commande `code` n'est pas reconnue (typique macOS si VS Code/Cursor n'a pas été configuré), ouvrez VS Code → `Cmd+Shift+P` → *"Shell Command: Install 'code' command in PATH"*. Sinon, `nano` ou `vim` font le job.



📝 Slide 5 : Ajouter un MCP — 2 syntaxes équivalentes

POURQUOI deux syntaxes ?

Les deux modifient le **même fichier** (`~/.claude.json`). Le choix dépend du goût :
- **CLI** : plus rapide pour ajouter / retirer
- **JSON** : plus de contrôle (env vars, multi-servers, copier-coller un template)

Méthode CLI

```bash
# Ajouter un MCP HTTP en 1 ligne
claude mcp add --transport http context7 https://mcp.context7.com/mcp

# Lister les MCPs configurés (depuis le shell, sans lancer claude)
claude mcp list

# Retirer un MCP
claude mcp remove context7
```

Méthode JSON

```bash
code ~/.claude.json
```

Dans le bloc `"mcpServers"` :

```json
"mcpServers": {
  "context7": {
    "type": "http",
    "url": "https://mcp.context7.com/mcp"
  },
  "shadcn-components": {
    "type": "stdio",
    "command": "npx",
    "args": ["@jpisnice/shadcn-ui-mcp-server"]
  }
}
```

Vérifier depuis Claude Code

```
/mcp        # liste des servers + statut connected/error/loading
/context    # tokens consommés (System tools, MCP tools, Memory files)
```

⚠️ Piège — il faut redémarrer

Après modification de `~/.claude.json`, **redémarrez** Claude Code (ou `/mcp` qui reload). Sinon vos modifs ne prennent pas effet.



📝 Slide 6 : Top 6 MCPs incontournables 2026

POURQUOI ce top 6 et pas un autre ?

Parce qu'ils couvrent les 5 douleurs récurrentes du dev en 2026 : **doc obsolète**, **collab GitHub**, **ticketing**, **tests E2E**, **debug prod**. Le 6ᵉ (shadcn) est niche mais critique si votre stack le concerne.

Le ranking — utilité dev généraliste

# MCP Type Douleur résolue Priorité
1 **Context7** http Doc à jour des libs (3000+ supportées) ⭐⭐⭐ Universel
2 **GitHub** stdio (Docker) Issues, PRs, code search ⭐⭐⭐ Universel
3 **Linear** http Tickets → contexte → code → ticket en review ⭐⭐ Si Linear
4 **Playwright** stdio (npx) Tests E2E + scraping (accessibility tree) ⭐⭐ Universel
5 **Sentry** http Stack trace prod → fix proposé ⭐⭐ Si Sentry
6 **shadcn-ui** stdio (npx) Composants UI React shadcn ⭐ Niche

Pourquoi Context7 est priorité 1

Un LLM avec un cutoff de fin 2024 ne connaît pas Vercel AI SDK v5, Next.js 16, Tanstack Query v6. Sans Context7, Claude génère du code **obsolète** qui plante. Avec Context7, Claude appelle `get-library-docs("ai")` au moment où il en a besoin et reçoit la doc **2026**.

Cas d'usage type — combiner GitHub + Sentry

Vous tapez : *"il y a une erreur en prod sur ce composant — debug-la"*

→ Claude appelle `mcp__sentry__get_issue(id)` (stack trace réel)
→ Claude appelle `mcp__github__get_file_contents` (lit le fichier fautif)
→ Claude propose le fix dans une PR via `mcp__github__create_pr`

**Boucle complète**, sans copier-coller manuel depuis le dashboard.

Coût en tokens — surveiller

5 MCPs branchés = **15-25k tokens** consommés à chaque tour rien que pour exposer leurs tools dans le contexte. À surveiller avec `/context`.

Type de MCP Tokens estimés / tour
Petit MCP (5 tools) ~500-1500
MCP moyen (15 tools) ~2500-5000
Gros MCP (50+ tools — GitHub exhaustif) ~7000-10000



📝 Slide 7 : Sécurité MCP en 2026 — 5 règles non négociables

POURQUOI insister sur la sécu ?

Parce qu'avril 2026 a vu **la première faille majeure** du SDK MCP officiel — ~200 000 serveurs publics affectés. Anthropic a refusé de modifier le protocole, jugeant que **le client doit sanitizer**. Conséquence : c'est à vous, pas au protocole, d'éviter le piège.

Règle 1 — Sources vérifiées seulement

Source Risque
Registry MCP officiel ✅ OK
Repos GitHub officiels (Anthropic, GitHub, Linear…) ✅ OK
"Y'a un super MCP recommandé sur Reddit/Twitter" ❌ NON
Fork random d'un MCP connu ⚠️ Audit avant install

Règle 2 — `${ENV_VAR}` toujours, jamais hardcodé

```json
// ❌ MAUVAIS — token en clair, fuite garantie si dotfiles pushed
"github": { "env": { "GITHUB_TOKEN": "ghp_AaBbCc..." } }

// ✅ BON — résolu depuis l'environnement shell
"github": { "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" } }
```

Et dans `~/.zshrc` :
```bash
export GITHUB_TOKEN="ghp_..."
```

Règle 3 — Scoped tokens (principe du moindre privilège)

Pour GitHub MCP usage "lire issues + ouvrir PR" :

Scope Activer ?
`repo:read` ✅ Oui
`issues:write` ✅ Oui
`pull_requests:write` ✅ Oui
`delete_repo` ❌ Non
`admin:org` ❌ Non

Si le token fuit, le dégât est **borné** aux scopes accordés.

Règle 4 — Préférer HTTP officiel à stdio communautaire

Quand un MCP existe en **HTTP officiel** (provider hébergé) ET en **stdio communautaire** (rebuild forké), prenez l'officiel. Le stdio communautaire embarque potentiellement la faille de design 2026.

Règle 5 — Désactiver ce qui ne sert pas

15 MCPs branchés "au cas où" = ~30-50k tokens de loyer par tour + surface d'attaque démultipliée. Surveillez `/context`. **Bonne pratique** :
- MCPs universels → `~/.claude.json` (global)
- MCPs spécifiques au projet → `.mcp.json` (uniquement actifs sur ce projet)

⚠️ `~/.claude.json` ≠ fichier neutre

Tentation : pousser `~/.claude.json` dans un repo dotfiles pour synchro entre machines. **Si vous le faites sans précautions** :
- Si vous avez `claude mcp add` avec un token en clair, il est dans le JSON
- `git push` → token sur GitHub → bot scanne → token compromis en < 60 secondes (cas réel documenté)

**Solution** : `${ENV_VAR}` (règle 2) + vérifier `git check-ignore -v ~/.claude.json` avant tout push de dotfiles.



📝 Slide 8 : `/mcp` et `/context` — vérifier et surveiller

POURQUOI ces deux commandes ?

Parce que sans elles, vous branchez des MCPs **à l'aveugle** : vous ne savez pas s'ils sont connectés, ni combien ils vous coûtent à chaque tour. Ce sont vos deux outils de diagnostic permanent.

`/mcp` — l'état de connexion

Tapez `/mcp` dans la session :

```
MCP Servers:
✅ context7      connected   (4 tools)
✅ github        connected   (15 tools)
❌ linear        error       (auth failed - check LINEAR_API_KEY)
🔄 playwright    loading
```

Lecture rapide :

Statut Action
✅ connected RAS
🔄 loading Patientez 2-3 s
❌ error Vérifier env vars, redémarrer, regarder les logs

`/context` — le coût en tokens

```
Context Usage
38k/1m tokens (3.8%)

⛁ System prompt:   8.8k tokens (0.9%)
⛁ System tools:   12.9k tokens (1.3%)
⛁ MCP tools:      11.4k tokens (1.1%)
  └ context7:    1.2k tokens (4 tools)
  └ github:      4.8k tokens (15 tools)
  └ playwright:  3.2k tokens (12 tools)
  └ sentry:      2.2k tokens (8 tools)
⛁ Memory files:    386 tokens
```

Drapeaux rouges à reconnaître

Ce que vous voyez Diagnostic
**MCP tools > 30k** Trop de MCPs ou MCPs trop verbeux — désactiver
**Un MCP seul > 10k** Outil avec 50+ tools (GitHub exhaustif) — voir s'il existe en version slim
**Total > 100k en début de session** Gonflement structurel — auditer commands + memory files

Bonne pratique de session

`/context` au **début** ET au **milieu** d'une session. C'est la **seule façon native** de surveiller la dérive de votre coût en tokens. Si vous voyez un saut anormal entre les deux, vous avez identifié la fuite.



📝 Slide 9 : MCP servers vs sub-agents — la confusion à éviter

POURQUOI cette distinction ?

Parce que les deux **étendent** Claude Code, mais à des niveaux différents. Les confondre vous empêche de choisir le bon outil pour un problème donné.

Comparatif

MCP server Sub-agent (`Task`)
**Étend la liste des tools** Encapsule un raisonnement
Branché via config (`~/.claude.json`) Lancé à la volée par le main agent
Permanent (chargé à chaque session) Éphémère (vit le temps de la mission)
Statique (tools définis par le serveur) Dynamique (mission décrite en prompt)
**Exemple** : Context7 expose `get-library-docs` **Exemple** : "explore tel module et résume-moi"

Combinaison possible

Un sub-agent **peut utiliser** des tools MCP (Context7, GitHub, Sentry…). Le scénario typique :

```
Main agent
  └─ Task (sub-agent)
       ├─ mcp__context7__get-library-docs
       ├─ mcp__github__list_issues
       └─ retourne un résumé au parent
```

Le sub-agent absorbe les ~10-30k tokens des appels MCP **dans son propre contexte**, le main agent ne reçoit que le résumé. **Combo gagnant** : MCPs comme outils, sub-agents comme isolateurs de coût.

Quand utiliser quoi

Besoin Outil
Brancher une nouvelle source de données (DB, API, doc) MCP server
Isoler une exploration coûteuse Sub-agent (`Task`)
Encapsuler une expertise réutilisable (sub-agent custom dans `.claude/agents/`) Sub-agent
Donner accès à un service externe à toutes vos sessions MCP server (global)



🎓 Ce que vous devez retenir

Concept Pourquoi c'est important
MCP = USB-C des agents IA Un serveur écrit 1×, utilisable par tous les clients (Claude, Cursor, Copilot…)
17 tools natifs + MCP = boîte extensible MCP est le **seul** moyen officiel d'ajouter des tools
stdio vs http stdio = process local, http = URL distante. Pas de mélange
5 emplacements de config Versionner ce qui aide l'équipe, perso pour le reste
2 syntaxes d'ajout `claude mcp add …` (CLI) ou édition de `~/.claude.json` (JSON)
Top 6 MCPs Context7 / GitHub / Linear / Playwright / Sentry / shadcn-ui
Sécurité — 5 règles Sources vérifiées, `${ENV_VAR}`, scoped tokens, HTTP officiel, désactiver l'inutile
Faille STDIO 2026 ~200k servers exposés — n'installer que des MCPs vérifiés
`/mcp` + `/context` Vérifier la connexion et surveiller le coût en tokens
MCP vs sub-agent Ce sont **deux mécanismes d'extension différents** — souvent combinés



➡️ Prochaine leçon

Maintenant que vous savez brancher des MCPs en sécurité sur Mac/Linux, on traite le cas **Windows** (WSL2, paths, terminaux PowerShell vs WSL). Les MCPs et hooks ont des subtilités spécifiques sur Windows qu'il vaut mieux anticiper que découvrir en plein TP. C'est la **leçon 1.3**.
