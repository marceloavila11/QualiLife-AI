from datetime import datetime, timedelta
from db.db_client import collection  # tu colección global

CACHE_DAYS = 30  # tiempo de validez del cache en días


async def get_cached_qli(country: str):
    """
    Obtiene un registro cacheado de Mongo si existe y no ha expirado.
    """
    doc = await collection.find_one({"country": country.lower()})
    if not doc:
        return None

    # Validar expiración
    created = doc.get("created_at", None)
    if not created:
        return None

    if created < datetime.utcnow() - timedelta(days=CACHE_DAYS):
        return None

    return doc


async def save_cached_qli(country: str, qli: float, data: dict, insights: dict):
    """
    Guarda o actualiza el registro cacheado de un país.
    """
    record = {
        "country": country.lower(),
        "qli": qli,
        "data": data,
        "insights": insights,
        "created_at": datetime.utcnow(),
    }

    await collection.update_one(
        {"country": country.lower()},
        {"$set": record},
        upsert=True
    )
