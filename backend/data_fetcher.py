# data_fetcher.py
from services.data_sources.merge_indicators import get_complete_country_profile
from services.country_mapper import COUNTRY_MAPPING, normalize_name

GLOBAL_BASELINES = {
    "economy": 0.45,
    "health": 0.60,
    "safety": 0.40,
    "climate": 0.55,
    "education": 0.50,
    "connectivity": 0.65,
    "equality": 0.45
}


def smooth_value(value: float | None, baseline: float) -> float:
    if value is None or value <= 0:
        return round(baseline, 3)
    return round(min(max(value, 0.05), 0.95), 3)


def fetch_country_data(country_name: str) -> dict:
    key = normalize_name(country_name)
    country_code = COUNTRY_MAPPING.get(key)

    if not country_code:
        raise ValueError(f"No se encontró código ISO3 para '{country_name}'.")

    try:
        profile = get_complete_country_profile(country_name, country_code)
    except Exception:
        profile = {}

    normalized = {
        k: smooth_value(profile.get(k), GLOBAL_BASELINES[k])
        for k in GLOBAL_BASELINES
    }

    sources = profile.get("sources", {})

    return {
        "country": country_name,
        "code": country_code,
        "normalized": normalized,
        "sources": sources,
        "source": "Global Multi-API",
        "meta": {
            "fetched_from": list(set(sources.values()))
        }
    }
