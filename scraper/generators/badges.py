"""
Generador de escudos SVG para equipos.
Crea un escudo simple con los colores del equipo.
"""
import os


def _abreviacion(nombre: str) -> str:
    """Genera una abreviación de 3 letras para el nombre del equipo."""
    palabras = [p for p in nombre.upper().split() if p not in
                ("FC", "AC", "AS", "CF", "CD", "SD", "UD", "US", "SC", "SS",
                 "DE", "DEL", "LA", "EL", "LOS", "LAS", "THE", "AFC", "FSV",
                 "TSG", "VFB", "VFL", "SV", "RB", "TSV", "SSD", "ASD", "ASD",
                 "SPORT", "CLUB", "CALCIO", "1907", "1908", "1909", "1910",
                 "1911", "1912", "1913", "1919", "1920", "1922", "1924", "1928",
                 "1929", "1932", "1946")]
    if len(palabras) == 0:
        return nombre[:3].upper()
    if len(palabras) == 1:
        return palabras[0][:3]
    if len(palabras) == 2:
        return palabras[0][:2] + palabras[1][0]
    return palabras[0][0] + palabras[1][0] + palabras[2][0]


def generar_svg(equipo_id: int, nombre: str, color1: str, color2: str) -> str:
    """Genera el contenido SVG de un escudo de equipo."""
    abr = _abreviacion(nombre)

    # Determinar color del texto (contraste)
    def luminancia(hex_color: str) -> float:
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return 0.299 * r + 0.587 * g + 0.114 * b

    texto_color = "#000000" if luminancia(color1) > 128 else "#FFFFFF"
    texto_color_alt = "#000000" if luminancia(color2) > 128 else "#FFFFFF"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 120" width="100" height="120">
  <!-- Fondo del escudo -->
  <path d="M50,4 L96,22 L96,66 Q96,98 50,116 Q4,98 4,66 L4,22 Z"
        fill="{color1}" stroke="{color2}" stroke-width="4"/>
  <!-- Franja vertical central -->
  <path d="M38,4 L62,4 L62,116 Q56,118 50,116 Q44,118 38,116 Z"
        fill="{color2}" opacity="0.35"/>
  <!-- Banda horizontal superior -->
  <rect x="4" y="38" width="92" height="20" fill="{color2}" opacity="0.25"/>
  <!-- Texto abreviación -->
  <text x="50" y="72"
        font-family="Arial Black, Arial, sans-serif"
        font-weight="900"
        font-size="22"
        text-anchor="middle"
        fill="{texto_color}"
        stroke="{texto_color_alt}"
        stroke-width="0.5"
        paint-order="stroke">{abr}</text>
  <!-- Borde exterior -->
  <path d="M50,4 L96,22 L96,66 Q96,98 50,116 Q4,98 4,66 L4,22 Z"
        fill="none" stroke="{color2}" stroke-width="3"/>
</svg>"""
    return svg


def generar_todos_los_escudos(equipos: list, output_dir: str) -> None:
    """Genera archivos SVG para todos los equipos."""
    badges_dir = os.path.join(output_dir, "..", "assets", "badges")
    badges_dir = os.path.normpath(badges_dir)
    os.makedirs(badges_dir, exist_ok=True)

    for equipo in equipos:
        eid = equipo["id"]
        nombre = equipo["nombre"]
        color1 = equipo.get("color_principal", "#003DA5")
        color2 = equipo.get("color_secundario", "#FFFFFF")

        svg_content = generar_svg(eid, nombre, color1, color2)
        ruta = os.path.join(badges_dir, f"{eid}.svg")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(svg_content)

    print(f"  OK {len(equipos)} escudos SVG -> {badges_dir}")
