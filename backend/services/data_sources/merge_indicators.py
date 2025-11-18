# services/data_sources/merge_indicators.py

from services.data_sources.world_bank_client import get_worldbank_data
from services.data_sources.numbeo_client import get_safety_data
from services.data_sources.undp_client import get_equality_data
from services.data_sources.unesco_client import get_education_data
from services.data_sources.climate_client import get_climate_data
from services.data_sources.who_client import get_health_data
from services.data_sources.itu_client import get_connectivity_data

from typing import Dict

# --------------------------------------------------------------
#  Utilidad: mapa mínimo de países a códigos ISO, puedes ampliarlo
# --------------------------------------------------------------
COUNTRY_ISO = {
    "ecuador": "ECU",
    "peru": "PER",
    "colombia": "COL",
    "argentina": "ARG",
    "chile": "CHL",
    "mexico": "MEX",
    "spain": "ESP",
}


def get_country_iso(country: str) -> str:
    """
    Devuelve un código ISO. Si no existe en el mapa,
    devuelve la versión de 3 letras basada en el nombre.
    """
    c = country.lower().strip()
    if c in COUNTRY_ISO:
        return COUNTRY_ISO[c]

    # fallback simple
    return c[:3].upper()


def get_complete_country_profile(country_name: str, country_code: str) -> Dict:
    wb = get_worldbank_data(country_code)
    safety = get_safety_data(country_name)
    equality = get_equality_data(country_name)
    edu = get_education_data(country_code)
    climate = get_climate_data(country_code)
    who = get_health_data(country_code)
    itu = get_connectivity_data(country_code)

    raw = {
        "economy": {"value": wb.get("gdp_per_capita_ppp"), "source": "World Bank"},
        "health_life": {"value": who.get("life_expectancy"), "source": "WHO"},
        "health_uhc": {"value": who.get("uhc_coverage"), "source": "WHO"},
        "connectivity_internet": {"value": itu.get("internet_users"), "source": "ITU"},
        "connectivity_mobile": {"value": itu.get("mobile_subscriptions"), "source": "ITU"},
        "safety": {"value": safety.get("crime_index"), "source": "Numbeo"},
        "equality": {"value": equality.get("gender_inequality"), "source": "UNDP"},
        "education": {"value": edu.get("school_enrollment"), "source": "UNESCO"},
        "climate_renewables": {"value": climate.get("renewables_percent"), "source": "Climate Portal"},
        "climate_co2": {"value": climate.get("co2_per_capita"), "source": "Climate Portal"},
    }

    # Normalización
    def norm(val, min_v, max_v, invert=False):
        try:
            v = float(val)
            v = max(min_v, min(v, max_v))
            scaled = (v - min_v) / (max_v - min_v)
            return round(1 - scaled if invert else scaled, 3)
        except Exception:
            return 0.0

    normalized = {
        "economy": norm(raw["economy"]["value"], 1000, 120000),
        "health": (
            norm(raw["health_life"]["value"], 50, 85)
            + norm(raw["health_uhc"]["value"], 30, 100)
        ) / 2,
        "connectivity": (
            norm(raw["connectivity_internet"]["value"], 5, 100)
            + norm(raw["connectivity_mobile"]["value"], 30, 180)
        ) / 2,
        "safety": norm(raw["safety"]["value"], 0, 100, invert=True),
        "equality": norm(raw["equality"]["value"], 0, 1, invert=True),
        "education": norm(raw["education"]["value"], 30, 100),
        "climate": (
            norm(raw["climate_renewables"]["value"], 0, 100)
            + norm(raw["climate_co2"]["value"], 0, 15, invert=True)
        ) / 2,
    }

    sources = {
        "economy": raw["economy"]["source"],
        "health": raw["health_life"]["source"],
        "connectivity": raw["connectivity_internet"]["source"],
        "safety": raw["safety"]["source"],
        "equality": raw["equality"]["source"],
        "education": raw["education"]["source"],
        "climate": raw["climate_renewables"]["source"],
    }

    # Evitar cero total
    for key in normalized:
        if normalized[key] <= 0:
            normalized[key] = 0.5

    return {
        "normalized": normalized,
        "sources": sources,
        "meta": {"country": country_name, "code": country_code},
    }


# --------------------------------------------------------------
#  Aquí está la función que tu main.py necesita
# --------------------------------------------------------------
async def merge_all_indicators(country: str) -> Dict:
    """
    Wrapper estándar usado por main.py.
    Obtiene el código ISO del país y ejecuta el perfil completo.
    """
    code = get_country_iso(country)
    result = get_complete_country_profile(
        country_name=country, country_code=code)
    return result
