"""
Descargador de historial H2H real desde football-data.co.uk
Fuente: https://www.football-data.co.uk/data.php
Cobertura: England (5 divs), Spain (2), Italy (2), Germany (2), France (2),
           Scotland, Belgium, Turkey, Greece.

CSV columns relevantes: HomeTeam, AwayTeam, FTHG, FTAG (full-time goals).
"""

import csv
import io
import time
import requests

# ─── Ligas disponibles en football-data.co.uk ──────────────────────────────
# Formato: (codigo_csv, liga_id_juego, primera_temporada_YY)
LIGAS_FD = [
    # Inglaterra
    ("E0",  2,   93),   # Premier League — desde 93/94
    ("E1",  201, 4),    # Championship — desde 04/05
    ("E2",  202, 4),    # League One
    ("E3",  203, 4),    # League Two
    ("EC",  204, 5),    # National League
    # España
    ("SP1", 1,   93),   # LaLiga
    ("SP2", 101, 99),   # LaLiga Hypermotion
    # Italia
    ("I1",  3,   93),   # Serie A
    ("I2",  301, 4),    # Serie B — desde 04/05 (antes de eso datos incompletos)
    # Alemania
    ("D1",  4,   93),   # Bundesliga
    ("D2",  401, 4),    # 2. Bundesliga
    # Francia
    ("F1",  5,   93),   # Ligue 1
    ("F2",  501, 4),    # Ligue 2
    # Otros
    ("B1",  20,  95),   # Belgian Pro League
    ("T1",  19,  93),   # Süper Lig
    ("G1",  27,  94),   # Super League Greece
    ("SC0", 22,  93),   # Scottish Premiership
]

