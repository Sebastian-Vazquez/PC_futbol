#!/usr/bin/env python3
"""
PC FUTBOL 2026 - Generador de datos v2 (Fase 2B)
Genera todos los JSONs para el juego en data/initial/
"""

import json
import os
import random
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from config import OUTPUT_DIR
from data.leagues_data import LIGAS_CONFIG, TORNEOS
from data.teams_england import ENGLAND
from data.teams_spain import SPAIN
from data.teams_argentina import ARGENTINA
from data.teams_germany_italy_france import GERMANY, ITALY, FRANCE
from data.teams_data import EQUIPOS_POR_LIGA as OTROS  # Brasil, Mexico, NED, POR
from data.teams_international import INTERNATIONAL
from generators.players import generar_plantilla
from generators.youth import generar_todas_las_canteras
from generators.badges import generar_todos_los_escudos
from generators.h2h_real import descargar_h2h_real
from generators.h2h_internacional import generar_h2h_internacional
from generators.real_squads import obtener_squad_real
from generators.attributes import (
    generar_atributos, generar_atributos_portero,
    calcular_media, calcular_valor_mercado, POSICIONES_SECUNDARIAS, PIES,
)
from data.club_historia import HISTORIA_REAL

random.seed(42)

# Combinar todos los equipos por liga
TODOS_EQUIPOS_POR_LIGA = {}
for d in [SPAIN, ENGLAND, ITALY, GERMANY, FRANCE, ARGENTINA]:
    TODOS_EQUIPOS_POR_LIGA.update(d)
# Agregar los otros (Brasil, Mexico, NED, POR) del archivo original
for liga_id in [7, 8, 9, 10]:
    if liga_id in OTROS:
        TODOS_EQUIPOS_POR_LIGA[liga_id] = OTROS[liga_id]
# Agregar ligas internacionales (IDs 11-33)
TODOS_EQUIPOS_POR_LIGA.update(INTERNATIONAL)


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


def _historia_para(equipo_id: int, reputacion: int) -> dict:
    """Devuelve datos históricos reales si existen, o valores generados por defecto."""
    if equipo_id in HISTORIA_REAL:
        return dict(HISTORIA_REAL[equipo_id])
    # Valores generados por defecto basados en reputación
    return {
        "fundacion": random.randint(1880, 1980),
        "titulos_liga": max(0, int((reputacion - 70) / 5)) if reputacion >= 70 else 0,
        "titulos_copa": max(0, int((reputacion - 65) / 7)) if reputacion >= 65 else 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    }


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
                    # base = 1_000_000 * factor; multiplicadores calibrados para valores reales
                    "presupuesto_fichajes": max(10_000, int(base * reputacion * 2.0)),
                    "balance":              max(10_000, int(base * reputacion * 1.5)),
                    "deuda": 0,
                    "masa_salarial_semanal":max(1_000,  int(base * reputacion * 0.03)),
                    "ingresos_tv_anual":    max(5_000,  int(base * reputacion * 1.5)),
                    "sponsor_camiseta":     max(1_000,  int(base * reputacion * 0.5)),
                    "sponsor_estadio":      max(500,    int(base * reputacion * 0.15)),
                    "merchandising_anual":  max(1_000,  int(base * reputacion * 0.8)),
                    "precio_entrada_base":  max(5,      int(reputacion * 0.5 * (1 + factor))),
                    "socios":               max(100,    int(reputacion * 300 * factor * random.uniform(0.5, 1.5))),
                },
                "tactica_default": random.choice(["4-3-3", "4-4-2", "4-2-3-1", "3-5-2", "5-3-2", "4-1-4-1"]),
                "color_principal": color1,
                "color_secundario": color2,
                "reputacion": reputacion,
                "nivel_cantera": max(1, min(5, int(reputacion / 20))),
                "nivel_ojeadores": max(1, min(5, int(reputacion / 25))),
                "nivel_medicina": max(1, min(5, int(reputacion / 20))),
                "historia": _historia_para(eid, reputacion),
            })
    print(f"     Total equipos: {len(equipos)}")
    return equipos


