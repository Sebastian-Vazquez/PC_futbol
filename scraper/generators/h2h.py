"""
Generador de historial H2H (cara a cara) entre clubs.
Produce un JSON pre-cargado con partidos históricos realistas
para que los duelos clásicos no aparezcan como "primer enfrentamiento".

Estrategia:
- Por cada liga, simula N temporadas históricas de partidos
- Teams más fuertes (mayor reputación) ganan más en media
- Rivalidades clásicas tienen registros especiales pre-definidos
- El formato es idéntico a LeagueSystem._h2h en GDScript
"""

import random
import math


# ─── Rivalidades clásicas con datos reales aproximados ────────────────────────
# Cada entrada: (id_a, id_b, PJ, W_a, D, W_b, GF_a, GC_a)
RIVALIDADES_CLASICAS = [
    # El Clásico: Real Madrid (1001) vs Barcelona (1002)
    (1001, 1002, 242, 97, 55, 90, 412, 391),
    # Madrid vs Atlético (1003)
    (1001, 1003, 198, 92, 52, 54, 311, 215),
    # Barcelona vs Atlético
    (1002, 1003, 180, 88, 48, 44, 295, 198),
    # Sevilla (1008) vs Betis (1007)
    (1007, 1008, 154, 56, 42, 56, 204, 210),
    # Athletic (1005) vs Real Sociedad (1004)
    (1004, 1005, 148, 58, 38, 52, 208, 202),
    # Valencia (1009) vs Villarreal (1006)
    (1006, 1009, 82, 32, 22, 28, 112, 102),
    # Real Madrid vs Sevilla
    (1001, 1008, 168, 88, 40, 40, 312, 192),
    # Barcelona vs Valencia
    (1002, 1009, 172, 92, 44, 36, 328, 188),
    # Real Madrid vs Athletic
    (1001, 1005, 186, 110, 46, 30, 386, 196),
    # Barcelona vs Sevilla
    (1002, 1008, 160, 86, 40, 34, 298, 178),
    # Osasuna (1020) vs Athletic
    (1005, 1020, 78, 36, 20, 22, 128, 96),
    # Osasuna vs Real Sociedad
    (1004, 1020, 82, 40, 22, 20, 138, 96),
    # Real Madrid vs Osasuna
    (1001, 1020, 98, 62, 22, 14, 228, 108),
    # Madrid vs Valencia
    (1001, 1009, 178, 98, 44, 36, 342, 208),
    # Madrid vs Villarreal
    (1001, 1006, 78, 44, 18, 16, 162, 86),
    # Madrid vs Betis
    (1001, 1007, 88, 52, 20, 16, 186, 96),
    # Barcelona vs Athletic
    (1002, 1005, 188, 102, 50, 36, 352, 202),
    # Zaragoza (1021) vs Sevilla
    (1008, 1021, 84, 38, 22, 24, 132, 106),
    # Sporting (1023) vs Oviedo (1037)
    (1023, 1037, 96, 40, 24, 32, 152, 138),
]


def _h2h_key(a: int, b: int) -> str:
    return f"{min(a, b)}_{max(a, b)}"


def _simular_partido_historico(rep_a: int, rep_b: int, es_local_a: bool) -> tuple:
    """
    Simula un partido histórico. Devuelve (goles_a, goles_b).
    El equipo con mayor reputación tiene más probabilidad de ganar.
    """
    home_bonus = 0.12 if es_local_a else -0.12
    ratio = (rep_a / max(rep_b, 1)) + home_bonus

    # xG base proporcional a reputación con algo de varianza
    xg_a = max(0.3, 1.15 * (2 / (1 + math.exp(-1.2 * (ratio - 1)))))
    xg_b = max(0.3, 1.15 * (2 / (1 + math.exp(-1.2 * (1/ratio - 1 + 0.12)))))

    # Añadir varianza lognormal
    xg_a *= math.exp(random.gauss(0, 0.22))
    xg_b *= math.exp(random.gauss(0, 0.22))

    # Poisson: algoritmo de Knuth
    def poisson(lam):
        L = math.exp(-max(0.01, lam))
        k, p = 0, 1.0
        while p > L:
            k += 1
            p *= random.random()
        return k - 1

    return poisson(xg_a), poisson(xg_b)


