# services/data_sources/climate_client.py
import requests


def get_climate_data(country_code: str) -> dict:
    """
    Usa indicadores de emisiones de CO2 y energía renovable del World Bank.
    Normaliza para evaluar sostenibilidad ambiental.
    """
    try:
        url_co2 = f"https://api.worldbank.org/v2/country/{country_code}/indicator/EN.ATM.CO2E.PC?format=json"
        url_renew = f"https://api.worldbank.org/v2/country/{country_code}/indicator/EG.FEC.RNEW.ZS?format=json"
        co2_data = requests.get(url_co2, timeout=10).json()
        renew_data = requests.get(url_renew, timeout=10).json()

        co2 = None
        renew = None
        if isinstance(co2_data, list) and len(co2_data) > 1:
            for r in co2_data[1]:
                if r.get("value"):
                    co2 = float(r["value"])
                    break
        if isinstance(renew_data, list) and len(renew_data) > 1:
            for r in renew_data[1]:
                if r.get("value"):
                    renew = float(r["value"])
                    break

        return {
            "co2_per_capita": co2 or 3.0,
            "renewables_percent": renew or 10.0,
        }
    except Exception:
        return {"co2_per_capita": 3.0, "renewables_percent": 10.0}
