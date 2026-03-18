# Definición completa de todas las ligas
# tier: nivel de la división (1=primera, 2=segunda, etc.)
# finanzas_factor: multiplier para presupuestos (1.0=primera división)

LIGAS_CONFIG = {
    # ═══════ ESPAÑA ═══════
    1:   {"nombre": "LaLiga",                    "pais": "ESP", "tier": 1, "finanzas_factor": 1.00, "descensos": 3, "plazas_champions": 4, "plazas_europa": 2, "num_equipos": 20},
    101: {"nombre": "LaLiga Hypermotion",         "pais": "ESP", "tier": 2, "finanzas_factor": 0.15, "descensos": 4, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 22},
    102: {"nombre": "Primera RFEF Grupo 1",       "pais": "ESP", "tier": 3, "finanzas_factor": 0.04, "descensos": 4, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 20},
    103: {"nombre": "Primera RFEF Grupo 2",       "pais": "ESP", "tier": 3, "finanzas_factor": 0.04, "descensos": 4, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 20},
    104: {"nombre": "Segunda RFEF Grupo 1",       "pais": "ESP", "tier": 4, "finanzas_factor": 0.01, "descensos": 4, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 18},
    105: {"nombre": "Segunda RFEF Grupo 2",       "pais": "ESP", "tier": 4, "finanzas_factor": 0.01, "descensos": 4, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 18},
    106: {"nombre": "Segunda RFEF Grupo 3",       "pais": "ESP", "tier": 4, "finanzas_factor": 0.01, "descensos": 4, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 18},
    107: {"nombre": "Segunda RFEF Grupo 4",       "pais": "ESP", "tier": 4, "finanzas_factor": 0.01, "descensos": 4, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 18},

    # ═══════ INGLATERRA ═══════
    2:   {"nombre": "Premier League",             "pais": "ENG", "tier": 1, "finanzas_factor": 1.20, "descensos": 3, "plazas_champions": 4, "plazas_europa": 2, "num_equipos": 20},
    201: {"nombre": "Championship",               "pais": "ENG", "tier": 2, "finanzas_factor": 0.18, "descensos": 3, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 24},
    202: {"nombre": "League One",                 "pais": "ENG", "tier": 3, "finanzas_factor": 0.05, "descensos": 4, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 24},
    203: {"nombre": "League Two",                 "pais": "ENG", "tier": 4, "finanzas_factor": 0.02, "descensos": 4, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 24},
    204: {"nombre": "National League",            "pais": "ENG", "tier": 5, "finanzas_factor": 0.008,"descensos": 4, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 24},
    205: {"nombre": "National League North",      "pais": "ENG", "tier": 6, "finanzas_factor": 0.003,"descensos": 4, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 22},
    206: {"nombre": "National League South",      "pais": "ENG", "tier": 6, "finanzas_factor": 0.003,"descensos": 4, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 22},

    # ═══════ ITALIA ═══════
    3:   {"nombre": "Serie A",                    "pais": "ITA", "tier": 1, "finanzas_factor": 0.90, "descensos": 3, "plazas_champions": 4, "plazas_europa": 2, "num_equipos": 20},
    301: {"nombre": "Serie B",                    "pais": "ITA", "tier": 2, "finanzas_factor": 0.12, "descensos": 4, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 20},
    302: {"nombre": "Serie C — Girone A",         "pais": "ITA", "tier": 3, "finanzas_factor": 0.03, "descensos": 4, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 20},
    303: {"nombre": "Serie C — Girone B",         "pais": "ITA", "tier": 3, "finanzas_factor": 0.03, "descensos": 4, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 20},
    304: {"nombre": "Serie C — Girone C",         "pais": "ITA", "tier": 3, "finanzas_factor": 0.03, "descensos": 4, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 20},
    305: {"nombre": "Serie D — Girone A",         "pais": "ITA", "tier": 4, "finanzas_factor": 0.008,"descensos": 4, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 18},
    306: {"nombre": "Serie D — Girone B",         "pais": "ITA", "tier": 4, "finanzas_factor": 0.008,"descensos": 4, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 18},
    307: {"nombre": "Serie D — Girone C",         "pais": "ITA", "tier": 4, "finanzas_factor": 0.008,"descensos": 4, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 18},

    # ═══════ ALEMANIA ═══════
    4:   {"nombre": "Bundesliga",                 "pais": "GER", "tier": 1, "finanzas_factor": 0.95, "descensos": 3, "plazas_champions": 4, "plazas_europa": 2, "num_equipos": 18},
    401: {"nombre": "2. Bundesliga",              "pais": "GER", "tier": 2, "finanzas_factor": 0.14, "descensos": 3, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 18},
    402: {"nombre": "3. Liga",                    "pais": "GER", "tier": 3, "finanzas_factor": 0.04, "descensos": 4, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 20},
    403: {"nombre": "Regionalliga Nord",          "pais": "GER", "tier": 4, "finanzas_factor": 0.01, "descensos": 4, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 18},
    404: {"nombre": "Regionalliga Nordost",       "pais": "GER", "tier": 4, "finanzas_factor": 0.01, "descensos": 4, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 18},
    405: {"nombre": "Regionalliga West",          "pais": "GER", "tier": 4, "finanzas_factor": 0.01, "descensos": 4, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 18},
    406: {"nombre": "Regionalliga Südwest",       "pais": "GER", "tier": 4, "finanzas_factor": 0.01, "descensos": 4, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 18},
    407: {"nombre": "Regionalliga Bayern",        "pais": "GER", "tier": 4, "finanzas_factor": 0.01, "descensos": 4, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 18},

    # ═══════ FRANCIA ═══════
    5:   {"nombre": "Ligue 1",                    "pais": "FRA", "tier": 1, "finanzas_factor": 0.80, "descensos": 3, "plazas_champions": 3, "plazas_europa": 2, "num_equipos": 18},
    501: {"nombre": "Ligue 2",                    "pais": "FRA", "tier": 2, "finanzas_factor": 0.10, "descensos": 3, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 20},
    502: {"nombre": "National",                   "pais": "FRA", "tier": 3, "finanzas_factor": 0.03, "descensos": 4, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 18},
    503: {"nombre": "National 2 Groupe A",        "pais": "FRA", "tier": 4, "finanzas_factor": 0.008,"descensos": 4, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 17},
    504: {"nombre": "National 2 Groupe B",        "pais": "FRA", "tier": 4, "finanzas_factor": 0.008,"descensos": 4, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 17},
    505: {"nombre": "National 2 Groupe C",        "pais": "FRA", "tier": 4, "finanzas_factor": 0.008,"descensos": 4, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 17},
    506: {"nombre": "National 2 Groupe D",        "pais": "FRA", "tier": 4, "finanzas_factor": 0.008,"descensos": 4, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 17},

    # ═══════ ARGENTINA ═══════
    6:   {"nombre": "Liga Profesional",           "pais": "ARG", "tier": 1, "finanzas_factor": 0.08, "descensos": 3, "plazas_champions": 0, "plazas_europa": 4, "num_equipos": 26},
    601: {"nombre": "Primera Nacional",           "pais": "ARG", "tier": 2, "finanzas_factor": 0.02, "descensos": 0, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 34},
    602: {"nombre": "Primera B Metropolitana",    "pais": "ARG", "tier": 3, "finanzas_factor": 0.005,"descensos": 3, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 16},
    603: {"nombre": "Torneo Federal A",           "pais": "ARG", "tier": 3, "finanzas_factor": 0.004,"descensos": 3, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 32},
    604: {"nombre": "Primera C",                  "pais": "ARG", "tier": 4, "finanzas_factor": 0.002,"descensos": 3, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 16},
    605: {"nombre": "Torneo Federal B",           "pais": "ARG", "tier": 4, "finanzas_factor": 0.001,"descensos": 3, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 32},
    606: {"nombre": "Primera D",                  "pais": "ARG", "tier": 5, "finanzas_factor": 0.001,"descensos": 3, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 16},

    # ═══════ OTROS (BRASIL, MEXICO, HOLANDA, PORTUGAL) ═══════
    7:   {"nombre": "Série A",                    "pais": "BRA", "tier": 1, "finanzas_factor": 0.12, "descensos": 4, "plazas_champions": 0, "plazas_europa": 4, "num_equipos": 20},
    8:   {"nombre": "Liga MX",                    "pais": "MEX", "tier": 1, "finanzas_factor": 0.15, "descensos": 0, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 18},
    9:   {"nombre": "Eredivisie",                 "pais": "NED", "tier": 1, "finanzas_factor": 0.20, "descensos": 2, "plazas_champions": 2, "plazas_europa": 2, "num_equipos": 18},
    10:  {"nombre": "Primeira Liga",              "pais": "POR", "tier": 1, "finanzas_factor": 0.18, "descensos": 3, "plazas_champions": 2, "plazas_europa": 2, "num_equipos": 18},

    # ═══════ INTERNACIONALES — Club World Cup / UCL / Copa Libertadores ═══════
    11:  {"nombre": "Saudi Pro League",           "pais": "SAU", "tier": 1, "finanzas_factor": 0.60, "descensos": 3, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 18},
    12:  {"nombre": "J1 League",                  "pais": "JPN", "tier": 1, "finanzas_factor": 0.12, "descensos": 3, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 18},
    13:  {"nombre": "K League 1",                 "pais": "KOR", "tier": 1, "finanzas_factor": 0.08, "descensos": 2, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 12},
    14:  {"nombre": "MLS",                        "pais": "USA", "tier": 1, "finanzas_factor": 0.25, "descensos": 0, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 29},
    15:  {"nombre": "A-League",                   "pais": "AUS", "tier": 1, "finanzas_factor": 0.08, "descensos": 0, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 12},
    16:  {"nombre": "Egyptian Premier League",    "pais": "EGY", "tier": 1, "finanzas_factor": 0.05, "descensos": 3, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 18},
    17:  {"nombre": "Botola Pro",                 "pais": "MAR", "tier": 1, "finanzas_factor": 0.04, "descensos": 3, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 16},
    18:  {"nombre": "Premier Soccer League",      "pais": "RSA", "tier": 1, "finanzas_factor": 0.04, "descensos": 3, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 16},
    19:  {"nombre": "Super Lig",                  "pais": "TUR", "tier": 1, "finanzas_factor": 0.35, "descensos": 3, "plazas_champions": 2, "plazas_europa": 2, "num_equipos": 19},
    20:  {"nombre": "Belgian Pro League",         "pais": "BEL", "tier": 1, "finanzas_factor": 0.25, "descensos": 3, "plazas_champions": 1, "plazas_europa": 2, "num_equipos": 16},
    21:  {"nombre": "Austrian Bundesliga",        "pais": "AUT", "tier": 1, "finanzas_factor": 0.22, "descensos": 3, "plazas_champions": 2, "plazas_europa": 1, "num_equipos": 12},
    22:  {"nombre": "Scottish Premiership",       "pais": "SCO", "tier": 1, "finanzas_factor": 0.18, "descensos": 3, "plazas_champions": 1, "plazas_europa": 2, "num_equipos": 12},
    23:  {"nombre": "Ukrainian Premier League",   "pais": "UKR", "tier": 1, "finanzas_factor": 0.15, "descensos": 3, "plazas_champions": 2, "plazas_europa": 1, "num_equipos": 16},
    24:  {"nombre": "Super League Switzerland",   "pais": "CHE", "tier": 1, "finanzas_factor": 0.25, "descensos": 2, "plazas_champions": 1, "plazas_europa": 1, "num_equipos": 10},
    25:  {"nombre": "Czech First League",         "pais": "CZE", "tier": 1, "finanzas_factor": 0.15, "descensos": 3, "plazas_champions": 1, "plazas_europa": 2, "num_equipos": 16},
    26:  {"nombre": "Serbian SuperLiga",          "pais": "SRB", "tier": 1, "finanzas_factor": 0.08, "descensos": 3, "plazas_champions": 1, "plazas_europa": 1, "num_equipos": 16},
    27:  {"nombre": "Super League Greece",        "pais": "GRE", "tier": 1, "finanzas_factor": 0.15, "descensos": 3, "plazas_champions": 1, "plazas_europa": 2, "num_equipos": 14},
    28:  {"nombre": "Danish Superliga",           "pais": "DNK", "tier": 1, "finanzas_factor": 0.18, "descensos": 3, "plazas_champions": 1, "plazas_europa": 1, "num_equipos": 14},
    29:  {"nombre": "Allsvenskan",                "pais": "SWE", "tier": 1, "finanzas_factor": 0.15, "descensos": 3, "plazas_champions": 1, "plazas_europa": 1, "num_equipos": 16},
    30:  {"nombre": "UAE Pro League",             "pais": "UAE", "tier": 1, "finanzas_factor": 0.30, "descensos": 3, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 14},
    31:  {"nombre": "Ligue Professionnelle 1",    "pais": "TUN", "tier": 1, "finanzas_factor": 0.04, "descensos": 3, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 14},
    32:  {"nombre": "NPFL Nigeria",               "pais": "NGA", "tier": 1, "finanzas_factor": 0.02, "descensos": 3, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 20},
    33:  {"nombre": "OFC Champions League",       "pais": "NZL", "tier": 1, "finanzas_factor": 0.01, "descensos": 0, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 8},
}

