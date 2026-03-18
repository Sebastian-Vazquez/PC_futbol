#!/usr/bin/env python3
"""
PC FUTBOL 2026 - Generador de datos v2 (Fase 2B)
Genera todos los JSONs para el juego en data/initial/
"""

import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))

from config import OUTPUT_DIR
from data.leagues_data import LIGAS_CONFIG, TORNEOS
from data.teams_england import ENGLAND
from data.teams_spain import SPAIN
from data.teams_argentina import ARGENTINA
from data.teams_germany_italy_france import GERMANY, ITALY, FRANCE
from data.teams_data import EQUIPOS_POR_LIGA as OTROS  # Brasil, Mexico, etc.
from generators.players import generar_plantilla
from generators.youth import generar_todas_las_canteras
from generators.badges import generar_todos_los_escudos

random.seed(42)

# Combinar todos los equipos por liga
TODOS_EQUIPOS_POR_LIGA = {}
for d in [SPAIN, ENGLAND, ITALY, GERMANY, FRANCE, ARGENTINA]:
    TODOS_EQUIPOS_POR_LIGA.update(d)
# Agregar los otros (Brasil, Mexico, NED, POR) del archivo original
for liga_id in [7, 8, 9, 10]:
    if liga_id in OTROS:
        TODOS_EQUIPOS_POR_LIGA[liga_id] = OTROS[liga_id]


def asegurar_directorio(ruta):
    os.makedirs(ruta, exist_ok=True)


