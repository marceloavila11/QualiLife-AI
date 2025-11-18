# services/data_sources/who_client.py
import requests


def get_health_data(country_code: str) -> dict:
    """
    Obtiene datos de salud desde la API de la OMS (WHO GHO).
    Usa esperanza de vida y cobertura sanitaria como indicadores.
    """
    base_url = "https://ghoapi.azureedge.net/api/"
    indicators = {
        "life_expectancy": "LIFE_EXPECTANCY",
        "uhc_coverage": "UHC_INDEX"
    }

    results = {}
    for key, ind in indicators.items():
        try:
            resp = requests.get(
                f"{base_url}{ind}?$filter=SpatialDim eq '{country_code}'", timeout=10)
            data = resp.json()
            if "value" in data and data["value"]:
                results[key] = float(data["value"][0].get("NumericValue", 0))
        except Exception:
            results[key] = None

    # fallback si no hay datos
    if not results.get("life_expectancy"):
        results["life_expectancy"] = 70.0
    if not results.get("uhc_coverage"):
        results["uhc_coverage"] = 65.0

    return results
