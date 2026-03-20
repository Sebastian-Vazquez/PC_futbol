#!/usr/bin/env python3
"""
PC FUTBOL 2026 - Scraper de plantillas desde Wikipedia
Fuente alternativa a Transfermarkt para equipos de 2ª división.
"""
import json
import os
import re
import sys
import time

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_SCRAPER_DIR = os.path.dirname(_THIS_DIR)
if _SCRAPER_DIR not in sys.path:
    sys.path.insert(0, _SCRAPER_DIR)

try:
    import requests
    from bs4 import BeautifulSoup
    _DEPS_OK = True
except ImportError:
    _DEPS_OK = False

_CACHE_DIR = os.path.join(_SCRAPER_DIR, "cache", "tm_squads")
_WIKI_API  = "https://en.wikipedia.org/w/api.php"
_HEADERS   = {"User-Agent": "PCFutbol2026/1.0 (educational game research)"}

# ── Mapeo Wikipedia page title → game team ID ───────────────────────────────
WIKI_TEAMS = {
    # Spain LaLiga Hypermotion (2ª)
    1021: "Real Zaragoza",
    1022: "SD Eibar",
    1023: "Sporting de Gijón",
    1024: "CD Tenerife",
    1025: "Racing de Santander",
    1026: "Málaga CF",
    1027: "Granada CF",
    1028: "Elche CF",
    1029: "UD Almería",
    1030: "Albacete Balompié",
    1031: "Levante UD",
    1032: "Cádiz CF",
    1033: "RC Deportivo de La Coruña",
    1034: "CD Castellón",
    1035: "FC Cartagena",
    1036: "SD Huesca",
    1037: "Real Oviedo",
    1038: "CD Mirandés",
    1039: "Racing de Ferrol",
    1041: "Eldense FC",

    # England Championship
    2021: "Sunderland A.F.C.",
    2022: "Leeds United F.C.",
    2023: "Burnley F.C.",
    2024: "Sheffield United F.C.",
    2025: "Middlesbrough F.C.",
    2026: "Coventry City F.C.",
    2027: "West Bromwich Albion F.C.",
    2028: "Millwall F.C.",
    2029: "Norwich City F.C.",
    2030: "Bristol City F.C.",
    2031: "Stoke City F.C.",
    2032: "Watford F.C.",
    2033: "Hull City A.F.C.",
    2034: "Swansea City A.F.C.",
    2035: "Preston North End F.C.",
    2036: "Blackburn Rovers F.C.",
    2037: "Queens Park Rangers F.C.",
    2038: "Cardiff City F.C.",
    2039: "Derby County F.C.",
    2040: "Sheffield Wednesday F.C.",
    2041: "Oxford United F.C.",
    2042: "Portsmouth F.C.",
    2043: "Plymouth Argyle F.C.",
    2044: "Luton Town F.C.",

    # Italy Serie B
    3021: "Palermo F.C.",
    3022: "Frosinone Calcio",
    3023: "US Catanzaro 1929",
    3024: "Spezia Calcio",
    3025: "SSC Bari",
    3026: "AC Reggiana 1919",
    3027: "U.C. Sampdoria",
    3028: "US Cremonese",
    3029: "AC Pisa 1909",
    3030: "Cesena F.C.",
    3031: "Modena F.C. 2018",
    3032: "Brescia Calcio",
    3033: "AS Cittadella",
    3034: "FC Südtirol",
    3035: "SS Juve Stabia",
    3036: "Cosenza Calcio",
    3037: "US Salernitana 1919",
    3038: "Carrarese Calcio",
    3039: "Mantova 1911",

    # Germany 2. Bundesliga
    4019: "Hamburger SV",
    4020: "Fortuna Düsseldorf",
    4021: "Karlsruher SC",
    4022: "SV Darmstadt 98",
    4024: "SpVgg Greuther Fürth",
    4025: "FC Schalke 04",
    4026: "Hannover 96",
    4027: "Eintracht Braunschweig",
    4028: "1. FC Nürnberg",
    4029: "SSV Jahn Regensburg",
    4030: "SV 07 Elversberg",
    4031: "SC Paderborn 07",
    4032: "1. FC Magdeburg",
    4033: "Hertha BSC",
    4034: "Preußen Münster",
    4035: "SSV Ulm 1846",

    # France Ligue 2
    5019: "Paris FC",
    5020: "SM Caen",
    5021: "Amiens SC",
    5022: "Grenoble Foot 38",
    5023: "Rodez AF",
    5024: "Pau FC",
    5026: "Stade Lavallois Mayenne FC",
    5027: "USL Dunkerque",
    5028: "ES Troyes AC",
    5029: "EA Guingamp",
    5031: "AC Ajaccio",
    5032: "FC Metz",
    5033: "FC Lorient",
    5034: "Clermont Foot 63",
    5035: "Red Star F.C.",
    5036: "SC Bastia",
    5037: "FC Martigues",

    # Argentina Primera Nacional
    6028: "Club Atlético Atlanta",
    6029: "Quilmes Atlético Club",
    6030: "All Boys",
    6032: "Ferro Carril Oeste",
    6033: "Defensores de Belgrano",
    6034: "Club Atlético Brown de Adrogué",
    6035: "Deportivo Morón",
    6036: "Club Atlético San Martín (Tucumán)",
    6038: "Nueva Chicago",
    6040: "Club Sportivo Independiente Rivadavia",
    6042: "Club Almagro",
    6048: "Temperley",
    6052: "Club Atlético San Martín (San Juan)",
}