# ─── Mapeo nombre CSV → ID de equipo en el juego ──────────────────────────
# IDs verificados contra teams_england.py, teams_spain.py,
# teams_germany_italy_france.py, teams_international.py
NOMBRE_A_ID = {

    # ══════════════════ ESPAÑA ══════════════════
    # LaLiga — IDs 1001-1020
    "Real Madrid":         1001,
    "Barcelona":           1002,
    "Ath Madrid":          1003,   # nombre en football-data.co.uk
    "Atletico Madrid":     1003,
    "Atl. Madrid":         1003,
    "Atletico de Madrid":  1003,
    "Sociedad":            1004,   # nombre en football-data.co.uk
    "Real Sociedad":       1004,
    "Ath Bilbao":          1005,   # nombre en football-data.co.uk
    "Athletic Club":       1005,
    "Athletic Bilbao":     1005,
    "Villarreal":          1006,
    "Betis":               1007,
    "Real Betis":          1007,
    "Sevilla":             1008,
    "Valencia":            1009,
    "Girona":              1010,
    "Vallecano":           1011,   # nombre en football-data.co.uk
    "Rayo Vallecano":      1011,
    "Celta":               1012,   # nombre en football-data.co.uk
    "Celta Vigo":          1012,
    "Celta de Vigo":       1012,
    "Getafe":              1013,
    "Alaves":              1014,
    "Deportivo Alaves":    1014,
    "Mallorca":            1015,
    "Las Palmas":          1016,
    "Leganes":             1017,
    "Valladolid":          1018,
    "Real Valladolid":     1018,
    "Espanol":             1019,
    "Espanyol":            1019,
    "Osasuna":             1020,

    # LaLiga Hypermotion — IDs 1021-1042
    "Zaragoza":            1021,
    "Real Zaragoza":       1021,
    "Eibar":               1022,
    "Sp Gijon":            1023,   # nombre en football-data.co.uk
    "Sporting Gijon":      1023,
    "Tenerife":            1024,
    "Santander":           1025,   # nombre en football-data.co.uk
    "Racing Santander":    1025,
    "Malaga":              1026,
    "Granada":             1027,
    "Granada CF":          1027,
    "Elche":               1028,
    "Almeria":             1029,
    "Albacete":            1030,
    "Levante":             1031,
    "Cadiz":               1032,
    "Dep. La Coruna":      1033,
    "La Coruna":           1033,
    "Deportivo La Coruna": 1033,
    "Deportivo":           1033,
    "Castellon":           1034,
    "Cartagena":           1035,   # nombre en football-data.co.uk
    "FC Cartagena":        1035,
    "Huesca":              1036,
    "Oviedo":              1037,
    "Real Oviedo":         1037,
    "Mirandes":            1038,   # nombre en football-data.co.uk
    "Ferrol":              1039,   # nombre en football-data.co.uk
    "Ponferradina":        1040,
    "Eldense":             1041,   # nombre en football-data.co.uk
    "Eldense FC":          1041,
    "R. Murcia":           1042,
    # Segunda RFEF — IDs en juego pero raramente en football-data
    "Alcorcon":            1093,   # nombre en football-data.co.uk (SP2)
    "Fuenlabrada":         1092,
    "Amorebieta":          1048,   # nombre en football-data.co.uk
    "Andorra":             1120,   # nombre en football-data.co.uk
    "Burgos":              1061,   # nombre en football-data.co.uk
    "Villarreal B":        1067,   # nombre en football-data.co.uk

    # ══════════════════ INGLATERRA ══════════════════
    # Premier League — IDs 2001-2020
    "Man City":            2001,
    "Manchester City":     2001,
    "Arsenal":             2002,
    "Liverpool":           2003,
    "Chelsea":             2004,
    "Tottenham":           2005,
    "Tottenham Hotspur":   2005,
    "Man United":          2006,
    "Manchester United":   2006,
    "Newcastle":           2007,
    "Newcastle United":    2007,
    "Aston Villa":         2008,
    "West Ham":            2009,
    "West Ham United":     2009,
    "Brighton":            2010,
    "Brighton & Hove Albion": 2010,
    "Wolves":              2011,
    "Wolverhampton":       2011,
    "Wolverhampton Wanderers": 2011,
    "Fulham":              2012,
    "Brentford":           2013,
    "Crystal Palace":      2014,
    "C. Palace":           2014,
    "Everton":             2015,
    "Nottm Forest":        2016,
    "Nott'm Forest":       2016,   # nombre en football-data.co.uk
    "Nottingham Forest":   2016,
    "Bournemouth":         2017,
    "Ipswich":             2018,
    "Ipswich Town":        2018,
    "Leicester":           2019,
    "Leicester City":      2019,
    "Southampton":         2020,

    # Championship — IDs 2021-2044
    "Sunderland":          2021,
    "Leeds":               2022,
    "Leeds United":        2022,
    "Burnley":             2023,
    "Sheffield United":    2024,
    "Sheffield Utd":       2024,
    "Middlesbrough":       2025,
    "Boro":                2025,
    "Coventry":            2026,
    "Coventry City":       2026,
    "West Brom":           2027,
    "West Bromwich Albion":2027,
    "Millwall":            2028,
    "Norwich":             2029,
    "Norwich City":        2029,
    "Bristol City":        2030,
    "Stoke":               2031,
    "Stoke City":          2031,
    "Watford":             2032,
    "Hull":                2033,
    "Hull City":           2033,
    "Swansea":             2034,
    "Swansea City":        2034,
    "Preston":             2035,
    "Preston North End":   2035,
    "Blackburn":           2036,
    "Blackburn Rovers":    2036,
    "QPR":                 2037,
    "Queens Park Rangers": 2037,
    "Cardiff":             2038,
    "Cardiff City":        2038,
    "Derby":               2039,
    "Derby County":        2039,
    "Sheffield Weds":      2040,
    "Sheffield Wednesday": 2040,
    "Oxford":              2041,
    "Oxford United":       2041,
    "Portsmouth":          2042,
    "Plymouth":            2043,
    "Plymouth Argyle":     2043,
    "Luton":               2044,
    "Luton Town":          2044,
    # Otros equipos históricos del Championship
    "Huddersfield":        2051,
    "Huddersfield Town":   2051,
    "Blackpool":           2057,
    "Rotherham":           2042,
    "Rotherham United":    2042,

    # League One — IDs 2045+
    "Birmingham":          2045,
    "Birmingham City":     2045,
    "Wrexham":             2046,
    "Stockport":           2047,
    "Stockport County":    2047,
    "Charlton":            2048,
    "Charlton Athletic":   2048,
    "Wigan":               2049,
    "Wigan Athletic":      2049,
    "Peterborough":        2050,
    "Peterboro":           2050,   # nombre en football-data.co.uk
    "Peterborough United": 2050,
    "Bolton":              2053,
    "Bolton Wanderers":    2053,
    "Exeter":              2054,
    "Exeter City":         2054,
    "Leyton Orient":       2055,
    "Lincoln":             2056,
    "Lincoln City":        2056,
    "Bristol Rvs":         2058,   # nombre en football-data.co.uk
    "Bristol Rovers":      2058,
    "Barnsley":            2052,
    "Cambridge":           2059,
    "Cambridge United":    2059,
    "Northampton":         2060,
    "Northampton Town":    2060,
    "Wycombe":             2063,
    "Wycombe Wanderers":   2063,
    "Burton":              2065,
    "Burton Albion":       2065,
    "Reading":             2052,
    "Shrewsbury":          2062,
    "Shrewsbury Town":     2062,

    # League Two / National League — IDs 2069+
    "Notts County":        2069,
    "Cheltenham":          2070,
    "Crewe":               2071,
    "Grimsby":             2072,
    "Newport County":      2073,
    "Newport":             2073,
    "Tranmere":            2074,
    "Gillingham":          2075,
    "Harrogate":           2076,
    "Morecambe":           2077,
    "Bradford":            2078,
    "Salford":             2079,
    "Swindon":             2080,
    # National League
    "Hartlepool":          2093,
    "Solihull":            2094,
    "Eastleigh":           2095,
    "Maidenhead":          2096,
    "Altrincham":          2097,
    "Gateshead":           2098,
    "Boreham Wood":        2099,
    "Woking":              2100,
    "Wealdstone":          2101,
    "Barnet":              2103,
    "York":                2104,

    # ══════════════════ ITALIA ══════════════════
    # Serie A — IDs 3001-3020
    "Juventus":            3001,
    "Inter":               3002,
    "Internazionale":      3002,
    "Milan":               3003,
    "AC Milan":            3003,
    "Napoli":              3004,
    "Roma":                3005,
    "AS Roma":             3005,
    "Lazio":               3006,
    "SS Lazio":            3006,
    "Atalanta":            3007,
    "Fiorentina":          3008,
    "Torino":              3009,
    "Bologna":             3010,
    "Udinese":             3011,
    "Monza":               3012,
    "Genoa":               3013,
    "Cagliari":            3014,
    "Sassuolo":            3015,
    "Verona":              3016,
    "Hellas Verona":       3016,
    "Empoli":              3017,
    "Frosinone":           3018,
    "Venezia":             3019,
    "Sampdoria":           3020,

    # Serie B — IDs 3021-3040
    "Palermo":             3021,
    "Catanzaro":           3023,
    "Spezia":              3024,
    "Bari":                3025,
    "Reggiana":            3026,
    "Cremonese":           3028,
    "Pisa":                3029,
    "Modena":              3031,
    "Brescia":             3032,
    "Cittadella":          3033,
    "Sudtirol":            3034,
    "Cosenza":             3036,
    "Salernitana":         3037,
    "Ascoli":              3040,

    # ══════════════════ ALEMANIA ══════════════════
    # Bundesliga — IDs 4001-4018
    "Bayern Munich":       4001,
    "Bayern":              4001,
    "Dortmund":            4002,
    "Borussia Dortmund":   4002,
    "Leverkusen":          4003,
    "Bayer Leverkusen":    4003,
    "RB Leipzig":          4004,
    "Leipzig":             4004,
    "Ein Frankfurt":       4005,   # nombre en football-data.co.uk
    "Eintracht Frankfurt": 4005,
    "Frankfurt":           4005,
    "Wolfsburg":           4006,
    "M'gladbach":          4007,   # nombre en football-data.co.uk
    "Gladbach":            4007,
    "Borussia Monchengladbach": 4007,
    "Freiburg":            4008,
    "SC Freiburg":         4008,
    "Hoffenheim":          4009,
    "TSG Hoffenheim":      4009,
    "Augsburg":            4010,
    "Werder Bremen":       4011,
    "Bremen":              4011,
    "Union Berlin":        4012,
    "Stuttgart":           4013,
    "VfB Stuttgart":       4013,
    "Bochum":              4014,
    "Mainz":               4015,
    "Mainz 05":            4015,
    "FC Koln":             4016,
    "Cologne":             4016,
    "Koln":                4016,
    "Heidenheim":          4017,

    # 2. Bundesliga — IDs 4019-4036
    "Hamburg":             4019,
    "Hamburger SV":        4019,
    "Fortuna Dusseldorf":  4020,
    "Karlsruhe":           4021,
    "Darmstadt":           4022,
    "St Pauli":            4023,
    "Greuther Furth":      4024,
    "Schalke 04":          4025,
    "Schalke":             4025,
    "Hannover":            4026,
    "Braunschweig":        4027,
    "Nurnberg":            4028,
    "Regensburg":          4029,
    "Elversberg":          4030,
    "Paderborn":           4031,
    "Magdeburg":           4032,
    "Hertha":              4033,
    "Hertha BSC":          4033,

    # ══════════════════ FRANCIA ══════════════════
    # Ligue 1 — IDs 5001-5018
    "Paris SG":            5001,
    "PSG":                 5001,
    "Paris Saint-Germain": 5001,
    "Marseille":           5002,
    "Lyon":                5003,
    "Monaco":              5004,
    "AS Monaco":           5004,
    "Lens":                5005,
    "RC Lens":             5005,
    "Lille":               5006,
    "Rennes":              5007,
    "Stade Rennais":       5007,
    "Nice":                5008,
    "OGC Nice":            5008,
    "Strasbourg":          5009,
    "Nantes":              5010,
    "Montpellier":         5011,
    "Toulouse":            5012,
    "Reims":               5013,
    "Brest":               5014,
    "Lorient":             5015,
    "Metz":                5016,
    "Clermont":            5017,
    "Clermont Foot":       5017,
    "Le Havre":            5018,

    # ══════════════════ BÉLGICA ══════════════════
    # Belgian Pro League — IDs 20001-20016
    "Club Brugge":         20001,
    "Anderlecht":          20002,
    "Gent":                20003,
    "KAA Gent":            20003,
    "Standard":            20004,
    "Standard Liege":      20004,
    "Genk":                20005,
    "KRC Genk":            20005,
    "St. Gilloise":        20006,   # Union Saint-Gilloise
    "Royale Union SG":     20006,
    "Antwerp":             20007,
    "Royal Antwerp":       20007,
    "Charleroi":           20008,
    "OH Leuven":           20009,
    "Oud-Heverlee Leuven": 20009,
    "Westerlo":            20010,
    "Cercle Brugge":       20011,
    "Mechelen":            20012,
    "KV Mechelen":         20012,
    "Kortrijk":            20013,
    "KV Kortrijk":         20013,
    "Eupen":               20014,
    "KAS Eupen":           20014,
    "Beerschot":           20015,
    "RWD Molenbeek":       20016,
    "RWDM":                20016,

    # ══════════════════ TURQUÍA ══════════════════
    # Süper Lig — IDs 19001-19019
    "Galatasaray":         19001,
    "Fenerbahce":          19002,
    "Besiktas":            19003,
    "Trabzonspor":         19004,
    "Basaksehir":          19005,
    "Istanbul Basaksehir": 19005,
    "Konyaspor":           19006,
    "Ad. Demirspor":       19007,   # nombre en football-data.co.uk
    "Adana Demirspor":     19007,
    "Kayserispor":         19008,
    "Kasimpasa":           19009,
    "Sivasspor":           19010,
    "Karagumruk":          19011,   # Fatih Karagümrük
    "Ankaragucu":          19012,
    "Ankaragücü":          19012,
    "Alanyaspor":          19013,
    "Gaziantep":           19014,
    "Gaziantepspor":       19014,
    "Hatayspor":           19015,
    "Rizespor":            19016,
    "Caykur Rizespor":     19016,
    "Istanbulspor":        19017,
    "Samsunspor":          19018,
    "Antalyaspor":         19019,

    # ══════════════════ GRECIA ══════════════════
    # Super League — IDs 27001-27014
    "Olympiakos":          27001,
    "Panathinaikos":       27002,
    "AEK":                 27003,
    "AEK Athens":          27003,
    "PAOK":                27004,
    "Aris":                27005,
    "OFI Crete":           27006,
    "Panetolikos":         27007,
    "Atromitos":           27008,
    "Asteras Tripolis":    27009,
    "Volos NFC":           27010,
    "Volos":               27010,
    "Lamia":               27011,
    "Panserraikos":        27012,
    "Giannina":            27014,
    "PAS Giannina":        27014,

    # ══════════════════ ESCOCIA ══════════════════
    # Scottish Premiership — IDs 22001-22012
    "Celtic":              22001,
    "Rangers":             22002,
    "Hearts":              22003,
    "Heart of Midlothian": 22003,
    "Aberdeen":            22004,
    "Hibs":                22005,
    "Hibernian":           22005,
    "Livingston":          22006,
    "Motherwell":          22007,
    "Ross County":         22008,
    "St Mirren":           22009,
    "St. Mirren":          22009,
    "Dundee":              22010,
    "Kilmarnock":          22011,
    "St Johnstone":        22012,
}


