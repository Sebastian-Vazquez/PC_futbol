import random

# Atributos base por posición (media, varianza)
PERFILES_POSICION = {
    "PO": {  # Portero
        "velocidad": (55, 10), "aceleracion": (55, 10),
        "disparo": (30, 10), "potencia_disparo": (40, 10),
        "pase_corto": (65, 10), "pase_largo": (60, 10),
        "centro": (40, 10), "regate": (30, 10),
        "control": (40, 10), "cabeceo": (55, 10),
        "defensa": (30, 10), "entrada": (20, 8),
        "fisico": (70, 10), "resistencia": (60, 10),
        "agresividad": (40, 10), "vision": (65, 10),
        "compostura": (70, 10), "posicionamiento_of": (30, 10),
        "desmarque": (30, 10), "tiro_lejano": (30, 10),
        "tiro_libre": (30, 8), "penaltis": (40, 15),
        "efecto": (30, 8),
        # Atributos portero
        "reflejos": (75, 12), "paradas": (75, 12),
        "estirada": (72, 12), "saque_portero": (60, 12),
        "posicionamiento_po": (72, 12),
    },
    "DFC": {  # Defensa central
        "velocidad": (62, 12), "aceleracion": (60, 12),
        "disparo": (40, 12), "potencia_disparo": (55, 12),
        "pase_corto": (65, 10), "pase_largo": (65, 12),
        "centro": (45, 10), "regate": (35, 10),
        "control": (55, 10), "cabeceo": (78, 10),
        "defensa": (80, 10), "entrada": (78, 10),
        "fisico": (82, 10), "resistencia": (75, 10),
        "agresividad": (72, 12), "vision": (60, 10),
        "compostura": (70, 10), "posicionamiento_of": (35, 10),
        "desmarque": (35, 10), "tiro_lejano": (38, 10),
        "tiro_libre": (35, 8), "penaltis": (45, 15),
        "efecto": (35, 8),
    },
    "LD": {  # Lateral derecho
        "velocidad": (74, 10), "aceleracion": (76, 10),
        "disparo": (45, 12), "potencia_disparo": (50, 10),
        "pase_corto": (68, 10), "pase_largo": (65, 10),
        "centro": (72, 10), "regate": (60, 10),
        "control": (62, 10), "cabeceo": (58, 10),
        "defensa": (72, 10), "entrada": (70, 10),
        "fisico": (72, 10), "resistencia": (80, 8),
        "agresividad": (65, 10), "vision": (62, 10),
        "compostura": (62, 10), "posicionamiento_of": (55, 10),
        "desmarque": (60, 10), "tiro_lejano": (42, 10),
        "tiro_libre": (38, 8), "penaltis": (42, 12),
        "efecto": (45, 8),
    },
    "LI": {  # Lateral izquierdo (mismo perfil que LD)
        "velocidad": (74, 10), "aceleracion": (76, 10),
        "disparo": (45, 12), "potencia_disparo": (50, 10),
        "pase_corto": (68, 10), "pase_largo": (65, 10),
        "centro": (72, 10), "regate": (60, 10),
        "control": (62, 10), "cabeceo": (58, 10),
        "defensa": (72, 10), "entrada": (70, 10),
        "fisico": (72, 10), "resistencia": (80, 8),
        "agresividad": (65, 10), "vision": (62, 10),
        "compostura": (62, 10), "posicionamiento_of": (55, 10),
        "desmarque": (60, 10), "tiro_lejano": (42, 10),
        "tiro_libre": (38, 8), "penaltis": (42, 12),
        "efecto": (45, 8),
    },
    "MCD": {  # Mediocentro defensivo
        "velocidad": (60, 10), "aceleracion": (60, 10),
        "disparo": (50, 12), "potencia_disparo": (55, 10),
        "pase_corto": (76, 8), "pase_largo": (72, 10),
        "centro": (52, 10), "regate": (55, 10),
        "control": (68, 8), "cabeceo": (62, 10),
        "defensa": (75, 8), "entrada": (74, 8),
        "fisico": (74, 10), "resistencia": (80, 8),
        "agresividad": (70, 10), "vision": (72, 8),
        "compostura": (72, 8), "posicionamiento_of": (50, 10),
        "desmarque": (50, 10), "tiro_lejano": (48, 10),
        "tiro_libre": (48, 10), "penaltis": (50, 12),
        "efecto": (45, 8),
    },
    "MC": {  # Mediocentro
        "velocidad": (64, 10), "aceleracion": (64, 10),
        "disparo": (60, 10), "potencia_disparo": (60, 10),
        "pase_corto": (78, 8), "pase_largo": (74, 8),
        "centro": (60, 10), "regate": (62, 10),
        "control": (72, 8), "cabeceo": (58, 10),
        "defensa": (58, 10), "entrada": (55, 10),
        "fisico": (68, 10), "resistencia": (78, 8),
        "agresividad": (58, 10), "vision": (78, 8),
        "compostura": (72, 8), "posicionamiento_of": (60, 10),
        "desmarque": (60, 10), "tiro_lejano": (55, 10),
        "tiro_libre": (55, 10), "penaltis": (52, 12),
        "efecto": (52, 8),
    },
    "MCO": {  # Mediapunta
        "velocidad": (68, 10), "aceleracion": (70, 10),
        "disparo": (72, 8), "potencia_disparo": (65, 10),
        "pase_corto": (82, 6), "pase_largo": (76, 8),
        "centro": (68, 10), "regate": (74, 8),
        "control": (80, 6), "cabeceo": (55, 10),
        "defensa": (42, 12), "entrada": (38, 12),
        "fisico": (60, 10), "resistencia": (70, 10),
        "agresividad": (55, 10), "vision": (84, 6),
        "compostura": (78, 8), "posicionamiento_of": (75, 8),
        "desmarque": (78, 8), "tiro_lejano": (68, 10),
        "tiro_libre": (70, 10), "penaltis": (62, 12),
        "efecto": (68, 8),
    },
    "ED": {  # Extremo derecho
        "velocidad": (84, 8), "aceleracion": (86, 6),
        "disparo": (68, 10), "potencia_disparo": (65, 10),
        "pase_corto": (72, 8), "pase_largo": (65, 10),
        "centro": (74, 8), "regate": (82, 6),
        "control": (78, 8), "cabeceo": (52, 10),
        "defensa": (35, 12), "entrada": (30, 12),
        "fisico": (60, 10), "resistencia": (72, 10),
        "agresividad": (52, 10), "vision": (70, 8),
        "compostura": (68, 10), "posicionamiento_of": (72, 8),
        "desmarque": (78, 6), "tiro_lejano": (60, 10),
        "tiro_libre": (58, 10), "penaltis": (55, 12),
        "efecto": (70, 8),
    },
    "EI": {  # Extremo izquierdo (mismo perfil que ED)
        "velocidad": (84, 8), "aceleracion": (86, 6),
        "disparo": (68, 10), "potencia_disparo": (65, 10),
        "pase_corto": (72, 8), "pase_largo": (65, 10),
        "centro": (74, 8), "regate": (82, 6),
        "control": (78, 8), "cabeceo": (52, 10),
        "defensa": (35, 12), "entrada": (30, 12),
        "fisico": (60, 10), "resistencia": (72, 10),
        "agresividad": (52, 10), "vision": (70, 8),
        "compostura": (68, 10), "posicionamiento_of": (72, 8),
        "desmarque": (78, 6), "tiro_lejano": (60, 10),
        "tiro_libre": (58, 10), "penaltis": (55, 12),
        "efecto": (70, 8),
    },
    "DC": {  # Delantero centro
        "velocidad": (72, 10), "aceleracion": (72, 10),
        "disparo": (82, 6), "potencia_disparo": (80, 8),
        "pase_corto": (65, 10), "pase_largo": (58, 10),
        "centro": (55, 10), "regate": (68, 10),
        "control": (72, 8), "cabeceo": (76, 8),
        "defensa": (30, 12), "entrada": (28, 12),
        "fisico": (74, 8), "resistencia": (70, 10),
        "agresividad": (65, 10), "vision": (68, 10),
        "compostura": (75, 8), "posicionamiento_of": (82, 6),
        "desmarque": (80, 6), "tiro_lejano": (62, 10),
        "tiro_libre": (60, 10), "penaltis": (72, 10),
        "efecto": (58, 8),
    },
}

