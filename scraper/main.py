#!/usr/bin/env python3
"""
PC FÚTBOL 2026 - Generador de datos
Genera los archivos JSON para el juego en data/initial/
"""

import json
import os
import random
import sys

# Asegurar que podemos importar los módulos locales
sys.path.insert(0, os.path.dirname(__file__))

from config import OUTPUT_DIR, LIGAS
from data.teams_data import EQUIPOS_POR_LIGA
from generators.players import generar_plantilla

random.seed(42)  # Seed fijo para reproducibilidad

def asegurar_directorio(ruta: str) -> None:
    os.makedirs(ruta, exist_ok=True)

def guardar_json(ruta: str, datos) -> None:
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    print(f"  OK {os.path.basename(ruta)} ({len(datos)} registros)")

def generar_ligas() -> list:
    print("\n[1/4] Generando ligas...")
    ligas = []
    for liga in LIGAS:
        ligas.append({
            "id": liga["id"],
            "nombre": liga["nombre"],
            "pais": liga["pais"],
            "nivel": liga["nivel"],
            "plazas_champions": liga["plazas_champions"],
            "plazas_europa": liga["plazas_europa"],
            "descensos": liga["descensos"],
            "num_equipos": len(EQUIPOS_POR_LIGA.get(liga["id"], [])),
        })
    return ligas

def generar_equipos() -> list:
    print("\n[2/4] Generando equipos...")
    equipos = []
    for liga_id, lista in EQUIPOS_POR_LIGA.items():
        liga = next((l for l in LIGAS if l["id"] == liga_id), None)
        pais = liga["pais"] if liga else "ESP"
        for datos in lista:
            eid, nombre, nombre_corto, reputacion, color1, color2, presupuesto, balance, masa_sal = datos
            equipos.append({
                "id": eid,
                "nombre": nombre,
                "nombre_corto": nombre_corto,
                "pais": pais,
                "liga_id": liga_id,
                "estadio": {
                    "nombre": f"Estadio {nombre_corto}",
                    "capacidad": int(reputacion * 700 * random.uniform(0.7, 1.4)),
                    "estado": random.randint(60, 95),
                    "nivel_vip": random.randint(0, 3),
                    "nivel_museo": 1 if reputacion >= 80 else 0,
                    "nivel_tienda": random.randint(0, 2),
                    "nivel_parking": random.randint(0, 2),
                    "ampliable": random.random() < 0.6,
                    "coste_mantenimiento_semanal": int(reputacion * 1500),
                },
                "finanzas": {
                    "presupuesto_fichajes": presupuesto,
                    "balance": balance,
                    "deuda": 0,
                    "masa_salarial_semanal": masa_sal,
                    "ingresos_tv_anual": int(reputacion * 600_000),
                    "sponsor_camiseta": int(reputacion * 200_000),
                    "sponsor_estadio": int(reputacion * 80_000),
                    "merchandising_anual": int(reputacion * 150_000),
                    "precio_entrada_base": max(15, int(reputacion * 0.6)),
                    "socios": int(reputacion * 500 * random.uniform(0.5, 1.5)),
                },
                "tactica_default": random.choice(["4-3-3", "4-4-2", "4-2-3-1", "3-5-2", "5-3-2", "4-1-4-1"]),
                "color_principal": color1,
                "color_secundario": color2,
                "reputacion": reputacion,
                "nivel_cantera": max(1, int(reputacion / 25)),
                "nivel_ojeadores": max(1, int(reputacion / 28)),
                "nivel_medicina": max(1, int(reputacion / 25)),
                "historia": {
                    "fundacion": random.randint(1890, 1980),
                    "titulos_liga": max(0, int((reputacion - 70) / 5)) if reputacion >= 70 else 0,
                    "titulos_copa": max(0, int((reputacion - 65) / 7)) if reputacion >= 65 else 0,
                },
            })
    return equipos

def generar_jugadores(equipos: list) -> list:
    print("\n[3/4] Generando jugadores...")
    todos_jugadores = []
    id_actual = 10001

    equipo_liga = {}
    for liga_id, lista in EQUIPOS_POR_LIGA.items():
        liga = next((l for l in LIGAS if l["id"] == liga_id), None)
        pais = liga["pais"] if liga else "ESP"
        for datos in lista:
            equipo_liga[datos[0]] = pais

    for equipo in equipos:
        pais = equipo_liga.get(equipo["id"], equipo.get("pais", "ESP"))
        jugadores = generar_plantilla(
            equipo_id=equipo["id"],
            pais_equipo=pais,
            reputacion=equipo["reputacion"],
            id_inicio=id_actual
        )
        todos_jugadores.extend(jugadores)
        id_actual += len(jugadores)

    print(f"     Total jugadores generados: {len(todos_jugadores)}")
    return todos_jugadores

def generar_paises() -> list:
    print("\n[4/4] Generando países...")
    return [
        {"id": "ESP", "nombre": "España",       "continente": "Europa"},
        {"id": "ENG", "nombre": "Inglaterra",   "continente": "Europa"},
        {"id": "GER", "nombre": "Alemania",     "continente": "Europa"},
        {"id": "FRA", "nombre": "Francia",      "continente": "Europa"},
        {"id": "ITA", "nombre": "Italia",       "continente": "Europa"},
        {"id": "ARG", "nombre": "Argentina",    "continente": "Sudamérica"},
        {"id": "BRA", "nombre": "Brasil",       "continente": "Sudamérica"},
        {"id": "MEX", "nombre": "México",       "continente": "CONCACAF"},
        {"id": "NED", "nombre": "Países Bajos", "continente": "Europa"},
        {"id": "POR", "nombre": "Portugal",     "continente": "Europa"},
        {"id": "BEL", "nombre": "Bélgica",      "continente": "Europa"},
        {"id": "SEN", "nombre": "Senegal",      "continente": "África"},
        {"id": "CMR", "nombre": "Camerún",      "continente": "África"},
        {"id": "CIV", "nombre": "Costa de Marfil", "continente": "África"},
        {"id": "COL", "nombre": "Colombia",     "continente": "Sudamérica"},
        {"id": "URU", "nombre": "Uruguay",      "continente": "Sudamérica"},
        {"id": "CRO", "nombre": "Croacia",      "continente": "Europa"},
        {"id": "MAR", "nombre": "Marruecos",    "continente": "África"},
        {"id": "USA", "nombre": "Estados Unidos","continente": "CONCACAF"},
        {"id": "JPN", "nombre": "Japón",        "continente": "Asia"},
    ]

def main():
    print("=" * 50)
    print("  PC FUTBOL 2026 -- Generador de datos")
    print("=" * 50)

    asegurar_directorio(OUTPUT_DIR)

    ligas = generar_ligas()
    equipos = generar_equipos()
    jugadores = generar_jugadores(equipos)
    paises = generar_paises()

    print("\nGuardando JSONs en:", OUTPUT_DIR)
    guardar_json(os.path.join(OUTPUT_DIR, "ligas.json"), ligas)
    guardar_json(os.path.join(OUTPUT_DIR, "equipos.json"), equipos)
    guardar_json(os.path.join(OUTPUT_DIR, "jugadores.json"), jugadores)
    guardar_json(os.path.join(OUTPUT_DIR, "paises.json"), paises)

    print("\n" + "=" * 50)
    print(f"  DONE -- {len(ligas)} ligas | {len(equipos)} equipos | {len(jugadores)} jugadores")
    print("=" * 50)

if __name__ == "__main__":
    main()
