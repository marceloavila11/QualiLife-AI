# services/data_sources/numbeo_client.py
import os
import requests
from typing import Optional

API_KEY = os.getenv("NUMBEO_API_KEY")


def get_safety_data(country: str) -> dict:
    """
    Usa el índice de seguridad de Numbeo para evaluar la seguridad del país.
    Normaliza para evaluar seguridad ciudadana.
    """

    if not API_KEY:
        return {"crime_index": None}
    try:
        resp = requests.get(
            "https://www.numbeo.com/api/country_crime",
            params={"api_key": API_KEY, "country": country}
        )
        resp.raise_for_status()
        data = resp.json()
        idx = data.get("index_safety")
        if idx is not None:
            return {"crime_index": (100 - float(idx))}
    except Exception:
        pass
    return {"crime_index": None}