# ── Mapeo de posiciones Wikipedia → juego ───────────────────────────────────
# Wikipedia usa: GK, DF, MF, FW
# Asignamos posiciones distribuyendo por número de jugadores típicos por posición
_POS_DIST = {
    "GK": ["PO", "PO", "PO"],
    "DF": ["DFC", "DFC", "LD", "LI", "DFC", "DFC", "LD", "LI"],
    "MF": ["MCD", "MC", "MC", "MCO", "MCD", "MC", "ED", "EI", "MC", "MCO"],
    "FW": ["DC", "ED", "EI", "DC", "DC"],
}
_pos_counters = {}

def _reset_pos_counters():
    global _pos_counters
    _pos_counters = {"GK": 0, "DF": 0, "MF": 0, "FW": 0}

def _mapear_pos(wiki_pos: str) -> str:
    key = wiki_pos.strip().upper()[:2]
    if key not in _POS_DIST:
        key = "MF"
    dist = _POS_DIST[key]
    idx = _pos_counters.get(key, 0)
    _pos_counters[key] = idx + 1
    return dist[idx % len(dist)]

# ── Mapeo de nacionalidades Wikipedia (FIFA/ISO) → nuestro código ───────────
_NAC_MAP = {
    "ENG": "ENG", "WAL": "WAL", "SCO": "SCO", "NIR": "IRL", "IRL": "IRL",
    "ESP": "ESP", "FRA": "FRA", "GER": "GER", "ITA": "ITA", "POR": "POR",
    "NED": "NED", "BEL": "BEL", "BRA": "BRA", "ARG": "ARG", "URU": "URU",
    "COL": "COL", "CHI": "CHI", "PER": "PER", "PAR": "PAR", "ECU": "ECU",
    "SWE": "SWE", "NOR": "NOR", "DEN": "DNK", "DNK": "DNK",
    "CZE": "CZE", "SVK": "SVK", "POL": "POL", "HUN": "HUN",
    "ROU": "ROU", "SRB": "SRB", "CRO": "CRO", "SVN": "SVN",
    "UKR": "UKR", "RUS": "RUS", "GRE": "GRE", "TUR": "TUR",
    "AUT": "AUT", "CHE": "CHE", "ISR": "ISR", "USA": "USA",
    "MEX": "MEX", "JAM": "JAM", "TRI": "TRI", "SEN": "SEN",
    "CMR": "CMR", "CIV": "CIV", "GHA": "GHA", "NGA": "NGA",
    "MAR": "MAR", "ALG": "ALG", "TUN": "TUN", "EGY": "EGY",
    "JPN": "JPN", "KOR": "KOR", "AUS": "AUS", "NZL": "NZL",
    "ISL": "ISL", "FIN": "FIN", "MKD": "MKD", "ALB": "ALB",
    "BIH": "BIH", "MNE": "MNE", "BGR": "BGR", "BUL": "BGR",
    "GEO": "GEO", "ARM": "ARM", "AZE": "AZE",
    "CAP": "CPV", "CPV": "CPV", "MLI": "MLI", "BFA": "BFA",
    "SLE": "SLE", "GIN": "GIN", "COD": "COD", "COG": "COG",
    "ZIM": "ZIM", "ZAM": "ZAM", "ANG": "ANG", "MOZ": "MOZ",
    "ERI": "ERI", "ETH": "ETH", "TAN": "TAN",
    "CAN": "CAN", "HON": "HON", "GTM": "GTM", "CRC": "CRC",
    "PAN": "PAN", "CUB": "CUB", "DOM": "DOM", "HTI": "HTI",
    "BOL": "BOL", "VEN": "VEN",
    "LUX": "LUX", "AND": "AND", "GIB": "GIB",
}

def _mapear_nac(wiki_nat: str) -> str:
    code = wiki_nat.strip().upper()
    return _NAC_MAP.get(code, "ESP")

# ── Funciones de scraping Wikipedia ─────────────────────────────────────────

def _get_squad_section_idx(page_title: str) -> str | None:
    """Busca el índice de la sección 'Squad' en la página Wikipedia."""
    params = {
        "action": "parse", "page": page_title,
        "prop": "sections", "format": "json"
    }
    try:
        r = requests.get(_WIKI_API, params=params, headers=_HEADERS, timeout=15)
        data = r.json()
        if "parse" not in data:
            return None
        for sec in data["parse"]["sections"]:
            line = sec.get("line", "").lower()
            if any(kw in line for kw in ("squad", "first-team", "players", "plantilla", "kader", "effectif", "rosa")):
                return sec["index"]
        return None
    except Exception:
        return None