def _h2h_key(a: int, b: int) -> str:
    return f"{min(a, b)}_{max(a, b)}"


def _registrar(h2h: dict, ea: int, eb: int, ga: int, gb: int) -> None:
    key = _h2h_key(ea, eb)
    id_a = min(ea, eb)
    id_b = max(ea, eb)
    if key not in h2h:
        h2h[key] = {"id_a": id_a, "id_b": id_b,
                    "PJ": 0, "W_a": 0, "D": 0, "W_b": 0,
                    "GF_a": 0, "GC_a": 0}
    rec = h2h[key]
    g_a, g_b = (ga, gb) if ea == id_a else (gb, ga)
    rec["PJ"] += 1
    rec["GF_a"] += g_a
    rec["GC_a"] += g_b
    if   g_a > g_b: rec["W_a"] += 1
    elif g_a < g_b: rec["W_b"] += 1
    else:           rec["D"]   += 1


def _temporadas(desde_yy: int) -> list[str]:
    """Genera lista de códigos: '9394', '9495', ..., '2425'"""
    codes = []
    y = desde_yy
    while True:
        y1 = y % 100
        y2 = (y + 1) % 100
        codes.append(f"{y1:02d}{y2:02d}")
        if y >= 124:
            break
        y += 1
    return codes


def _descargar_csv(codigo: str, temporada: str, session: requests.Session) -> list[dict]:
    url = f"https://www.football-data.co.uk/mmz4281/{temporada}/{codigo}.csv"
    try:
        r = session.get(url, timeout=15)
        if r.status_code != 200:
            return []
        text = r.content.decode("latin-1")
        reader = csv.DictReader(io.StringIO(text))
        rows = []
        for row in reader:
            if row.get("FTHG") and row.get("FTAG") and row.get("HomeTeam") and row.get("AwayTeam"):
                try:
                    rows.append({
                        "home": row["HomeTeam"].strip(),
                        "away": row["AwayTeam"].strip(),
                        "hg": int(row["FTHG"]),
                        "ag": int(row["FTAG"]),
                    })
                except (ValueError, KeyError):
                    continue
        return rows
    except Exception:
        return []