# Posiciones secundarias compatibles
POSICIONES_SECUNDARIAS = {
    "PO": [],
    "DFC": ["LD", "LI"],
    "LD": ["DFC", "MC"],
    "LI": ["DFC", "MC"],
    "MCD": ["MC", "DFC"],
    "MC": ["MCD", "MCO", "ED", "EI"],
    "MCO": ["MC", "ED", "EI", "DC"],
    "ED": ["EI", "MCO", "DC"],
    "EI": ["ED", "MCO", "DC"],
    "DC": ["ED", "EI", "MCO"],
}

PIES = {"PO": "derecho", "DFC": "derecho", "LD": "derecho", "LI": "izquierdo",
        "MCD": "derecho", "MC": "derecho", "MCO": "derecho",
        "ED": "derecho", "EI": "izquierdo", "DC": "derecho"}

def generar_atributos(posicion: str, calidad: float, edad: int) -> dict:
    """
    Genera atributos para un jugador.
    calidad: 0.0 (peor) a 1.0 (mejor), determina la media general.
    edad: afecta velocidad y resistencia en jugadores mayores.
    """
    perfil = PERFILES_POSICION.get(posicion, PERFILES_POSICION["MC"])

    # Factor de calidad: entre 0.60 y 1.15 escala los atributos
    factor = 0.60 + calidad * 0.55

    # Factor de edad: jugadores muy jóvenes o muy mayores penalizados
    if edad < 20:
        factor_edad = 0.80 + (edad - 16) * 0.04  # 16->0.80, 20->0.96
    elif edad > 32:
        factor_edad = 1.0 - (edad - 32) * 0.025  # 33->0.975, 38->0.85
    else:
        factor_edad = 1.0

    attrs = {}
    for attr, (media, varianza) in perfil.items():
        if attr in ("reflejos", "paradas", "estirada", "saque_portero", "posicionamiento_po"):
            continue  # Solo para porteros, se manejan aparte
        valor = media * factor * factor_edad + random.gauss(0, varianza * 0.3)
        # Penalizar velocidad/aceleracion con edad
        if attr in ("velocidad", "aceleracion") and edad > 30:
            valor -= (edad - 30) * 1.5
        attrs[attr] = max(25, min(99, int(round(valor))))

    return attrs

