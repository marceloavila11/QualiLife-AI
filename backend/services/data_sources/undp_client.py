# services/data_sources/undp_client.py
import requests
from typing import Optional


def get_equality_data(country: str) -> dict:
    """
    Usa el índice de desigualdad de género del UNDP.
    Normaliza para evaluar igualdad de género.
    """
    try:
        url = f"https://hdr.undp.org/data-center/thematic-composite-indices/gender-inequality-index#/api/countries/{country}"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        gii = data.get("GII")
        if gii is not None:
            return {"gender_inequality": float(gii)}
    except Exception:
        pass
    return {"gender_inequality": None}
