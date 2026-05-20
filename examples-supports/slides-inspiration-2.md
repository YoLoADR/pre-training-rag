Leçon 1.4 : Sub-agents — Théorie

🎯 Objectif de la leçon

Comprendre **ce qu'est** un sub-agent dans Claude Code (un fichier markdown, rien de plus), **comment** il économise drastiquement du contexte, **comment le restreindre** pour qu'il ne casse rien, et **où placer la limite** entre Skills, Subagents et Agent Teams. À la fin, vous saurez créer un sub-agent en 4 lignes, en restreindre les capacités via 3 niveaux de défense, et arbitrer le bon mécanisme pour un besoin donné.



📝 Slide 1 : Sub-agent — un fichier markdown, rien de plus

POURQUOI démarrer par cette précision ?

Parce que le mot "agent" évoque souvent un framework lourd (CrewAI, AutoGen, n8n, Langchain agents) avec runtime, orchestrateur, rôles hard-codés. **Claude Code, c'est l'inverse** : un sub-agent = **un fichier `.md` avec un frontmatter YAML**. Pas de code, pas de runtime, pas de framework.

L'anatomie minimale (4 lignes utiles)

```markdown
---
name: my-agent
description: Use this agent when [trigger précis]
---

You are an expert in [domaine]. Your job is to [mission].
```

Vous posez ce fichier dans `.claude/agents/` (projet) ou `~/.claude/agents/` (perso). Claude Code le découvre. Le sub-agent est dispo.

Ce qui change par rapport au main agent

Main agent (la session) Sub-agent
Voit tout l'historique de conversation **Démarre avec un contexte VIERGE**
Tools du main Tools restreignables (allowlist / denylist)
Same model que la conversation Modèle choisi par agent (`haiku` / `sonnet` / `opus`)
Reçoit votre prompt direct Reçoit son `system prompt` + un brief
Renvoie texte + actions **Renvoie UN RÉSUMÉ au parent**

Pourquoi c'est puissant

Vous routez chaque type de tâche vers un agent **avec déjà l'expertise pré-chargée et seulement les permissions nécessaires** :

Prompt utilisateur Sub-agent invoqué
*"Add an `email_verified_at` column to users"* `db-migration-expert` (tools : Edit + Write + Bash, hook qui interdit DROP)
*"Build a settings page with shadcn"* `shadcn-ui-builder` (MCP shadcn préchargé)
*"Review my recent changes"* `code-reviewer` (read-only — Read + Grep + Bash uniquement)
*"Find all places where `getUserById` is used"* `Explore` (built-in, Haiku, read-only)



📝 Slide 2 : Sub-agent ≠ tool `Agent` — la confusion à dissiper

POURQUOI cette distinction ?

Parce que les deux mécanismes coexistent et se confondent :
- **Tool `Agent`** (anciennement `Task`, **renommé en v2.1.63**) = le **mécanisme de spawn**
- **Sub-agent** (`.claude/agents/*.md`) = un **agent défini par fichier** avec son system prompt

Le tool `Agent` peut soit invoquer un built-in, soit invoquer un de **vos** sub-agents nommés.

Comparatif

Tool `Agent` (mécanisme) Named subagent (`.claude/agents/foo.md`)
Spawn générique d'un agent enfant Définition d'un agent **nommé**, prompt sur-mesure
Toujours dispo (built-in dans Claude Code) Vit dans un fichier `.md` versionné
Sans config = built-ins (Explore, Plan, general-purpose) Avec config = comportement spécifique
"Tool de délégation" "Fiche de poste"

⚠️ Note historique

Le tool `Task` a été **renommé `Agent`** en v2.1.63. Les anciens scripts (`Task(...)`) continuent de marcher comme aliases, mais **toute formation 2025 mentionnant `Task` doit mentalement remplacer par `Agent`**.

Bonne phrase à mémoriser

> *"`Agent` est la **porte** ; les sub-agents nommés sont les **personnes** qui passent par cette porte."*



📝 Slide 3 : Les 16 champs frontmatter — la sélection à connaître