def _parse_squad_html(html: str) -> list:
    """Extrae jugadores de la tabla de plantilla Wikipedia."""
    soup = BeautifulSoup(html, "html.parser")
    _reset_pos_counters()
    players = []

    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        if len(rows) < 5:
            continue

        for row in rows[1:]:
            tds = row.find_all("td")
            if len(tds) < 3:
                continue

            # Buscar posición (GK/DF/MF/FW) en alguna celda
            pos_td = None
            name_td = None
            nat_code = "ESP"

            for i, td in enumerate(tds):
                txt = td.get_text(strip=True)
                if txt.upper() in ("GK", "DF", "MF", "FW"):
                    pos_td = txt.upper()
                    # La celda siguiente suele tener la bandera/nación
                    # Buscar el código de nación
                    span = td.find_next_sibling("td")
                    if span:
                        img = span.find("img")
                        if img:
                            alt = img.get("alt", "") or img.get("title", "")
                            # Extraer código de país del alt text
                            m = re.search(r'\b([A-Z]{3})\b', alt)
                            if m:
                                nat_code = m.group(1)
                    break

            if pos_td is None:
                continue

            # Nombre: buscar link a jugador en la fila
            for td in tds:
                link = td.find("a", href=re.compile(r"/wiki/"))
                if link:
                    name_txt = link.get_text(strip=True)
                    if len(name_txt) > 2 and not name_txt.startswith("("):
                        name_td = name_txt
                        # También buscar imagen de bandera en la fila
                        imgs = td.find_all_previous("td", limit=2)
                        for prev in imgs:
                            img = prev.find("img")
                            if img:
                                alt = img.get("alt", "") or img.get("title", "")
                                m = re.search(r'\b([A-Z]{3})\b', alt)
                                if m:
                                    nat_code = m.group(1)
                        break

            if not name_td:
                continue

            # Separar nombre y apellido
            parts = name_td.strip().split()
            if len(parts) == 0:
                continue
            elif len(parts) == 1:
                nombre, apellido = parts[0], parts[0]
            else:
                nombre = parts[0]
                apellido = " ".join(parts[1:])

            nombre_corto = f"{nombre[0]}. {apellido[:10]}" if len(nombre) > 0 else apellido[:12]

            posicion = _mapear_pos(pos_td)
            nacionalidad = _mapear_nac(nat_code)

            players.append({
                "nombre": nombre,
                "apellido": apellido,
                "nombre_corto": nombre_corto,
                "fecha_nacimiento": "1996-06-15",  # placeholder
                "nacionalidad": nacionalidad,
                "posicion_principal": posicion,
                "valor_mercado_real": 2_000_000,   # placeholder mid-range
                "calidad": 0.45,
            })

        if len(players) >= 15:
            break

    return players


def _descargar_squad_wiki(page_title: str) -> list | None:
    """Descarga y parsea el squad de una página Wikipedia."""
    section_idx = _get_squad_section_idx(page_title)
    if section_idx is None:
        # Intentar con la página entera
        params = {
            "action": "parse", "page": page_title,
            "prop": "text", "format": "json"
        }
    else:
        params = {
            "action": "parse", "page": page_title,
            "prop": "text", "section": section_idx, "format": "json"
        }

    try:
        r = requests.get(_WIKI_API, params=params, headers=_HEADERS, timeout=20)
        data = r.json()
        if "parse" not in data:
            return None
        html = data["parse"]["text"]["*"]
        players = _parse_squad_html(html)
        return players if players else None
    except Exception as e:
        print(f"  [WIKI] Error: {e}")
        return None


def _cache_path(equipo_id: int) -> str:
    return os.path.join(_CACHE_DIR, f"{equipo_id}.json")


def _escribir_cache(equipo_id: int, datos: list):
    os.makedirs(_CACHE_DIR, exist_ok=True)
    with open(_cache_path(equipo_id), "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


def descargar_squads_wiki(forzar: bool = False):
    """Descarga squads desde Wikipedia para todos los equipos de 2ª división."""
    if not _DEPS_OK:
        print("[WIKI] requests/beautifulsoup4 no disponibles")
        return

    total = len(WIKI_TEAMS)
    ok = 0
    fallo = 0

    for i, (eid, page_title) in enumerate(WIKI_TEAMS.items()):
        cache_file = _cache_path(eid)
        if not forzar and os.path.exists(cache_file):
            print(f"  [{i+1}/{total}] Equipo {eid} ({page_title[:30]})... [CACHE]")
            ok += 1
            continue

        print(f"  [{i+1}/{total}] Equipo {eid} ({page_title[:30]})...", end="", flush=True)
        squad = _descargar_squad_wiki(page_title)
        if squad and len(squad) >= 10:
            _escribir_cache(eid, squad)
            print(f" OK ({len(squad)} jugadores)")
            ok += 1
        else:
            print(f" FALLO ({len(squad) if squad else 0} jugadores)")
            fallo += 1

        if i < total - 1:
            time.sleep(1.0)  # Wikipedia pide ~1s entre requests

    print(f"\n[WIKI] Resumen: {ok} OK, {fallo} fallidos de {total}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--forzar", action="store_true")
    args = parser.parse_args()
    descargar_squads_wiki(forzar=args.forzar)