def descargar_h2h_real(verbose: bool = True) -> dict:
    """
    Descarga todos los resultados históricos reales de football-data.co.uk
    y construye el diccionario H2H en el formato de LeagueSystem._h2h.
    """
    h2h: dict = {}
    session = requests.Session()
    session.headers["User-Agent"] = "PC-Futbol-2026-DataLoader/1.0"

    total_partidos = 0
    no_mapeados: set = set()

    for (codigo, liga_id, desde_yy) in LIGAS_FD:
        temporadas = _temporadas(desde_yy)
        partidos_liga = 0

        for temp in temporadas:
            filas = _descargar_csv(codigo, temp, session)
            for f in filas:
                id_h = NOMBRE_A_ID.get(f["home"])
                id_a = NOMBRE_A_ID.get(f["away"])
                if id_h and id_a and id_h != id_a:
                    _registrar(h2h, id_h, id_a, f["hg"], f["ag"])
                    partidos_liga += 1
                else:
                    if not id_h: no_mapeados.add(f["home"])
                    if not id_a: no_mapeados.add(f["away"])
            time.sleep(0.05)

        if verbose and partidos_liga > 0:
            print(f"  [{codigo}] liga_id={liga_id}: {partidos_liga:,} partidos reales")
        total_partidos += partidos_liga

    if verbose and no_mapeados:
        # Solo mostrar los que podrían ser equipos del juego
        print(f"\n  [INFO] {len(no_mapeados)} nombres sin mapear "
              f"(históricos o equipos no incluidos en el juego)")

    print(f"\n[H2H] TOTAL REAL: {len(h2h)} pares | {total_partidos:,} partidos históricos")
    return h2h