def _jugador_desde_real(datos_tm: dict, equipo_id: int, id_jugador: int) -> dict:
    """
    Construye un jugador completo a partir de los datos reales de TM.
    Usa nombre/apellido/fecha/nac/posicion reales; atributos generados según calidad.
    """
    posicion = datos_tm["posicion_principal"]
    calidad  = datos_tm["calidad"]

    # Edad desde fecha de nacimiento
    try:
        from datetime import date as _date
        fnac = datetime.strptime(datos_tm["fecha_nacimiento"], "%Y-%m-%d").date()
        hoy  = _date(2026, 1, 1)
        edad = int((hoy - fnac).days / 365.25)
        edad = max(16, min(45, edad))
    except Exception:
        edad = 25

    attrs    = generar_atributos(posicion, calidad, edad)
    attrs_po = generar_atributos_portero(calidad, edad) if posicion == "PO" else None

    media = calcular_media(attrs_po if posicion == "PO" else attrs, posicion)
    valor = calcular_valor_mercado(media, edad, posicion)

    # Respetar valor real si es significativo
    if datos_tm["valor_mercado_real"] > 0:
        valor = datos_tm["valor_mercado_real"]

    posiciones_sec = [p for p in POSICIONES_SECUNDARIAS.get(posicion, []) if random.random() < 0.4]
    pie = PIES.get(posicion, "derecho")
    if random.random() < 0.15:
        pie = "izquierdo" if pie == "derecho" else "derecho"

    salario_base = max(1_000, int(valor * random.uniform(0.004, 0.008)))
    fin_contrato = f"{2026 + random.randint(0, 4)}-06-30"

    from generators.players import _altura_por_posicion, _calcular_potencial
    return {
        "id":                    id_jugador,
        "nombre":                datos_tm["nombre"],
        "apellido":              datos_tm["apellido"],
        "nombre_corto":          datos_tm["nombre_corto"],
        "fecha_nacimiento":      datos_tm["fecha_nacimiento"],
        "nacionalidad":          datos_tm["nacionalidad"],
        "nacionalidad_secundaria": None,
        "posicion_principal":    posicion,
        "posiciones_secundarias": posiciones_sec,
        "pie_habil":             pie,
        "altura_cm":             _altura_por_posicion(posicion),
        "peso_kg":               random.randint(65, 90),
        "equipo_id":             equipo_id,
        "numero_camiseta":       0,
        "atributos":             attrs,
        "atributos_portero":     attrs_po,
        "contrato": {
            "salario_semanal":   salario_base,
            "clausula":          int(valor * random.uniform(2.0, 5.0)) if media >= 75 else 0,
            "fin_contrato":      fin_contrato,
            "bonus_gol":         int(salario_base * 0.1) if posicion in ("DC", "ED", "EI", "MCO") else 0,
            "bonus_asistencia":  int(salario_base * 0.05),
        },
        "valor_mercado":         valor,
        "media":                 media,
        "potencial":             _calcular_potencial(media, edad),
        "moral":                 random.randint(60, 90),
        "forma_fisica":          random.randint(65, 95),
        "personalidad": {
            "profesionalismo":   random.randint(50, 99),
            "ambicion":          random.randint(50, 99),
            "lealtad":           random.randint(30, 99),
            "temperamento":      random.randint(30, 99),
        },
    }


def _asignar_numeros_camiseta(jugadores: list) -> None:
    """Reutiliza la lógica de asignación de números de players.py."""
    from generators.players import _asignar_numeros
    _asignar_numeros(jugadores)


def generar_jugadores(equipos):
    print("\n[3/6] Generando jugadores senior...")
    todos = []
    id_actual = 10001
    reales_count = 0
    generados_count = 0

    pais_por_liga = {lid: cfg["pais"] for lid, cfg in LIGAS_CONFIG.items()}

    for equipo in equipos:
        eid    = equipo["id"]
        liga_id = equipo.get("liga_id", 1)
        pais   = pais_por_liga.get(liga_id, equipo.get("pais", "ESP"))

        # Intentar obtener squad real de Transfermarkt
        squad_real = None
        try:
            squad_real = obtener_squad_real(eid)
        except Exception as e:
            print(f"     [TM] Error obteniendo squad real para equipo {eid}: {e}")

        if squad_real:
            # Crear jugadores con nombres reales y atributos simulados según calidad
            jugadores = []
            for datos_tm in squad_real:
                try:
                    jugador = _jugador_desde_real(datos_tm, eid, id_actual)
                    jugadores.append(jugador)
                    id_actual += 1
                except Exception as e:
                    print(f"     [TM] Error procesando jugador {datos_tm.get('nombre_corto', '?')}: {e}")

            # Asignar números de camiseta
            if jugadores:
                _asignar_numeros_camiseta(jugadores)
                todos.extend(jugadores)
                reales_count += len(jugadores)
                continue

        # Fallback: generacion aleatoria
        jugadores = generar_plantilla(
            equipo_id=eid,
            pais_equipo=pais,
            reputacion=equipo["reputacion"],
            id_inicio=id_actual
        )
        todos.extend(jugadores)
        generados_count += len(jugadores)
        id_actual += len(jugadores)

    print(f"     Total jugadores senior: {len(todos)}")
    print(f"     Con nombres reales (TM): {reales_count} | Generados: {generados_count}")
    return todos, id_actual


