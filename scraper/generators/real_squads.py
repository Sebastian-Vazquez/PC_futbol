#!/usr/bin/env python3
"""
PC FUTBOL 2026 - Scraper de plantillas reales desde Transfermarkt
Descarga y cachea los squads de equipos reales para poblar el juego.

Uso independiente:
    python generators/real_squads.py              # descarga todos los equipos con TM ID
    python generators/real_squads.py --equipo 1001  # descarga solo Real Madrid
"""

import json
import os
import random
import re
import sys
import time
from datetime import datetime

# Soporte para ejecución directa y como módulo
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_SCRAPER_DIR = os.path.dirname(_THIS_DIR)
if _SCRAPER_DIR not in sys.path:
    sys.path.insert(0, _SCRAPER_DIR)

try:
    import requests
    from bs4 import BeautifulSoup
    _DEPS_OK = True
except ImportError as _e:
    _DEPS_OK = False
    _IMPORT_ERROR = str(_e)

from data.tm_ids import TM_IDS, TM_NOMBRES

# ── Configuración ────────────────────────────────────────────────────────────
_CACHE_DIR = os.path.join(_SCRAPER_DIR, "cache", "tm_squads")
_TM_BASE = "https://www.transfermarkt.com"
_SAISON = "2024"
_DELAY_MIN = 2.0
_DELAY_MAX = 3.5

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://www.transfermarkt.com/",
    "DNT": "1",
}

# ── Mapeo de posiciones TM → juego ─────────────────────────────────────────
_POS_MAP = {
    # Portero
    "goalkeeper":           "PO",
    "keeper":               "PO",
    # Defensa central
    "centre-back":          "DFC",
    "center-back":          "DFC",
    "central defender":     "DFC",
    "sweeper":              "DFC",
    # Lateral derecho
    "right-back":           "LD",
    "right back":           "LD",
    "right wing-back":      "LD",
    # Lateral izquierdo
    "left-back":            "LI",
    "left back":            "LI",
    "left wing-back":       "LI",
    # Mediocentro defensivo
    "defensive midfield":   "MCD",
    "defensive midfielder": "MCD",
    "holding midfield":     "MCD",
    "defensive mid":        "MCD",
    # Mediocentro
    "central midfield":     "MC",
    "central midfielder":   "MC",
    "box-to-box mid":       "MC",
    "box-to-box midfield":  "MC",
    # Mediapunta
    "attacking midfield":   "MCO",
    "attacking midfielder": "MCO",
    "second striker":       "MCO",
    "behind the striker":   "MCO",
    # Extremo derecho
    "right midfield":       "ED",
    "right winger":         "ED",
    "right wing":           "ED",
    # Extremo izquierdo
    "left midfield":        "EI",
    "left winger":          "EI",
    "left wing":            "EI",
    # Delantero centro
    "centre-forward":       "DC",
    "center-forward":       "DC",
    "striker":              "DC",
    "forward":              "DC",
}

