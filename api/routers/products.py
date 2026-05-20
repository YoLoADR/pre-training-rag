from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

router = APIRouter(prefix="/products", tags=["products"])


class ProducerResult(BaseModel):
    id: int
    nom: str
    type: str
    produits: list[str]
    latitude: float
    longitude: float
    distance_calculee_km: float
    livraison: bool
    min_commande_eur: float
    phone: str
    horaires: str
    description: str


@router.get("/search", response_model=list[ProducerResult])
async def search_products(
    query: str = Query(default="", description="Mot-clé produit ou type d'artisan"),
    product_type: str = Query(default="", description="Type : légumes, pain, fromage, viande, épicerie, artisan-*"),
    max_km: float = Query(default=30.0, ge=0, le=100, description="Distance maximale en km"),
    delivery_only: bool = Query(default=False, description="Uniquement avec livraison"),
    limit: int = Query(default=10, ge=1, le=30),
):
    """Recherche des producteurs locaux et artisans."""
    try:
        from homebutler.services.marketplace import search_producers
        results = search_producers(
            query=query,
            product_type=product_type,
            max_distance_km=max_km,
            delivery_only=delivery_only,
            limit=limit,
        )
        return [
            ProducerResult(
                id=p["id"],
                nom=p["nom"],
                type=p["type"],
                produits=p["produits"],
                latitude=p["latitude"],
                longitude=p["longitude"],
                distance_calculee_km=p["distance_calculee_km"],
                livraison=p.get("livraison", False),
                min_commande_eur=p.get("min_commande_eur", 0),
                phone=p.get("phone", ""),
                horaires=p.get("horaires", ""),
                description=p.get("description", ""),
            )
            for p in results
        ]
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
