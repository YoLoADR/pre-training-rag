"""
Agent ReAct HomeButler.
Utilise le prompt standard de LangChain Hub (hwchase17/react).
Supporte LangSmith (via env vars) et Langfuse (via LangfuseService).
"""

from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
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
    # (LANGCHAIN_TRACING_V2, LANGCHAIN_API_KEY, LANGCHAIN_PROJECT)
    return callbacks


def get_agent_executor(verbose: bool = True) -> AgentExecutor:
    """
    Crée et retourne un AgentExecutor ReAct.
    - verbose=True : affiche le raisonnement Thought→Action→Observation
    - verbose=False : pour l'API (silencieux)
    """
    llm = get_llm(temperature=0.1, max_tokens=2048)

    # Prompt ReAct standard depuis LangChain Hub
    # hwchase17/react est le plus robuste avec Anthropic et Ollama
    try:
        prompt = hub.pull("hwchase17/react")
    except Exception:
        # Fallback local si pas d'accès hub
        from langchain_core.prompts import PromptTemplate
        prompt = PromptTemplate.from_template(
            "Answer the following questions as best you can. You have access to the following tools:\n\n"
            "{tools}\n\n"
            "Use the following format:\n\n"
            "Question: the input question you must answer\n"
            "Thought: you should always think about what to do\n"
            "Action: the action to take, should be one of [{tool_names}]\n"
            "Action Input: the input to the action\n"
            "Observation: the result of the action\n"
            "... (this Thought/Action/Action Input/Observation can repeat N times)\n"
            "Thought: I now know the final answer\n"
            "Final Answer: the final answer to the original input question\n\n"
            "Begin!\n\n"
            "Question: {input}\n"
            "Thought:{agent_scratchpad}"
        )

    callbacks = _setup_tracing()

    agent = create_react_agent(llm, ALL_TOOLS, prompt)

    return AgentExecutor(
        agent=agent,
        tools=ALL_TOOLS,
        verbose=verbose,
        max_iterations=8,
        handle_parsing_errors=True,  # robustesse avec Ollama non fine-tuné
        callbacks=callbacks if callbacks else None,
    )


# Singleton pour l'API (initialisé une seule fois)
_agent_executor: AgentExecutor | None = None


def get_singleton_agent(verbose: bool = False) -> AgentExecutor:
    """Retourne l'agent singleton (pour usage en API)."""
    global _agent_executor
    if _agent_executor is None:
        _agent_executor = get_agent_executor(verbose=verbose)
    return _agent_executor
