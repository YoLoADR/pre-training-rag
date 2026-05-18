"""
API FastAPI HomeButler AI.
Endpoints : /chat, /consumption/analyze, /products/search, /order
Sécurité  : filtre prompt injection, CORS, clé API optionnelle
"""

import re
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from homebutler import config

# ── Patterns de détection prompt injection ───────────────────────────────────
_INJECTION_PATTERNS = [
    r"ignore\s+(tes|les|toutes|mes|vos)\s+instructions",
    r"oublie\s+(le|ton|tes|votre|toutes)\s+(contexte|instructions?|prompt)",
    r"system\s*prompt",
    r"jailbreak",
    r"act\s+as\s+",
    r"pretend\s+(you\s+are|to\s+be)",
    r"disregard\s+(all|your|previous)",
    r"ignore\s+all\s+previous",
    r"tu\s+es\s+maintenant",
    r"désactive\s+tes\s+restrictions",
]
_INJECTION_RE = re.compile("|".join(_INJECTION_PATTERNS), re.IGNORECASE)


# ── Lifespan : initialisation au démarrage ────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("HomeButler AI — démarrage de l'API")
    # Pré-initialisation de l'agent (évite le cold-start sur la première requête)
    try:
        from homebutler.agent.react_agent import get_singleton_agent
        get_singleton_agent(verbose=False)
        print("  ✓ Agent ReAct initialisé")
    except Exception as e:
        print(f"  ⚠ Agent non initialisé (index RAG manquant ?) : {e}")
    yield
    print("HomeButler AI — arrêt de l'API")


app = FastAPI(
    title="HomeButler AI API",
    description="Conciergerie domestique intelligente — Formation RAFT",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — permissif pour le développement (à restreindre en production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Middleware : filtre prompt injection ──────────────────────────────────────
@app.middleware("http")
async def prompt_injection_filter(request: Request, call_next):
    if request.method == "POST":
        body_bytes = await request.body()
        body_text = body_bytes.decode("utf-8", errors="ignore")

        if _INJECTION_RE.search(body_text):
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "security_filter",
                    "message": "Requête refusée par le filtre de sécurité.",
                },
            )
        # Remettre le body pour que les routers puissent le lire
        request._body = body_bytes

    return await call_next(request)


# ── Routes ────────────────────────────────────────────────────────────────────
from api.routers import chat, consumption, products, orders  # noqa: E402

app.include_router(chat.router)
app.include_router(consumption.router)
app.include_router(products.router)
app.include_router(orders.router)


@app.get("/", tags=["health"])
async def root():
    return {
        "service": "HomeButler AI API",
        "version": "1.0.0",
        "llm_provider": config.LLM_PROVIDER,
        "status": "ok",
    }


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}