POURQUOI passer du temps sur le frontmatter ?

Parce que **toute la puissance** d'un sub-agent vit dans son frontmatter : tools, modèle, MCPs, skills, hooks, memory, isolation. C'est ce qui transforme un "prompt avec un nom" en agent **spécialisé et restreint**.

Les 2 obligatoires + 14 optionnels (selon doc officielle Anthropic mai 2026)

# Champ Obligatoire Rôle
1 `name` ✅ Identifiant lowercase + hyphens (ex: `code-reviewer`)
2 `description` ✅ Quand Claude doit déléguer — **le champ le plus important**
3 `tools` Allowlist (sécurité)
4 `disallowedTools` Denylist
5 `model` `sonnet` (défaut prod), `opus`, `haiku`, `inherit`
6 `permissionMode` `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan`
7 `mcpServers` MCP servers scopés à ce sub-agent
8 `skills` Skills à **précharger** (full content injecté au boot)
9 `hooks` Hooks lifecycle scopés au sub-agent
10 `memory` `user`, `project`, `local` — persistent memory entre sessions
11 `isolation` `worktree` — git worktree isolé
12 `background` `true` pour run en arrière-plan
13 `effort` `low`, `medium`, `high`, `xhigh`, `max`
14 `maxTurns` Garde-fou anti-boucle
15 `color` `red`, `blue`, `green`… (UI)
16 `initialPrompt` Premier user-turn auto si lancé via `claude --agent`

Pour les 95 % de cas, vous utilisez 5-7 champs : `name`, `description`, `tools`, `model`, `color`, parfois `permissionMode` ou `memory`.

System prompt = corps markdown

Tout ce qui suit le frontmatter est **le system prompt de l'agent**. Le sub-agent **ne reçoit pas** le system prompt Claude Code complet du main — seulement votre markdown. Vous repartez d'une feuille blanche, soyez explicite sur tout ce qu'il doit savoir.



📝 Slide 4 : `description` — le champ qui pousse à la délégation

POURQUOI insister sur ce champ ?

Parce que le main agent **ne délègue que s'il "sent" que le sub-agent matche**. Une mauvaise `description` = sub-agent jamais invoqué. Une bonne `description` = délégation automatique au bon moment.

Les 3 leviers d'une bonne description

Levier Ce que ça donne
**Trigger phrase** *"Use proactively when…"* / *"Use immediately after …"* — la doc Anthropic le recommande explicitement
**Mots-clés présents dans vos prompts** Si vous prompts *"add a migration"*, la description doit contenir le mot "migration"
**Stack explicite** *"shadcn/ui on Next.js 15"* > *"UI work"*

Comparatif — bon vs flou

❌ Description floue ✅ Description forte
*"Helps with code"* *"Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code."*
*"UI agent"* *"Use this agent for shadcn/ui component work on Next.js 15. Use proactively when adding pages or modifying components."*
*"Database stuff"* *"Use this agent when you need to write or review database migrations. Use proactively for any schema change."*

Diagnostiquer un mauvais matching

Symptôme Diagnostic
Vous prompts *"add a migration"* mais le main code lui-même Description trop générique ("schema change") ou trigger phrase manquante
Le sub-agent est invoqué pour des tâches sans rapport Description trop large — restreindre le scope
Plusieurs sub-agents matchent le même prompt Conflits de scope — préciser les domaines



📝 Slide 5 : 3 niveaux de défense — tools, disallowedTools, permissionMode

POURQUOI 3 niveaux et pas un seul ?

Parce que la défense en profondeur évite qu'**une seule erreur** (oubli, agent mal configuré) compromette tout. Chaque niveau intercepte à un endroit différent.

Niveau 1 — `tools` (allowlist) — l'arme la plus stricte

```yaml
tools: Read, Grep, Glob       # Lecture seule pure
```

Le sub-agent **ne peut utiliser que** ces tools. Tout le reste est invisible pour lui.

Niveau 2 — `disallowedTools` (denylist) — héritage avec exceptions

