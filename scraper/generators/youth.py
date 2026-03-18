"""
Generador de jugadores juveniles.
Crea canteras (U19/U18) para equipos de 1ª y 2ª división.
"""
import random
from generators.attributes import generar_atributos, generar_atributos_portero, calcular_media, calcular_valor_mercado
from generators.names import nombre_aleatorio, nombre_corto

# Plantilla tipo para una cantera (menos porteros, más jugadores de campo)
PLANTILLA_JUVENIL = [
    ("PO",  2),
    ("DFC", 3),
    ("LD",  2),
    ("LI",  2),
    ("MCD", 2),
    ("MC",  3),
    ("MCO", 2),
    ("ED",  2),
    ("EI",  2),
    ("DC",  2),
]


def generar_cantera(equipo_id: int, pais_equipo: str, reputacion: int,
                    id_inicio: int, categoria: str = "U19") -> list:
    """
    Genera cantera para un equipo.
    categoria: 'U19' (16-19) o 'U18' (15-18)
    """
    jugadores = []
    id_actual = id_inicio

    edad_max = 19 if categoria == "U19" else 18
    edad_min = 16 if categoria == "U19" else 15

    # Calidad reducida respecto a la plantilla senior
    calidad_base = ((reputacion - 55) / 45.0) * 0.55  # Max 55% de la calidad senior

    for posicion, cantidad in PLANTILLA_JUVENIL:
        for _ in range(cantidad):
            edad = random.randint(edad_min, edad_max)
            calidad = max(0.05, calidad_base * random.uniform(0.6, 1.0))

            # Nacionalidad: 80% del país del equipo para canteras
            nac = pais_equipo if random.random() < 0.80 else random.choice(
                ["ESP", "ENG", "GER", "FRA", "ITA", "ARG", "BRA", "POR", "SEN", "CMR"]
            )

            nombre, apellido = nombre_aleatorio(nac)
            nc = nombre_corto(nombre, apellido)

            anio_nac = 2026 - edad
            mes = random.randint(1, 12)
            dia = random.randint(1, 28)
            fecha_nac = f"{anio_nac}-{mes:02d}-{dia:02d}"

            attrs = generar_atributos(posicion, calidad, edad)
            attrs_po = generar_atributos_portero(calidad, edad) if posicion == "PO" else None

            media = calcular_media(attrs_po if posicion == "PO" else attrs, posicion)
            valor = calcular_valor_mercado(media, edad, posicion)
            # Los juveniles valen más relativamente por potencial
            valor = int(valor * random.uniform(1.2, 2.0))

            potencial_base = media + random.randint(10, 25)  # Juveniles tienen alto potencial
            potencial = min(99, potencial_base)

            salario_base = max(200, int(valor * 0.002))
            fin_contrato_anio = 2026 + random.randint(1, 3)

            jugador = {
                "id": id_actual,
                "nombre": nombre,
                "apellido": apellido,
                "nombre_corto": nc,
                "fecha_nacimiento": fecha_nac,
                "nacionalidad": nac,
                "nacionalidad_secundaria": None,
                "posicion_principal": posicion,
                "posiciones_secundarias": [],
                "pie_habil": "derecho" if random.random() > 0.2 else "izquierdo",
                "altura_cm": random.randint(165, 188),
                "peso_kg": random.randint(60, 80),
                "equipo_id": equipo_id,
                "equipo_cantera_id": equipo_id,  # Marca que es de la cantera
                "categoria_juvenil": categoria,
                "numero_camiseta": id_actual % 99 + 1,
                "atributos": attrs,
                "atributos_portero": attrs_po,
                "contrato": {
                    "salario_semanal": salario_base,
                    "clausula": int(valor * 3.0),
                    "fin_contrato": f"{fin_contrato_anio}-06-30",
                    "bonus_gol": 0,
                    "bonus_asistencia": 0,
                },
                "valor_mercado": valor,
                "media": media,
                "potencial": potencial,
                "moral": random.randint(65, 95),
                "forma_fisica": random.randint(70, 95),
                "es_juvenil": True,
                "personalidad": {
                    "profesionalismo": random.randint(40, 99),
                    "ambicion": random.randint(60, 99),  # Los jóvenes son ambiciosos
                    "lealtad": random.randint(50, 99),
                    "temperamento": random.randint(40, 90),
                },
            }
            jugadores.append(jugador)
            id_actual += 1

    return jugadores


def generar_todas_las_canteras(equipos: list, ligas_config: dict, id_inicio: int) -> list:
    """Genera canteras para equipos de 1ª y 2ª división."""
    from data.leagues_data import LIGAS_CONFIG
    todos = []
    id_actual = id_inicio

    pais_por_liga = {lid: cfg["pais"] for lid, cfg in LIGAS_CONFIG.items()}

    for equipo in equipos:
        liga_id = equipo.get("liga_id", 0)
        tier = LIGAS_CONFIG.get(liga_id, {}).get("tier", 99)

        if tier == 1:
            # 1ª división: U19 completa
            pais = pais_por_liga.get(liga_id, "ESP")
            juveniles = generar_cantera(
                equipo["id"], pais, equipo["reputacion"], id_actual, "U19"
            )
            todos.extend(juveniles)
            id_actual += len(juveniles)

        elif tier == 2:
            # 2ª división: U18 reducida
            pais = pais_por_liga.get(liga_id, "ESP")
            juveniles = generar_cantera(
                equipo["id"], pais, equipo["reputacion"], id_actual, "U18"
            )
            todos.extend(juveniles)
            id_actual += len(juveniles)

    return todos