# ── Mapeo de nacionalidades TM → código ISO 3 letras ───────────────────────
_NAC_MAP = {
    "spain":            "ESP", "espana":          "ESP", "españa":          "ESP",
    "england":          "ENG", "inglaterra":       "ENG",
    "germany":          "GER", "alemania":         "GER", "deutschland":     "GER",
    "france":           "FRA", "francia":          "FRA",
    "italy":            "ITA", "italia":           "ITA",
    "netherlands":      "NED", "holanda":          "NED", "paises bajos":    "NED",
    "portugal":         "POR",
    "belgium":          "BEL", "belgica":          "BEL",
    "brazil":           "BRA", "brasil":           "BRA",
    "argentina":        "ARG",
    "croatia":          "CRO", "croacia":          "CRO",
    "austria":          "AUT",
    "switzerland":      "CHE", "suiza":            "CHE",
    "denmark":          "DNK", "dinamarca":        "DNK",
    "sweden":           "SWE", "suecia":           "SWE",
    "norway":           "NOR", "noruega":          "NOR",
    "poland":           "POL", "polonia":          "POL",
    "czechia":          "CZE", "czech republic":   "CZE", "republica checa": "CZE",
    "slovakia":         "SVK",
    "slovenia":         "SVN",
    "hungary":          "HUN",
    "romania":          "ROU",
    "serbia":           "SRB",
    "ukraine":          "UKR", "ucrania":          "UKR",
    "greece":           "GRE", "grecia":           "GRE",
    "turkey":           "TUR", "turquia":          "TUR",
    "scotland":         "SCO", "escocia":          "SCO",
    "wales":            "WAL",
    "ireland":          "IRL",
    "northern ireland": "NIR",
    "usa":              "USA", "united states":    "USA", "estados unidos":  "USA",
    "mexico":           "MEX", "méxico":           "MEX",
    "canada":           "CAN",
    "colombia":         "COL",
    "chile":            "CHL",
    "uruguay":          "URU",
    "peru":             "PER", "perú":             "PER",
    "ecuador":          "ECU",
    "venezuela":        "VEN",
    "paraguay":         "PAR",
    "bolivia":          "BOL",
    "morocco":          "MAR", "marruecos":        "MAR",
    "egypt":            "EGY", "egipto":           "EGY",
    "nigeria":          "NGA",
    "senegal":          "SEN",
    "ivory coast":      "CIV", "cote d'ivoire":    "CIV", "costa de marfil": "CIV",
    "ghana":            "GHA",
    "cameroon":         "CMR", "camerun":          "CMR",
    "mali":             "MLI",
    "algeria":          "ALG", "argelia":          "ALG",
    "south africa":     "RSA", "sudafrica":        "RSA",
    "kenya":            "KEN",
    "tunisia":          "TUN", "tunez":            "TUN",
    "japan":            "JPN", "japon":            "JPN",
    "south korea":      "KOR", "korea, south":     "KOR", "corea del sur":   "KOR",
    "saudi arabia":     "SAU", "arabia saudita":   "SAU",
    "australia":        "AUS",
    "china":            "CHN",
    "iran":             "IRN",
    "iraq":             "IRQ", "irak":             "IRQ",
    "uzbekistan":       "UZB",
    "indonesia":        "IDN",
    "new zealand":      "NZL", "nueva zelanda":    "NZL",
    "georgia":          "GEO",
    "albania":          "ALB",
    "costa rica":       "CRC",
    "honduras":         "HON",
    "jamaica":          "JAM",
    "panama":           "PAN", "panamá":           "PAN",
    "trinidad and tobago": "TRI",
    "el salvador":      "SLV",
    "guatemala":        "GTM",
    "united arab emirates": "UAE", "emiratos arabes": "UAE",
}


# ── Funciones auxiliares ────────────────────────────────────────────────────

def _asegurar_cache_dir():
    os.makedirs(_CACHE_DIR, exist_ok=True)


def _cache_path(equipo_id: int) -> str:
    return os.path.join(_CACHE_DIR, f"{equipo_id}.json")


def _leer_cache(equipo_id: int):
    """Lee el squad desde cache. Devuelve lista o None."""
    ruta = _cache_path(equipo_id)
    if os.path.exists(ruta):
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None


def _escribir_cache(equipo_id: int, datos: list):
    """Guarda el squad en cache."""
    _asegurar_cache_dir()
    ruta = _cache_path(equipo_id)
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"  [TM] Advertencia: no se pudo guardar cache para {equipo_id}: {e}")