```yaml
disallowedTools: Write, Edit  # Tous les tools du main sauf l'écriture
```

Si les deux sont définis, **denylist gagne** (un tool listé dans les deux est retiré).

Niveau 3 — `permissionMode` — comment les permissions sont demandées

Mode Comportement
`default` Demande confirmation pour chaque action sensible
`acceptEdits` Auto-accepte les `Edit`/`Write` sur le `cwd`
`auto` Mode auto avec classifier en background
`dontAsk` Auto-deny des prompts (seuls les tools allowed marchent)
`bypassPermissions` Skippe toutes les permissions ⚠️ déconseillé
`plan` Read-only exploration (Plan Mode)

⚠️ Règle de précédence parent → sub-agent

Si le **parent** est en `bypassPermissions` ou `acceptEdits`, le sub-agent **hérite et ne peut pas downgrade**. La sécurité d'un sub-agent dépend du contexte parent.

Pattern recommandé

Commencez par le **plus restrictif** (`tools: Read, Grep, Glob`) et élargissez seulement quand c'est nécessaire. Un sub-agent qui n'a pas besoin de Bash ne devrait **pas** avoir Bash.

Et pour les contraintes critiques : doublez les `Rules` du system prompt par un mécanisme bloquant (`disallowedTools` ou un `PreToolUse` hook). Les Rules en langage naturel sont du conseil, pas une garantie.



📝 Slide 6 : Les 5 scopes — où poser un sub-agent

POURQUOI 5 emplacements ?

Parce que les besoins divergent : agent perso utile partout, agent projet partagé en équipe, agent CI/CD éphémère, agent organisation imposé par l'admin.

Table des scopes (priorité décroissante)

# Location Scope Priorité
1 **Managed settings** (admin) Organisation entière **Plus haute**
2 `--agents` CLI flag (JSON) Session courante seulement 2
3 `.claude/agents/` Projet (versionné via git) 3
4 `~/.claude/agents/` Tous vos projets (perso) 4
5 Plugin's `agents/` Là où le plugin est activé **Plus basse**

Si deux sub-agents ont le **même `name`**, la priorité la plus haute gagne.

Décider où poser

Vous voulez… Allez dans…
Un agent utile sur tous vos projets perso `~/.claude/agents/`
Un agent partagé avec votre équipe sur ce projet `.claude/agents/` (commité)
Un agent en CI/CD pour 1 run `claude --agents '{...}'` (JSON inline)
Un agent imposé à toute l'organisation Managed settings (admin)

⚠️ Cas particulier — plugin sub-agents

Pour des raisons de sécurité, les sub-agents installés via plugin **ne supportent pas** `hooks`, `mcpServers`, ni `permissionMode`. Ces champs sont **silencieusement ignorés**. Si vous avez besoin de ces capacités, **copiez l'agent** dans `.claude/agents/` ou `~/.claude/agents/`.

Restart ou pas restart ?

Méthode de création Restart nécessaire ?
Manuel (poser un `.md` à la main) ✅ Oui, redémarrer la session
`/agents` UI in-session ❌ Non, dispo immédiatement
`claude --agents '{...}'` ❌ Non, agents définis pour la session



📝 Slide 7 : Les 5 built-in subagents — laisser Claude bosser tout seul

POURQUOI les connaître si Claude les invoque tout seul ?

Parce que comprendre **quand** ils sont invoqués vous évite d'écrire un sub-agent custom qui fait déjà ce qu'un built-in fait. Et parce que vous pouvez les **désactiver** sélectivement si vous voulez forcer le routing vers vos agents.

Les 5 built-ins

Nom Modèle Tools Quand il est invoqué
**Explore** Haiku Read-only "find all places where X is used", recherche codebase
**Plan** inherit Read-only Pendant Plan Mode (cf. 1.1) — recherche avant plan
**general-purpose** inherit Tous Tâches multi-étapes (exploration + modif + raisonnement) — couteau suisse
**statusline-setup** Sonnet Read + Edit Quand vous lancez `/statusline`
**claude-code-guide** Haiku Bash + Read + WebFetch + WebSearch Quand vous posez une question sur Claude Code lui-même