def generar_atributos_portero(calidad: float, edad: int) -> dict:
    perfil = PERFILES_POSICION["PO"]
    factor = 0.60 + calidad * 0.55
    if edad > 32:
        factor *= 1.0 - (edad - 32) * 0.01  # Los porteros aguantan más

    attrs = {}
    for attr in ("reflejos", "paradas", "estirada", "saque_portero", "posicionamiento_po"):
        media, varianza = perfil[attr]
        valor = media * factor + random.gauss(0, varianza * 0.3)
        attrs[attr] = max(25, min(99, int(round(valor))))
    return attrs

def calcular_media(atributos: dict, posicion: str) -> int:
    """Calcula la media general del jugador según posición."""
    pesos = {
        "PO":  ["reflejos", "paradas", "estirada", "posicionamiento_po", "saque_portero"],  # no en attrs normales
        "DFC": ["defensa", "entrada", "cabeceo", "fisico", "posicionamiento_of"],
        "LD":  ["defensa", "velocidad", "centro", "resistencia", "entrada"],
        "LI":  ["defensa", "velocidad", "centro", "resistencia", "entrada"],
        "MCD": ["defensa", "entrada", "pase_corto", "vision", "resistencia"],
        "MC":  ["pase_corto", "pase_largo", "vision", "control", "resistencia"],
        "MCO": ["pase_corto", "vision", "regate", "disparo", "desmarque"],
        "ED":  ["velocidad", "regate", "centro", "control", "desmarque"],
        "EI":  ["velocidad", "regate", "centro", "control", "desmarque"],
        "DC":  ["disparo", "posicionamiento_of", "desmarque", "cabeceo", "control"],
    }
    claves = pesos.get(posicion, list(atributos.keys())[:8])
    valores = [atributos.get(k, 60) for k in claves if k in atributos]
    if not valores:
        valores = list(atributos.values())
    return int(sum(valores) / len(valores))

def calcular_valor_mercado(media: int, edad: int, posicion: str) -> int:
    """Calcula valor de mercado basado en media, edad y posición."""
    if media >= 88:
        base = 80_000_000
    elif media >= 82:
        base = 35_000_000
    elif media >= 76:
        base = 15_000_000
    elif media >= 70:
        base = 6_000_000
    elif media >= 64:
        base = 2_000_000
    else:
        base = 500_000

    # Factor edad: pico entre 24-28
    if edad < 21:
        factor = 1.2 + (21 - edad) * 0.1  # Jóvenes valen más por potencial
    elif edad <= 28:
        factor = 1.4 - (edad - 24) * 0.05
    elif edad <= 32:
        factor = 1.0 - (edad - 28) * 0.1
    else:
        factor = 0.5 - (edad - 32) * 0.05

    valor = int(base * max(0.1, factor))
    # Variación aleatoria ±20%
    valor = int(valor * random.uniform(0.8, 1.2))
    return max(50_000, valor)
