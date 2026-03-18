import os

# Ruta de salida de los JSONs (relativa a este script)
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "pc-futbol-2026", "data", "initial")

# Temporada actual
TEMPORADA = "2025-26"
ANIO_INICIO = 2025

# Ligas a generar
LIGAS = [
    {"id": 1,  "nombre": "LaLiga",          "pais": "ESP", "nivel": 1, "plazas_champions": 4, "plazas_europa": 2, "descensos": 3},
    {"id": 2,  "nombre": "Premier League",  "pais": "ENG", "nivel": 1, "plazas_champions": 4, "plazas_europa": 2, "descensos": 3},
    {"id": 3,  "nombre": "Serie A",         "pais": "ITA", "nivel": 1, "plazas_champions": 4, "plazas_europa": 2, "descensos": 3},
    {"id": 4,  "nombre": "Bundesliga",      "pais": "GER", "nivel": 1, "plazas_champions": 4, "plazas_europa": 2, "descensos": 3},
    {"id": 5,  "nombre": "Ligue 1",         "pais": "FRA", "nivel": 1, "plazas_champions": 3, "plazas_europa": 2, "descensos": 3},
    {"id": 6,  "nombre": "Liga Profesional","pais": "ARG", "nivel": 1, "plazas_champions": 0, "plazas_europa": 4, "descensos": 3},
    {"id": 7,  "nombre": "Série A",         "pais": "BRA", "nivel": 1, "plazas_champions": 0, "plazas_europa": 4, "descensos": 4},
    {"id": 8,  "nombre": "Liga MX",         "pais": "MEX", "nivel": 1, "plazas_champions": 0, "plazas_europa": 0, "descensos": 3},
    {"id": 9,  "nombre": "Eredivisie",      "pais": "NED", "nivel": 1, "plazas_champions": 2, "plazas_europa": 2, "descensos": 2},
    {"id": 10, "nombre": "Primeira Liga",   "pais": "POR", "nivel": 1, "plazas_champions": 2, "plazas_europa": 2, "descensos": 3},
]
