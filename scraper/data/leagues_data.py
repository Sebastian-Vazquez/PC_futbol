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

    # ═══════ OTROS ═══════
    7:   {"nombre": "Série A",                    "pais": "BRA", "tier": 1, "finanzas_factor": 0.12, "descensos": 4, "plazas_champions": 0, "plazas_europa": 4, "num_equipos": 20},
    8:   {"nombre": "Liga MX",                    "pais": "MEX", "tier": 1, "finanzas_factor": 0.15, "descensos": 0, "plazas_champions": 0, "plazas_europa": 0, "num_equipos": 18},
    9:   {"nombre": "Eredivisie",                 "pais": "NED", "tier": 1, "finanzas_factor": 0.20, "descensos": 2, "plazas_champions": 2, "plazas_europa": 2, "num_equipos": 18},
    10:  {"nombre": "Primeira Liga",              "pais": "POR", "tier": 1, "finanzas_factor": 0.18, "descensos": 3, "plazas_champions": 2, "plazas_europa": 2, "num_equipos": 18},
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
    # Europa
    {"id": 9001, "nombre": "UEFA Champions League", "pais": "EUR", "tipo": "champions",         "participantes": "clasificados"},
    {"id": 9002, "nombre": "UEFA Europa League",    "pais": "EUR", "tipo": "europa_league",     "participantes": "clasificados"},
    {"id": 9003, "nombre": "UEFA Conference League","pais": "EUR", "tipo": "conference",        "participantes": "clasificados"},
    # Sudamérica
    {"id": 9101, "nombre": "Copa Libertadores",     "pais": "SAM", "tipo": "libertadores",      "participantes": "clasificados"},
    {"id": 9102, "nombre": "Copa Sudamericana",     "pais": "SAM", "tipo": "sudamericana",      "participantes": "clasificados"},
]