def _parsear_valor(texto: str) -> int:
    """
    Convierte texto de valor TM a entero en euros.
    Ejemplos: "€80.00m" -> 80_000_000, "€500k" -> 500_000, "-" -> 0
    """
    if not texto or texto.strip() in ("-", "", "€-"):
        return 0
    texto = texto.strip().lower().replace(",", ".")
    texto = texto.replace("€", "").strip()
    try:
        if texto.endswith("m"):
            return int(float(texto[:-1]) * 1_000_000)
        elif texto.endswith("k"):
            return int(float(texto[:-1]) * 1_000)
        elif texto.replace(".", "").isdigit():
            return int(float(texto))
    except (ValueError, TypeError):
        pass
    return 0


def _valor_a_calidad(valor_euros: int) -> float:
    """Convierte valor de mercado en euros a calidad 0.0-1.0."""
    if valor_euros >= 100_000_000:  return 1.0
    elif valor_euros >= 60_000_000:  return 0.92
    elif valor_euros >= 40_000_000:  return 0.85
    elif valor_euros >= 25_000_000:  return 0.78
    elif valor_euros >= 15_000_000:  return 0.70
    elif valor_euros >= 8_000_000:   return 0.62
    elif valor_euros >= 4_000_000:   return 0.54
    elif valor_euros >= 1_500_000:   return 0.45
    elif valor_euros >= 500_000:     return 0.36
    else:                            return 0.28


def _mapear_posicion(texto: str) -> str:
    """Convierte posición TM (inglés) a código interno."""
    if not texto:
        return "MC"
    clave = texto.strip().lower()
    if clave in _POS_MAP:
        return _POS_MAP[clave]
    # Búsqueda parcial
    for k, v in _POS_MAP.items():
        if k in clave or clave in k:
            return v
    return "MC"


def _mapear_nacionalidad(texto: str) -> str:
    """Convierte nombre de país TM a código ISO 3 letras."""
    if not texto:
        return "ESP"
    clave = texto.strip().lower()
    if clave in _NAC_MAP:
        return _NAC_MAP[clave]
    # Búsqueda parcial
    for k, v in _NAC_MAP.items():
        if k in clave or clave in k:
            return v
    return "ESP"