`Explore` — celui que vous croiserez le plus

3 niveaux de profondeur :

Niveau Quand l'utiliser
`quick` Single targeted lookup ("où est défini `getUserById` ?")
`medium` Exploration moyenne (5-10 fichiers)
`very thorough` Cartographie large (multi-locations + naming conventions)

Désactiver un built-in

Dans `.claude/settings.json` :

```json
{ "permissions": { "deny": ["Agent(Explore)"] } }
```

→ Claude ne pourra plus invoquer Explore. Force le routing vers vos custom agents (rare en pratique).



📝 Slide 8 : Skills vs Subagents vs Agent Teams — où placer la limite

POURQUOI cette comparaison est piégeuse ?

Parce que les 3 mécanismes "rajoutent quelque chose" à Claude Code, et confondre lesquels mène à des agents inutilement lourds ou à des Skills mal employés.

Comparatif

**Skills** **Subagents** **Agent Teams**
Quoi Recette portable (md + scripts) Worker isolé avec son contexte Multi-sessions parallèles
Exécution **Dans** la conversation main Dans son **propre contexte** Sessions Claude Code séparées
Communication Modifie le main Ne parle qu'au parent (résumé) Teammates s'envoient des messages
Token cost Léger (~100 tokens metadata + chargement on-demand) Modéré (system prompt rechargé par invocation) Élevé (1 contexte full par teammate)
Quand l'utiliser "Comment faire X ?" (savoir-faire) "Fais X isolément" (tâche bornée) Plusieurs agents en parallèle qui dialoguent

L'arbre de décision

```
Vous voulez un savoir-faire réutilisable ?
├─ Oui → Skill (recette portable)
└─ Non → vous voulez isoler la verbosité d'une tâche ?
   ├─ Oui → Subagent
   └─ Non → vous avez besoin de paralléliser ET de dialogue inter-agents ?
      ├─ Oui → Agent Teams (experimental)
      └─ Non → restez sur le main agent
```

Le combo gagnant — Subagent + Skills préchargés

```yaml
---
name: api-developer
description: Implement API endpoints following team conventions
skills:
  - api-conventions
  - error-handling-patterns
---
```

Le sub-agent absorbe le coût (contexte isolé), les Skills lui donnent l'expertise figée au boot. **Pattern recommandé** pour les agents experts qui ont besoin de connaître des conventions précises.



📝 Slide 9 : Choix du modèle — sonnet par défaut, exceptions documentées

POURQUOI ne pas tout mettre sur Opus ?

Parce qu'Opus 4.7 est ~5× plus cher que Sonnet, et que pour 90 % des tâches **la différence n'est pas perceptible**. Mettre le bon modèle sur le bon agent économise 80 % de la facture sans dégrader la qualité.

Le tableau de décision (mai 2026)

Alias Modèle Quand l'utiliser Cas type
`sonnet` `claude-sonnet-4-6` **Défaut prod** pour 90% des sub-agents UI builder, refacto, API dev, data analysis
`opus` `claude-opus-4-7` Raisonnement profond critique Architecture review, debug retors, security review
`haiku` `claude-haiku-4-5` Tâches rapides simples Lint fix, formattage, file discovery, triage logs
`inherit` (du main) Cohérence dans une chaîne d'agents Sub-agent qui doit "matcher" la profondeur du main

Ordre de résolution

Si plusieurs sources définissent le modèle, l'ordre de précédence est :

