"""
Agent ReAct HomeButler.
- Prompt hwchase17/react-chat (supporte chat_history pour la mémoire conversationnelle).
- Session memory : ConversationBufferWindowMemory par session_id (k=6 tours).
- Debug mode : return_intermediate_steps=True pour exposer la trace Thought/Action.
- Tracing : LangSmith (env vars) ou Langfuse (TRACING_PROVIDER=langfuse).
"""

from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain.memory import ConversationBufferWindowMemory
from homebutler.llm.provider import get_llm
from homebutler.agent.tools import ALL_TOOLS
from homebutler import config


def _setup_tracing() -> list:
    """Configure les callbacks de tracing selon TRACING_PROVIDER."""
    callbacks = []

    if config.TRACING_PROVIDER == "langfuse" and config.LANGFUSE_PUBLIC_KEY:
        try:
            from langfuse.callback import CallbackHandler as LangfuseHandler
        except ImportError:
            try:
                from langfuse.langchain import CallbackHandler as LangfuseHandler
            except ImportError:
                LangfuseHandler = None

        if LangfuseHandler:
            callbacks.append(
                LangfuseHandler(
                    public_key=config.LANGFUSE_PUBLIC_KEY,
                    secret_key=config.LANGFUSE_SECRET_KEY,
                    host=config.LANGFUSE_HOST,
                )
            )

    # LangSmith s'active automatiquement via les env vars propagées dans config.py
    return callbacks


def _build_fallback_prompt():
    """Prompt ReAct local avec support chat_history (si hub indisponible)."""
    from langchain_core.prompts import PromptTemplate
    return PromptTemplate.from_template(
        "Tu es HomeButler, conciergerie domestique intelligente.\n"
        "Tu as accès aux outils suivants :\n\n"
        "{tools}\n\n"
        "Format STRICT :\n"
        "Question : la question posée\n"
        "Réflexion : réfléchis à ce que tu dois faire\n"
        "Action : l'outil à utiliser, doit être l'un de [{tool_names}]\n"
        "Entrée de l'action : l'entrée pour l'outil\n"
        "Observation : le résultat de l'outil\n"
        "... (répète si nécessaire)\n"
        "Réflexion : Je connais maintenant la réponse finale\n"
        "Réponse finale : la réponse à la question originale\n\n"
        "Historique de conversation :\n{chat_history}\n\n"
        "Commence !\n\n"
        "Question : {input}\n"
        "Réflexion : {agent_scratchpad}"
    )


def get_agent_executor(
    verbose: bool = True,
    debug: bool = False,
    memory: ConversationBufferWindowMemory | None = None,
) -> AgentExecutor:
    """
    Crée et retourne un AgentExecutor ReAct.
    - verbose : affiche le raisonnement Thought→Action→Observation
    - debug   : return_intermediate_steps=True (expose la trace dans l'API)
    - memory  : ConversationBufferWindowMemory pour la mémoire de session
    """
    llm = get_llm(temperature=0.1, max_tokens=2048)

    # Prompt react-chat supporte {chat_history} pour la mémoire conversationnelle
    try:
        prompt = hub.pull("hwchase17/react-chat")
    except Exception:
        prompt = _build_fallback_prompt()

    callbacks = _setup_tracing()

    agent = create_react_agent(llm, ALL_TOOLS, prompt)

    return AgentExecutor(
        agent=agent,
        tools=ALL_TOOLS,
        verbose=verbose,
        max_iterations=8,
        handle_parsing_errors=True,
        return_intermediate_steps=debug,
        memory=memory,
        callbacks=callbacks if callbacks else None,
    )


# ── Sessions avec mémoire conversationnelle ───────────────────────────────────

_sessions: dict[str, AgentExecutor] = {}


def get_session_agent(session_id: str = "default") -> AgentExecutor:
    """
    Retourne un agent avec mémoire conversationnelle par session_id.
    k=6 : garde les 6 derniers tours (3 questions + 3 réponses).
    Pédagogie J2 : montre qu'un agent peut garder le contexte conversationnel.
    Note : la mémoire est en RAM → reset si l'API redémarre.
    """
    if session_id not in _sessions:
        memory = ConversationBufferWindowMemory(
            k=6,
            memory_key="chat_history",
            return_messages=True,
            output_key="output",
        )
        _sessions[session_id] = get_agent_executor(
            verbose=False,
            debug=False,
            memory=memory,
        )
    return _sessions[session_id]


def get_session_agent_debug(session_id: str = "default") -> AgentExecutor:
    """Variante debug : return_intermediate_steps=True pour exposer la trace."""
    memory = ConversationBufferWindowMemory(
        k=6,
        memory_key="chat_history",
        return_messages=True,
        output_key="output",
    )
    return get_agent_executor(verbose=True, debug=True, memory=memory)


# ── Singleton pour l'API (sans mémoire, rétrocompatibilité) ──────────────────

_agent_executor: AgentExecutor | None = None


def get_singleton_agent(verbose: bool = False) -> AgentExecutor:
    """Retourne l'agent singleton sans mémoire (rétrocompatibilité lifespan API)."""
    global _agent_executor
    if _agent_executor is None:
        _agent_executor = get_agent_executor(verbose=verbose)
    return _agent_executor