def generar_juveniles(equipos, id_inicio):
    print("\n[4/6] Generando jugadores juveniles (U18/U19)...")
    juveniles = generar_todas_las_canteras(equipos, LIGAS_CONFIG, id_inicio)
    print(f"     Total juveniles: {len(juveniles)}")
    return juveniles


def generar_agentes_libres(id_inicio):
    """
    Genera ~400 jugadores sin equipo (equipo_id = -1).
    Divididos en 3 grupos de calidad:
      - Veteranos retirados de equipos top (rep 88-95 → calidad alta pero con edad)
      - Jugadores mid (rep 70-80)
      - Jóvenes sin contrato (rep 60-70)
    """
    print("\n[3b] Generando agentes libres...")
    todos = []
    id_actual = id_inicio

    # (reputacion_ficticia, cantidad_plantillas, paises_pool)
    grupos = [
        (92, 4, ["ESP", "ENG", "BRA", "ARG", "FRA", "GER", "ITA", "POR"]),   # ~104 jugadores top
        (75, 6, ["ESP", "ENG", "GER", "FRA", "ITA", "NED", "POR", "BEL",
                 "TUR", "ARG", "BRA", "URU", "COL"]),                          # ~156 mid
        (63, 6, ["ESP", "ENG", "GER", "FRA", "ITA", "ARG", "BRA", "MEX",
                 "SAU", "JPN", "KOR", "EGY", "MAR", "RSA", "NGA"]),            # ~156 low
    ]

    for rep, n_plantillas, paises in grupos:
        for _ in range(n_plantillas):
            pais = random.choice(paises)
            plantilla = generar_plantilla(
                equipo_id=-1,
                pais_equipo=pais,
                reputacion=rep + random.randint(-5, 5),
                id_inicio=id_actual
            )
            # Marcar como agente libre
            for j in plantilla:
                j["equipo_id"] = -1
                j["es_agente_libre"] = True
            todos.extend(plantilla)
            id_actual += len(plantilla)

    print(f"     Total agentes libres: {len(todos)}")
    return todos


