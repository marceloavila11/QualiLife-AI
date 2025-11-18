# services/data_sources/unesco_client.py
import requests


def get_education_data(country: str) -> dict:
    """
    Devuelve tasa de matrícula escolar total o alfabetización aproximada.
    Si no hay datos, devuelve un valor por defecto.
    """
    try:
        # Fuente: UNESCO SDMX API (UIS.Stat)
        # Ejemplo: Educación secundaria total (% de grupo etario)
        url = f"https://api.uis.unesco.org/sdmx/json/data/SE.SEC.ENRR.FE.ZS.{country}"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            # Lectura simple (podría variar por estructura de API real)
            value = (
                data.get("dataSets", [{}])[0]
                .get("observations", {})
                .get("0:0:0:0", [None])[0]
            )
            if value:
                return {"school_enrollment": float(value)}
    except Exception:
        pass
    # Valor por defecto aproximado
    return {"school_enrollment": 70.0}
