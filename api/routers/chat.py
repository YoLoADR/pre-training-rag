from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: str = Field(default="default")


class ChatResponse(BaseModel):
    response: str
    session_id: str
    llm_provider: str


@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    Endpoint principal de chat avec l'agent ReAct HomeButler.
    L'agent orchestre automatiquement les outils nécessaires.
    """
    try:
        from homebutler.agent.react_agent import get_singleton_agent
        from homebutler import config

        agent = get_singleton_agent(verbose=False)
        result = agent.invoke({"input": req.message})
        response_text = result.get("output", "Je n'ai pas pu générer de réponse.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur agent : {str(e)}")

    from homebutler import config
    return ChatResponse(
        response=response_text,
        session_id=req.session_id,
        llm_provider=config.LLM_PROVIDER,
    )
