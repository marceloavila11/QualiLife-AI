# services/data_sources/world_bank_client.py
import requests
from typing import Optional

BASE_URL = "https://api.worldbank.org/v2"


def get_indicator_latest(country_code: str, indicator: str) -> Optional[float]:
    """
    Obtiene el valor más reciente disponible para un indicador específico del World Bank.
    """
    url = f"{BASE_URL}/country/{country_code}/indicator/{indicator}?format=json&per_page=20"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list) and len(data) > 1 and isinstance(data[1], list):
            for rec in data[1]:
                if rec.get("value") is not None:
                    return float(rec["value"])
    except Exception:
        return None
    return None


def get_worldbank_data(country_code: str) -> dict:
    return {
        "gdp_per_capita_ppp": get_indicator_latest(country_code, "NY.GDP.PCAP.PP.KD"),
        "life_expectancy": get_indicator_latest(country_code, "SP.DYN.LE00.IN"),
        "internet_users_percent": get_indicator_latest(country_code, "IT.NET.USER.ZS"),
    }