1. Env var `CLAUDE_CODE_SUBAGENT_MODEL` (override global)
2. Paramètre per-invocation (au lancement)
3. Frontmatter (`model: …`)
4. Main conversation (si rien n'est défini)

⚠️ Le piège du défaut

`model: inherit` est le défaut **si vous n'écrivez rien**. Si votre main tourne sur Opus 4.7, votre sub-agent simple **aussi** → facturation salée pour rien.

**Toujours expliciter** `model: sonnet` ou `model: haiku` pour les sub-agents simples afin d'éviter la dérive.



📝 Slide 10 : Options avancées — `isolation`, `memory`, `hooks` frontmatter

POURQUOI ces 3 options méritent un slide dédié ?

Parce qu'elles transforment un sub-agent "prompt + restrictions" en agent **résilient et persistant** : il peut expérimenter sans risque, retenir des learnings, et se gardes-fou ses propres tool calls.

`isolation: worktree` — le filet de sécurité par-conception

```yaml
isolation: worktree
```

Le sub-agent travaille dans un **git worktree temporaire** créé à partir de votre HEAD. Tous ses `Edit` / `Write` vont dans cette copie isolée.

Cas Comportement
Sub-agent ne modifie rien Worktree supprimé automatiquement
Sub-agent modifie quelque chose Vous recevez le path + le nom de la branche dans le résumé final → à vous de merger

**Combo gagnant** : `isolation: worktree` + git baseline = zéro risque d'altération non-revertible.

`memory: project` — persistent memory entre sessions

```yaml
memory: project   # ou: user, local
```

Scope Location Quand l'utiliser
`memory: user` `~/.claude/agent-memory/<name>/` Learnings broad (across projets)
`memory: project` `.claude/agent-memory/<name>/` Spécifique projet, partageable git ⭐ recommandé
`memory: local` `.claude/agent-memory-local/<name>/` Spécifique projet, non versionné

Le sub-agent reçoit automatiquement des instructions read/write sur son `MEMORY.md`, plus les 200 premières lignes (~25 KB) injectées à chaque invocation.

`hooks` — gardes-fous à l'intérieur du sub-agent

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-bash.sh"
```

Cas d'usage classique : un sub-agent "DB reader" qui peut faire `Bash` mais **uniquement des `SELECT`**. Le hook `PreToolUse` valide chaque commande avant exécution. Si la commande contient `INSERT/UPDATE/DELETE/DROP`, le hook exit 2 → la commande est bloquée.

Combinaison ultime

```yaml
---
name: experimental-refactor
description: Try an experimental refactoring approach
tools: Read, Edit, Write, Bash
model: sonnet
isolation: worktree
memory: project
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-no-deploy.sh"
---
```

→ Sub-agent qui modifie dans un worktree isolé, retient ses learnings, et a un hook qui interdit les commandes de déploiement. Vous pouvez le lancer en confiance.



🎓 Ce que vous devez retenir

Concept Pourquoi c'est important
Sub-agent = un fichier markdown Pas de framework, pas de runtime — `.md` + frontmatter YAML
2 champs obligatoires `name` + `description`. Tout le reste est optionnel
Tool `Agent` ≠ sub-agent `Agent` est la porte ; les sub-agents nommés sont les personnes
`description` = le champ critique Trigger phrases ("Use proactively when…") + stack explicite
3 niveaux de défense `tools` (allowlist) > `disallowedTools` (denylist) > `permissionMode`
5 scopes par priorité Managed > CLI flag > project > user > plugin
5 built-in subagents Explore, Plan, general-purpose, statusline-setup, claude-code-guide
Skills vs Subagents vs Agent Teams Skill = savoir-faire ; Subagent = isolation ; Agent Teams = parallélisation+dialogue
Modèle — sonnet par défaut Opus pour raisonnement profond, Haiku pour tâches simples
`isolation: worktree` Filet de sécurité par-conception (combo avec git baseline)
`memory: project` Persistent memory entre sessions, partageable via git
Restart ou pas `/agents` UI = pas de restart. Création manuelle `.md` = restart obligatoire



➡️ Prochaine leçon

Vous savez créer et restreindre des sub-agents. La leçon **1.5** zoome sur les **grosses codebases** où le contexte explose : stratégies pour gérer un repo de 100k+ LOC, auto-memory, `/compact`, et MCPs spécialisés (Serena pour le semantic search). C'est la suite logique : un sub-agent bien fait + une bonne gestion de mémoire = vraiment scalable.