def guardar_json(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    tipo = os.path.basename(ruta)
    n = len(datos) if isinstance(datos, list) else len(datos)
    print(f"  OK {tipo} ({n} registros)")


def generar_ligas():
    print("\n[1/6] Generando ligas...")
    ligas = []
    for lid, cfg in LIGAS_CONFIG.items():
        n_equipos = len(TODOS_EQUIPOS_POR_LIGA.get(lid, []))
        ligas.append({
            "id": lid,
            "nombre": cfg["nombre"],
            "pais": cfg["pais"],
            "tier": cfg["tier"],
            "finanzas_factor": cfg["finanzas_factor"],
            "descensos": cfg["descensos"],
            "plazas_champions": cfg["plazas_champions"],
            "plazas_europa": cfg["plazas_europa"],
            "num_equipos": n_equipos if n_equipos > 0 else cfg.get("num_equipos", 0),
        })
    return ligas


def generar_equipos():
    print("\n[2/6] Generando equipos...")
    equipos = []
    for liga_id, lista in TODOS_EQUIPOS_POR_LIGA.items():
        cfg = LIGAS_CONFIG.get(liga_id, {})
        pais = cfg.get("pais", "ESP")
        tier = cfg.get("tier", 1)
        factor = cfg.get("finanzas_factor", 1.0)

        for datos in lista:
            eid, nombre, nombre_corto, reputacion, color1, color2 = datos[:6]

            # Escalar finanzas por tier y reputacion
            base = 1_000_000 * factor
            equipos.append({
                "id": eid,
                "nombre": nombre,
                "nombre_corto": nombre_corto,
                "pais": pais,
                "liga_id": liga_id,
                "tier": tier,
                "estadio": {
                    "nombre": f"Estadio {nombre_corto}",
                    "capacidad": max(1000, int(reputacion * 700 * random.uniform(0.5, 1.5) * factor * 2 + 1000)),
                    "estado": random.randint(55, 95),
                    "nivel_vip": min(3, max(0, int((reputacion - 60) / 15))),
                    "nivel_museo": 1 if reputacion >= 80 else 0,
                    "nivel_tienda": min(3, max(0, int((reputacion - 55) / 20))),
                    "nivel_parking": random.randint(0, 2),
                    "ampliable": random.random() < 0.6,
                    "coste_mantenimiento_semanal": max(500, int(reputacion * 1500 * factor)),
                },
                "finanzas": {
                    "presupuesto_fichajes": max(10_000, int(base * reputacion * 3_000)),
                    "balance": max(10_000, int(base * reputacion * 5_000)),
                    "deuda": 0,
                    "masa_salarial_semanal": max(1_000, int(base * reputacion * 100)),
                    "ingresos_tv_anual": max(5_000, int(base * reputacion * 600)),
                    "sponsor_camiseta": max(1_000, int(base * reputacion * 200)),
                    "sponsor_estadio": max(500, int(base * reputacion * 80)),
                    "merchandising_anual": max(1_000, int(base * reputacion * 150)),
                    "precio_entrada_base": max(5, int(reputacion * 0.5 * (1 + factor))),
                    "socios": max(100, int(reputacion * 300 * factor * random.uniform(0.5, 1.5))),
                },
                "tactica_default": random.choice(["4-3-3", "4-4-2", "4-2-3-1", "3-5-2", "5-3-2", "4-1-4-1"]),
                "color_principal": color1,
                "color_secundario": color2,
                "reputacion": reputacion,
                "nivel_cantera": max(1, min(5, int(reputacion / 20))),
                "nivel_ojeadores": max(1, min(5, int(reputacion / 25))),
                "nivel_medicina": max(1, min(5, int(reputacion / 20))),
                "historia": {
                    "fundacion": random.randint(1880, 1980),
                    "titulos_liga": max(0, int((reputacion - 70) / 5)) if reputacion >= 70 else 0,
                    "titulos_copa": max(0, int((reputacion - 65) / 7)) if reputacion >= 65 else 0,
                },
            })
    print(f"     Total equipos: {len(equipos)}")
    return equipos


def generar_jugadores(equipos):
    print("\n[3/6] Generando jugadores senior...")
    todos = []
    id_actual = 10001

    pais_por_liga = {lid: cfg["pais"] for lid, cfg in LIGAS_CONFIG.items()}

    for equipo in equipos:
        liga_id = equipo.get("liga_id", 1)
        pais = pais_por_liga.get(liga_id, equipo.get("pais", "ESP"))
        jugadores = generar_plantilla(
            equipo_id=equipo["id"],
            pais_equipo=pais,
            reputacion=equipo["reputacion"],
            id_inicio=id_actual
        )
        todos.extend(jugadores)
        id_actual += len(jugadores)

    print(f"     Total jugadores senior: {len(todos)}")
    return todos, id_actual


def generar_juveniles(equipos, id_inicio):
    print("\n[4/6] Generando jugadores juveniles (U18/U19)...")
    juveniles = generar_todas_las_canteras(equipos, LIGAS_CONFIG, id_inicio)
    print(f"     Total juveniles: {len(juveniles)}")
    return juveniles


def generar_paises():
    print("\n[5/6] Generando paises...")
    return [
        {"id": "ESP", "nombre": "Espana",        "continente": "Europa"},
        {"id": "ENG", "nombre": "Inglaterra",     "continente": "Europa"},
        {"id": "GER", "nombre": "Alemania",       "continente": "Europa"},
        {"id": "FRA", "nombre": "Francia",        "continente": "Europa"},
        {"id": "ITA", "nombre": "Italia",         "continente": "Europa"},
        {"id": "ARG", "nombre": "Argentina",      "continente": "Sudamerica"},
        {"id": "BRA", "nombre": "Brasil",         "continente": "Sudamerica"},
        {"id": "MEX", "nombre": "Mexico",         "continente": "CONCACAF"},
        {"id": "NED", "nombre": "Paises Bajos",   "continente": "Europa"},
        {"id": "POR", "nombre": "Portugal",       "continente": "Europa"},
        {"id": "BEL", "nombre": "Belgica",        "continente": "Europa"},
        {"id": "SEN", "nombre": "Senegal",        "continente": "Africa"},
        {"id": "CMR", "nombre": "Camerun",        "continente": "Africa"},
        {"id": "CIV", "nombre": "Costa de Marfil","continente": "Africa"},
        {"id": "COL", "nombre": "Colombia",       "continente": "Sudamerica"},
        {"id": "URU", "nombre": "Uruguay",        "continente": "Sudamerica"},
        {"id": "CRO", "nombre": "Croacia",        "continente": "Europa"},
        {"id": "MAR", "nombre": "Marruecos",      "continente": "Africa"},
        {"id": "USA", "nombre": "Estados Unidos", "continente": "CONCACAF"},
        {"id": "JPN", "nombre": "Japon",          "continente": "Asia"},
        {"id": "CHL", "nombre": "Chile",          "continente": "Sudamerica"},
        {"id": "PAR", "nombre": "Paraguay",       "continente": "Sudamerica"},
        {"id": "BOL", "nombre": "Bolivia",        "continente": "Sudamerica"},
        {"id": "PER", "nombre": "Peru",           "continente": "Sudamerica"},
        {"id": "ECU", "nombre": "Ecuador",        "continente": "Sudamerica"},
    ]


def main():
    print("=" * 55)
    print("  PC FUTBOL 2026 -- Generador de datos v2 (Fase 2B)")
    print("=" * 55)

    asegurar_directorio(OUTPUT_DIR)

    ligas = generar_ligas()
    equipos = generar_equipos()
    jugadores_senior, proximo_id = generar_jugadores(equipos)
    juveniles = generar_juveniles(equipos, proximo_id)
    paises = generar_paises()

    todos_jugadores = jugadores_senior + juveniles

    print("\n[6/6] Guardando JSON + escudos SVG...")
    guardar_json(os.path.join(OUTPUT_DIR, "ligas.json"), ligas)
    guardar_json(os.path.join(OUTPUT_DIR, "equipos.json"), equipos)
    guardar_json(os.path.join(OUTPUT_DIR, "jugadores.json"), todos_jugadores)
    guardar_json(os.path.join(OUTPUT_DIR, "paises.json"), paises)
    guardar_json(os.path.join(OUTPUT_DIR, "torneos.json"), TORNEOS)

    # Generar escudos SVG
    generar_todos_los_escudos(equipos, OUTPUT_DIR)

    total = len(todos_jugadores)
    print("\n" + "=" * 55)
    print(f"  DONE -- {len(ligas)} ligas | {len(equipos)} equipos | {total} jugadores")
    print(f"  ({len(jugadores_senior)} senior + {len(juveniles)} juveniles)")
    print("=" * 55)


if __name__ == "__main__":
    main()
