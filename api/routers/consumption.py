from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

router = APIRouter(prefix="/consumption", tags=["consumption"])


class ConsumptionStats(BaseModel):
    annual_kwh: float
    annual_eur: float
    avg_daily_kwh: float
    anomaly_count: int
    monthly_summary: list[dict]
    anomalies: list[dict]


@router.get("/stats", response_model=ConsumptionStats)
async def get_consumption_stats():
    """Retourne les statistiques complètes de consommation électrique."""
    try:
        from homebutler.services.energy import (
            load_consumption, get_annual_stats, get_monthly_summary, detect_anomalies
        )
        df = load_consumption()
        stats = get_annual_stats(df)
        monthly = get_monthly_summary(df)
        anomalies = detect_anomalies(df)

        return ConsumptionStats(
            annual_kwh=stats["total_kwh"],
            annual_eur=stats["total_eur"],
            avg_daily_kwh=stats["avg_daily_kwh"],
            anomaly_count=stats["anomaly_count"],
            monthly_summary=monthly,
            anomalies=[
                {
                    "date": str(a["date"]),
                    "consommation_kwh": a["consommation_kwh"],
                    "z_score": a.get("z_score"),
                }
                for a in anomalies
            ],
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class AnalyzeRequest(BaseModel):
    question: str = "Ma consommation électrique est-elle normale ?"


class AnalyzeResponse(BaseModel):
    analysis: str
    raw_stats: dict


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_consumption(req: AnalyzeRequest):
    """Analyse la consommation via le LLM avec les données réelles."""
    try:
        from homebutler.services.energy import load_consumption, format_summary_for_llm, get_annual_stats
        from homebutler.llm.provider import get_llm
        from homebutler.llm.prompts import ENERGY_ANALYSIS_TEMPLATE

        df = load_consumption()
        summary = format_summary_for_llm(df)
        stats = get_annual_stats(df)

        from homebutler.services.energy import detect_anomalies, get_monthly_summary
        anomalies_raw = detect_anomalies(df)
        anomaly_str = "\n".join(
            f"  - {str(a['date'])[:10]}: {a['consommation_kwh']} kWh (z-score: {a.get('z_score', '?')})"
            for a in anomalies_raw[:5]
        ) or "Aucune anomalie détectée"

        monthly_raw = get_monthly_summary(df)
        monthly_str = "\n".join(
            f"  - {m['month']}: {m['total_kwh']} kWh ({m['total_eur']}€)"
            for m in monthly_raw[-3:]
        )

        llm = get_llm(temperature=0.1)
        chain = ENERGY_ANALYSIS_TEMPLATE | llm
        result = chain.invoke({
            "question": req.question,
            "monthly_summary": monthly_str,
            "anomalies": anomaly_str,
        })

        return AnalyzeResponse(
            analysis=result.content,
            raw_stats=stats,
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
