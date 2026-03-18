import random
from datetime import date, timedelta
from generators.attributes import (
    generar_atributos, generar_atributos_portero,
    calcular_media, calcular_valor_mercado, POSICIONES_SECUNDARIAS, PIES
)
from generators.names import nombre_aleatorio, nombre_corto

# Plantilla tipo por equipo (cantidad de jugadores por posición)
PLANTILLA_TIPO = [
    ("PO", 3),
    ("DFC", 4),
    ("LD", 2),
    ("LI", 2),
    ("MCD", 3),
    ("MC", 3),
    ("MCO", 2),
    ("ED", 2),
    ("EI", 2),
    ("DC", 3),
]

def _fecha_nacimiento_aleatoria(edad_min: int, edad_max: int) -> str:
    edad = random.randint(edad_min, edad_max)
    anio_actual = 2026
    anio_nac = anio_actual - edad
    mes = random.randint(1, 12)
    dia = random.randint(1, 28)
    return f"{anio_nac}-{mes:02d}-{dia:02d}"

def generar_plantilla(equipo_id: int, pais_equipo: str, reputacion: int, id_inicio: int) -> list:
    """
    Genera una plantilla de ~26 jugadores para un equipo.
    reputacion: 55-100, determina la calidad media de los jugadores.
    """
    jugadores = []
    id_actual = id_inicio
    calidad_base = (reputacion - 55) / 45.0  # 0.0 a 1.0

    for posicion, cantidad in PLANTILLA_TIPO:
        for i in range(cantidad):
            # El primer jugador de cada posición es titular (más calidad)
            es_titular = (i == 0)
            calidad = calidad_base * random.uniform(0.85, 1.0) if es_titular else calidad_base * random.uniform(0.65, 0.90)
            calidad = max(0.05, min(1.0, calidad))

            # Edad según rol
            if posicion == "PO":
                edad = random.randint(22, 38) if es_titular else random.randint(18, 36)
            elif posicion in ("DFC", "MCD"):
                edad = random.randint(21, 35) if es_titular else random.randint(17, 34)
            elif posicion in ("ED", "EI", "DC"):
                edad = random.randint(19, 33) if es_titular else random.randint(16, 32)
            else:
                edad = random.randint(20, 34) if es_titular else random.randint(17, 33)

            # Nacionalidad: 60% del país del equipo, 40% extranjero
            if random.random() < 0.60:
                nac = pais_equipo
            else:
                nac = random.choice(["ESP", "ENG", "GER", "FRA", "ITA", "ARG", "BRA", "POR", "NED", "BEL", "SEN", "CMR", "CIV"])

            nombre, apellido = nombre_aleatorio(nac)
            nc = nombre_corto(nombre, apellido)

            fecha_nac = _fecha_nacimiento_aleatoria(edad, edad)

            attrs = generar_atributos(posicion, calidad, edad)
            attrs_po = generar_atributos_portero(calidad, edad) if posicion == "PO" else None

            media = calcular_media(attrs_po if posicion == "PO" else attrs, posicion)
            valor = calcular_valor_mercado(media, edad, posicion)

            posiciones_sec = [p for p in POSICIONES_SECUNDARIAS.get(posicion, []) if random.random() < 0.4]

            pie = PIES.get(posicion, "derecho")
            if random.random() < 0.15:  # 15% ambidiestros o pie contrario
                pie = "izquierdo" if pie == "derecho" else "derecho"

            salario_base = int(valor * random.uniform(0.004, 0.008))
            salario_base = max(1000, salario_base)
            fin_contrato_anio = 2026 + random.randint(0, 4)
            fin_contrato = f"{fin_contrato_anio}-06-30"

            jugador = {
                "id": id_actual,
                "nombre": nombre,
                "apellido": apellido,
                "nombre_corto": nc,
                "fecha_nacimiento": fecha_nac,
                "nacionalidad": nac,
                "nacionalidad_secundaria": None,
                "posicion_principal": posicion,
                "posiciones_secundarias": posiciones_sec,
                "pie_habil": pie,
                "altura_cm": _altura_por_posicion(posicion),
                "peso_kg": random.randint(65, 90),
                "equipo_id": equipo_id,
                "numero_camiseta": 0,  # Se asigna después
                "atributos": attrs,
                "atributos_portero": attrs_po,
                "contrato": {
                    "salario_semanal": salario_base,
                    "clausula": int(valor * random.uniform(2.0, 5.0)) if media >= 75 else 0,
                    "fin_contrato": fin_contrato,
                    "bonus_gol": int(salario_base * 0.1) if posicion in ("DC", "ED", "EI", "MCO") else 0,
                    "bonus_asistencia": int(salario_base * 0.05),
                },
                "valor_mercado": valor,
                "media": media,
                "potencial": _calcular_potencial(media, edad),
                "moral": random.randint(60, 90),
                "forma_fisica": random.randint(65, 95),
                "personalidad": {
                    "profesionalismo": random.randint(50, 99),
                    "ambicion": random.randint(50, 99),
                    "lealtad": random.randint(30, 99),
                    "temperamento": random.randint(30, 99),
                },
            }
            jugadores.append(jugador)
            id_actual += 1

    # Asignar números de camiseta
    _asignar_numeros(jugadores)
    return jugadores

def _asignar_numeros(jugadores: list) -> None:
    usados = set()
    porteros = [j for j in jugadores if j["posicion_principal"] == "PO"]
    resto = [j for j in jugadores if j["posicion_principal"] != "PO"]

    # Porteros: 1, 13, 25
    nums_po = [1, 13, 25, 33]
    for i, po in enumerate(porteros):
        po["numero_camiseta"] = nums_po[i % len(nums_po)]
        usados.add(nums_po[i % len(nums_po)])

    disponibles = [n for n in range(2, 50) if n not in usados]
    random.shuffle(disponibles)
    for j, num in zip(resto, disponibles):
        j["numero_camiseta"] = num

def _altura_por_posicion(posicion: str) -> int:
    alturas = {
        "PO": (183, 198), "DFC": (180, 196), "LD": (170, 185), "LI": (170, 185),
        "MCD": (172, 188), "MC": (170, 186), "MCO": (168, 182),
        "ED": (165, 182), "EI": (165, 182), "DC": (172, 195),
    }
    min_h, max_h = alturas.get(posicion, (170, 185))
    return random.randint(min_h, max_h)

def _calcular_potencial(media: int, edad: int) -> int:
    if edad <= 18:
        potencial = media + random.randint(8, 20)
    elif edad <= 21:
        potencial = media + random.randint(3, 12)
    elif edad <= 24:
        potencial = media + random.randint(0, 6)
    elif edad <= 28:
        potencial = media + random.randint(-2, 3)
    else:
        potencial = media + random.randint(-5, 0)
    return max(media, min(99, potencial))
