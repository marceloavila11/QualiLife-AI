import json
import unicodedata
import pycountry
import requests


def normalize_name(name: str) -> str:
    name = name.lower().strip()
    name = unicodedata.normalize("NFKD", name)
    return "".join(c for c in name if not unicodedata.combining(c))


def generate_country_mappings():
    url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    geo = requests.get(url).json()

    mapping = {}

    for f in geo["features"]:
        name = f["properties"]["name"]
        norm = normalize_name(name)

        iso = None

        try:
            c = pycountry.countries.search_fuzzy(name)[0]
            iso = c.alpha_3
        except Exception:
            pass

        mapping[norm] = iso

    return mapping


COUNTRY_MAPPING = generate_country_mappings()
