PLAN MAESTRO: PC FÚTBOL 2026
FASE 0 — ENTORNO DE DESARROLLO
Duración estimada: 1-2 horas

1. Instalar Godot 4
Descargar Godot 4.x (última estable) desde godotengine.org
Versión: Godot 4.3+ (con .NET si quieres C#, pero nosotros usaremos GDScript puro)
Sin instalador — es un ejecutable portable. Extráelo en C:\Godot\
2. Instalar Python (para el Scraper)
Python 3.12+ desde python.org
Verificar: python --version en terminal
Librerías: pip install requests beautifulsoup4 selenium pandas
3. Editor de código: VSCode (ya tienes Claude Code aquí)
Extensión: godot-tools (autocompletado GDScript)
Extensión: Python (para el scraper)
4. Git — ya configurado ✓
FASE 1 — ESQUELETO DEL PROYECTO
Sistemas: Estructura de carpetas + Autoloads vacíos

Crear la estructura de proyecto Godot con todas las carpetas según tu diseño y los 4 sistemas del núcleo (S01-S04) como stubs vacíos que ya se comunican entre sí.


pc_futbol_2026/
├── core/           ← S01-S08 (GDScript)
├── match/          ← S05 Motor 3D
├── ui/             ← Pantallas y HUD
├── data/
│   ├── initial/    ← JSONs del scraper (read-only)
│   └── saves/      ← Partidas guardadas
├── assets/
│   ├── models/     ← Modelos 3D jugadores/campo
│   ├── textures/
│   ├── audio/
│   └── fonts/
└── scraper/        ← Python scripts
Entregable: Proyecto Godot arranca, los 4 Autoloads están registrados, sin errores.

FASE 2 — DATOS Y SCRAPER
Sistemas: S03 Database + scraper Python

Construir el scraper Python que genera los JSONs de datos reales, y el sistema de base de datos en Godot que los carga.

Fuentes de datos (gratuitas/legales):

transfermarkt.com — valores de mercado, contratos
fbref.com — estadísticas reales
sofifa.com — atributos estilo FIFA
worldfootball.net — historial
Entregable: JSON con ~500 jugadores cargados en Godot, consultables.

FASE 3 — NÚCLEO DEL JUEGO
Sistemas: S01 GameManager + S02 Calendar + S04 Save/Load

El "reloj" del juego funciona: puedes avanzar días/semanas, los eventos se programan, y puedes guardar/cargar partida.

Entregable: Consola de debug que muestra fecha avanzando, eventos disparándose, save/load funcionando.

FASE 4 — LIGAS Y COMPETICIONES
Sistemas: S06 Simulation Engine + S07 League System + S08 Referee

Una liga de 20 equipos simula toda una temporada en segundos. Resultados, clasificación, ascensos/descensos.

Entregable: Liga española simulada completa, clasificación correcta al final.

FASE 5 — GESTIÓN ECONÓMICA
Sistemas: S09 Economy + S10 Transfer Market

Las finanzas del club funcionan. Puedes comprar/vender jugadores. La IA también ficha.

Entregable: Una temporada completa con mercado de fichajes funcional.

FASE 6 — PANTALLAS DE GESTIÓN (UI)
Sistemas: UI Layer completo

Todas las pantallas de gestión: despacho, plantilla, tácticas, finanzas, mercado, clasificación, calendario.

Entregable: Juego de gestión 2D completamente jugable (sin motor 3D).

FASE 7 — MOTOR 3D: CAMPO Y BALÓN
Sistemas: S05 Match Engine 3D — parte 1

El campo 3D con líneas, porterías y física del balón. Puedes lanzar el balón y se comporta correctamente.

Assets necesarios aquí:

Campo: se genera proceduralmente (MeshInstance3D)
Balón: modelo low-poly descargado de Kenney.nl (gratuito) o OpenGameArt.org
FASE 8 — MOTOR 3D: JUGADORES E IA
Sistemas: S05 Match Engine 3D — parte 2

22 jugadores en campo con animaciones básicas e IA funcional. Partido jugable de principio a fin.

Assets necesarios aquí — MODELOS 3D:

Opción A (recomendada): Modelos low-poly de Kenney.nl → "Sports Kit" o similares
Opción B: Generar con Mixamo (Adobe, gratuito) — personajes + animaciones
Opción C: Usar Ready Player Me para personajes más detallados
Assets de audio:

Freesound.org — silbatos, multitud, golpe de balón
OpenGameArt.org — música de fondo
FASE 9 — SISTEMAS AVANZADOS
Sistemas: S11 Staff + S12 Stadium + S13 Youth + S14 Training + S15 Board + S16 News

Los sistemas de profundidad que hacen el juego rico: cantera, entrenamiento, directiva, noticias.

FASE 10 — PULIDO Y LANZAMIENTO
Audio completo
Internacionalización (ES/EN)
Menú principal con música
Tutorial
Optimización de rendimiento
RESUMEN DE ASSETS NECESARIOS
Asset	Fuente	Coste
Modelos 3D jugadores	Kenney.nl o Mixamo	Gratis
Animaciones	Mixamo	Gratis
Campo 3D	Procedural en Godot	—
Balón	Kenney.nl o Sketchfab	Gratis
Iconos UI	Kenney.nl UI Pack	Gratis
Fuentes	Google Fonts	Gratis
Audio SFX	Freesound.org	Gratis
Música	OpenGameArt.org	Gratis
Fotos jugadores	Placeholder generadas	—