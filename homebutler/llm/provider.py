from langchain_anthropic import ChatAnthropic
from langchain_community.chat_models import ChatOllama
from homebutler import config


def get_llm(temperature: float = 0.1, max_tokens: int = 1024, streaming: bool = False):
    """
    Retourne le LLM configuré selon LLM_PROVIDER.
    - "anthropic" → Claude via Anthropic API
    - "ollama"    → modèle local/VPS via Ollama
    streaming=True : active le streaming token par token (J3 déploiement).
    """
    if config.LLM_PROVIDER == "anthropic":
        if not config.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY manquant dans .env")
        return ChatAnthropic(
            model=config.ANTHROPIC_MODEL,
            api_key=config.ANTHROPIC_API_KEY,
            temperature=temperature,
            max_tokens=max_tokens,
            streaming=streaming,
        )

    # Ollama (modèle local ou VPS)
    return ChatOllama(
        base_url=config.OLLAMA_HOST,
        model=config.OLLAMA_MODEL,
        temperature=temperature,
        num_predict=max_tokens,
    )


def get_llm_cached(temperature: float = 0.1, max_tokens: int = 1024):
    """
    Version Anthropic avec prompt caching (beta 'prompt-caching-2024-07-31').
    Réduit le coût token du system prompt après le premier appel (cache 5 min).
    Pédagogie J3 — optimisation production.
    Fallback sur get_llm() si provider != anthropic.
    """
    if config.LLM_PROVIDER == "anthropic":
        if not config.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY manquant dans .env")
        return ChatAnthropic(
            model=config.ANTHROPIC_MODEL,
            api_key=config.ANTHROPIC_API_KEY,
            temperature=temperature,
            max_tokens=max_tokens,
            model_kwargs={
                "extra_headers": {"anthropic-beta": "prompt-caching-2024-07-31"}
            },
        )
    return get_llm(temperature, max_tokens)