# Torneos/Copas
TORNEOS = [
    # España
    {"id": 1001, "nombre": "Copa del Rey",          "pais": "ESP", "tipo": "copa_eliminacion", "participantes": "todos"},
    {"id": 1002, "nombre": "Supercopa de España",   "pais": "ESP", "tipo": "supercopa",         "participantes": "top4"},
    # Inglaterra
    {"id": 2001, "nombre": "FA Cup",                "pais": "ENG", "tipo": "copa_eliminacion", "participantes": "todos"},
    {"id": 2002, "nombre": "EFL Cup",               "pais": "ENG", "tipo": "copa_eliminacion", "participantes": "profesional"},
    {"id": 2003, "nombre": "Community Shield",      "pais": "ENG", "tipo": "supercopa",         "participantes": "top2"},
    # Italia
    {"id": 3001, "nombre": "Coppa Italia",          "pais": "ITA", "tipo": "copa_eliminacion", "participantes": "profesional"},
    {"id": 3002, "nombre": "Supercoppa Italiana",   "pais": "ITA", "tipo": "supercopa",         "participantes": "top2"},
    # Alemania
    {"id": 4001, "nombre": "DFB-Pokal",             "pais": "GER", "tipo": "copa_eliminacion", "participantes": "todos"},
    {"id": 4002, "nombre": "DFL-Supercup",          "pais": "GER", "tipo": "supercopa",         "participantes": "top2"},
    # Francia
    {"id": 5001, "nombre": "Coupe de France",       "pais": "FRA", "tipo": "copa_eliminacion", "participantes": "todos"},
    {"id": 5002, "nombre": "Coupe de la Ligue",     "pais": "FRA", "tipo": "copa_eliminacion", "participantes": "profesional"},
    {"id": 5003, "nombre": "Trophée des Champions", "pais": "FRA", "tipo": "supercopa",         "participantes": "top2"},
    # Argentina
    {"id": 6001, "nombre": "Copa Argentina",        "pais": "ARG", "tipo": "copa_eliminacion", "participantes": "todos"},
    {"id": 6002, "nombre": "Copa de la Liga",       "pais": "ARG", "tipo": "copa_grupos",       "participantes": "primera"},
    {"id": 6003, "nombre": "Supercopa Argentina",   "pais": "ARG", "tipo": "supercopa",         "participantes": "top2"},
    # Europa — UEFA
    {"id": 9001, "nombre": "UEFA Champions League",  "pais": "EUR", "tipo": "champions",        "participantes": "clasificados", "cupos": 36,
     "cupos_pais": {"ESP": 4, "ENG": 4, "GER": 4, "ITA": 4, "FRA": 3, "NED": 2, "POR": 2, "TUR": 2, "BEL": 1, "AUT": 2, "SCO": 1, "UKR": 2, "CHE": 1, "CZE": 1, "SRB": 1, "GRE": 1, "DNK": 1, "SWE": 1}},
    {"id": 9002, "nombre": "UEFA Europa League",     "pais": "EUR", "tipo": "europa_league",    "participantes": "clasificados", "cupos": 36,
     "cupos_pais": {"ESP": 2, "ENG": 2, "GER": 2, "ITA": 2, "FRA": 2, "NED": 2, "POR": 2, "TUR": 2, "BEL": 2, "AUT": 1, "SCO": 2, "UKR": 1, "CHE": 1, "CZE": 2, "SRB": 1, "GRE": 2, "DNK": 1, "SWE": 1}},
    {"id": 9003, "nombre": "UEFA Conference League", "pais": "EUR", "tipo": "conference",       "participantes": "clasificados", "cupos": 36,
     "cupos_pais": {"ESP": 1, "ENG": 1, "GER": 1, "ITA": 1, "FRA": 1, "NED": 1, "POR": 1, "TUR": 1, "BEL": 1, "AUT": 1, "SCO": 1, "UKR": 1, "CHE": 1, "CZE": 1, "SRB": 1, "GRE": 1, "DNK": 1, "SWE": 1}},
    {"id": 9004, "nombre": "UEFA Super Cup",         "pais": "EUR", "tipo": "supercopa",        "participantes": "campeones_uefa"},
    # Sudamérica — CONMEBOL
    {"id": 9101, "nombre": "Copa Libertadores",      "pais": "SAM", "tipo": "libertadores",     "participantes": "clasificados", "cupos": 32,
     "cupos_pais": {"ARG": 6, "BRA": 8, "URU": 3, "CHL": 3, "COL": 3, "ECU": 2, "PER": 2, "BOL": 2, "PAR": 2, "VEN": 1}},
    {"id": 9102, "nombre": "Copa Sudamericana",      "pais": "SAM", "tipo": "sudamericana",     "participantes": "clasificados", "cupos": 32,
     "cupos_pais": {"ARG": 5, "BRA": 5, "URU": 2, "CHL": 2, "COL": 2, "ECU": 2, "PER": 2, "BOL": 2, "PAR": 2, "VEN": 2}},
    {"id": 9103, "nombre": "Recopa Sudamericana",    "pais": "SAM", "tipo": "supercopa",        "participantes": "campeones_sam"},
    # CONCACAF
    {"id": 9201, "nombre": "CONCACAF Champions Cup", "pais": "CONCACAF", "tipo": "champions",  "participantes": "clasificados", "cupos": 27,
     "cupos_pais": {"USA": 7, "MEX": 7, "CAN": 3, "CRC": 1, "HON": 1, "JAM": 1, "GTM": 1, "SLV": 1, "TRI": 1, "PAN": 1}},
    {"id": 9202, "nombre": "CONCACAF League",        "pais": "CONCACAF", "tipo": "copa",       "participantes": "clasificados", "cupos": 22},
    # África — CAF
    {"id": 9301, "nombre": "CAF Champions League",   "pais": "AFR", "tipo": "champions",       "participantes": "clasificados", "cupos": 16,
     "cupos_pais": {"EGY": 2, "MAR": 2, "RSA": 2, "TUN": 2, "NGA": 2, "CMR": 1, "SEN": 1, "CIV": 1, "GHA": 1}},
    {"id": 9302, "nombre": "CAF Confederation Cup",  "pais": "AFR", "tipo": "europa_league",   "participantes": "clasificados", "cupos": 16},
    {"id": 9303, "nombre": "CAF Super Cup",           "pais": "AFR", "tipo": "supercopa",       "participantes": "campeones_caf"},
    # Asia — AFC
    {"id": 9401, "nombre": "AFC Champions League Elite","pais": "ASI", "tipo": "champions",    "participantes": "clasificados", "cupos": 24,
     "cupos_pais": {"SAU": 4, "JPN": 4, "KOR": 4, "UAE": 2, "CHN": 2, "IRN": 2, "AUS": 2, "IRQ": 2, "UZB": 1, "IDN": 1}},
    {"id": 9402, "nombre": "AFC Champions League Two","pais": "ASI", "tipo": "europa_league",  "participantes": "clasificados", "cupos": 24},
    # Mundial — FIFA
    {"id": 9501, "nombre": "FIFA Club World Cup",    "pais": "FIFA", "tipo": "mundial_clubes",  "participantes": "clasificados", "cupos": 32,
     "cupos_confederacion": {"UEFA": 12, "CONMEBOL": 6, "CONCACAF": 4, "AFC": 4, "CAF": 4, "OFC": 1, "HOST": 1}},
    {"id": 9502, "nombre": "FIFA Intercontinental Cup","pais": "FIFA", "tipo": "intercontinental","participantes": "campeones"},
    # Selecciones (datos de referencia)
    {"id": 9601, "nombre": "UEFA Euro",              "pais": "EUR", "tipo": "selecciones",     "participantes": "selecciones_uefa", "cupos": 24},
    {"id": 9602, "nombre": "Copa America",           "pais": "SAM", "tipo": "selecciones",     "participantes": "selecciones_conmebol", "cupos": 16},
    {"id": 9603, "nombre": "FIFA World Cup",         "pais": "FIFA", "tipo": "selecciones",    "participantes": "clasificadas", "cupos": 48},
    {"id": 9604, "nombre": "CONCACAF Gold Cup",      "pais": "CONCACAF", "tipo": "selecciones","participantes": "clasificadas", "cupos": 16},
    {"id": 9605, "nombre": "Africa Cup of Nations",  "pais": "AFR", "tipo": "selecciones",     "participantes": "clasificadas", "cupos": 24},
    {"id": 9606, "nombre": "AFC Asian Cup",          "pais": "ASI", "tipo": "selecciones",     "participantes": "clasificadas", "cupos": 24},
]
