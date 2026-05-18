"""
Endpoint de commande (simulation).
Enregistre les commandes dans un fichier JSON local (data/orders.json).
Pas de vraie transaction — usage pédagogique uniquement.
"""

import json
import os
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/order", tags=["orders"])

ORDERS_FILE = os.path.join("data", "orders.json")


class OrderItem(BaseModel):
    producer_id: int
    produit: str
    quantite: str = Field(description="Ex: '2 kg', '1 barquette', '1 unité'")


class OrderRequest(BaseModel):
    items: list[OrderItem] = Field(min_length=1)
    nom_client: str
    adresse_livraison: str = ""
    notes: str = ""


class OrderResponse(BaseModel):
    order_id: str
    status: str
    message: str
    items_count: int
    created_at: str


@router.post("", response_model=OrderResponse)
async def create_order(req: OrderRequest):
    """Crée une commande simulée auprès d'un producteur local."""
    try:
        # Charger les commandes existantes
        orders = []
        if os.path.exists(ORDERS_FILE):
            with open(ORDERS_FILE, encoding="utf-8") as f:
                orders = json.load(f)

        # Créer la commande
        order_id = f"HB-{datetime.now().strftime('%Y%m%d%H%M%S')}-{len(orders)+1:04d}"
        order = {
            "order_id": order_id,
            "status": "pending",
            "nom_client": req.nom_client,
            "adresse_livraison": req.adresse_livraison,
            "notes": req.notes,
            "items": [item.model_dump() for item in req.items],
            "created_at": datetime.now().isoformat(),
        }

        orders.append(order)

        os.makedirs(os.path.dirname(ORDERS_FILE), exist_ok=True)
        with open(ORDERS_FILE, "w", encoding="utf-8") as f:
            json.dump(orders, f, ensure_ascii=False, indent=2)

        return OrderResponse(
            order_id=order_id,
            status="pending",
            message=(
                f"Commande enregistrée ! Votre conciergerie HomeButler va contacter "
                f"le producteur pour confirmer la disponibilité."
            ),
            items_count=len(req.items),
            created_at=order["created_at"],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{order_id}", tags=["orders"])
async def get_order(order_id: str):
    """Récupère le statut d'une commande."""
    if not os.path.exists(ORDERS_FILE):
        raise HTTPException(status_code=404, detail="Aucune commande enregistrée")

    with open(ORDERS_FILE, encoding="utf-8") as f:
        orders = json.load(f)

    order = next((o for o in orders if o["order_id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail=f"Commande {order_id} introuvable")

    return order