def _parsear_fecha(texto: str, es_edad: bool = False) -> str:
    """
    Convierte edad (número) o fecha TM a YYYY-MM-DD.
    TM actualmente muestra solo la edad, no la fecha completa.
    """
    if not texto:
        return "1995-01-01"
    texto = texto.strip()

    # Si es edad directa (ej: "26"), convertir a año aproximado
    if es_edad or re.match(r'^\d{1,2}$', texto):
        try:
            edad = int(texto)
            anio_nac = 2025 - edad  # temporada 2024/25
            return f"{anio_nac}-06-15"
        except ValueError:
            pass

    # Quitar edad entre paréntesis: "Jan 5, 2000 (24)"
    texto = re.sub(r'\s*\(\d+\)\s*$', '', texto).strip()

    formatos = [
        "%b %d, %Y", "%B %d, %Y",
        "%d.%m.%Y", "%d/%m/%Y",
        "%Y-%m-%d",
    ]
    for fmt in formatos:
        try:
            dt = datetime.strptime(texto, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    # Extraer año si lo hay
    m = re.search(r'(\d{4})', texto)
    if m:
        return f"{m.group(1)}-06-15"
    return "1995-01-01"


def _separar_nombre(nombre_completo: str):
    """
    Divide un nombre completo en (nombre, apellido).
    TM suele mostrar "Apellido Nombre" o solo "Nombre Apellido".
    """
    partes = nombre_completo.strip().split()
    if not partes:
        return "Desconocido", "Jugador"
    if len(partes) == 1:
        return partes[0], partes[0]
    # Heurística: primer token = nombre, resto = apellido
    nombre = partes[0]
    apellido = " ".join(partes[1:])
    return nombre, apellido


def _nombre_corto(nombre: str, apellido: str) -> str:
    """Genera nombre corto tipo 'N. Apellido'."""
    if not nombre:
        return apellido[:12]
    inicial = nombre[0].upper()
    ap = apellido[:10] if apellido else nombre
    return f"{inicial}. {ap}"


# ── Parser HTML de Transfermarkt ────────────────────────────────────────────

def _parsear_tabla_jugadores(html: str) -> list:
    """
    Extrae lista de jugadores desde el HTML de la página de plantilla de TM.
    Estructura TM 2024: tabla.items con filas odd/even, cada fila tiene:
      td[0]: número camiseta
      td[1] (posrela): tabla interna → fila1=foto+nombre, fila2=posición
      td[2]: edad (número)
      td[3]: bandera de nacionalidad (img.flaggenrahmen alt=country)
      td[4]: escudo del club (ignorar)
      td[5]: valor de mercado (rechts hauptlink)
    """
    soup = BeautifulSoup(html, "html.parser")
    jugadores = []

    tabla = soup.find("table", {"class": "items"})
    if tabla is None:
        for t in soup.find_all("table"):
            if t.find("a", href=re.compile(r"/profil/spieler/")):
                tabla = t
                break
    if tabla is None:
        return []

    filas = tabla.find_all("tr", class_=re.compile(r"(odd|even)"))

    for fila in filas:
        try:
            celdas = fila.find_all("td", recursive=False)
            if len(celdas) < 4:
                continue

            # td posrela: nombre + posición
            td_posrela = fila.find("td", class_="posrela")
            if not td_posrela:
                continue

            # Nombre: link con href /profil/spieler/
            link = td_posrela.find("a", href=re.compile(r"/profil/spieler/"))
            if not link:
                continue
            nombre_completo = link.get_text(strip=True)
            if not nombre_completo or len(nombre_completo) < 2:
                continue

            # Posición: segunda fila de la tabla interna
            posicion_texto = ""
            tabla_int = td_posrela.find("table", class_="inline-table")
            if tabla_int:
                filas_int = tabla_int.find_all("tr")
                if len(filas_int) >= 2:
                    posicion_texto = filas_int[1].get_text(strip=True)

            # Índice de td_posrela en la fila
            try:
                idx = list(celdas).index(td_posrela)
            except ValueError:
                idx = 1

            # Edad: celda siguiente a posrela
            edad_texto = ""
            if idx + 1 < len(celdas):
                edad_texto = celdas[idx + 1].get_text(strip=True)

            # Nacionalidad: img.flaggenrahmen en la celda siguiente
            nacionalidad_texto = ""
            if idx + 2 < len(celdas):
                img_flag = celdas[idx + 2].find("img", class_="flaggenrahmen")
                if img_flag:
                    nacionalidad_texto = img_flag.get("alt", "")
            # Fallback: buscar cualquier flaggenrahmen en la fila
            if not nacionalidad_texto:
                img_flag = fila.find("img", class_="flaggenrahmen")
                if img_flag:
                    nacionalidad_texto = img_flag.get("alt", "")

            # Valor de mercado: td rechts hauptlink
            valor_texto = ""
            td_valor = fila.find("td", class_=lambda c: c and "rechts" in c and "hauptlink" in c)
            if td_valor:
                a_val = td_valor.find("a")
                valor_texto = a_val.get_text(strip=True) if a_val else td_valor.get_text(strip=True)

            jugadores.append({
                "nombre_completo":    nombre_completo,
                "posicion_texto":     posicion_texto,
                "nacionalidad_texto": nacionalidad_texto,
                "fecha_texto":        edad_texto,
                "es_edad":            True,
                "valor_texto":        valor_texto,
            })

        except Exception:
            continue

    return jugadores


def _procesar_jugadores_raw(jugadores_raw: list) -> list:
    """
    Convierte los datos crudos del parser en el formato del juego.
    """
    resultado = []
    for raw in jugadores_raw:
        try:
            nombre_completo = raw.get("nombre_completo", "")
            nombre, apellido = _separar_nombre(nombre_completo)
            nc = _nombre_corto(nombre, apellido)
            posicion = _mapear_posicion(raw.get("posicion_texto", ""))
            nacionalidad = _mapear_nacionalidad(raw.get("nacionalidad_texto", ""))
            fecha_nacimiento = _parsear_fecha(raw.get("fecha_texto", ""), es_edad=raw.get("es_edad", False))
            valor = _parsear_valor(raw.get("valor_texto", ""))
            calidad = _valor_a_calidad(valor)

            resultado.append({
                "nombre":              nombre,
                "apellido":            apellido,
                "nombre_corto":        nc,
                "fecha_nacimiento":    fecha_nacimiento,
                "nacionalidad":        nacionalidad,
                "posicion_principal":  posicion,
                "valor_mercado_real":  valor,
                "calidad":             calidad,
            })
        except Exception:
            continue
    return resultado


# ── Descarga HTTP ────────────────────────────────────────────────────────────

_session = None

def _get_session():
    global _session
    if _session is None:
        _session = requests.Session()
        _session.headers.update(_HEADERS)
    return _session


def _descargar_html(tm_id: int, slug: str) -> str | None:
    """Descarga el HTML de la página de plantilla de TM."""
    url = f"{_TM_BASE}/{slug}/kader/verein/{tm_id}/saison_id/{_SAISON}"
    try:
        sess = _get_session()
        resp = sess.get(url, timeout=20)
        if resp.status_code == 200:
            return resp.text
        elif resp.status_code == 403:
            print(f"  [TM] Error 403 (bloqueado) para {slug}")
        elif resp.status_code == 404:
            print(f"  [TM] Error 404 (no encontrado) para {slug}")
        else:
            print(f"  [TM] HTTP {resp.status_code} para {slug}")
    except requests.exceptions.Timeout:
        print(f"  [TM] Timeout descargando {slug}")
    except requests.exceptions.ConnectionError:
        print(f"  [TM] Error de conexion para {slug}")
    except Exception as e:
        print(f"  [TM] Error inesperado descargando {slug}: {e}")
    return None


# ── API pública ──────────────────────────────────────────────────────────────

def obtener_squad_real(equipo_id: int) -> list | None:
    """
    Obtiene el squad real de un equipo desde TM (con cache en disco).

    Returns:
        Lista de dicts con campos del jugador, o None si falla o no hay TM ID.
    """
    if not _DEPS_OK:
        print(f"  [TM] Dependencias no disponibles ({_IMPORT_ERROR}). Usando jugadores generados.")
        return None

    # Verificar si tenemos TM ID para este equipo
    if equipo_id not in TM_IDS:
        return None

    tm_id, slug = TM_IDS[equipo_id]
    nombre_equipo = TM_NOMBRES.get(equipo_id, f"Equipo {equipo_id}")

    # Intentar leer desde cache
    cached = _leer_cache(equipo_id)
    if cached is not None:
        print(f"  [TM] Cache hit: {nombre_equipo}")
        return cached

    # Descargar desde TM
    print(f"  [TM] Descargando {nombre_equipo} ({tm_id})...")

    html = _descargar_html(tm_id, slug)
    if html is None:
        return None

    # Parsear jugadores
    try:
        jugadores_raw = _parsear_tabla_jugadores(html)
    except Exception as e:
        print(f"  [TM] Error parseando HTML de {nombre_equipo}: {e}")
        return None

    if not jugadores_raw:
        print(f"  [TM] Advertencia: no se encontraron jugadores para {nombre_equipo}")
        return None

    jugadores = _procesar_jugadores_raw(jugadores_raw)

    if not jugadores:
        print(f"  [TM] Advertencia: no se pudieron procesar jugadores de {nombre_equipo}")
        return None

    # Si hay más de 30 jugadores, tomar los 26 más valiosos
    if len(jugadores) > 30:
        jugadores.sort(key=lambda j: j["valor_mercado_real"], reverse=True)
        jugadores = jugadores[:26]

    print(f"  [TM] OK: {nombre_equipo} -> {len(jugadores)} jugadores")

    # Guardar en cache
    _escribir_cache(equipo_id, jugadores)

    # Rate limiting
    tiempo_espera = random.uniform(_DELAY_MIN, _DELAY_MAX)
    time.sleep(tiempo_espera)

    return jugadores


def descargar_todos_los_squads(forzar: bool = False):
    """
    Descarga y cachea los squads de todos los equipos con TM ID.
    forzar=True ignora el cache existente.
    """
    if not _DEPS_OK:
        print(f"[TM] Error: dependencias no disponibles. Instala: pip install requests beautifulsoup4")
        print(f"     Detalle: {_IMPORT_ERROR}")
        return

    _asegurar_cache_dir()
    equipos = sorted(TM_IDS.keys())
    total = len(equipos)
    descargados = 0
    fallidos = 0
    cache_hits = 0

    print(f"\n[TM] Iniciando descarga de {total} equipos...")
    print(f"[TM] Cache dir: {_CACHE_DIR}\n")

    for i, equipo_id in enumerate(equipos, 1):
        tm_id, slug = TM_IDS[equipo_id]
        nombre_equipo = TM_NOMBRES.get(equipo_id, f"Equipo {equipo_id}")

        print(f"  [{i:3d}/{total}] {nombre_equipo}...", end=" ", flush=True)

        if not forzar and _leer_cache(equipo_id) is not None:
            print(f"[cache]")
            cache_hits += 1
            continue

        html = _descargar_html(tm_id, slug)
        if html is None:
            print(f"[FALLO]")
            fallidos += 1
            continue

        try:
            jugadores_raw = _parsear_tabla_jugadores(html)
            jugadores = _procesar_jugadores_raw(jugadores_raw)

            if not jugadores:
                print(f"[sin datos]")
                fallidos += 1
                continue

            if len(jugadores) > 30:
                jugadores.sort(key=lambda j: j["valor_mercado_real"], reverse=True)
                jugadores = jugadores[:26]

            _escribir_cache(equipo_id, jugadores)
            print(f"[OK: {len(jugadores)} jugadores]")
            descargados += 1

        except Exception as e:
            print(f"[ERROR: {e}]")
            fallidos += 1

        # Rate limiting
        time.sleep(random.uniform(_DELAY_MIN, _DELAY_MAX))

    print(f"\n[TM] Resumen:")
    print(f"     Descargados: {descargados}")
    print(f"     Cache hits:  {cache_hits}")
    print(f"     Fallidos:    {fallidos}")
    print(f"     Total:       {total}")


# ── Entry point independiente ────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Scraper de plantillas Transfermarkt")
    parser.add_argument(
        "--equipo", type=int, default=None,
        help="ID del equipo a descargar (ej: 1001 = Real Madrid). Sin argumento descarga todos."
    )
    parser.add_argument(
        "--forzar", action="store_true",
        help="Ignorar cache y re-descargar todo."
    )
    args = parser.parse_args()

    if args.equipo is not None:
        if args.equipo not in TM_IDS:
            print(f"[TM] Error: equipo {args.equipo} no tiene TM ID registrado.")
            print(f"[TM] Equipos disponibles: {sorted(TM_IDS.keys())}")
            sys.exit(1)
        if args.forzar:
            ruta = _cache_path(args.equipo)
            if os.path.exists(ruta):
                os.remove(ruta)
        resultado = obtener_squad_real(args.equipo)
        if resultado:
            print(f"\n[TM] Squad obtenido ({len(resultado)} jugadores):")
            for j in resultado:
                print(f"  {j['nombre_corto']:20s}  {j['posicion_principal']:4s}  "
                      f"calidad={j['calidad']:.2f}  valor={j['valor_mercado_real']:>12,}")
        else:
            print(f"[TM] No se pudo obtener el squad.")
    else:
        descargar_todos_los_squads(forzar=args.forzar)