def generar_h2h(todos_equipos_por_liga: dict, ligas_config: dict) -> dict:
    """
    Genera el diccionario H2H completo.
    todos_equipos_por_liga: {liga_id: [(eid, nombre, ...), ...]}
    ligas_config: {liga_id: {tier, ...}}

    Retorna: {"min_max": {id_a, id_b, PJ, W_a, D, W_b, GF_a, GC_a}, ...}
    """
    print("\n[H2H] Generando historial cara a cara...")
    h2h: dict = {}

    # ─── 1. Registrar rivalidades clásicas hardcodeadas ───
    for (ia, ib, pj, wa, d, wb, gfa, gca) in RIVALIDADES_CLASICAS:
        key = _h2h_key(ia, ib)
        id_a = min(ia, ib)
        id_b = max(ia, ib)
        # Ajustar perspectiva si ia > ib
        if ia == id_a:
            h2h[key] = {"id_a": id_a, "id_b": id_b,
                        "PJ": pj, "W_a": wa, "D": d, "W_b": wb,
                        "GF_a": gfa, "GC_a": gca}
        else:
            h2h[key] = {"id_a": id_a, "id_b": id_b,
                        "PJ": pj, "W_a": wb, "D": d, "W_b": wa,
                        "GF_a": gca, "GC_a": gfa}

    # Construir mapa equipo → reputación
    rep_map: dict = {}
    for liga_id, lista in todos_equipos_por_liga.items():
        for datos in lista:
            eid = datos[0]
            rep = datos[3] if len(datos) > 3 else 60
            rep_map[eid] = rep

    # ─── 2. Simular temporadas históricas por liga ───────
    temporadas_por_tier = {1: 12, 2: 8, 3: 5, 4: 3, 5: 2}

    for liga_id, lista in todos_equipos_por_liga.items():
        cfg = ligas_config.get(liga_id, {})
        tier = cfg.get("tier", 3)
        n_temporadas = temporadas_por_tier.get(tier, 2)

        equipos_ids = [datos[0] for datos in lista]
        n = len(equipos_ids)
        if n < 4:
            continue

        # Generar n_temporadas completas de ida y vuelta
        for _ in range(n_temporadas):
            for i in range(n):
                for j in range(i + 1, n):
                    ea, eb = equipos_ids[i], equipos_ids[j]
                    # Partido de ida: ea local
                    rep_a = rep_map.get(ea, 60)
                    rep_b = rep_map.get(eb, 60)
                    ga, gb = _simular_partido_historico(rep_a, rep_b, True)
                    _registrar(h2h, ea, eb, ga, gb)
                    # Partido de vuelta: eb local
                    ga2, gb2 = _simular_partido_historico(rep_b, rep_a, True)
                    _registrar(h2h, ea, eb, gb2, ga2)

    total = len(h2h)
    total_partidos = sum(r["PJ"] for r in h2h.values())
    print(f"[H2H] {total} pares | {total_partidos:,} partidos históricos generados")
    return h2h


def _registrar(h2h: dict, ea: int, eb: int, ga: int, gb: int) -> None:
    """Acumula resultado en el diccionario h2h."""
    key = _h2h_key(ea, eb)
    id_a = min(ea, eb)
    id_b = max(ea, eb)

    if key not in h2h:
        h2h[key] = {"id_a": id_a, "id_b": id_b,
                    "PJ": 0, "W_a": 0, "D": 0, "W_b": 0,
                    "GF_a": 0, "GC_a": 0}

    rec = h2h[key]
    # Normalizar perspectiva respecto a id_a
    if ea == id_a:
        g_a, g_b = ga, gb
    else:
        g_a, g_b = gb, ga

    rec["PJ"] += 1
    rec["GF_a"] += g_a
    rec["GC_a"] += g_b
    if g_a > g_b:
        rec["W_a"] += 1
    elif g_a < g_b:
        rec["W_b"] += 1
    else:
        rec["D"] += 1
