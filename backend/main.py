import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from services.data_sources.merge_indicators import merge_all_indicators
from services.qli_cache_service import get_cached_qli, save_cached_qli
from ia.ai_interpreter import generate_detailed_insight

load_dotenv()

app = FastAPI(title="QualiLife AI - Multi-Source Intelligence")

allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in allowed_origins if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/qli/auto")
async def qli_auto(country: str):
    country = country.strip().lower()

    cached = await get_cached_qli(country)
    if cached:
        return {
            "qli": cached["qli"],
            "data": cached["data"],
            "insights": cached["insights"],
            "source": "cache"
        }

    merged = await merge_all_indicators(country)
    normalized = merged["normalized"]
    sources = merged["sources"]

    qli = round(
        sum([
            normalized["economy"],
            normalized["health"],
            normalized["climate"],
            normalized["safety"],
            normalized["education"],
            normalized["connectivity"],
            normalized["equality"],
        ]) / 7,
        3
    )

    try:
        insights = generate_detailed_insight(
            country.capitalize(),
            normalized,
            sources
        )
    except Exception:
        insights = {
            "summary": f"No fue posible generar el análisis con IA. QLI estimado: {qli*100:.1f}%.",
            "sources": {src: "Sin interpretación generada." for src in sources.values()},
        }

    await save_cached_qli(
        country=country,
        qli=qli,
        data=normalized,
        insights=insights
    )

    return {
        "qli": qli,
        "data": {**normalized, "qli": qli, "country": country},
        "insights": insights,
        "source": "live"
    }
