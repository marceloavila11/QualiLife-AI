# services/data_sources/itu_client.py
import requests


def get_connectivity_data(country_code: str) -> dict:
    """
    Recupera datos de conectividad desde la ITU.
    Incluye porcentaje de usuarios de Internet y suscripciones móviles.
    """
    try:
        url_internet = f"https://api.itu.int/statistics/ICT_INTERNET_USER?country={country_code}"
        url_mobile = f"https://api.itu.int/statistics/MOBILE_SUBSCRIPTIONS?country={country_code}"

        internet = None
        mobile = None

        resp_internet = requests.get(url_internet, timeout=10)
        resp_mobile = requests.get(url_mobile, timeout=10)

        if resp_internet.status_code == 200:
            internet = resp_internet.json().get("value", 60)
        if resp_mobile.status_code == 200:
            mobile = resp_mobile.json().get("value", 100)

        return {
            "internet_users": float(internet or 60),
            "mobile_subscriptions": float(mobile or 100)
        }
    except Exception:
        return {"internet_users": 60.0, "mobile_subscriptions": 100.0}
