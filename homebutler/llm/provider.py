from langchain_anthropic import ChatAnthropic
from langchain_community.chat_models import ChatOllama
from homebutler import config


def get_llm(temperature: float = 0.1, max_tokens: int = 1024):
    """
    Retourne le LLM configuré selon LLM_PROVIDER.
    - "anthropic" → Claude via Anthropic API
    - "ollama"    → modèle local/VPS via Ollama
    """
    if config.LLM_PROVIDER == "anthropic":
        if not config.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY manquant dans .env")
        return ChatAnthropic(
            model=config.ANTHROPIC_MODEL,
            api_key=config.ANTHROPIC_API_KEY,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    # Ollama (modèle local ou VPS)
    return ChatOllama(
        base_url=config.OLLAMA_HOST,
        model=config.OLLAMA_MODEL,
        temperature=temperature,
        num_predict=max_tokens,
    )