def generar_paises():
    print("\n[5/6] Generando paises...")
    return [
        # Europa
        {"id": "ESP", "nombre": "Espana",           "continente": "Europa",     "confederacion": "UEFA"},
        {"id": "ENG", "nombre": "Inglaterra",        "continente": "Europa",     "confederacion": "UEFA"},
        {"id": "GER", "nombre": "Alemania",          "continente": "Europa",     "confederacion": "UEFA"},
        {"id": "FRA", "nombre": "Francia",           "continente": "Europa",     "confederacion": "UEFA"},
        {"id": "ITA", "nombre": "Italia",            "continente": "Europa",     "confederacion": "UEFA"},
        {"id": "NED", "nombre": "Paises Bajos",      "continente": "Europa",     "confederacion": "UEFA"},
        {"id": "POR", "nombre": "Portugal",          "continente": "Europa",     "confederacion": "UEFA"},
        {"id": "BEL", "nombre": "Belgica",           "continente": "Europa",     "confederacion": "UEFA"},
        {"id": "TUR", "nombre": "Turquia",           "continente": "Europa",     "confederacion": "UEFA"},
        {"id": "AUT", "nombre": "Austria",           "continente": "Europa",     "confederacion": "UEFA"},
        {"id": "SCO", "nombre": "Escocia",           "continente": "Europa",     "confederacion": "UEFA"},
        {"id": "UKR", "nombre": "Ucrania",           "continente": "Europa",     "confederacion": "UEFA"},
        {"id": "CHE", "nombre": "Suiza",             "continente": "Europa",     "confederacion": "UEFA"},
        {"id": "CZE", "nombre": "Republica Checa",   "continente": "Europa",     "confederacion": "UEFA"},
        {"id": "SRB", "nombre": "Serbia",            "continente": "Europa",     "confederacion": "UEFA"},
        {"id": "GRE", "nombre": "Grecia",            "continente": "Europa",     "confederacion": "UEFA"},
        {"id": "DNK", "nombre": "Dinamarca",         "continente": "Europa",     "confederacion": "UEFA"},
        {"id": "SWE", "nombre": "Suecia",            "continente": "Europa",     "confederacion": "UEFA"},
        {"id": "NOR", "nombre": "Noruega",           "continente": "Europa",     "confederacion": "UEFA"},
        {"id": "CRO", "nombre": "Croacia",           "continente": "Europa",     "confederacion": "UEFA"},
        {"id": "POL", "nombre": "Polonia",           "continente": "Europa",     "confederacion": "UEFA"},
        {"id": "ROU", "nombre": "Rumania",           "continente": "Europa",     "confederacion": "UEFA"},
        {"id": "SVN", "nombre": "Eslovenia",         "continente": "Europa",     "confederacion": "UEFA"},
        {"id": "SVK", "nombre": "Eslovaquia",        "continente": "Europa",     "confederacion": "UEFA"},
        {"id": "HUN", "nombre": "Hungria",           "continente": "Europa",     "confederacion": "UEFA"},
        {"id": "ALB", "nombre": "Albania",           "continente": "Europa",     "confederacion": "UEFA"},
        {"id": "GEO", "nombre": "Georgia",           "continente": "Europa",     "confederacion": "UEFA"},
        # Sudamerica / CONMEBOL
        {"id": "ARG", "nombre": "Argentina",         "continente": "Sudamerica", "confederacion": "CONMEBOL"},
        {"id": "BRA", "nombre": "Brasil",            "continente": "Sudamerica", "confederacion": "CONMEBOL"},
        {"id": "URU", "nombre": "Uruguay",           "continente": "Sudamerica", "confederacion": "CONMEBOL"},
        {"id": "CHL", "nombre": "Chile",             "continente": "Sudamerica", "confederacion": "CONMEBOL"},
        {"id": "COL", "nombre": "Colombia",          "continente": "Sudamerica", "confederacion": "CONMEBOL"},
        {"id": "ECU", "nombre": "Ecuador",           "continente": "Sudamerica", "confederacion": "CONMEBOL"},
        {"id": "PER", "nombre": "Peru",              "continente": "Sudamerica", "confederacion": "CONMEBOL"},
        {"id": "BOL", "nombre": "Bolivia",           "continente": "Sudamerica", "confederacion": "CONMEBOL"},
        {"id": "PAR", "nombre": "Paraguay",          "continente": "Sudamerica", "confederacion": "CONMEBOL"},
        {"id": "VEN", "nombre": "Venezuela",         "continente": "Sudamerica", "confederacion": "CONMEBOL"},
        # CONCACAF
        {"id": "USA", "nombre": "Estados Unidos",    "continente": "CONCACAF",   "confederacion": "CONCACAF"},
        {"id": "MEX", "nombre": "Mexico",            "continente": "CONCACAF",   "confederacion": "CONCACAF"},
        {"id": "CAN", "nombre": "Canada",            "continente": "CONCACAF",   "confederacion": "CONCACAF"},
        {"id": "CRC", "nombre": "Costa Rica",        "continente": "CONCACAF",   "confederacion": "CONCACAF"},
        {"id": "HON", "nombre": "Honduras",          "continente": "CONCACAF",   "confederacion": "CONCACAF"},
        {"id": "JAM", "nombre": "Jamaica",           "continente": "CONCACAF",   "confederacion": "CONCACAF"},
        {"id": "GTM", "nombre": "Guatemala",         "continente": "CONCACAF",   "confederacion": "CONCACAF"},
        {"id": "SLV", "nombre": "El Salvador",       "continente": "CONCACAF",   "confederacion": "CONCACAF"},
        {"id": "TRI", "nombre": "Trinidad y Tobago", "continente": "CONCACAF",   "confederacion": "CONCACAF"},
        {"id": "PAN", "nombre": "Panama",            "continente": "CONCACAF",   "confederacion": "CONCACAF"},
        # Asia / AFC
        {"id": "SAU", "nombre": "Arabia Saudita",    "continente": "Asia",       "confederacion": "AFC"},
        {"id": "JPN", "nombre": "Japon",             "continente": "Asia",       "confederacion": "AFC"},
        {"id": "KOR", "nombre": "Corea del Sur",     "continente": "Asia",       "confederacion": "AFC"},
        {"id": "UAE", "nombre": "Emiratos Arabes",   "continente": "Asia",       "confederacion": "AFC"},
        {"id": "AUS", "nombre": "Australia",         "continente": "Oceania",    "confederacion": "AFC"},
        {"id": "CHN", "nombre": "China",             "continente": "Asia",       "confederacion": "AFC"},
        {"id": "IRN", "nombre": "Iran",              "continente": "Asia",       "confederacion": "AFC"},
        {"id": "IRQ", "nombre": "Irak",              "continente": "Asia",       "confederacion": "AFC"},
        {"id": "UZB", "nombre": "Uzbekistan",        "continente": "Asia",       "confederacion": "AFC"},
        {"id": "IDN", "nombre": "Indonesia",         "continente": "Asia",       "confederacion": "AFC"},
        # Africa / CAF
        {"id": "EGY", "nombre": "Egipto",            "continente": "Africa",     "confederacion": "CAF"},
        {"id": "MAR", "nombre": "Marruecos",         "continente": "Africa",     "confederacion": "CAF"},
        {"id": "RSA", "nombre": "Sudafrica",         "continente": "Africa",     "confederacion": "CAF"},
        {"id": "TUN", "nombre": "Tunez",             "continente": "Africa",     "confederacion": "CAF"},
        {"id": "NGA", "nombre": "Nigeria",           "continente": "Africa",     "confederacion": "CAF"},
        {"id": "SEN", "nombre": "Senegal",           "continente": "Africa",     "confederacion": "CAF"},
        {"id": "CMR", "nombre": "Camerun",           "continente": "Africa",     "confederacion": "CAF"},
        {"id": "CIV", "nombre": "Costa de Marfil",   "continente": "Africa",     "confederacion": "CAF"},
        {"id": "GHA", "nombre": "Ghana",             "continente": "Africa",     "confederacion": "CAF"},
        {"id": "ALG", "nombre": "Argelia",           "continente": "Africa",     "confederacion": "CAF"},
        {"id": "MLI", "nombre": "Mali",              "continente": "Africa",     "confederacion": "CAF"},
        {"id": "KEN", "nombre": "Kenya",             "continente": "Africa",     "confederacion": "CAF"},
        # Oceania / OFC
        {"id": "NZL", "nombre": "Nueva Zelanda",     "continente": "Oceania",    "confederacion": "OFC"},
        {"id": "FIJ", "nombre": "Fiji",              "continente": "Oceania",    "confederacion": "OFC"},
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
    proximo_id += len(juveniles)
    agentes_libres = generar_agentes_libres(proximo_id)
    paises = generar_paises()

    todos_jugadores = jugadores_senior + juveniles + agentes_libres

    # Historial H2H real (football-data.co.uk)
    print("\n[H2H] Descargando resultados históricos reales...")
    h2h = descargar_h2h_real(verbose=True)

    # Fusionar H2H de competiciones internacionales (Intercontinental + CWC)
    print("[H2H] Fusionando resultados internacionales...")
    h2h_int = generar_h2h_internacional()
    for k, v in h2h_int.items():
        if k not in h2h:
            h2h[k] = v
        else:
            # Acumular estadísticas sobre el registro existente
            rec = h2h[k]
            rec["PJ"]   += v["PJ"]
            rec["W_a"]  += v["W_a"]
            rec["D"]    += v["D"]
            rec["W_b"]  += v["W_b"]
            rec["GF_a"] += v["GF_a"]
            rec["GC_a"] += v["GC_a"]
    print(f"[H2H] Total pares tras fusión: {len(h2h)}")

    print("\n[6/6] Guardando JSON + escudos SVG...")
    guardar_json(os.path.join(OUTPUT_DIR, "ligas.json"), ligas)
    guardar_json(os.path.join(OUTPUT_DIR, "equipos.json"), equipos)
    guardar_json(os.path.join(OUTPUT_DIR, "jugadores.json"), todos_jugadores)
    guardar_json(os.path.join(OUTPUT_DIR, "paises.json"), paises)
    guardar_json(os.path.join(OUTPUT_DIR, "torneos.json"), TORNEOS)
    guardar_json(os.path.join(OUTPUT_DIR, "h2h.json"), h2h)

    # Generar escudos SVG
    generar_todos_los_escudos(equipos, OUTPUT_DIR)

    total = len(todos_jugadores)
    print("\n" + "=" * 55)
    print(f"  DONE -- {len(ligas)} ligas | {len(equipos)} equipos | {total} jugadores")
    print(f"  ({len(jugadores_senior)} senior + {len(juveniles)} juveniles + {len(agentes_libres)} libres)")
    print("=" * 55)


if __name__ == "__main__":
    main()
