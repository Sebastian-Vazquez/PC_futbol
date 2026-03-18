┌─────────────────────────────────────────────────────────────────┐
│                      PC FÚTBOL 2026                             │
│                   ARQUITECTURA GENERAL                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐    ┌──────────────────────────────────────────┐   │
│  │ SCRAPER  │───▶│           DATA LAYER (JSON/DB)           │   │
│  │ (Python) │    │  Jugadores · Equipos · Ligas · Estadios  │   │
│  └──────────┘    └────────────────┬─────────────────────────┘   │
│                                   │                             │
│                                   ▼                             │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    GAME MANAGER (Singleton)                │ │
│  │         Estado global · Guardado · Calendario              │ │
│  └──────┬──────────┬──────────┬──────────┬───────────────────┘ │
│         │          │          │          │                      │
│         ▼          ▼          ▼          ▼                      │
│  ┌──────────┐ ┌─────────┐ ┌────────┐ ┌──────────┐             │
│  │SIMULATION│ │ MATCH   │ │ECONOMY │ │ TRANSFER │             │
│  │  ENGINE  │ │ENGINE 3D│ │ SYSTEM │ │  MARKET  │             │
│  │          │ │(Jugable)│ │        │ │          │             │
│  └──────────┘ └─────────┘ └────────┘ └──────────┘             │
│         │          │          │          │                      │
│         ▼          ▼          ▼          ▼                      │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                     UI LAYER                               │ │
│  │  Despacho · Plantilla · Táctica · Finanzas · Estadio      │ │
│  │  Calendario · Clasificación · Noticias · Fichajes          │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                   PERSISTENCE LAYER                        │ │
│  │              Guardado · Carga · Autosave                   │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│                  MAPA DE SISTEMAS                          │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  🔵 NÚCLEO (Core)                                         │
│  ├── S01. Game Manager (orquestador global)                │
│  ├── S02. Calendar & Time System                           │
│  ├── S03. Database System                                  │
│  └── S04. Save/Load System                                 │
│                                                            │
│  ⚽ FÚTBOL (Match)                                         │
│  ├── S05. Match Engine 3D (jugable)                        │
│  ├── S06. Match Simulation Engine (simulación rápida)      │
│  ├── S07. League & Competition System                      │
│  └── S08. Referee & Rules System                           │
│                                                            │
│  💰 GESTIÓN (Management)                                   │
│  ├── S09. Economy & Finance System                         │
│  ├── S10. Transfer Market System                           │
│  ├── S11. Staff & Personnel System                         │
│  ├── S12. Stadium & Infrastructure System                  │
│  └── S13. Youth Academy System                             │
│                                                            │
│  👥 PERSONAS (People)                                      │
│  ├── S14. Player Development & Training System             │
│  └── S15. Board & Directors System                         │
│                                                            │
│  📰 PRESENTACIÓN (Presentation)                            │
│  └── S16. News & Media System                              │
│                                                            │
└────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ S01. GAME MANAGER                               │
├─────────────────────────────────────────────────┤
│                                                 │
│ RESPONSABILIDAD:                                │
│ Orquestar TODOS los sistemas. Punto central     │
│ de comunicación. Controla el flujo del juego.   │
│                                                 │
│ DATOS QUE MANTIENE:                             │
│ ├── estado_juego (menú/jugando/partido/pausa)   │
│ ├── equipo_jugador (referencia)                 │
│ ├── temporada_actual                            │
│ ├── fecha_actual                                │
│ ├── configuración (dificultad, idioma, etc.)    │
│ └── referencias a todos los subsistemas         │
│                                                 │
│ FUNCIONES PRINCIPALES:                          │
│ ├── iniciar_nueva_partida(equipo, liga)          │
│ ├── cargar_partida(slot)                        │
│ ├── guardar_partida(slot)                       │
│ ├── avanzar_dia()                               │
│ ├── avanzar_semana()                            │
│ ├── avanzar_hasta_proximo_evento()              │
│ ├── obtener_estado_global() → Dictionary        │
│ └── cambiar_escena(pantalla)                    │
│                                                 │
│ SEÑALES QUE EMITE:                              │
│ ├── dia_avanzado(fecha)                         │
│ ├── semana_avanzada(num_semana)                 │
│ ├── temporada_iniciada(año)                     │
│ ├── temporada_finalizada(año)                   │
│ └── evento_importante(tipo, datos)              │
│                                                 │
│ TIPO: Autoload/Singleton                        │
│ ARCHIVO: core/game_manager.gd                   │
│                                                 │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ S02. CALENDAR & TIME SYSTEM                     │
├─────────────────────────────────────────────────┤
│                                                 │
│ RESPONSABILIDAD:                                │
│ Gestionar el paso del tiempo. Programar         │
│ eventos futuros. Controlar ventanas de          │
│ fichajes, pretemporada, descansos.              │
│                                                 │
│ ESTRUCTURA TEMPORAL:                            │
│ ├── Temporada (Agosto año N → Junio año N+1)   │
│ ├── Meses                                       │
│ ├── Semanas (unidad de avance principal)        │
│ └── Días (para eventos específicos)             │
│                                                 │
│ CALENDARIO ANUAL:                               │
│ ├── JUL: Pretemporada, mercado abierto          │
│ ├── AGO: Inicio ligas, mercado cierra 31/8     │
│ ├── SEP-NOV: Liga + Copas + Champions          │
│ ├── DIC: Mundial de Clubes (si aplica)          │
│ ├── ENE: Mercado invernal (1-31 ene)            │
│ ├── FEB-ABR: Liga + Copas + Champions           │
│ ├── MAY: Finales, ascensos/descensos            │
│ ├── JUN: Fin temporada, renovaciones            │
│ │        Torneos de selecciones (si toca)       │
│ └── Fechas FIFA internacionales                 │
│                                                 │
│ EVENTOS PROGRAMABLES:                           │
│ ├── partidos (liga, copa, amistoso)             │
│ ├── apertura/cierre mercado                     │
│ ├── pago_salarios (semanal)                     │
│ ├── cobro_tv / cobro_sponsor                    │
│ ├── asamblea_directiva                          │
│ ├── sorteo_copa / sorteo_champions              │
│ ├── draft_juveniles                             │
│ └── fin_temporada_procesamiento                 │
│                                                 │
│ FUNCIONES:                                      │
│ ├── obtener_fecha_actual() → {d, m, a}          │
│ ├── avanzar(dias)                               │
│ ├── programar_evento(fecha, tipo, datos)        │
│ ├── obtener_proximos_eventos(n) → Array         │
│ ├── es_mercado_abierto() → bool                 │
│ ├── es_pretemporada() → bool                    │
│ ├── obtener_jornada_actual(liga) → int          │
│ └── generar_calendario_temporada(liga) → Array  │
│                                                 │
│ ARCHIVO: core/calendar_system.gd                │
│                                                 │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ S03. DATABASE SYSTEM                            │
├─────────────────────────────────────────────────┤
│                                                 │
│ RESPONSABILIDAD:                                │
│ Cargar, indexar y proveer acceso eficiente      │
│ a TODOS los datos del juego.                    │
│                                                 │
│ ORIGEN DE DATOS:                                │
│ ├── /data/initial/ → JSONs del scraper          │
│ │   (datos iniciales, no se modifican)          │
│ └── /saves/ → Estado modificado en partida      │
│                                                 │
│ ENTIDADES:                                      │
│ ├── Jugador (~100,000 registros)                │
│ ├── Equipo (~5,000 registros)                   │
│ ├── Liga (~200 registros)                       │
│ ├── País (~220 registros)                       │
│ ├── Estadio (~5,000 registros)                  │
│ ├── Staff (~20,000 registros)                   │
│ ├── Competición (~500 registros)                │
│ └── Sponsor (~1,000 registros)                  │
│                                                 │
│ ÍNDICES (para búsquedas rápidas):               │
│ ├── jugadores_por_equipo: {equipo_id: [jugadores]}│
│ ├── jugadores_por_posicion: {pos: [jugadores]}  │
│ ├── jugadores_por_pais: {pais: [jugadores]}     │
│ ├── equipos_por_liga: {liga_id: [equipos]}      │
│ ├── equipos_por_pais: {pais: [equipos]}         │
│ └── jugadores_libres: [jugadores sin equipo]    │
│                                                 │
│ FUNCIONES:                                      │
│ ├── cargar_todo()                               │
│ ├── obtener_jugador(id) → Jugador               │
│ ├── obtener_equipo(id) → Equipo                 │
│ ├── buscar_jugadores(filtros) → Array           │
│ │   filtros: posicion, edad_min, edad_max,      │
│ │   media_min, valor_max, nacionalidad, liga    │
│ ├── obtener_plantilla(equipo_id) → Array        │
│ ├── obtener_clasificacion(liga_id) → Array      │
│ ├── obtener_once_titular(equipo_id) → Array     │
│ ├── obtener_agentes_libres(filtros) → Array     │
│ └── actualizar_entidad(tipo, id, datos)         │
│                                                 │
│ FORMATO JSON DE DATOS:                          │
│                                                 │
│ jugador.json:                                   │
│ {                                               │
│   "id": 10001,                                  │
│   "nombre": "Lionel",                           │
│   "apellido": "Messi",                          │
│   "nombre_corto": "Messi",                      │
│   "fecha_nacimiento": "1987-06-24",             │
│   "nacionalidad": "ARG",                        │
│   "nacionalidad_secundaria": null,              │
│   "posicion_principal": "ED",                   │
│   "posiciones_secundarias": ["MCO", "DC"],      │
│   "pie_habil": "izquierdo",                     │
│   "altura_cm": 170,                             │
│   "peso_kg": 72,                                │
│   "equipo_id": 5001,                            │
│   "numero_camiseta": 10,                        │
│   "atributos": {                                │
│     "velocidad": 78, "aceleracion": 82,         │
│     "disparo": 88, "potencia_disparo": 80,      │
│     "pase_corto": 91, "pase_largo": 86,         │
│     "centro": 82, "regate": 93,                 │
│     "control": 95, "cabeceo": 65,               │
│     "defensa": 35, "entrada": 30,               │
│     "fisico": 60, "resistencia": 70,            │
│     "agresividad": 60, "vision": 95,            │
│     "compostura": 93, "posicionamiento_of": 90, │
│     "desmarque": 85, "tiro_lejano": 82,         │
│     "tiro_libre": 88, "penaltis": 75,           │
│     "efecto": 85                                │
│   },                                            │
│   "atributos_portero": null,                    │
│   "contrato": {                                 │
│     "salario_semanal": 500000,                  │
│     "clausula": 0,                              │
│     "fin_contrato": "2027-06-30",               │
│     "bonus_gol": 5000,                          │
│     "bonus_asistencia": 3000                    │
│   },                                            │
│   "valor_mercado": 25000000,                    │
│   "potencial": 88,                              │
│   "moral": 75,                                  │
│   "forma_fisica": 80,                           │
│   "personalidad": {                             │
│     "profesionalismo": 90,                      │
│     "ambicion": 85,                             │
│     "lealtad": 70,                              │
│     "temperamento": 65                          │
│   }                                             │
│ }                                               │
│                                                 │
│ equipo.json:                                    │
│ {                                               │
│   "id": 5001,                                   │
│   "nombre": "Inter Miami CF",                   │
│   "nombre_corto": "Inter Miami",                │
│   "pais": "USA",                                │
│   "liga_id": 301,                               │
│   "estadio": {                                  │
│     "nombre": "Chase Stadium",                  │
│     "capacidad": 21550,                         │
│     "estado": 80,                               │
│     "nivel_vip": 2,                             │
│     "nivel_museo": 0,                           │
│     "nivel_tienda": 1,                          │
│     "nivel_parking": 1,                         │
│     "ampliable": true,                          │
│     "coste_mantenimiento_semanal": 150000       │
│   },                                            │
│   "finanzas": {                                 │
│     "presupuesto_fichajes": 50000000,           │
│     "balance": 120000000,                       │
│     "deuda": 0,                                 │
│     "masa_salarial_semanal": 3500000,           │
│     "ingresos_tv_anual": 45000000,              │
│     "sponsor_camiseta": 15000000,               │
│     "sponsor_estadio": 5000000,                 │
│     "merchandising_anual": 8000000,             │
│     "precio_entrada_base": 45,                  │
│     "socios": 35000                             │
│   },                                            │
│   "tactica_default": "4-3-3",                   │
│   "color_principal": "#F7B5CD",                 │
│   "color_secundario": "#000000",                │
│   "reputacion": 78,                             │
│   "nivel_cantera": 3,                           │
│   "nivel_ojeadores": 2,                         │
│   "nivel_medicina": 3,                          │
│   "historia": {                                 │
│     "fundacion": 2018,                          │
│     "titulos_liga": 1,                          │
│     "titulos_copa": 1                           │
│   }                                             │
│ }                                               │
│                                                 │
│ ARCHIVO: core/database.gd                       │
│                                                 │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ S04. SAVE/LOAD SYSTEM                           │
├─────────────────────────────────────────────────┤
│                                                 │
│ RESPONSABILIDAD:                                │
│ Serializar/deserializar el estado completo      │
│ del juego. Autosave. Múltiples slots.           │
│                                                 │
│ LO QUE SE GUARDA:                               │
│ ├── Estado de TODOS los jugadores               │
│ │   (atributos, contratos, estadísticas)        │
│ ├── Estado de TODOS los equipos                 │
│ │   (finanzas, plantilla, estadio)              │
│ ├── Estado de TODAS las ligas                   │
│ │   (clasificación, calendario, resultados)     │
│ ├── Fecha y temporada actual                    │
│ ├── Historial de transferencias                 │
│ ├── Historial de resultados                     │
│ ├── Trofeos y records                           │
│ ├── Noticias generadas                          │
│ └── Configuración del jugador                   │
│                                                 │
│ FORMATO: JSON comprimido (.sav)                 │
│ SLOTS: 10 slots + 1 autosave                    │
│ AUTOSAVE: cada inicio de semana                 │
│                                                 │
│ FUNCIONES:                                      │
│ ├── guardar(slot_id)                            │
│ ├── cargar(slot_id) → bool                      │
│ ├── autosave()                                  │
│ ├── listar_saves() → Array[SaveInfo]            │
│ ├── borrar_save(slot_id)                        │
│ └── obtener_preview(slot_id) → SaveInfo         │
│     {equipo, fecha, liga, posición, temporada}  │
│                                                 │
│ ARCHIVO: core/save_system.gd                    │
│                                                 │
└─────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│ S05. MATCH ENGINE 3D (JUGABLE)                       │
├──────────────────────────────────────────────────────┤
│                                                      │
│ RESPONSABILIDAD:                                     │
│ Renderizar y ejecutar partidos de fútbol en 3D       │
│ con control directo del jugador (estilo PC Fútbol).  │
│ También permite "solo ver" (modo espectador).        │
│                                                      │
│ MODOS:                                               │
│ ├── JUGAR: El usuario controla su equipo             │
│ ├── VER: Ambos equipos controlados por IA            │
│ └── SIMULAR: Sin 3D, resultado instantáneo (→ S06)   │
│                                                      │
│ ESCENA 3D - COMPONENTES:                             │
│ ├── Campo (Pitch3D)                                  │
│ │   ├── Césped (MeshInstance3D + textura)            │
│ │   ├── Líneas de campo                              │
│ │   ├── Porterías (2x StaticBody3D)                  │
│ │   ├── Redes (SoftBody3D o animadas)                │
│ │   ├── Banquillos (decorativo)                      │
│ │   └── Público (sprites/partículas en gradas)       │
│ │                                                    │
│ ├── Balón (Ball3D)                                   │
│ │   ├── RigidBody3D con esfera de colisión           │
│ │   ├── Física: gravedad, rebote, efecto, fricción   │
│ │   ├── Estados: libre, controlado, en_vuelo,        │
│ │   │   en_red, fuera                                │
│ │   └── Trail visual (línea de trayectoria)          │
│ │                                                    │
│ ├── Jugadores (PlayerUnit3D) x22                     │
│ │   ├── CharacterBody3D                              │
│ │   ├── Modelo 3D low-poly                           │
│ │   │   ├── Cuerpo con colores del equipo            │
│ │   │   ├── Número en espalda                        │
│ │   │   └── Animaciones:                             │
│ │   │       ├── idle (parado)                        │
│ │   │       ├── run (correr)                         │
│ │   │       ├── sprint (sprint)                      │
│ │   │       ├── kick (chutar)                        │
│ │   │       ├── pass (pasar)                         │
│ │   │       ├── header (cabezazo)                    │
│ │   │       ├── tackle (entrada)                     │
│ │   │       ├── slide_tackle (barrida)               │
│ │   │       ├── celebrate (celebrar gol)             │
│ │   │       ├── gk_dive_left/right (portero)         │
│ │   │       ├── gk_catch (portero atrapa)            │
│ │   │       └── fall (caer por falta)                │
│ │   │                                                │
│ │   ├── IA de Jugador (PlayerAI)                     │
│ │   │   ├── Estados:                                 │
│ │   │   │   ├── SIN_BALON_ATACANDO (desmarque)      │
│ │   │   │   ├── SIN_BALON_DEFENDIENDO (marca)       │
│ │   │   │   ├── CON_BALON (decidir acción)          │
│ │   │   │   ├── PERSIGUIENDO_BALON                  │
│ │   │   │   ├── EN_POSICION (mantener formación)    │
│ │   │   │   └── FUERA_DE_JUEGO_IDLE                 │
│ │   │   ├── Decisiones basadas en atributos:        │
│ │   │   │   ├── vision → calidad de pases           │
│ │   │   │   ├── compostura → no perder balón        │
│ │   │   │   ├── agresividad → presión               │
│ │   │   │   └── posicionamiento → dónde estar       │
│ │   │   └── Influenciado por la táctica del equipo  │
│ │   │                                                │
│ │   └── Indicador (flecha/circle debajo)            │
│ │       ├── Amarillo: jugador seleccionado           │
│ │       └── Rojo: portador del balón rival           │
│ │                                                    │
│ ├── Cámaras                                         │
│ │   ├── Cámara TV (lateral, sigue balón)             │
│ │   ├── Cámara aérea (cenital)                       │
│ │   ├── Cámara detrás portería                       │
│ │   └── Cámara replay (goles)                        │
│ │                                                    │
│ ├── Árbitro (simplificado)                           │
│ │   ├── Detección de faltas por colisiones           │
│ │   ├── Fuera de juego (offside line)                │
│ │   ├── Saques de banda/puerta/esquina              │
│ │   ├── Tarjetas (basado en agresividad de falta)   │
│ │   └── Penaltis                                     │
│ │                                                    │
│ └── HUD del Partido                                 │
│     ├── Marcador (equipos, goles, minuto)            │
│     ├── Radar/minimapa                               │
│     ├── Indicador de stamina del jugador actual       │
│     ├── Nombre del jugador seleccionado              │
│     └── Eventos (gol, falta, cambio) en ticker       │
│                                                      │
│ CONTROLES JUGABLE:                                   │
│ ├── WASD / Flechas → Mover jugador seleccionado     │
│ ├── Espacio → Pase (dirección automática al mejor    │
│ │             compañero o manual con flechas)         │
│ ├── Shift → Disparo a puerta (potencia con          │
│ │           tiempo presionado)                        │
│ ├── E → Pase en profundidad / centro                 │
│ ├── Q → Cambiar jugador controlado                   │
│ ├── Ctrl → Sprint (gasta stamina)                    │
│ ├── X → Entrada / tackle                             │
│ ├── Z → Barrida (más agresiva, riesgo falta)        │
│ ├── Tab → Menú táctico rápido (pausado)              │
│ ├── 1,2,3 → Velocidad de juego (solo modo VER)      │
│ ├── P / Esc → Pausa                                  │
│ └── C → Cambiar cámara                               │
│                                                      │
│ MECÁNICAS DE BALÓN:                                  │
│ ├── Pase rastrero: velocidad media, precisión alta   │
│ ├── Pase largo: arco parabólico                      │
│ ├── Centro: alto, hacia área                         │
│ ├── Disparo: fuerza + dirección + efecto             │
│ ├── Cabezazo: si balón alto y jugador cerca          │
│ ├── Control: al recibir, basado en atributo          │
│ │   (mal control = balón se aleja)                   │
│ ├── Regate: automático al ir con balón cerca         │
│ │   de rival (éxito basado en regate vs defensa)     │
│ └── Efecto: basado en atributo + input               │
│                                                      │
│ MECÁNICAS DE PORTERO (IA):                           │
│ ├── Posicionamiento automático                       │
│ ├── Reflejos → tiempo de reacción a disparo          │
│ ├── Estirada → rango de alcance                      │
│ ├── Saque → precisión de distribución                │
│ ├── 1vs1 → salir a achicar                           │
│ └── Atrapar vs Rechazar (basado en parada attr)      │
│                                                      │
│ FLUJO DE UN PARTIDO:                                 │
│ ├── 1. Pantalla previa (alineaciones, táctica)       │
│ ├── 2. Animación de entrada                          │
│ ├── 3. Primera parte (45 min simulados)              │
│ ├── 4. Entretiempo (cambios, táctica)                │
│ ├── 5. Segunda parte                                 │
│ ├── 6. Prórroga (si aplica en copa)                  │
│ ├── 7. Penaltis (si aplica)                          │
│ ├── 8. Pantalla de resultado/estadísticas            │
│ └── 9. Vuelta al modo gestión                        │
│                                                      │
│ ARCHIVOS:                                            │
│ ├── match/match_manager.gd (orquesta el partido)     │
│ ├── match/ball.gd                                    │
│ ├── match/player_unit.gd                             │
│ ├── match/player_ai.gd                               │
│ ├── match/team_ai.gd (IA táctica del equipo)         │
│ ├── match/referee.gd                                 │
│ ├── match/match_camera.gd                            │
│ ├── match/match_hud.gd                               │
│ └── match/match_physics.gd (helpers física balón)    │
│                                                      │
└──────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ S06. MATCH SIMULATION ENGINE                    │
├─────────────────────────────────────────────────┤
│                                                 │
│ RESPONSABILIDAD:                                │
│ Simular partidos SIN renderizar 3D.             │
│ Para partidos que no son del jugador o cuando   │
│ elige "simular rápido". Genera resultado +      │
│ eventos + estadísticas.                         │
│                                                 │
│ ALGORITMO:                                      │
│ ├── Calcula "fuerza de equipo" (media ponderada │
│ │   de titulares + bonus táctica + moral +      │
│ │   ventaja local + racha)                      │
│ ├── Simula minuto a minuto (90 iteraciones)     │
│ ├── Cada minuto:                                │
│ │   ├── ¿Quién tiene posesión? (probabilidad)   │
│ │   ├── ¿Genera ocasión? (ataque vs defensa)    │
│ │   ├── ¿Ocasión = gol? (disparo vs portero)    │
│ │   ├── ¿Hay falta? (agresividad)              │
│ │   ├── ¿Hay tarjeta?                           │
│ │   ├── ¿Hay lesión?                            │
│ │   └── ¿Hay cambio (IA)?                       │
│ ├── Genera eventos textuales                     │
│ │   ("Min 34: ¡Gol de Mbappé! Asist: Vinícius")│
│ └── Actualiza estadísticas de jugadores          │
│                                                 │
│ OUTPUT:                                         │
│ {                                               │
│   "local": "Real Madrid",                       │
│   "visitante": "Barcelona",                     │
│   "goles_local": 2,                             │
│   "goles_visitante": 1,                         │
│   "goleadores": [...],                          │
│   "asistentes": [...],                          │
│   "tarjetas": [...],                            │
│   "lesiones": [...],                            │
│   "posesion": [55, 45],                         │
│   "disparos": [12, 8],                          │
│   "corners": [6, 3],                            │
│   "eventos": [                                  │
│     {"min": 23, "tipo": "gol", ...},            │
│     {"min": 45, "tipo": "amarilla", ...}        │
│   ],                                            │
│   "puntuaciones_jugadores": {...}               │
│ }                                               │
│                                                 │
│ ARCHIVO: core/match_simulation.gd               │
│                                                 │
└─────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────┐
│ S07. LEAGUE & COMPETITION SYSTEM                  │
├───────────────────────────────────────────────────┤
│                                                   │
│ RESPONSABILIDAD:                                  │
│ Gestionar TODAS las competiciones del juego.      │
│                                                   │
│ TIPOS DE COMPETICIÓN:                             │
│ ├── LIGA (round-robin ida/vuelta)                 │
│ │   ├── Clasificación por puntos (3-1-0)         │
│ │   ├── Desempate: GD, GF, H2H                  │
│ │   ├── Ascensos (top N suben)                   │
│ │   ├── Descensos (bottom N bajan)               │
│ │   ├── Playoffs ascenso (configurable)          │
│ │   └── Plazas europeas/internacionales          │
│ │                                                 │
│ ├── COPA NACIONAL (eliminatorias)                 │
│ │   ├── Sorteo por bombos                        │
│ │   ├── Ida/vuelta o partido único               │
│ │   ├── Prórroga + penaltis                      │
│ │   └── Equipos de divisiones inferiores          │
│ │                                                 │
│ ├── SUPERCOPA (finalistas liga + copa)            │
│ │                                                 │
│ ├── CHAMPIONS LEAGUE / LIBERTADORES               │
│ │   ├── Clasificación por posición en liga        │
│ │   ├── Fase de grupos (nuevo formato 2024+)     │
│ │   ├── Eliminatorias                             │
│ │   └── Final                                     │
│ │                                                 │
│ ├── EUROPA LEAGUE / SUDAMERICANA                   │
│ │                                                 │
│ └── MUNDIAL DE CLUBES                              │
│                                                   │
│ LIGAS INCLUIDAS (objetivo total):                 │
│ ├── 🇪🇸 España: 1a, 2a, 2aB, 3a                  │
│ ├── 🇬🇧 Inglaterra: Premier, Champion, L1, L2,   │
│ │                    National League               │
│ ├── 🇮🇹 Italia: Serie A, Serie B                  │
│ ├── 🇩🇪 Alemania: Bundesliga, 2.Bundesliga       │
│ ├── 🇫🇷 Francia: Ligue 1, Ligue 2               │
│ ├── 🇦🇷 Argentina: Primera, Nacional B, Primera B│
│ ├── 🇧🇷 Brasil: Série A, Série B                 │
│ ├── 🇲🇽 México: Liga MX                          │
│ ├── 🇺🇸 USA: MLS                                 │
│ ├── 🇵🇹 Portugal: Primeira Liga                  │
│ ├── 🇳🇱 Holanda: Eredivisie                      │
│ ├── 🇹🇷 Turquía: Süper Lig                       │
│ ├── ... (50+ países objetivo)                     │
│ └── Ligas menores generadas proceduralmente       │
│                                                   │
│ FUNCIONES:                                        │
│ ├── crear_liga(equipos, config)                   │
│ ├── generar_calendario_liga(liga_id)               │
│ ├── registrar_resultado(liga_id, jornada, result) │
│ ├── obtener_clasificacion(liga_id) → Array        │
│ ├── obtener_proxima_jornada(liga_id) → Array      │
│ ├── procesar_fin_temporada(liga_id)               │
│ │   ├── calcular_ascensos()                       │
│ │   ├── calcular_descensos()                      │
│ │   └── asignar_plazas_europeas()                 │
│ ├── crear_copa(equipos, formato)                  │
│ ├── sorteo_copa(copa_id, ronda)                   │
│ └── crear_champions(equipos_clasificados)          │
│                                                   │
│ ARCHIVO: core/league_system.gd                    │
│                                                   │
└───────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ S08. REFEREE & RULES SYSTEM                     │
├─────────────────────────────────────────────────┤
│                                                 │
│ RESPONSABILIDAD:                                │
│ Reglas del fútbol aplicadas tanto en 3D como    │
│ en simulación.                                  │
│                                                 │
│ REGLAS IMPLEMENTADAS:                           │
│ ├── Fuera de juego (offside)                    │
│ ├── Faltas y tiros libres                       │
│ ├── Penaltis                                    │
│ ├── Tarjetas amarillas y rojas                  │
│ ├── Doble amarilla = roja                       │
│ ├── Acumulación tarjetas = sanción              │
│ │   (5 amarillas = 1 partido, configurable)     │
│ ├── Saques de banda, esquina, puerta            │
│ ├── Tiempo añadido                              │
│ ├── Sustituciones (5 en 3 ventanas)             │
│ ├── Prórroga (2x15 min)                         │
│ └── Tanda de penaltis                           │
│                                                 │
│ ARCHIVO: core/referee_system.gd                 │
│                                                 │
└─────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────┐
│ S09. ECONOMY & FINANCE SYSTEM                         │
├───────────────────────────────────────────────────────┤
│                                                       │
│ RESPONSABILIDAD:                                      │
│ TODO el flujo de dinero del club.                     │
│                                                       │
│ INGRESOS:                                             │
│ ├── 🎫 TAQUILLA                                      │
│ │   ├── Asistencia = f(reputación, rival,             │
│ │   │   importancia partido, precio, clima, racha)    │
│ │   ├── Precio entrada configurable por zona:         │
│ │   │   ├── General                                   │
│ │   │   ├── Tribuna                                   │
│ │   │   ├── VIP / Palcos                              │
│ │   │   └── Grada animación                           │
│ │   └── Eventos especiales (clásicos) = +precio       │
│ │                                                     │
│ ├── 📺 DERECHOS DE TV                                 │
│ │   ├── Contrato anual negociable                     │
│ │   ├── Depende de: liga, posición, audiencia         │
│ │   ├── PPV para partidos especiales                  │
│ │   └── Reparto equitativo vs proporcional            │
│ │                                                     │
│ ├── 👕 SPONSORS                                       │
│ │   ├── Camiseta (frontal): el más caro               │
│ │   ├── Camiseta (manga)                              │
│ │   ├── Camiseta (espalda)                            │
│ │   ├── Pantalón                                      │
│ │   ├── Estadio (naming rights)                       │
│ │   ├── Vallas publicitarias                          │
│ │   ├── Sponsor de entrenamiento                      │
│ │   └── Duración: 1-5 temporadas                     │
│ │   └── Valor = f(reputación, audiencia, éxitos)      │
│ │                                                     │
│ ├── 🛍️ MERCHANDISING                                 │
│ │   ├── Venta de camisetas (más si hay estrella)      │
│ │   ├── Bufandas, gorras, etc.                        │
│ │   ├── Nivel de tienda oficial afecta ventas         │
│ │   └── Ventas online (proporcional a socios)         │
│ │                                                     │
│ ├── 🏟️ SOCIOS / ABONADOS                             │
│ │   ├── Cuota mensual/anual                           │
│ │   ├── Cantidad = f(reputación, éxitos, precio)      │
│ │   └── Beneficios: ingreso estable                   │
│ │                                                     │
│ ├── 🏆 PREMIOS POR COMPETICIÓN                        │
│ │   ├── Liga: premio por posición final               │
│ │   ├── Copa: premio por ronda alcanzada              │
│ │   ├── Champions: premio por fase + pool TV          │
│ │   └── Supercopa, Mundial Clubes                     │
│ │                                                     │
│ └── 💸 VENTAS DE JUGADORES                            │
│     └── Plusvalías (vendido - comprado = ganancia)     │
│                                                       │
│ GASTOS:                                               │
│ ├── 💰 SALARIOS (semanal)                             │
│ │   ├── Jugadores (el gasto más grande)               │
│ │   ├── Staff técnico                                 │
│ │   ├── Staff médico                                  │
│ │   ├── Ojeadores                                     │
│ │   ├── Personal estadio                              │
│ │   └── Directiva                                     │
│ │                                                     │
│ ├── 🏗️ INFRAESTRUCTURA                               │
│ │   ├── Mantenimiento estadio                         │
│ │   ├── Mantenimiento ciudad deportiva                │
│ │   ├── Ampliaciones / construcciones                 │
│ │   └── Mejoras instalaciones                         │
│ │                                                     │
│ ├── ⚽ FICHAJES                                       │
│ │   ├── Traspaso (pago único o plazos)                │
│ │   ├── Prima de fichaje al jugador                   │
│ │   ├── Comisión de agente (3-10%)                    │
│ │   └── Cesiones (pago parcial salario)               │
│ │                                                     │
│ ├── 🏥 MÉDICO                                        │
│ │   ├── Tratamiento lesiones                          │
│ │   └── Mejor staff = recuperación más rápida         │
│ │                                                     │
│ ├── ⚖️ MULTAS                                        │
│ │   ├── Sanciones disciplinarias                      │
│ │   └── Fair Play Financiero (si lo implementamos)    │
│ │                                                     │
│ └── 🏦 INTERESES DE DEUDA                             │
│     ├── Préstamo bancario disponible                  │
│     └── Interés mensual sobre deuda                   │
│                                                       │
│ BALANCE Y REPORTES:                                   │
│ ├── Balance semanal (mini resumen)                    │
│ ├── Balance mensual (detallado)                       │
│ ├── Balance de temporada (completo)                   │
│ ├── Gráficos de evolución                             │
│ ├── Comparativa con otros clubes                      │
│ └── Alertas: "¡Estás en números rojos!"              │
│                                                       │
│ CONSECUENCIAS ECONÓMICAS:                             │
│ ├── Balance negativo prolongado:                      │
│ │   ├── Directiva fuerza ventas                       │
│ │   ├── No puedes fichar                              │
│ │   ├── Jugadores piden salir                         │
│ │   └── Ultimátum: vende o despedido                  │
│ ├── Superávit: directiva feliz, más presupuesto      │
│ └── Fair Play: no gastar más de X% en salarios       │
│                                                       │
│ ARCHIVO: core/economy_system.gd                       │
│                                                       │
└───────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────┐
│ S10. TRANSFER MARKET SYSTEM                       │
├───────────────────────────────────────────────────┤
│                                                   │
│ RESPONSABILIDAD:                                  │
│ Todo lo relacionado con compra/venta/cesión       │
│ de jugadores.                                     │
│                                                   │
│ TIPOS DE OPERACIÓN:                               │
│ ├── COMPRA DIRECTA                                │
│ │   ├── Hacer oferta al club                      │
│ │   ├── Club acepta/rechaza/contraoferta          │
│ │   ├── Si acepta → negociar con jugador          │
│ │   │   (salario, duración, prima, cláusula)      │
│ │   ├── Pago: inmediato o en plazos               │
│ │   ├── Cláusula de rescisión: pago directo       │
│ │   └── Variables del jugador para aceptar:       │
│ │       ambición, lealtad, salario, proyecto,     │
│ │       reputación club, liga, compañeros         │
│ │                                                 │
│ ├── VENTA                                         │
│ │   ├── Poner en venta (otros clubs hacen oferta) │
│ │   ├── Aceptar/rechazar ofertas                  │
│ │   └── Jugador puede negarse a ir                │
│ │                                                 │
│ ├── CESIÓN (Préstamo)                             │
│ │   ├── Con opción de compra                      │
│ │   ├── Sin opción                                │
│ │   ├── Pago parcial/total del salario            │
│ │   └── Duración: 6 meses o 1 temporada          │
│ │                                                 │
│ ├── AGENTE LIBRE                                  │
│ │   ├── Jugadores sin contrato                    │
│ │   ├── Solo negociar con jugador                 │
│ │   └── Prima de fichaje más alta                 │
│ │                                                 │
│ ├── INTERCAMBIO                                   │
│ │   └── Jugador + dinero por jugador              │
│ │                                                 │
│ └── CESIÓN DE CANTERA                             │
│     └── Enviar juvenil a equipo menor             │
│         para que juegue y se desarrolle           │
│                                                   │
│ MERCADO IA:                                       │
│ ├── Otros equipos también fichan entre sí         │
│ ├── Lógica: equipos ricos buscan estrellas        │
│ │   equipos medios buscan calidad/precio          │
│ │   equipos pobres buscan cesiones y jóvenes      │
│ ├── Deadline day (último día = locura de          │
│ │   fichajes, más ofertas, precios inflados)      │
│ └── Enero: mercado más conservador                │
│                                                   │
│ INTERFAZ:                                         │
│ ├── Lista de transferibles (filtrable)            │
│ ├── Buscador de jugadores (con filtros)           │
│ ├── Ofertas recibidas                             │
│ ├── Ofertas enviadas (estado: pendiente,          │
│ │   aceptada, rechazada)                          │
│ ├── Negociación (pantalla dedicada)               │
│ └── Historial de fichajes                         │
│                                                   │
│ ARCHIVO: core/transfer_system.gd                  │
│                                                   │
└───────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│ S11. STAFF & PERSONNEL SYSTEM                        │
├──────────────────────────────────────────────────────┤
│                                                      │
│ TIPOS DE STAFF:                                      │
│ ├── 🧑‍💼 SEGUNDO ENTRENADOR (1-2)                    │
│ │   ├── Atributos: táctica, motivación,              │
│ │   │   trabajo_jóvenes, defensa, ataque             │
│ │   ├── Afecta: rendimiento táctico,                 │
│ │   │   moral del equipo                             │
│ │   └── Puede sugerir alineaciones y cambios         │
│ │                                                    │
│ ├── 🏋️ PREPARADOR FÍSICO (1-2)                      │
│ │   ├── Atributos: preparacion, prevencion,          │
│ │   │   recuperacion, intensidad                     │
│ │   ├── Afecta: resistencia jugadores,               │
│ │   │   frecuencia lesiones musculares,              │
│ │   │   velocidad recuperación forma física          │
│ │   └── Mejor preparador = jugadores rinden          │
│ │       más en minutos finales                       │
│ │                                                    │
│ ├── 🏥 STAFF MÉDICO (1-5 doctores)                   │
│ │   ├── Atributos: cirugia, fisioterapia,            │
│ │   │   diagnostico, rehabilitacion                  │
│ │   ├── Afecta:                                      │
│ │   │   ├── Velocidad recuperación lesiones          │
│ │   │   ├── Precisión del diagnóstico                │
│ │   │   │   (tiempo estimado vs real)                │
│ │   │   ├── Prevención de recaídas                   │
│ │   │   └── Menos médicos = colas de tratamiento     │
│ │   └── Nivel de instalaciones médicas multiplica    │
│ │                                                    │
│ ├── 🔍 OJEADORES / SCOUTS (1-15)                    │
│ │   ├── Atributos: descubrimiento, juicio_talento,   │
│ │   │   red_contactos, conocimiento_regional         │
│ │   ├── Cada ojeador cubre REGIONES:                 │
│ │   │   ├── Se le asigna: "Sudamérica"              │
│ │   │   │   o "Europa del Este" o "África"           │
│ │   │   └── Mejor ojeador = encuentra mejores        │
│ │   │       jugadores ocultos en esa zona            │
│ │   ├── Afecta:                                      │
│ │   │   ├── Visibilidad de atributos reales          │
│ │   │   │   (sin scout ves ████ datos ocultos)       │
│ │   │   ├── Descubrir jugadores de ligas menores     │
│ │   │   ├── Informes: fiabilidad del potencial       │
│ │   │   └── Red de contactos: facilita fichajes      │
│ │   ├── Informe de ojeador:                          │
│ │   │   ├── ⭐ Básico (1 semana): nombre, pos,       │
│ │   │   │   media aprox, edad                        │
│ │   │   ├── ⭐⭐ Medio (3 semanas): atributos         │
│ │   │   │   principales, personalidad                │
│ │   │   └── ⭐⭐⭐ Completo (6 semanas): todo,         │
│ │   │       potencial, comparación con plantilla     │
│ │   └── Máximo ojeadores = f(nivel instalaciones)    │
│ │                                                    │
│ ├── 🎓 DIRECTOR CANTERA (1)                          │
│ │   ├── Atributos: formacion_jovenes,                │
│ │   │   descubrimiento_local, paciencia              │
│ │   ├── Afecta:                                      │
│ │   │   ├── Calidad de juveniles generados           │
│ │   │   ├── Velocidad desarrollo canteranos          │
│ │   │   └── Retención de promesas                    │
│ │   └── Trabaja en conjunto con ojeadores locales    │
│ │                                                    │
│ ├── 🗣️ DIRECTOR DEPORTIVO (1)                        │
│ │   ├── Atributos: negociacion, vision_mercado,      │
│ │   │   contactos_agentes, planificacion             │
│ │   ├── Afecta:                                      │
│ │   │   ├── Precio final de fichajes (-5% a -20%)   │
│ │   │   ├── Velocidad de negociaciones               │
│ │   │   ├── Ofertas que llegan por tus jugadores     │
│ │   │   └── Propone fichajes interesantes            │
│ │   └── Puede automatizar fichajes menores           │
│ │                                                    │
│ ├── 📢 DIRECTOR MARKETING (1)                        │
│ │   ├── Atributos: negociacion_sponsors,             │
│ │   │   creatividad, redes_sociales, eventos         │
│ │   ├── Afecta:                                      │
│ │   │   ├── Valor de contratos de sponsors           │
│ │   │   ├── Ingresos por merchandising               │
│ │   │   ├── Número de socios                         │
│ │   │   └── Reputación mediática del club            │
│ │   └── Propone campañas de marketing                │
│ │                                                    │
│ ├── 🏟️ JEFE DE OPERACIONES (1)                       │
│ │   ├── Atributos: gestion, logistica,               │
│ │   │   mantenimiento, organizacion_eventos          │
│ │   ├── Afecta:                                      │
│ │   │   ├── Coste mantenimiento estadio              │
│ │   │   ├── Velocidad construcciones                 │
│ │   │   ├── Calidad día de partido                   │
│ │   │   │   (afecta satisfacción público)            │
│ │   │   └── Gestión de personal de estadio           │
│ │   └── Necesario para obras grandes                 │
│ │                                                    │
│ └── 👨‍🍳 PERSONAL DE APOYO (cantidad)                │
│     ├── Utileros                                     │
│     ├── Jardineros (mantenimiento césped)            │
│     ├── Seguridad                                    │
│     ├── Taquilleros                                  │
│     └── Afectan costes operativos y calidad          │
│         de la experiencia en el estadio              │
│                                                      │
│ CONTRATACIÓN DE STAFF:                               │
│ ├── Mercado de staff (disponible todo el año)        │
│ ├── Cada staff tiene salario                         │
│ ├── Contratos de 1-3 años                            │
│ ├── Mejor staff = más caro                           │
│ ├── Staff puede ser robado por otros clubs           │
│ └── Staff envejece y se retira (55-70 años)          │
│                                                      │
│ FUNCIONES:                                           │
│ ├── contratar_staff(tipo, persona)                   │
│ ├── despedir_staff(persona)                          │
│ ├── listar_disponibles(tipo, filtros) → Array        │
│ ├── obtener_staff_actual() → Dictionary              │
│ ├── calcular_coste_salarial_staff() → int            │
│ ├── asignar_ojeador_region(ojeador, region)          │
│ ├── solicitar_informe(ojeador, jugador, nivel)       │
│ └── obtener_informes_pendientes() → Array            │
│                                                      │
│ ARCHIVO: core/staff_system.gd                        │
│                                                      │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│ S12. STADIUM & INFRASTRUCTURE SYSTEM                 │
├──────────────────────────────────────────────────────┤
│                                                      │
│ RESPONSABILIDAD:                                     │
│ Gestión del estadio, ciudad deportiva y todas        │
│ las instalaciones del club.                          │
│                                                      │
│ ═══════════════════════════════════════════           │
│ 🏟️ ESTADIO                                          │
│ ═══════════════════════════════════════════           │
│                                                      │
│ ZONAS DEL ESTADIO (cada una ampliable):              │
│ ├── 🪑 GRADAS                                       │
│ │   ├── Fondo Norte (grada animación)                │
│ │   ├── Fondo Sur                                    │
│ │   ├── Lateral Este                                 │
│ │   ├── Lateral Oeste (tribuna principal)            │
│ │   ├── Cada grada tiene:                            │
│ │   │   ├── Capacidad actual                         │
│ │   │   ├── Nivel (1-5): asientos, techo,            │
│ │   │   │   comodidad, baños, bares                  │
│ │   │   ├── Estado (0-100%): se deteriora            │
│ │   │   └── Coste ampliación: exponencial            │
│ │   └── Ampliación: +2000 a +10000 por obra          │
│ │                                                    │
│ ├── 🎩 PALCOS VIP                                    │
│ │   ├── Nivel 0-5                                    │
│ │   ├── Cada nivel: +20 palcos                       │
│ │   ├── Ingreso por palco MUCHO mayor que            │
│ │   │   entrada normal                               │
│ │   └── Atrae sponsors premium                       │
│ │                                                    │
│ ├── 🏪 TIENDA OFICIAL                                │
│ │   ├── Nivel 0 (sin tienda) a 5 (megastore)        │
│ │   ├── Afecta: ingresos merchandising               │
│ │   ├── Nivel 3+: tienda online                      │
│ │   └── Cada estrella fichada = pico de ventas       │
│ │                                                    │
│ ├── 🏛️ MUSEO DEL CLUB                                │
│ │   ├── Nivel 0-3                                    │
│ │   ├── Ingreso por visitas (turismo)                │
│ │   ├── Más trofeos ganados = más visitantes         │
│ │   └── Solo rentable para clubs grandes             │
│ │                                                    │
│ ├── 🍔 RESTAURANTE / HOSPITALITY                     │
│ │   ├── Nivel 0-3                                    │
│ │   ├── Ingresos día de partido                      │
│ │   └── Eventos corporativos entre semana            │
│ │                                                    │
│ ├── 🅿️ PARKING                                       │
│ │   ├── Nivel 0-3                                    │
│ │   ├── Ingreso por parking día de partido           │
│ │   └── Afecta satisfacción de público               │
│ │                                                    │
│ ├── 📺 SALA DE PRENSA                                │
│ │   ├── Nivel 0-3                                    │
│ │   └── Afecta: reputación mediática                 │
│ │                                                    │
│ ├── 🔦 ILUMINACIÓN                                   │
│ │   ├── Nivel 1-5                                    │
│ │   ├── Nivel 3+ requerido para competición europea  │
│ │   └── Afecta: derechos de TV (mejor imagen)        │
│ │                                                    │
│ ├── 📡 MARCADOR / PANTALLAS                          │
│ │   ├── Nivel 0-3                                    │
│ │   ├── Nivel 2: pantalla gigante                    │
│ │   └── Nivel 3: anillo LED 360° (más sponsors)      │
│ │                                                    │
│ └── 🌱 CÉSPED                                        │
│     ├── Natural nivel 1-3 / Híbrido / Sintético      │
│     ├── Afecta: calidad de juego, lesiones            │
│     ├── Mantenimiento continuo necesario             │
│     └── Jardineros afectan calidad                   │
│                                                      │
│ SISTEMA DE CONSTRUCCIÓN:                             │
│ ├── Cada obra tiene:                                 │
│ │   ├── Coste (€)                                    │
│ │   ├── Duración (semanas)                           │
│ │   ├── Requisito previo (ej: VIP requiere           │
│ │   │   grada lateral nivel 3+)                      │
│ │   └── Aforo reducido durante obras                 │
│ ├── Solo 1-2 obras simultáneas                       │
│ │   (más con mejor jefe de operaciones)              │
│ ├── Obras pueden retrasarse (clima, permisos)        │
│ └── Contratar constructora:                          │
│     ├── Barata: lenta, posibles problemas            │
│     ├── Media: estándar                              │
│     └── Premium: rápida, sin imprevistos, 2x coste  │
│                                                      │
│ ESTADIO NUEVO:                                       │
│ ├── Si llegas a cierto nivel, opción de              │
│ │   construir estadio NUEVO                          │
│ ├── Coste enorme (100M-1000M según capacidad)        │
│ ├── 2-4 temporadas de construcción                   │
│ ├── Mientras tanto juegas en estadio temporal         │
│ │   (alquilado, menos aforo)                         │
│ └── Naming rights: sponsor paga parte a cambio       │
│     del nombre ("Etihad Stadium")                    │
│                                                      │
│ ═══════════════════════════════════════════           │
│ 🏋️ CIUDAD DEPORTIVA                                 │
│ ═══════════════════════════════════════════           │
│                                                      │
│ INSTALACIONES:                                       │
│ ├── ⚽ CAMPOS DE ENTRENAMIENTO                       │
│ │   ├── Nivel 1-5 (1 campo tierra → 5 campos        │
│ │   │   de élite con tecnología)                     │
│ │   └── Afecta: calidad entrenamiento,               │
│ │       desarrollo jugadores                         │
│ │                                                    │
│ ├── 🏋️ GIMNASIO                                     │
│ │   ├── Nivel 1-5                                    │
│ │   └── Afecta: desarrollo físico, prevención        │
│ │       lesiones, recuperación                       │
│ │                                                    │
│ ├── 🏥 CENTRO MÉDICO                                 │
│ │   ├── Nivel 1-5                                    │
│ │   ├── Multiplica efecto del staff médico           │
│ │   └── Nivel 4+: crioterapia, última tecnología    │
│ │                                                    │
│ ├── 🎓 ACADEMIA / CANTERA                            │
│ │   ├── Nivel 1-5                                    │
│ │   ├── Nivel 1: solo juvenil A                      │
│ │   ├── Nivel 3: juvenil A + B + cadetes             │
│ │   ├── Nivel 5: academia completa (benjamín-juv)    │
│ │   ├── Afecta: calidad y cantidad de canteranos     │
│ │   │   generados cada temporada                     │
│ │   └── Mejor academia = jóvenes con más potencial   │
│ │                                                    │
│ ├── 🎬 SALA DE ANÁLISIS / VIDEO                      │
│ │   ├── Nivel 0-3                                    │
│ │   └── Afecta: preparación táctica de partidos      │
│ │       (bonus rendimiento vs rivales analizados)    │
│ │                                                    │
│ ├── 🍽️ COCINA / NUTRICIÓN                            │
│ │   ├── Nivel 0-3                                    │
│ │   └── Afecta: recuperación, forma física           │
│ │                                                    │
│ └── 🏠 RESIDENCIA JUVENIL                            │
│     ├── Nivel 0-3                                    │
│     ├── Necesaria para canteranos foráneos           │
│     └── Mejor residencia = atraer mejores jóvenes    │
│                                                      │
│ TABLA DE COSTES EJEMPLO:                             │
│ ┌────────────────────┬──────────┬──────────┐         │
│ │ Mejora             │ Coste    │ Semanas  │         │
│ ├────────────────────┼──────────┼──────────┤         │
│ │ Grada +5000 asient │ €8M      │ 16       │         │
│ │ VIP Nivel 1→2      │ €5M      │ 12       │         │
│ │ Tienda Nivel 0→1   │ €500K    │ 4        │         │
│ │ Tienda Nivel 2→3   │ €3M      │ 8        │         │
│ │ Museo Nivel 0→1    │ €2M      │ 8        │         │
│ │ Campo entren. 2→3  │ €4M      │ 10       │         │
│ │ Gimnasio 1→2       │ €1.5M    │ 6        │         │
│ │ Centro médico 3→4  │ €6M      │ 12       │         │
│ │ Academia 2→3       │ €8M      │ 16       │         │
│ │ Césped híbrido     │ €2M      │ 4        │         │
│ │ Pantalla LED 360°  │ €4M      │ 8        │         │
│ │ Estadio NUEVO 40K  │ €350M    │ 104 (2T) │         │
│ │ Estadio NUEVO 80K  │ €900M    │ 156 (3T) │         │
│ └────────────────────┴──────────┴──────────┘         │
│                                                      │
│ FUNCIONES:                                           │
│ ├── obtener_estadio() → StadiumData                  │
│ ├── obtener_ciudad_deportiva() → FacilityData        │
│ ├── iniciar_obra(tipo, nivel_destino)                │
│ ├── obtener_obras_en_curso() → Array                 │
│ ├── cancelar_obra(obra_id) → penalización           │
│ ├── calcular_capacidad_total() → int                 │
│ ├── calcular_coste_mantenimiento() → int             │
│ ├── calcular_ingresos_matchday(rival, comp) → int    │
│ ├── deteriorar_instalaciones() → called weekly       │
│ ├── obtener_mejoras_disponibles() → Array            │
│ └── puede_jugar_competicion(comp) → bool             │
│     (¿cumple requisitos mínimos de la UEFA etc?)     │
│                                                      │
│ ARCHIVO: core/stadium_system.gd                      │
│                                                      │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│ S13. YOUTH ACADEMY SYSTEM                            │
├──────────────────────────────────────────────────────┤
│                                                      │
│ RESPONSABILIDAD:                                     │
│ Generación, desarrollo y promoción de canteranos.    │
│                                                      │
│ GENERACIÓN DE CANTERANOS:                            │
│ ├── Cada temporada (junio/julio):                    │
│ │   ├── Se generan 3-15 jugadores nuevos             │
│ │   │   (cantidad = f(nivel_academia,                │
│ │   │    director_cantera, residencia))              │
│ │   ├── Calidad = f(nivel_academia, país,            │
│ │   │   director_cantera, reputación club)           │
│ │   ├── Nacionalidad: mayoría local +                │
│ │   │   algunos extranjeros si hay residencia        │
│ │   └── Edad: 16-17 años                            │
│ │                                                    │
│ ├── Generación procedural:                           │
│ │   ├── Nombre generado por base de datos            │
│ │   │   de nombres del país                          │
│ │   ├── Posición: aleatoria con tendencias           │
│ │   ├── Atributos: media 35-55 (son jóvenes)        │
│ │   ├── Potencial: 55-95 (la joya oculta)           │
│ │   ├── Potencial REAL vs ESTIMADO                   │
│ │   │   (el estimado puede fallar ±10)               │
│ │   └── Personalidad generada aleatoriamente         │
│ │                                                    │
│ └── Jugadores "joya":                                │
│     ├── 5% probabilidad de generar un crack          │
│     │   (potencial 85+)                              │
│     ├── 0.5% probabilidad de "generacional"          │
│     │   (potencial 90+)                              │
│     └── Mejor academia = más probabilidad            │
│                                                      │
│ DESARROLLO DE CANTERANOS:                            │
│ ├── Entrenamiento semanal en academia                │
│ │   ├── Plan: técnico, físico, táctico, mixto        │
│ │   └── Crecimiento = f(edad, potencial,             │
│ │       entrenamiento, staff, instalaciones)         │
│ ├── Juegan partidos de juveniles (simulados)         │
│ │   ├── Informe semanal de rendimiento               │
│ │   └── Partidos = experiencia = crecimiento         │
│ ├── Cesión a equipo menor (acelerador)               │
│ │   ├── Si juega titular en cesión, crece más        │
│ │   └── Riesgo: puede no querer volver               │
│ └── Promoción al primer equipo                       │
│     ├── El jugador decidir si es buen momento        │
│     ├── Si no juega en primer equipo, frustra        │
│     └── Promesa rota = pierde moral y lealtad        │
│                                                      │
│ INFORMES DE CANTERA:                                 │
│ ├── Lista de todos los canteranos                    │
│ ├── Progreso mensual (gráfico)                       │
│ ├── Director sugiere promocionables                  │
│ ├── "Joya de la cantera" (el mejor potencial)        │
│ └── Comparación con canteranos de otros clubs        │
│                                                      │
│ FUNCIONES:                                           │
│ ├── generar_canteranos_temporada() → Array           │
│ ├── obtener_canteranos() → Array                     │
│ ├── promover_a_primer_equipo(jugador_id)             │
│ ├── enviar_en_cesion(jugador_id, equipo_id)          │
│ ├── establecer_plan_entrenamiento(jugador, plan)     │
│ ├── obtener_informe_progreso(jugador_id) → Report    │
│ ├── simular_jornada_juvenil() → resultados           │
│ └── evaluar_potencial(jugador_id) → estimación       │
│     (precisión depende del director de cantera)      │
│                                                      │
│ ARCHIVO: core/youth_academy.gd                       │
│                                                      │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│ S14. PLAYER DEVELOPMENT & TRAINING SYSTEM            │
├──────────────────────────────────────────────────────┤
│                                                      │
│ RESPONSABILIDAD:                                     │
│ Evolución de atributos de jugadores a lo largo       │
│ del tiempo. Entrenamiento. Curvas de crecimiento.    │
│                                                      │
│ CURVA DE DESARROLLO POR EDAD:                        │
│                                                      │
│  Potencial                                           │
│  100│            ┌──────────┐                        │
│   90│         ┌──┘          └──┐                     │
│   80│      ┌──┘    PICO        └──┐                  │
│   70│   ┌──┘    (27-31 años)      └──┐               │
│   60│┌──┘                            └──┐            │
│   50││  CRECIMIENTO     DECLIVE          └──┐        │
│   40││  (16-26)         (32-38)              │       │
│   30│└                                       └──     │
│     └──────────────────────────────────────────      │
│      16  20  24  28  32  36  40  (edad)              │
│                                                      │
│ FACTORES DE CRECIMIENTO:                             │
│ ├── Edad (jóvenes crecen más)                        │
│ ├── Potencial (techo máximo)                         │
│ ├── Minutos jugados (jugar = mejorar)                │
│ ├── Calidad de entrenamiento                         │
│ │   = staff + instalaciones + plan                   │
│ ├── Profesionalismo del jugador                      │
│ │   (alta = entrena mejor, baja = estancamiento)     │
│ ├── Moral (jugador contento mejora más)              │
│ └── Liga competitiva = más desarrollo                │
│                                                      │
│ ENTRENAMIENTO SEMANAL:                               │
│ ├── Plan de equipo (afecta a todos):                 │
│ │   ├── Físico intenso                               │
│ │   ├── Técnica individual                           │
│ │   ├── Juego táctico                                │
│ │   ├── Balón parado                                 │
│ │   ├── Preparación de partido                       │
│ │   └── Descanso/recuperación                        │
│ │                                                    │
│ ├── Entrenamiento individual (por jugador):          │
│ │   ├── Disparos                                     │
│ │   ├── Pases                                        │
│ │   ├── Regates                                      │
│ │   ├── Defensa                                      │
│ │   ├── Velocidad                                    │
│ │   ├── Fuerza                                       │
│ │   ├── Portero                                      │
│ │   └── Libre (el jugador elige)                     │
│ │                                                    │
│ └── Pretemporada (julio):                            │
│     ├── Entrenamientos dobles                        │
│     ├── Gran mejora de forma física                  │
│     ├── Partidos amistosos (ingresos menores +       │
│     │   probar jugadores nuevos)                     │
│     └── Concentración (optional, gasto extra,        │
│         bonus moral y cohesión)                      │
│                                                      │
│ DECLIVE (32+ años):                                  │
│ ├── Velocidad y aceleración bajan primero            │
│ ├── Resistencia baja gradualmente                    │
│ ├── Visión y compostura pueden SUBIR                 │
│ ├── Lesiones más frecuentes y largas                 │
│ ├── Algunos jugadores "envejecen bien"               │
│ │   (Modric, Thiago Silva) → declive lento           │
│ └── Profesionalismo alto = declive más lento         │
│                                                      │
│ FORMA FÍSICA:                                        │
│ ├── 0-100 (no es lo mismo que energía)               │
│ ├── Forma baja = rinde peor en partido               │
│ ├── Sube con: entrenamientos, jugar regularmente     │
│ ├── Baja con: lesión, no jugar, fin temporada        │
│ └── Pretemporada restaura forma de todos             │
│                                                      │
│ FUNCIONES:                                           │
│ ├── procesar_semana_entrenamiento(equipo)            │
│ ├── establecer_plan_equipo(plan)                     │
│ ├── establecer_plan_individual(jugador, plan)        │
│ ├── procesar_desarrollo_mensual(jugador) → cambios   │
│ ├── procesar_declive_anual(jugador) → cambios        │
│ ├── calcular_forma_fisica(jugador) → int             │
│ ├── obtener_informe_progreso(jugador) → datos        │
│ └── simular_pretemporada(equipo) → resultados        │
│                                                      │
│ ARCHIVO: core/training_system.gd                     │
│                                                      │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│ S15. BOARD & DIRECTORS SYSTEM                        │
├──────────────────────────────────────────────────────┤
│                                                      │
│ RESPONSABILIDAD:                                     │
│ La directiva que te contrata, te evalúa y te         │
│ puede despedir. Objetivos y expectativas.            │
│                                                      │
│ LA DIRECTIVA:                                        │
│ ├── PRESIDENTE (NPC con personalidad)                │
│ │   ├── Tipo: ambicioso / conservador / austero /    │
│ │   │   gastador / constructor / mediático           │
│ │   ├── Paciencia: baja/media/alta                   │
│ │   └── Cada tipo afecta expectativas y recursos     │
│ │                                                    │
│ ├── OBJETIVOS DE TEMPORADA:                          │
│ │   ├── Deportivos:                                  │
│ │   │   ├── "Ganar la liga"                          │
│ │   │   ├── "Top 4"                                  │
│ │   │   ├── "Evitar descenso"                        │
│ │   │   ├── "Ascender"                               │
│ │   │   ├── "Cuartos de Champions"                   │
│ │   │   └── "Ganar la copa"                          │
│ │   ├── Económicos:                                  │
│ │   │   ├── "No superar masa salarial de X"          │
│ │   │   ├── "Generar superávit"                      │
│ │   │   ├── "Reducir deuda"                          │
│ │   │   └── "Vender jugador por X o más"             │
│ │   ├── Desarrollo:                                  │
│ │   │   ├── "Integrar 2 canteranos"                  │
│ │   │   ├── "Ampliar estadio"                        │
│ │   │   └── "Mejorar academia a nivel X"             │
│ │   └── Estilo de juego (según presidente):          │
│ │       ├── "Jugar con posesión" / "Jugar directo"   │
│ │       └── "Apostar por jóvenes"                    │
│ │                                                    │
│ ├── EVALUACIÓN:                                      │
│ │   ├── Confianza de la directiva (0-100%)           │
│ │   ├── Sube con: victorias, cumplir objetivos,      │
│ │   │   buenas finanzas, buen juego                  │
│ │   ├── Baja con: derrotas, incumplimiento,          │
│ │   │   crisis económica, vestuario roto             │
│ │   ├── < 20%: DESPIDO (Game Over → buscar           │
│ │   │   otro club o cargar partida)                  │
│ │   ├── < 40%: Advertencia, restricciones            │
│ │   ├── > 70%: Felicitaciones, bonus presupuesto     │
│ │   └── > 90%: Renovación automática, carta blanca   │
│ │                                                    │
│ ├── PRESUPUESTO:                                     │
│ │   ├── La directiva APRUEBA presupuesto de fichajes │
│ │   ├── Puedes solicitar ampliación (si confían)     │
│ │   ├── Directiva puede FORZAR venta de jugador      │
│ │   │   (si crisis financiera)                       │
│ │   └── Directiva puede VETAR fichaje                │
│ │       ("demasiado caro para nuestro nivel")        │
│ │                                                    │
│ └── DESPIDO / NUEVO CLUB:                            │
│     ├── Si te despiden, puedes:                      │
│     │   ├── Buscar otro club (te ofrecen según       │
│     │   │   tu reputación como mánager)              │
│     │   ├── Esperar (pasan semanas, llegan ofertas)  │
│     │   └── Ir al desempleo y empezar desde abajo    │
│     ├── Tu reputación de mánager se acumula:         │
│     │   ├── Trofeos ganados                          │
│     │   ├── Ascensos logrados                        │
│     │   ├── Jugadores desarrollados                  │
│     │   └── Estabilidad financiera                   │
│     └── Clubs más grandes te llaman si tienes        │
│         buena reputación                             │
│                                                      │
│ FUNCIONES:                                           │
│ ├── obtener_objetivos() → Array[Objetivo]            │
│ ├── obtener_confianza() → int (0-100)                │
│ ├── evaluar_cumplimiento() → Dictionary              │
│ ├── solicitar_presupuesto_extra(cantidad) → bool     │
│ ├── reunion_directiva() → Decisiones                 │
│ ├── procesar_despido() → ofertas_disponibles         │
│ ├── elegir_nuevo_club(equipo_id)                     │
│ ├── obtener_reputacion_manager() → int               │
│ └── generar_cambio_directiva() → nuevo presidente    │
│     (cada 2-6 temporadas, elecciones)                │
│                                                      │
│ ARCHIVO: core/board_system.gd                        │
│                                                      │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│ S16. NEWS & MEDIA SYSTEM                             │
├──────────────────────────────────────────────────────┤
│                                                      │
│ RESPONSABILIDAD:                                     │
│ Generar noticias dinámicas, periódico deportivo,     │
│ ambiente inmersivo. El "mundo vive".                 │
│                                                      │
│ FUENTES DE NOTICIAS:                                 │
│ ├── 📰 RESULTADOS                                    │
│ │   ├── "¡Goleada del Madrid! 5-0 al Sevilla"       │
│ │   ├── "Sorpresa: colista vence al líder"           │
│ │   └── Resumen de jornada con destacados            │
│ │                                                    │
│ ├── 💰 FICHAJES                                      │
│ │   ├── "BOMBAZO: Mbappé al Madrid por €180M"        │
│ │   ├── "Rumor: el Barça sigue a joven estrella"     │
│ │   ├── Rumores (algunos falsos) generados por IA    │
│ │   └── Tus fichajes siempre son noticia             │
│ │                                                    │
│ ├── 🏆 CLASIFICACIONES                               │
│ │   ├── "El Madrid es nuevo líder"                   │
│ │   ├── "Drama en el descenso: 4 equipos luchan"     │
│ │   └── Comparativa de rachas                        │
│ │                                                    │
│ ├── 🤕 LESIONES                                      │
│ │   ├── "Vinícius, 3 semanas de baja"               │
│ │   └── "Epidemia de lesiones en el Barça"           │
│ │                                                    │
│ ├── 🏟️ INFRAESTRUCTURA                               │
│ │   ├── "El Madrid inaugura nueva grada: +15K"       │
│ │   └── "Plan de modernización del Camp Nou"         │
│ │                                                    │
│ ├── 👔 DIRECTIVA                                     │
│ │   ├── "El presidente renueva confianza en mánager" │
│ │   ├── "Rumores de destitución en el Valencia"       │
│ │   └── "Nuevo entrenador para el Atlético"          │
│ │                                                    │
│ ├── 🌟 RECORDS Y LOGROS                              │
│ │   ├── "Messi supera los 800 goles"                │
│ │   ├── "Histórico: Girona en Champions"             │
│ │   └── "Canterano debuta con hat-trick"             │
│ │                                                    │
│ ├── 🌍 SELECCIONES                                   │
│ │   ├── "Convocatoria de España: tus 5 jugadores"    │
│ │   └── "Lesión en fecha FIFA: Pedri baja 2 sem"    │
│ │                                                    │
│ └── 📊 PREMIOS                                       │
│     ├── Balón de Oro (fin de año)                    │
│     ├── MVP de la liga (mensual y anual)             │
│     ├── Mejor canterano                              │
│     ├── Máximo goleador                              │
│     └── Mejor portero                                │
│                                                      │
│ FORMATO DE NOTICIA:                                  │
│ {                                                    │
│   "id": 45001,                                       │
│   "fecha": "2026-09-15",                             │
│   "tipo": "resultado",                               │
│   "prioridad": "alta",                               │
│   "titular": "¡Goleada histórica!",                  │
│   "subtitular": "El Madrid humilla 6-0 al rival",   │
│   "cuerpo": "En una noche mágica en el Bernabéu...",│
│   "imagen_tipo": "gol_celebracion",                  │
│   "equipos_relacionados": [1001],                    │
│   "jugadores_relacionados": [10034, 10022],          │
│   "leida": false                                     │
│ }                                                    │
│                                                      │
│ INTERFAZ:                                            │
│ ├── Periódico diario en pantalla del despacho        │
│ ├── Ticker de noticias (scroll inferior)             │
│ ├── Archivo de noticias (buscable por fecha/tipo)    │
│ └── Noticias sobre TU club destacadas en amarillo    │
│                                                      │
│ GENERACIÓN:                                          │
│ ├── Templates con variables:                         │
│ │   "¡{jugador} marca {goles} goles y el            │
│ │    {equipo} golea {resultado} al {rival}!"         │
│ ├── 50+ templates por tipo de noticia                │
│ ├── Variación de tono: neutral, entusiasta,          │
│ │   dramático, crítico                               │
│ └── Noticias contextuales (si vas primero, el        │
│     tono es celebratorio; si vas último, crítico)    │
│                                                      │
│ FUNCIONES:                                           │
│ ├── generar_noticias_jornada(resultados) → Array     │
│ ├── generar_noticia_fichaje(datos) → Noticia         │
│ ├── generar_noticia_evento(tipo, datos) → Noticia    │
│ ├── obtener_noticias_hoy() → Array                   │
│ ├── obtener_noticias_semana() → Array                │
│ ├── obtener_noticias_mi_club() → Array               │
│ ├── generar_rueda_prensa() → preguntas/respuestas    │
│ └── generar_premios_temporada() → Array              │
│                                                      │
│ ARCHIVO: core/news_system.gd                         │
│                                                      │
└──────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│                    MAPA DE DEPENDENCIAS                            │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│                      ┌──────────────┐                              │
│                      │ S01. GAME    │                              │
│               ┌──────│   MANAGER    │──────┐                       │
│               │      └──────┬───────┘      │                       │
│               │             │              │                       │
│               ▼             ▼              ▼                       │
│        ┌──────────┐  ┌──────────┐  ┌────────────┐                 │
│        │S02.      │  │S03.      │  │S04.        │                 │
│        │CALENDAR  │  │DATABASE  │  │SAVE/LOAD   │                 │
│        └────┬─────┘  └────┬─────┘  └────────────┘                 │
│             │             │                                        │
│    ┌────────┼─────────────┼────────────────┐                       │
│    │        │             │                │                       │
│    ▼        ▼             ▼                ▼                       │
│ ┌──────┐ ┌──────┐ ┌───────────┐ ┌──────────────┐                  │
│ │S07.  │ │S05.  │ │S06. MATCH │ │S09. ECONOMY  │                  │
│ │LEAGUE│─│MATCH │ │SIMULATION │ │              │                  │
│ │SYSTEM│ │3D    │ │           │ │  ┌──────────┐│                  │
│ └──┬───┘ └──┬───┘ └─────┬─────┘ │  │INGRESOS ││                  │
│    │        │           │       │  │MatchDay  ││                  │
│    │        └─────┬─────┘       │  │TV        ││                  │
│    │              │             │  │Sponsors  ││                  │
│    │              ▼             │  │Merch     ││                  │
│    │        ┌──────────┐       │  └──────────┘│                  │
│    │        │S08.      │       │  ┌──────────┐│                  │
│    │        │REFEREE   │       │  │GASTOS    ││                  │
│    │        └──────────┘       │  │Salarios  ││                  │
│    │                           │  │Obras     ││                  │
│    │              ┌────────────│  │Fichajes  ││                  │
│    │              │            │  └──────────┘│                  │
│    │              ▼            └──────┬───────┘                   │
│    │        ┌──────────┐             │                            │
│    │        │S10.      │◄────────────┘                            │
│    │        │TRANSFER  │       (presupuesto)                      │
│    │        │MARKET    │                                          │
│    │        └──────────┘                                          │
│    │              │                                               │
│    │              ▼                                               │
│    │        ┌──────────┐     ┌──────────────┐                     │
│    │        │S11.      │     │S12. STADIUM  │                     │
│    │        │STAFF     │     │INFRASTRUCTURE│                     │
│    │        └────┬─────┘     └──────┬───────┘                     │
│    │             │                  │                              │
│    │             ▼                  │                              │
│    │        ┌──────────┐           │                              │
│    │        │S14.      │◄──────────┘                              │
│    │        │TRAINING  │  (instalaciones afectan)                 │
│    │        └────┬─────┘                                          │
│    │             │                                                │
│    │             ▼                                                │
│    │        ┌──────────┐                                          │
│    │        │S13. YOUTH│                                          │
│    │        │ACADEMY   │                                          │
│    │        └──────────┘                                          │
│    │                                                              │
│    │        ┌──────────┐     ┌──────────────┐                     │
│    └───────▶│S15.      │     │S16. NEWS &   │                     │
│             │BOARD     │     │MEDIA         │◄── TODOS alimentan  │
│             └──────────┘     └──────────────┘    noticias         │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

PCFutbol2026/
│
├── 📄 project.godot                    # Config proyecto Godot
├── 📄 ARQUITECTURA.md                  # Este documento
├── 📄 README.md                        # Descripción del proyecto
│
│
├── 📁 autoload/                        # Singletons (se cargan siempre)
│   ├── game_manager.gd                 # S01 - Orquestador global
│   ├── database.gd                     # S03 - Acceso a datos
│   ├── calendar.gd                     # S02 - Tiempo y eventos
│   ├── save_manager.gd                 # S04 - Guardar/cargar
│   └── audio_manager.gd               # Música y SFX global
│
│
├── 📁 core/                            # Lógica de negocio (sistemas)
│   ├── 📁 match/                       # S05 + S06 - Motor de partido
│   │   ├── match_manager.gd            # Orquesta un partido completo
│   │   ├── match_simulation.gd         # S06 - Simulación sin 3D
│   │   ├── match_events.gd             # Eventos: gol, falta, etc.
│   │   ├── team_ai.gd                  # IA táctica de equipo
│   │   ├── player_ai.gd               # IA individual de jugador
│   │   ├── ball_physics.gd             # Física del balón
│   │   ├── player_controller.gd        # Input del jugador humano
│   │   ├── formation_manager.gd        # Posiciones según táctica
│   │   └── referee.gd                  # S08 - Árbitro
│   │
│   ├── 📁 league/                      # S07 - Competiciones
│   │   ├── league_system.gd            # Liga (round robin)
│   │   ├── cup_system.gd              # Copa (eliminatoria)
│   │   ├── continental_system.gd       # Champions, Libertadores
│   │   ├── promotion_relegation.gd     # Ascensos/descensos
│   │   ├── calendar_generator.gd       # Genera fixtures
│   │   └── standings.gd               # Tabla de posiciones
│   │
│   ├── 📁 economy/                     # S09 - Finanzas
│   │   ├── economy_system.gd           # Sistema principal
│   │   ├── income_manager.gd           # Todos los ingresos
│   │   ├── expense_manager.gd          # Todos los gastos
│   │   ├── sponsor_system.gd           # Patrocinadores
│   │   ├── matchday_income.gd          # Taquilla
│   │   ├── tv_rights.gd               # Derechos TV
│   │   ├── merchandising.gd            # Merchandising
│   │   └── financial_report.gd         # Reportes/balances
│   │
│   ├── 📁 transfers/                   # S10 - Mercado
│   │   ├── transfer_system.gd          # Sistema principal
│   │   ├── transfer_negotiation.gd     # Negociación club-club
│   │   ├── contract_negotiation.gd     # Negociación con jugador
│   │   ├── transfer_ai.gd             # IA de otros equipos
│   │   ├── loan_system.gd             # Cesiones
│   │   ├── free_agents.gd             # Agentes libres
│   │   └── transfer_history.gd         # Historial
│   │
│   ├── 📁 staff/                       # S11 - Personal
│   │   ├── staff_system.gd             # Sistema principal
│   │   ├── scout_system.gd             # Ojeadores y reportes
│   │   ├── medical_system.gd           # Staff médico + lesiones
│   │   └── staff_market.gd            # Contratar/despedir staff
│   │
│   ├── 📁 stadium/                     # S12 - Infraestructura
│   │   ├── stadium_system.gd           # Estadio
│   │   ├── construction_manager.gd     # Obras
│   │   ├── facilities.gd              # Ciudad deportiva
│   │   └── maintenance.gd             # Deterioro y mantenimiento
│   │
│   ├── 📁 youth/                       # S13 - Cantera
│   │   ├── youth_academy.gd            # Sistema principal
│   │   ├── youth_generator.gd          # Generación procedural
│   │   └── youth_development.gd        # Desarrollo de canteranos
│   │
│   ├── 📁 training/                    # S14 - Entrenamiento
│   │   ├── training_system.gd          # Sistema principal
│   │   ├── player_development.gd       # Curvas de crecimiento
│   │   └── preseason.gd               # Pretemporada
│   │
│   ├── 📁 board/                       # S15 - Directiva
│   │   ├── board_system.gd             # Sistema principal
│   │   ├── objectives.gd              # Objetivos de temporada
│   │   └── manager_reputation.gd       # Reputación del mánager
│   │
│   └── 📁 news/                        # S16 - Noticias
│       ├── news_system.gd              # Sistema principal
│       ├── news_generator.gd           # Generador de noticias
│       ├── news_templates.gd           # Templates con variables
│       └── awards.gd                  # Premios de temporada
│
│
├── 📁 entities/                        # Clases de datos (Resources)
│   ├── player.gd                       # class_name Player
│   ├── team.gd                         # class_name Team
│   ├── league_data.gd                  # class_name LeagueData
│   ├── stadium_data.gd                 # class_name StadiumData
│   ├── staff_member.gd                 # class_name StaffMember
│   ├── contract.gd                     # class_name Contract
│   ├── transfer_offer.gd              # class_name TransferOffer
│   ├── match_result.gd                 # class_name MatchResult
│   ├── news_item.gd                    # class_name NewsItem
│   ├── objective.gd                    # class_name Objective
│   ├── sponsor_data.gd                 # class_name SponsorData
│   └── construction.gd                 # class_name Construction
│
│
├── 📁 scenes/                          # Escenas Godot (.tscn)
│   │
│   ├── 📁 boot/                        # Inicio del juego
│   │   ├── splash_screen.tscn          # Logo del "estudio"
│   │   └── main_menu.tscn             # Menú principal
│   │       ├── Nueva partida
│   │       ├── Cargar partida
│   │       ├── Opciones
│   │       └── Créditos
│   │
│   ├── 📁 setup/                       # Configurar nueva partida
│   │   ├── select_league.tscn          # Elegir liga
│   │   ├── select_team.tscn           # Elegir equipo
│   │   ├── manager_profile.tscn        # Nombre y foto del mánager
│   │   └── difficulty_settings.tscn    # Dificultad
│   │
│   ├── 📁 office/                      # DESPACHO (hub principal)
│   │   ├── office_main.tscn           # Escritorio del mánager
│   │   │   ├── Periódico del día (noticias)
│   │   │   ├── Próximo partido
│   │   │   ├── Acceso rápido a menús
│   │   │   ├── Alertas (ofertas, lesiones, etc.)
│   │   │   └── Botón "Avanzar día/semana"
│   │   ├── calendar_view.tscn          # Vista de calendario
│   │   └── inbox.tscn                 # Bandeja de mensajes
│   │
│   ├── 📁 squad/                       # PLANTILLA
│   │   ├── squad_list.tscn            # Lista de jugadores
│   │   ├── player_detail.tscn          # Ficha completa jugador
│   │   ├── player_comparison.tscn      # Comparar 2 jugadores
│   │   └── player_history.tscn         # Historial del jugador
│   │
│   ├── 📁 tactics/                     # TÁCTICA
│   │   ├── formation_editor.tscn       # Arrastar jugadores
│   │   │   ├── Campo con posiciones
│   │   │   ├── Lista de jugadores disponibles
│   │   │   ├── Elegir formación (4-4-2, etc.)
│   │   │   └── Instrucciones tácticas
│   │   ├── set_pieces.tscn            # Balón parado
│   │   └── match_preparation.tscn      # Preparar rival
│   │
│   ├── 📁 transfers/                   # FICHAJES
│   │   ├── transfer_hub.tscn          # Centro de fichajes
│   │   ├── player_search.tscn          # Buscador con filtros
│   │   ├── negotiation_screen.tscn     # Negociación
│   │   ├── offers_received.tscn        # Ofertas recibidas
│   │   ├── shortlist.tscn             # Lista de seguimiento
│   │   └── transfer_history.tscn       # Historial
│   │
│   ├── 📁 finances/                    # FINANZAS
│   │   ├── finance_overview.tscn       # Vista general
│   │   ├── income_detail.tscn          # Desglose ingresos
│   │   ├── expense_detail.tscn         # Desglose gastos
│   │   ├── sponsors_screen.tscn        # Gestión sponsors
│   │   ├── salary_overview.tscn        # Masa salarial
│   │   └── financial_projection.tscn   # Proyección
│   │
│   ├── 📁 stadium/                     # ESTADIO
│   │   ├── stadium_overview.tscn       # Vista general estadio
│   │   ├── stadium_upgrade.tscn        # Mejoras disponibles
│   │   ├── facilities_overview.tscn    # Ciudad deportiva
│   │   ├── construction_progress.tscn  # Obras en curso
│   │   └── new_stadium_planner.tscn    # Planificador estadio nuevo
│   │
│   ├── 📁 staff/                       # STAFF
│   │   ├── staff_overview.tscn         # Todo el personal
│   │   ├── staff_hire.tscn            # Contratar nuevo
│   │   ├── scout_assignments.tscn      # Asignar ojeadores
│   │   └── scout_reports.tscn          # Informes de scouting
│   │
│   ├── 📁 youth/                       # CANTERA
│   │   ├── academy_overview.tscn       # Vista general
│   │   ├── youth_players.tscn          # Lista canteranos
│   │   └── promote_player.tscn         # Promover jugador
│   │
│   ├── 📁 league/                      # COMPETICIONES
│   │   ├── standings.tscn             # Clasificación
│   │   ├── fixtures.tscn              # Calendario/resultados
│   │   ├── cup_bracket.tscn           # Cuadro copa
│   │   ├── stats_leaders.tscn          # Goleadores, asistentes
│   │   └── other_leagues.tscn          # Ver otras ligas
│   │
│   ├── 📁 match/                       # PARTIDO 3D
│   │   ├── match_intro.tscn           # Previa (alineaciones)
│   │   ├── match_3d.tscn              # ESCENA PRINCIPAL 3D
│   │   │   ├── Pitch (campo 3D)
│   │   │   ├── Ball (balón RigidBody3D)
│   │   │   ├── PlayerUnits x22 (CharacterBody3D)
│   │   │   ├── Goals x2 (porterías)
│   │   │   ├── Cameras (TV, aérea, replay)
│   │   │   ├── Lighting (iluminación estadio)
│   │   │   ├── Crowd (público en gradas)
│   │   │   ├── HUD (marcador, radar, stamina)
│   │   │   └── EventTicker (gol, falta, cambio)
│   │   │
│   │   ├── match_halftime.tscn         # Entretiempo
│   │   │   ├── Estadísticas primer tiempo
│   │   │   ├── Cambiar táctica
│   │   │   ├── Hacer sustituciones
│   │   │   └── Instrucciones individuales
│   │   │
│   │   ├── match_penalties.tscn        # Tanda de penaltis
│   │   │   ├── Cámara especial detrás portería
│   │   │   ├── Control de dirección disparo
│   │   │   ├── Control de dirección portero
│   │   │   └── Marcador de tanda
│   │   │
│   │   ├── match_result.tscn           # Pantalla post-partido
│   │   │   ├── Resultado final
│   │   │   ├── Goleadores y asistentes
│   │   │   ├── Estadísticas completas
│   │   │   ├── Mejor jugador del partido
│   │   │   ├── Puntuaciones individuales
│   │   │   ├── Mapa de calor (simplificado)
│   │   │   └── Botón: volver al despacho
│   │   │
│   │   └── match_replay.tscn           # Repetición de goles
│   │       ├── Cámara cinemática
│   │       ├── Cámara lenta
│   │       └── Múltiples ángulos
│   │
│   ├── 📁 training/                    # ENTRENAMIENTO
│   │   ├── training_overview.tscn      # Plan semanal
│   │   ├── training_individual.tscn    # Asignar por jugador
│   │   └── preseason_plan.tscn         # Planificar pretemporada
│   │
│   ├── 📁 board/                       # DIRECTIVA
│   │   ├── board_meeting.tscn          # Reunión directiva
│   │   ├── objectives_screen.tscn      # Objetivos actuales
│   │   └── manager_profile.tscn        # Tu perfil/reputación
│   │
│   ├── 📁 news/                        # NOTICIAS
│   │   ├── newspaper.tscn             # Periódico diario
│   │   ├── news_archive.tscn          # Archivo de noticias
│   │   └── press_conference.tscn       # Rueda de prensa
│   │
│   └── 📁 common/                      # COMPONENTES REUTILIZABLES
│       ├── top_bar.tscn               # Barra superior
│       │   ├── Nombre del club
│       │   ├── Presupuesto actual
│       │   ├── Fecha actual
│       │   └── Botones navegación rápida
│       ├── bottom_nav.tscn             # Navegación inferior
│       ├── player_card_small.tscn      # Tarjeta jugador mini
│       ├── player_card_large.tscn      # Tarjeta jugador grande
│       ├── player_row.tscn             # Fila en tabla jugadores
│       ├── match_row.tscn              # Fila de resultado
│       ├── standings_row.tscn          # Fila de clasificación
│       ├── news_card.tscn              # Tarjeta de noticia
│       ├── offer_card.tscn             # Tarjeta de oferta
│       ├── staff_card.tscn             # Tarjeta de staff
│       ├── construction_card.tscn      # Tarjeta de obra
│       ├── stat_bar.tscn               # Barra de atributo
│       ├── confirmation_dialog.tscn    # Popup confirmar
│       ├── notification_popup.tscn     # Popup de alerta
│       ├── filter_panel.tscn           # Panel de filtros
│       ├── pagination.tscn             # Paginación tablas
│       └── loading_screen.tscn         # Pantalla de carga
│
│
├── 📁 assets/                          # RECURSOS DEL JUEGO
│   │
│   ├── 📁 models/                      # Modelos 3D
│   │   ├── 📁 pitch/                   # Campo
│   │   │   ├── pitch.glb               # Césped + líneas
│   │   │   ├── goal_net.glb            # Portería con red
│   │   │   ├── corner_flag.glb         # Banderín
│   │   │   ├── bench.glb               # Banquillo
│   │   │   └── stadium_shell.glb       # Estructura gradas
│   │   │       (low-poly, varios niveles)
│   │   │
│   │   ├── 📁 player/                  # Modelo jugador
│   │   │   ├── player_base.glb         # Modelo base low-poly
│   │   │   │   ├── ~800-1500 polígonos
│   │   │   │   ├── Rig básico (esqueleto)
│   │   │   │   └── Separado: cuerpo, pelo, botas
│   │   │   │
│   │   │   ├── 📁 animations/          # Animaciones
│   │   │   │   ├── idle.glb
│   │   │   │   ├── walk.glb
│   │   │   │   ├── run.glb
│   │   │   │   ├── sprint.glb
│   │   │   │   ├── kick_low.glb        # Disparo raso
│   │   │   │   ├── kick_high.glb       # Disparo alto
│   │   │   │   ├── kick_volley.glb     # Volea
│   │   │   │   ├── pass_short.glb      # Pase corto
│   │   │   │   ├── pass_long.glb       # Pase largo
│   │   │   │   ├── header.glb          # Cabezazo
│   │   │   │   ├── header_jump.glb     # Cabezazo saltando
│   │   │   │   ├── tackle_stand.glb    # Entrada de pie
│   │   │   │   ├── tackle_slide.glb    # Barrida
│   │   │   │   ├── throw_in.glb        # Saque de banda
│   │   │   │   ├── celebrate_01.glb    # Celebración 1
│   │   │   │   ├── celebrate_02.glb    # Celebración 2
│   │   │   │   ├── celebrate_03.glb    # Celebración 3
│   │   │   │   ├── fall.glb            # Caer
│   │   │   │   ├── get_up.glb          # Levantarse
│   │   │   │   ├── argue.glb           # Protestar
│   │   │   │   ├── gk_idle.glb         # Portero parado
│   │   │   │   ├── gk_dive_left.glb    # Estirada izq
│   │   │   │   ├── gk_dive_right.glb   # Estirada der
│   │   │   │   ├── gk_dive_low_l.glb   # Estirada baja izq
│   │   │   │   ├── gk_dive_low_r.glb   # Estirada baja der
│   │   │   │   ├── gk_catch.glb        # Atrapar
│   │   │   │   ├── gk_punch.glb        # Puñetazo despeje
│   │   │   │   ├── gk_throw.glb        # Saque con mano
│   │   │   │   └── gk_kick.glb         # Saque con pie
│   │   │   │
│   │   │   └── 📁 hair/               # Variantes pelo
│   │   │       ├── hair_short.glb
│   │   │       ├── hair_medium.glb
│   │   │       ├── hair_long.glb
│   │   │       ├── hair_bald.glb
│   │   │       └── hair_mohawk.glb
│   │   │
│   │   ├── 📁 ball/
│   │   │   └── football.glb           # Balón
│   │   │
│   │   └── 📁 referee/
│   │       └── referee.glb            # Modelo árbitro
│   │
│   ├── 📁 textures/                    # Texturas
│   │   ├── 📁 pitch/
│   │   │   ├── grass_albedo.png        # Textura césped
│   │   │   ├── grass_normal.png        # Normal map
│   │   │   └── pitch_lines.png         # Líneas del campo
│   │   │
│   │   ├── 📁 kits/                    # Equipaciones
│   │   │   ├── README.md               # Formato de textura kit
│   │   │   ├── template_kit.png        # Template UV
│   │   │   ├── 📁 generated/           # Generadas por código
│   │   │   │   └── (se generan desde colores del equipo)
│   │   │   └── Las equipaciones se generan
│   │   │       dinámicamente con los colores
│   │   │       del equipo (color1, color2, patrón)
│   │   │
│   │   ├── 📁 ball/
│   │   │   └── ball_texture.png
│   │   │
│   │   └── 📁 stadium/
│   │       ├── crowd_texture.png       # Público (tiled)
│   │       ├── seat_colors.png         # Colores asientos
│   │       └── ad_boards/              # Vallas publicitarias
│   │           ├── ad_template.png
│   │           └── (generadas dinámicamente
│   │               con nombre de sponsors)
│   │
│   ├── 📁 ui/                          # Assets de interfaz
│   │   ├── 📁 icons/
│   │   │   ├── icon_ball.svg
│   │   │   ├── icon_trophy.svg
│   │   │   ├── icon_money.svg
│   │   │   ├── icon_calendar.svg
│   │   │   ├── icon_stadium.svg
│   │   │   ├── icon_shirt.svg
│   │   │   ├── icon_whistle.svg
│   │   │   ├── icon_medical.svg
│   │   │   ├── icon_scout.svg
│   │   │   ├── icon_training.svg
│   │   │   ├── icon_newspaper.svg
│   │   │   ├── icon_star.svg
│   │   │   ├── icon_arrow_up.svg       # Mejora atributo
│   │   │   ├── icon_arrow_down.svg     # Baja atributo
│   │   │   ├── icon_yellow_card.svg
│   │   │   ├── icon_red_card.svg
│   │   │   ├── icon_injury.svg
│   │   │   ├── icon_goal.svg
│   │   │   ├── icon_assist.svg
│   │   │   ├── icon_substitution.svg
│   │   │   └── ... (50+ iconos)
│   │   │
│   │   ├── 📁 flags/                   # Banderas de países
│   │   │   ├── ARG.png
│   │   │   ├── ESP.png
│   │   │   ├── GBR.png
│   │   │   ├── BRA.png
│   │   │   └── ... (220 países)
│   │   │
│   │   ├── 📁 club_badges/            # Escudos de equipos
│   │   │   ├── README.md              # Generados o placeholder
│   │   │   └── (escudos genéricos generados
│   │   │       por combinación de formas +
│   │   │       colores del equipo)
│   │   │
│   │   ├── 📁 backgrounds/
│   │   │   ├── office_bg.png           # Fondo despacho
│   │   │   ├── menu_bg.png             # Fondo menú
│   │   │   └── paper_texture.png       # Textura periódico
│   │   │
│   │   └── 📁 portraits/              # Retratos de personas
│   │       ├── README.md              # Generados proceduralmente
│   │       └── (se generan combinando:
│   │           cara_base + pelo + tono_piel
│   │           + rasgos según nacionalidad)
│   │
│   ├── 📁 fonts/
│   │   ├── main_font.ttf              # Fuente principal UI
│   │   ├── title_font.ttf             # Fuente títulos
│   │   ├── scoreboard_font.ttf        # Fuente marcador
│   │   ├── numbers_font.ttf           # Números camiseta
│   │   └── newspaper_font.ttf         # Fuente periódico
│   │
│   ├── 📁 audio/
│   │   ├── 📁 music/
│   │   │   ├── menu_theme.ogg         # Tema menú principal
│   │   │   ├── office_ambient.ogg     # Ambiente despacho
│   │   │   ├── match_buildup.ogg      # Previa partido
│   │   │   ├── match_tension.ogg      # Partido tenso
│   │   │   ├── match_winning.ogg      # Vas ganando
│   │   │   ├── match_losing.ogg       # Vas perdiendo
│   │   │   ├── victory_theme.ogg      # Victoria
│   │   │   ├── defeat_theme.ogg       # Derrota
│   │   │   ├── title_won.ogg          # ¡Campeón!
│   │   │   └── transfer_deadline.ogg  # Deadline day
│   │   │
│   │   └── 📁 sfx/
│   │       ├── kick_ball.ogg           # Patear balón
│   │       ├── kick_hard.ogg           # Disparo fuerte
│   │       ├── header.ogg              # Cabezazo
│   │       ├── ball_net.ogg            # Balón en red (GOL)
│   │       ├── ball_post.ogg           # Balón en palo
│   │       ├── ball_catch.ogg          # Portero atrapa
│   │       ├── whistle_short.ogg       # Pitido falta
│   │       ├── whistle_long.ogg        # Pitido final
│   │       ├── whistle_start.ogg       # Pitido inicio
│   │       ├── crowd_ambient.ogg       # Público ambiente
│   │       ├── crowd_cheer.ogg         # Público celebra
│   │       ├── crowd_boo.ogg           # Público abuchea
│   │       ├── crowd_tension.ogg       # Público tenso
│   │       ├── crowd_goal.ogg          # Público gol
│   │       ├── crowd_sing.ogg          # Público canta
│   │       ├── ui_click.ogg            # Click botón
│   │       ├── ui_hover.ogg            # Hover botón
│   │       ├── ui_confirm.ogg          # Confirmar
│   │       ├── ui_cancel.ogg           # Cancelar
│   │       ├── ui_notification.ogg     # Notificación
│   │       ├── ui_page_turn.ogg        # Pasar página
│   │       ├── cash_register.ogg       # Dinero/fichaje
│   │       ├── typewriter.ogg          # Escribir noticia
│   │       └── camera_flash.ogg        # Flash foto
│   │
│   └── 📁 shaders/                     # Shaders visuales
│       ├── grass.gdshader              # Shader césped
│       ├── kit_color.gdshader          # Colorear equipación
│       ├── ball_trail.gdshader         # Estela del balón
│       ├── selection_circle.gdshader   # Círculo selección
│       ├── ui_blur.gdshader            # Blur de fondo menús
│       └── retro_crt.gdshader          # Efecto CRT (opcional)
│
│
├── 📁 data/                            # DATOS INICIALES (JSONs)
│   │
│   ├── 📁 countries/                   # Datos de países
│   │   └── countries.json              # Lista de 220 países
│   │       {id, nombre, confederacion, coeficiente,
│   │        nombres_masculinos[], apellidos[]}
│   │
│   ├── 📁 leagues/                     # Configuración de ligas
│   │   ├── spain.json                  # Liga española config
│   │   │   {id, nombre, pais, nivel, num_equipos,
│   │   │    ascensos, descensos, plazas_europeas,
│   │   │    formato_copa, tv_reparto, reglas_extranjeros}
│   │   ├── england.json
│   │   ├── italy.json
│   │   ├── germany.json
│   │   ├── france.json
│   │   ├── argentina.json
│   │   ├── brazil.json
│   │   └── ... (50+ archivos)
│   │
│   ├── 📁 teams/                       # Equipos por liga
│   │   ├── spain_1.json                # Primera División
│   │   │   [{id, nombre, nombre_corto, pais, liga_id,
│   │   │     color1, color2, color3, patron_camiseta,
│   │   │     estadio{}, finanzas{}, reputacion,
│   │   │     historia{}, instalaciones{}}]
│   │   ├── spain_2.json                # Segunda División
│   │   ├── england_1.json              # Premier League
│   │   ├── england_2.json              # Championship
│   │   ├── england_3.json              # League One
│   │   ├── england_4.json              # League Two
│   │   ├── england_5.json              # National League
│   │   ├── argentina_1.json
│   │   ├── argentina_2.json
│   │   └── ... (100+ archivos)
│   │
│   ├── 📁 players/                     # Jugadores por equipo
│   │   ├── team_1001.json              # Plantilla Real Madrid
│   │   │   [{id, nombre, apellido, ...atributos completos}]
│   │   ├── team_1002.json              # Plantilla Barcelona
│   │   ├── free_agents.json            # Agentes libres
│   │   └── ... (5000+ archivos)
│   │
│   ├── 📁 staff/                       # Staff disponible
│   │   ├── coaches.json                # Entrenadores
│   │   ├── scouts.json                 # Ojeadores
│   │   ├── medics.json                 # Médicos
│   │   └── directors.json              # Directores
│   │
│   ├── 📁 competitions/                # Competiciones internac.
│   │   ├── champions_league.json
│   │   ├── europa_league.json
│   │   ├── conference_league.json
│   │   ├── copa_libertadores.json
│   │   ├── copa_sudamericana.json
│   │   └── club_world_cup.json
│   │
│   ├── 📁 sponsors/                    # Sponsors disponibles
│   │   ├── global_sponsors.json        # Nike, Adidas, etc.
│   │   ├── regional_sponsors.json      # Por país
│   │   └── sponsor_templates.json      # Tipos de contrato
│   │
│   ├── 📁 names/                       # Para generación procedural
│   │   ├── names_spanish.json          # {nombres:[], apellidos:[]}
│   │   ├── names_english.json
│   │   ├── names_italian.json
│   │   ├── names_german.json
│   │   ├── names_french.json
│   │   ├── names_portuguese.json
│   │   ├── names_argentinian.json
│   │   ├── names_brazilian.json
│   │   ├── names_african.json
│   │   ├── names_japanese.json
│   │   └── ... (30+ archivos)
│   │
│   ├── 📁 news_templates/              # Templates de noticias
│   │   ├── match_results.json
│   │   ├── transfers.json
│   │   ├── injuries.json
│   │   ├── standings.json
│   │   ├── records.json
│   │   ├── board.json
│   │   └── generic.json
│   │
│   └── 📁 config/                      # Configuraciones del juego
│       ├── game_config.json            # Config general
│       ├── difficulty_presets.json      # Presets de dificultad
│       ├── attribute_weights.json      # Pesos para simulación
│       ├── economy_config.json         # Parámetros económicos
│       ├── training_config.json        # Parámetros entrenamiento
│       ├── development_curves.json     # Curvas de desarrollo edad
│       ├── match_engine_config.json    # Config motor partido
│       ├── stadium_upgrades.json       # Catálogo de mejoras
│       └── construction_costs.json     # Costes de construcción
│
│
├── 📁 saves/                           # Partidas guardadas
│   ├── autosave.sav
│   ├── slot_01.sav
│   ├── slot_02.sav
│   └── ... (hasta slot_10.sav)
│
│
└── 📁 tools/                           # HERRAMIENTAS (Python)
    │                                   # NO se incluyen en el build
    │                                   # Solo para DESARROLLO
    │
    ├── 📁 scrapers/
    │   ├── scraper_transfermarkt.py    # Scraper Transfermarkt
    │   ├── scraper_sofifa.py           # Scraper SoFIFA (atributos)
    │   ├── scraper_fbref.py            # Scraper FBref (estadísticas)
    │   ├── scraper_worldfootball.py    # Ligas menores
    │   └── scraper_utils.py            # Utilidades comunes
    │
    ├── 📁 generators/
    │   ├── generate_all_data.py        # Script maestro
    │   ├── generate_players.py         # Generar jugadores JSON
    │   ├── generate_teams.py           # Generar equipos JSON
    │   ├── generate_leagues.py         # Generar ligas JSON
    │   ├── generate_staff.py           # Generar staff JSON
    │   ├── generate_sponsors.py        # Generar sponsors JSON
    │   ├── generate_names_db.py        # Generar base de nombres
    │   ├── fill_missing_attributes.py  # Completar attrs faltantes
    │   └── validate_data.py            # Validar integridad JSONs
    │
    ├── 📁 converters/
    │   ├── sofifa_to_game_attrs.py     # Convertir attrs FIFA→juego
    │   ├── merge_data_sources.py       # Combinar Transfermarkt+SoFIFA
    │   └── export_to_godot_json.py     # Formato final para Godot
    │
    └── requirements.txt                # Dependencias Python
        # requests
        # beautifulsoup4
        # lxml
        # pandas
        # tqdm

┌───────────────────────────────────────────────────────────────┐
│        MATCH_3D.TSCN - ÁRBOL DE NODOS COMPLETO               │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  Match3D (Node3D) ← match_manager.gd                        │
│  │                                                            │
│  ├── Environment (WorldEnvironment)                          │
│  │   ├── Sky (cielo, hora del día)                           │
│  │   ├── DirectionalLight3D (sol/focos)                      │
│  │   └── AmbientLight                                        │
│  │                                                            │
│  ├── Pitch (Node3D) ← pitch.gd                              │
│  │   ├── GrassFloor (MeshInstance3D)                         │
│  │   │   └── grass.gdshader                                  │
│  │   ├── PitchLines (MeshInstance3D)                         │
│  │   │   └── Líneas blancas sobre el césped                  │
│  │   ├── CenterCircle (MeshInstance3D)                       │
│  │   ├── PenaltyAreas x2 (MeshInstance3D)                   │
│  │   ├── CornerFlags x4 (MeshInstance3D)                     │
│  │   ├── GoalLocal (StaticBody3D)                            │
│  │   │   ├── GoalMesh (portería 3D)                          │
│  │   │   ├── NetMesh (red, animada al gol)                   │
│  │   │   ├── GoalLineDetector (Area3D)                       │
│  │   │   │   └── Detecta si balón cruzó línea               │
│  │   │   └── CollisionShape3D                                │
│  │   ├── GoalVisitor (StaticBody3D)                          │
│  │   │   └── (misma estructura)                              │
│  │   ├── Boundaries (StaticBody3D)                           │
│  │   │   └── Paredes invisibles alrededor                    │
│  │   └── OutOfBoundsDetectors                                │
│  │       ├── TouchlineLeft (Area3D)                          │
│  │       ├── TouchlineRight (Area3D)                         │
│  │       ├── GoallineLocal (Area3D)                          │
│  │       └── GoallineVisitor (Area3D)                        │
│  │                                                            │
│  ├── Stadium (Node3D) ← visual only                         │
│  │   ├── StandsNorth (MeshInstance3D)                        │
│  │   ├── StandsSouth (MeshInstance3D)                        │
│  │   ├── StandsEast (MeshInstance3D)                         │
│  │   ├── StandsWest (MeshInstance3D)                         │
│  │   ├── CrowdParticles (GPUParticles3D)                    │
│  │   │   └── Simula público con partículas/sprites          │
│  │   ├── AdBoards (MeshInstance3D)                           │
│  │   │   └── Vallas LED con sponsors (animadas)              │
│  │   ├── Scoreboard3D (MeshInstance3D)                       │
│  │   │   └── Marcador gigante en grada                       │
│  │   ├── Floodlights x4 (MeshInstance3D + Light3D)          │
│  │   ├── BenchLocal (MeshInstance3D)                         │
│  │   ├── BenchVisitor (MeshInstance3D)                       │
│  │   └── TunnelEntrance (MeshInstance3D)                     │
│  │                                                            │
│  ├── Ball (RigidBody3D) ← ball.gd                           │
│  │   ├── BallMesh (MeshInstance3D)                           │
│  │   │   └── Esfera con textura de balón                     │
│  │   ├── BallCollision (CollisionShape3D)                    │
│  │   │   └── SphereShape3D (radio ≈ 0.11)                   │
│  │   ├── BallShadow (Sprite3D)                               │
│  │   │   └── Sombra proyectada en suelo                      │
│  │   ├── BallTrail (MeshInstance3D)                          │
│  │   │   └── Estela visual en disparos fuertes               │
│  │   └── BallAudio (AudioStreamPlayer3D)                     │
│  │       └── Sonidos de impacto según fuerza                 │
│  │                                                            │
│  ├── TeamLocal (Node3D) ← team_controller.gd                │
│  │   ├── Player_1 (CharacterBody3D) ← player_unit.gd        │
│  │   │   ├── PlayerModel (MeshInstance3D)                    │
│  │   │   │   └── Modelo low-poly + textura equipo local      │
│  │   │   ├── ShirtNumber (Label3D)                           │
│  │   │   │   └── Número en espalda (siempre mirando cámara) │
│  │   │   ├── PlayerName (Label3D)                            │
│  │   │   │   └── Nombre sobre cabeza (opcional)              │
│  │   │   ├── SelectionCircle (MeshInstance3D)                │
│  │   │   │   └── Círculo amarillo si seleccionado            │
│  │   │   ├── AnimationPlayer                                 │
│  │   │   │   └── Todas las animaciones cargadas              │
│  │   │   ├── AnimationTree                                   │
│  │   │   │   └── Blend entre idle/walk/run/acción           │
│  │   │   ├── NavigationAgent3D                               │
│  │   │   │   └── Para pathfinding de IA                      │
│  │   │   ├── CollisionShape3D                                │
│  │   │   │   └── CapsuleShape3D                              │
│  │   │   ├── BallDetector (Area3D)                           │
│  │   │   │   └── Detecta si balón está cerca (para control)  │
│  │   │   ├── TackleZone (Area3D)                             │
│  │   │   │   └── Zona donde puede hacer entrada              │
│  │   │   ├── StaminaBar (ProgressBar - en HUD)              │
│  │   │   └── PlayerAI (Node) ← player_ai.gd                │
│  │   │       └── Máquina de estados para IA                  │
│  │   │                                                        │
│  │   ├── Player_2 ... Player_11 (misma estructura)           │
│  │   └── Subs_1 ... Subs_7 (en banquillo, inactivos)        │
│  │                                                            │
│  ├── TeamVisitor (Node3D)                                    │
│  │   └── (misma estructura que TeamLocal)                    │
│  │                                                            │
│  ├── Referee (CharacterBody3D) ← referee_3d.gd              │
│  │   ├── RefereeModel (MeshInstance3D)                       │
│  │   ├── AnimationPlayer                                     │
│  │   ├── OffsideLine (MeshInstance3D)                        │
│  │   │   └── Línea visual de fuera de juego                  │
│  │   └── CardDisplay (Sprite3D)                              │
│  │       └── Muestra tarjeta amarilla/roja                   │
│  │                                                            │
│  ├── Cameras (Node3D) ← match_camera.gd                     │
│  │   ├── CameraTV (Camera3D)                                │
│  │   │   └── Vista lateral clásica TV                        │
│  │   │       Sigue el balón horizontalmente                  │
│  │   │       Zoom dinámico según zona de juego               │
│  │   ├── CameraAerial (Camera3D)                            │
│  │   │   └── Vista cenital (zoom alejado)                    │
│  │   ├── CameraBehindGoal (Camera3D)                        │
│  │   │   └── Detrás de portería (corners, penaltis)         │
│  │   ├── CameraReplay (Camera3D)                            │
│  │   │   └── Cámara libre para repeticiones                  │
│  │   └── CameraTransition (AnimationPlayer)                  │
│  │       └── Transiciones suaves entre cámaras              │
│  │                                                            │
│  ├── MatchHUD (CanvasLayer) ← match_hud.gd                  │
│  │   ├── Scoreboard (HBoxContainer)                          │
│  │   │   ├── HomeTeamName (Label)                            │
│  │   │   ├── HomeScore (Label)                               │
│  │   │   ├── Separator (Label) " - "                         │
│  │   │   ├── AwayScore (Label)                               │
│  │   │   ├── AwayTeamName (Label)                            │
│  │   │   └── MatchTime (Label) "45:32"                       │
│  │   │                                                        │
│  │   ├── Radar (SubViewportContainer)                        │
│  │   │   └── Minimapa cenital con puntos                     │
│  │   │       ○ = local  ● = visitante  ◉ = balón             │
│  │   │                                                        │
│  │   ├── SelectedPlayerInfo (PanelContainer)                 │
│  │   │   ├── PlayerName (Label)                              │
│  │   │   ├── PlayerNumber (Label)                            │
│  │   │   ├── StaminaBar (ProgressBar)                        │
│  │   │   └── ActionHint (Label) "[Espacio] Pase [Shift] Tiro"│
│  │   │                                                        │
│  │   ├── EventTicker (ScrollContainer)                       │
│  │   │   └── Lista de eventos (goles, faltas, etc.)          │
│  │   │                                                        │
│  │   ├── SpeedControl (HBoxContainer)                        │
│  │   │   └── [1x] [2x] [4x] (solo modo espectador)          │
│  │   │                                                        │
│  │   └── PauseMenu (PopupPanel)                              │
│  │       ├── Continuar                                       │
│  │       ├── Táctica                                         │
│  │       ├── Sustituciones                                   │
│  │       ├── Ver estadísticas                                │
│  │       └── Salir del partido                               │
│  │                                                            │
│  ├── MatchAudio (Node) ← match_audio.gd                     │
│  │   ├── CrowdAmbient (AudioStreamPlayer)                   │
│  │   │   └── Loop de público (volumen dinámico               │
│  │   │       según emoción del partido)                      │
│  │   ├── CrowdReactions (AudioStreamPlayer)                  │
│  │   │   └── Gritos, celebraciones, abucheos                │
│  │   ├── WhistleSFX (AudioStreamPlayer)                      │
│  │   ├── BallSFX (AudioStreamPlayer3D)                       │
│  │   └── MusicTrack (AudioStreamPlayer)                      │
│  │       └── Música dinámica según tensión                   │
│  │                                                            │
│  └── MatchLogic (Node) ← match_state_machine.gd             │
│      ├── Estados del partido:                                │
│      │   ├── PREGAME (alineaciones, salida jugadores)        │
│      │   ├── KICKOFF_H1 (saque inicial 1T)                  │
│      │   ├── PLAYING (en juego normal)                       │
│      │   ├── DEAD_BALL (balón parado: falta, saque, etc.)   │
│      │   ├── GOAL_SCORED (celebración + repetición)          │
│      │   ├── HALFTIME (entretiempo)                          │
│      │   ├── KICKOFF_H2 (saque inicial 2T)                  │
│      │   ├── EXTRA_TIME_H1 (prórroga 1T)                    │
│      │   ├── EXTRA_TIME_H2 (prórroga 2T)                    │
│      │   ├── PENALTIES (tanda de penaltis)                   │
│      │   ├── FULL_TIME (final del partido)                   │
│      │   └── POST_MATCH (estadísticas)                       │
│      │                                                        │
│      └── SubEstados de DEAD_BALL:                            │
│          ├── THROW_IN (saque de banda)                       │
│          ├── GOAL_KICK (saque de puerta)                     │
│          ├── CORNER_KICK (córner)                            │
│          ├── FREE_KICK (tiro libre)                          │
│          ├── PENALTY (penalti)                               │
│          ├── OFFSIDE (fuera de juego)                        │
│          └── SUBSTITUTION (cambio)                           │
│                                                               │
└───────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                       FLUJO DE NAVEGACIÓN                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐                                                    │
│  │ SPLASH      │                                                    │
│  │ SCREEN      │                                                    │
│  └──────┬──────┘                                                    │
│         ▼                                                           │
│  ┌─────────────┐     ┌──────────────┐     ┌─────────────────┐      │
│  │ MENÚ        │────▶│ NUEVA        │────▶│ ELEGIR LIGA     │      │
│  │ PRINCIPAL   │     │ PARTIDA      │     └────────┬────────┘      │
│  │             │     └──────────────┘              ▼                │
│  │ • Nueva     │     ┌──────────────┐     ┌─────────────────┐      │
│  │ • Cargar    │────▶│ CARGAR       │     │ ELEGIR EQUIPO   │      │
│  │ • Opciones  │     │ PARTIDA      │     └────────┬────────┘      │
│  │ • Créditos  │     └──────┬───────┘              ▼                │
│  │ • Salir     │            │             ┌─────────────────┐      │
│  └─────────────┘            │             │ PERFIL MÁNAGER  │      │
│                             │             └────────┬────────┘      │
│                             │                      ▼                │
│                             │    ┌──────────────────────────────┐   │
│                             └───▶│                              │   │
│                                  │     📋 DESPACHO (OFFICE)     │   │
│                                  │     ══════════════════════   │   │
│                                  │     Hub central del juego    │   │
│                                  │                              │   │
│                                  └──────────────┬───────────────┘   │
│                                                 │                   │
│            ┌────────┬────────┬─────────┬────────┼────────┬──────┐   │
│            ▼        ▼        ▼         ▼        ▼        ▼      ▼   │
│       ┌────────┐┌───────┐┌───────┐┌────────┐┌──────┐┌──────┐┌─────┐│
│       │PLANTIL-││TÁCTI- ││FICHA- ││FINAN-  ││ESTA- ││STAFF ││LIGA ││
│       │LA      ││CA     ││JES    ││ZAS     ││DIO   ││      ││     ││
│       └───┬────┘└───┬───┘└───┬───┘└───┬────┘└──┬───┘└──┬───┘└──┬──┘│
│           │         │        │        │        │       │       │    │
│           ▼         ▼        ▼        ▼        ▼       ▼       ▼    │
│       ┌────────┐┌───────┐┌───────┐┌────────┐┌──────┐┌──────┐┌─────┐│
│       │Detalle ││Editor ││Buscar ││Balance ││Obras ││Scout ││Clasi││
│       │jugador ││forma- ││jugad. ││mensual ││en    ││repor-││fica-││
│       │        ││ción   ││       ││        ││curso ││tes   ││ción ││
│       │Compara-││Instr. ││Negoci-││Sponsors││Ciudad││Asig- ││     ││
│       │tiva    ││tácti- ││ación  ││        ││depor-││nar   ││Calen││
│       │        ││cas    ││       ││Proyec- ││tiva  ││regio-││dario││
│       │Histor- ││       ││Oferta ││ción    ││      ││nes   ││     ││
│       │ial     ││Balón  ││recib. ││        ││Nuevo ││      ││Copa ││
│       └────────┘│parado ││       ││Salary  ││esta- ││Contra││     ││
│                 └───────┘│Presta-││cap     ││dio   ││tar   ││Otras││
│                          │mos    ││        ││      ││      ││ligas││
│                          └───────┘└────────┘└──────┘└──────┘└─────┘│
│                                                                     │
│       ┌────────┐ ┌─────────┐ ┌──────────┐ ┌───────────┐            │
│       │CANTERA │ │ENTRENA- │ │DIRECTIVA │ │NOTICIAS   │            │
│       │        │ │MIENTO   │ │          │ │           │            │
│       │Juveni- │ │Plan     │ │Objetivos │ │Periódico  │            │
│       │les     │ │semanal  │ │Confianza │ │Archivo    │            │
│       │Promo-  │ │Plan     │ │Reunión   │ │Rueda de   │            │
│       │cionar  │ │individ. │ │          │ │prensa     │            │
│       │Cesión  │ │Pretem-  │ │          │ │           │            │
│       └────────┘ │porada   │ └──────────┘ └───────────┘            │
│                  └─────────┘                                        │
│                                                                     │
│                                                                     │
│                  ┌──────────────────────────────────┐               │
│    Desde el ───▶ │        ⚽ PARTIDO                │               │
│    calendario    │                                  │               │
│    cuando hay    │  ┌──────┐  ┌──────┐  ┌────────┐  │               │
│    partido       │  │PREVIA│─▶│JUGAR │─▶│RESULT. │  │               │
│                  │  │      │  │  O   │  │        │  │               │
│                  │  │Aline.│  │SIMUL.│  │Estadís.│  │               │
│                  │  │Tácti.│  │  O   │  │Notas   │  │               │
│                  │  │      │  │ VER  │  │        │  │               │
│                  │  └──────┘  └──────┘  └───┬────┘  │               │
│                  │                          │       │               │
│                  └──────────────────────────┼───────┘               │
│                                             │                       │
│                                             ▼                       │
│                                     Vuelve al DESPACHO              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                  GAME LOOP PRINCIPAL                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐                                        │
│  │ Jugador está     │                                        │
│  │ en DESPACHO      │◄──────────────────────────┐           │
│  └────────┬─────────┘                           │           │
│           │                                      │           │
│           ▼                                      │           │
│  ┌─────────────────────────────┐                │           │
│  │ Gestiona su equipo:        │                │           │
│  │ • Revisa noticias          │                │           │
│  │ • Hace fichajes            │                │           │
│  │ • Prepara táctica          │                │           │
│  │ • Gestiona estadio         │                │           │
│  │ • Entrena jugadores        │                │           │
│  │ • etc.                     │                │           │
│  └────────┬───────────────────┘                │           │
│           │                                      │           │
│           ▼                                      │           │
│  ┌─────────────────────────────┐                │           │
│  │ AVANZAR TIEMPO              │                │           │
│  │ (botón "Avanzar día" o      │                │           │
│  │  "Avanzar al próximo        │                │           │
│  │   partido")                 │                │           │
│  └────────┬───────────────────┘                │           │
│           │                                      │           │
│           ▼                                      │           │
│  ┌─────────────────────────────┐                │           │
│  │ PROCESAMIENTO DIARIO:       │                │           │
│  │                             │                │           │
│  │ Por cada día avanzado:      │                │           │
│  │ ├── Calendar: check eventos │                │           │
│  │ ├── Training: procesar      │                │           │
│  │ ├── Medical: recuperación   │                │           │
│  │ ├── Construction: progreso  │                │           │
│  │ ├── Transfers: IA negocia   │                │           │
│  │ ├── Economy: gastos diarios │                │           │
│  │ ├── News: generar noticias  │                │           │
│  │ ├── Moral: actualizar       │                │           │
│  │ └── Board: evaluar          │                │           │
│  └────────┬───────────────────┘                │           │
│           │                                      │           │
│           ▼                                      │           │
│  ┌─────────────────────────────┐                │           │
│  │ ¿HAY PARTIDO HOY?           │                │           │
│  │                             │                │           │
│  │    NO ──────────────────────┼────────────────┘           │
│  │                             │                            │
│  │    SÍ                       │                            │
│  └────────┬───────────────────┘                             │
│           │                                                  │
│           ▼                                                  │
│  ┌─────────────────────────────┐                             │
│  │ PREVIA DEL PARTIDO          │                             │
│  │ • Confirmar alineación      │                             │
│  │ • Últimos ajustes tácticos  │                             │
│  │ • Elegir: JUGAR / VER /     │                             │
│  │   SIMULAR                   │                             │
│  └────────┬───────────────────┘                             │
│           │                                                  │
│     ┌─────┼──────────────┐                                  │
│     │     │              │                                   │
│     ▼     ▼              ▼                                   │
│  ┌──────┐┌──────┐ ┌───────────┐                             │
│  │JUGAR ││ VER  │ │ SIMULAR   │                             │
│  │3D    ││ 3D   │ │ (instant) │                             │
│  │      ││      │ │           │                             │
│  │Contro││Auto +│ │S06 motor  │                             │
│  │las tu││veloc.│ │matemático │                             │
│  │equipo││      │ │           │                             │
│  └──┬───┘└──┬───┘ └─────┬─────┘                             │
│     │       │            │                                   │
│     └───────┴────────────┘                                   │
│                 │                                            │
│                 ▼                                            │
│  ┌─────────────────────────────┐                             │
│  │ RESULTADO DEL PARTIDO       │                             │
│  │ • Actualizar estadísticas   │                             │
│  │ • Actualizar clasificación  │                             │
│  │ • Procesar lesiones         │                             │
│  │ • Procesar tarjetas         │                             │
│  │ • Calcular ingresos taquilla│                             │
│  │ • Actualizar moral          │                             │
│  │ • Generar noticias          │                             │
│  │ • Evaluar directiva         │                             │
│  └────────┬───────────────────┘                             │
│           │                                                  │
│           ▼                                                  │
│  ┌─────────────────────────────┐                             │
│  │ PANTALLA POST-PARTIDO       │                             │
│  │ • Resultado y estadísticas  │──────▶ Vuelve al DESPACHO  │
│  │ • Puntuaciones jugadores    │                             │
│  │ • Noticias generadas        │                             │
│  └─────────────────────────────┘                             │
│                                                              │
│                                                              │
│  ═══════════════════════════════════════════                  │
│  PROCESOS SEMANALES (cada 7 días):                           │
│  ├── Pago de salarios                                        │
│  ├── Informe financiero semanal                              │
│  ├── Autosave                                                │
│  ├── Actualizar forma física                                 │
│  └── Procesar ojeadores (avance informes)                    │
│                                                              │
│  PROCESOS MENSUALES (cada 30 días):                          │
│  ├── Cobro de sponsors                                       │
│  ├── Cobro de socios/abonados                                │
│  ├── Reporte financiero mensual                              │
│  ├── Evaluación directiva                                    │
│  ├── Desarrollo de jugadores                                 │
│  ├── Deterioro de instalaciones                              │
│  └── Actualizar valores de mercado                           │
│                                                              │
│  PROCESOS DE FIN DE TEMPORADA:                               │
│  ├── Calcular ascensos/descensos                             │
│  ├── Repartir premios económicos                             │
│  ├── Procesar fin de contratos                               │
│  ├── Generar canteranos nuevos                               │
│  ├── Retirada de jugadores veteranos                         │
│  ├── Sorteo nuevas competiciones                             │
│  ├── Premios (Balón de Oro, MVP, etc.)                       │
│  ├── Evaluar cumplimiento objetivos                          │
│  ├── Nuevo presupuesto de temporada                          │
│  ├── Envejecer todos los jugadores +1 año                    │
│  ├── Declive de veteranos                                    │
│  └── Cambios de directiva (si toca)                          │
│                                                              │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                   SISTEMA TÁCTICO                            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  FORMACIONES DISPONIBLES:                                    │
│  ┌──────────────────────────────────────────┐                │
│  │                                          │                │
│  │  4-4-2       4-3-3       4-2-3-1         │                │
│  │  ○           ○  ○  ○        ○            │                │
│  │  ○  ○       ○  ○  ○     ○  ○  ○         │                │
│  │  ○  ○  ○  ○    ○  ○  ○    ○  ○          │                │
│  │  ○  ○  ○  ○  ○  ○  ○  ○  ○  ○  ○  ○    │                │
│  │     ●              ●           ●         │                │
│  │                                          │                │
│  │  3-5-2       4-1-4-1     4-4-1-1         │                │
│  │  ○  ○        ○           ○               │                │
│  │  ○  ○  ○  ○  ○  ○  ○  ○     ○           │                │
│  │  ○  ○  ○       ○        ○  ○  ○  ○      │                │
│  │  ○  ○  ○     ○  ○  ○  ○  ○  ○  ○  ○    │                │
│  │     ●              ●           ●         │                │
│  │                                          │                │
│  │  5-3-2       3-4-3       4-5-1           │                │
│  │  ○  ○       ○  ○  ○        ○             │                │
│  │  ○  ○  ○     ○  ○  ○  ○  ○  ○  ○  ○     │                │
│  │  ○  ○  ○  ○  ○     ○  ○  ○     ○        │                │
│  │  ○  ○  ○  ○  ○  ○  ○  ○  ○  ○  ○  ○    │                │
│  │     ●              ●           ●         │                │
│  │                                          │                │
│  └──────────────────────────────────────────┘                │
│                                                              │
│  INSTRUCCIONES DE EQUIPO:                                    │
│  ├── Estilo de juego:                                        │
│  │   ├── Posesión (pases cortos, paciencia)                 │
│  │   ├── Contraataque (directo, velocidad)                  │
│  │   ├── Juego directo (balones largos)                     │
│  │   ├── Pressing alto (presión arriba)                     │
│  │   └── Equilibrado                                        │
│  │                                                           │
│  ├── Mentalidad:                                             │
│  │   ├── Ultradefensiva (aparcar el bus)                    │
│  │   ├── Defensiva                                          │
│  │   ├── Equilibrada                                        │
│  │   ├── Ofensiva                                           │
│  │   └── Ultraofensiva (all-in)                             │
│  │                                                           │
│  ├── Presión:                                                │
│  │   ├── Baja (esperan atrás)                               │
│  │   ├── Media                                              │
│  │   └── Alta (pressing constante, gasta stamina)           │
│  │                                                           │
│  ├── Línea defensiva:                                        │
│  │   ├── Muy retrasada                                      │
│  │   ├── Retrasada                                          │
│  │   ├── Normal                                             │
│  │   ├── Adelantada                                         │
│  │   └── Muy adelantada (trampa del fuera de juego)         │
│  │                                                           │
│  ├── Amplitud:                                               │
│  │   ├── Estrecho (juego interior)                          │
│  │   ├── Normal                                             │
│  │   └── Amplio (juego por bandas)                          │
│  │                                                           │
│  └── Tempo:                                                  │
│      ├── Lento (retener balón)                              │
│      ├── Normal                                             │
│      └── Rápido (transiciones veloces)                      │
│                                                              │
│  INSTRUCCIONES INDIVIDUALES (por jugador):                   │
│  ├── Rol específico:                                         │
│  │   ├── Lateral: "Subir al ataque" / "Quedarse atrás"     │
│  │   ├── Central: "Salir con balón" / "Despejar"           │
│  │   ├── Mediocentro: "Llegar al área" / "Quedarse"        │
│  │   ├── Extremo: "Recortar adentro" / "Ir a línea fondo" │
│  │   └── Delantero: "Fijar central" / "Movilidad libre"    │
│  │                                                           │
│  ├── Libertad creativa:                                      │
│  │   ├── Disciplinado (sigue instrucciones al pie)          │
│  │   ├── Normal                                             │
│  │   └── Libre (toma decisiones propias, impredecible,     │
│  │       mejor para jugadores con alta visión/compostura)   │
│  │                                                           │
│  ├── Marcaje:                                                │
│  │   ├── Zonal (marca zona, no jugador)                     │
│  │   ├── Individual (sigue a un rival asignado)             │
│  │   └── Mixto                                              │
│  │                                                           │
│  └── Corners y balón parado:                                 │
│      ├── Asignar lanzador de corners                        │
│      ├── Asignar lanzador de faltas                         │
│      ├── Asignar lanzador de penaltis                       │
│      ├── Jugadores en barrera                                │
│      ├── Jugadores que suben al área en corner              │
│      └── Jugador que queda atrás en corner                  │
│                                                              │
│  CÓMO AFECTA LA TÁCTICA AL MATCH ENGINE:                    │
│  ┌──────────────────────────────────────────────┐            │
│  │                                              │            │
│  │  Cada instrucción modifica PARÁMETROS        │            │
│  │  internos de la IA de equipo y jugadores:    │            │
│  │                                              │            │
│  │  Mentalidad Ofensiva:                        │            │
│  │   → jugadores_suben_linea = true             │            │
│  │   → umbral_disparo = bajo (tiran más)        │            │
│  │   → cobertura_defensiva = reducida           │            │
│  │   → riesgo_pase = alto (pases más largos)    │            │
│  │                                              │            │
│  │  Pressing Alto:                              │            │
│  │   → zona_presion = campo_rival               │            │
│  │   → agresividad_recuperacion = alta           │            │
│  │   → desgaste_stamina = +30%                  │            │
│  │   → probabilidad_robo = +20%                 │            │
│  │                                              │            │
│  │  Posesión:                                   │            │
│  │   → preferencia_pase_corto = +40%            │            │
│  │   → tiempo_con_balon = retener               │            │
│  │   → movimiento_sin_balon = crear_lineas      │            │
│  │   → riesgo_pase = bajo                       │            │
│  │                                              │            │
│  │  Contraataque:                               │            │
│  │   → velocidad_transicion = máxima            │            │
│  │   → jugadores_en_ataque_rapido = 3-4         │            │
│  │   → pases_directos_al_espacio = +50%         │            │
│  │   → retener_balon = mínimo                   │            │
│  │                                              │            │
│  │  Línea Adelantada:                           │            │
│  │   → posicion_y_defensas = 60% campo          │            │
│  │   → trampa_offside = activa                  │            │
│  │   → espacio_a_espalda = vulnerable           │            │
│  │   → presion_natural = mayor                  │            │
│  │                                              │            │
│  └──────────────────────────────────────────────┘            │
│                                                              │
│  POSICIONES DETALLADAS EN EL CAMPO:                          │
│  (Coordenadas base que la formación asigna)                  │
│                                                              │
│  ┌─── Campo (coordenadas normalizadas 0-100) ───┐           │
│  │                                               │           │
│  │  POR:  (50, 5)                                │           │
│  │                                               │           │
│  │  DFC:  (35, 20) (65, 20)                     │           │
│  │  LI:   (10, 25)                              │           │
│  │  LD:   (90, 25)                              │           │
│  │                                               │           │
│  │  MCD:  (50, 35)                              │           │
│  │  MC:   (35, 45) (65, 45)                     │           │
│  │  MCO:  (50, 55)                              │           │
│  │                                               │           │
│  │  EI:   (15, 65)                              │           │
│  │  ED:   (85, 65)                              │           │
│  │                                               │           │
│  │  DC:   (40, 80) (60, 80)                     │           │
│  │  MP:   (50, 72)                              │           │
│  │                                               │           │
│  │  (Estas posiciones se ajustan dinámicamente   │           │
│  │   según mentalidad, amplitud, línea defensiva │           │
│  │   y situación del partido)                    │           │
│  │                                               │           │
│  └───────────────────────────────────────────────┘           │
│                                                              │
│  TÁCTICAS GUARDADAS:                                         │
│  ├── El jugador puede guardar 3 tácticas predefinidas       │
│  │   ├── Táctica A (ej: "Normal 4-3-3")                    │
│  │   ├── Táctica B (ej: "Defensiva 5-4-1")                 │
│  │   └── Táctica C (ej: "All-in 3-4-3")                    │
│  ├── Cambio rápido durante partido (Tab → elegir A/B/C)     │
│  └── IA del rival también cambia táctica durante partido     │
│      según resultado y minuto                                │
│                                                              │
│  ARCHIVO: core/match/formation_manager.gd                    │
│                                                              │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│              INTELIGENCIA ARTIFICIAL DEL PARTIDO              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ═══════════════════════════════════════                      │
│  NIVEL 1: IA DE EQUIPO (TeamAI)                              │
│  ═══════════════════════════════════════                      │
│                                                              │
│  Decide la ESTRATEGIA general del equipo rival (y de tu      │
│  equipo cuando no controlas directamente a un jugador).      │
│                                                              │
│  DECISIONES:                                                 │
│  ├── ¿Presionar o replegar?                                  │
│  │   → Basado en: resultado, minuto, stamina general,       │
│  │     táctica asignada, importancia del partido             │
│  │                                                           │
│  ├── ¿Cambiar formación durante el partido?                  │
│  │   → Si pierde por 2+ goles en min 60+ → más ofensivo    │
│  │   → Si gana por 1 en min 80+ → más defensivo             │
│  │   → Si expulsado → ajustar formación                     │
│  │                                                           │
│  ├── ¿Hacer sustituciones?                                   │
│  │   → Jugador con stamina <30%                             │
│  │   → Jugador con amarilla y jugando agresivo              │
│  │   → Jugador rindiendo mal (puntuación <5)                │
│  │   → Cambio táctico (meter delantero si pierde)           │
│  │   → Regla: máximo 5 cambios en 3 ventanas               │
│  │                                                           │
│  ├── Posesión de equipo:                                     │
│  │   → Mover el "centro de gravedad" del equipo             │
│  │   → Equipo ataca: línea sube                             │
│  │   → Equipo defiende: línea baja                          │
│  │   → Transición: velocidad según táctica                  │
│  │                                                           │
│  └── Balón parado:                                           │
│      → Elegir tipo de jugada ensayada                       │
│      → Asignar marcas en corners defensivos                 │
│                                                              │
│  ═══════════════════════════════════════                      │
│  NIVEL 2: IA DE JUGADOR (PlayerAI)                           │
│  ═══════════════════════════════════════                      │
│                                                              │
│  Cada jugador individual decide sus acciones.                │
│  La calidad de las decisiones depende de sus ATRIBUTOS.      │
│                                                              │
│  MÁQUINA DE ESTADOS:                                         │
│  ┌─────────────────────────────────────────────────┐         │
│  │                                                 │         │
│  │              ┌────────────────┐                  │         │
│  │         ┌───▶│ EN_POSICION    │◀───┐             │         │
│  │         │    │ (mantener      │    │             │         │
│  │         │    │  formación)    │    │             │         │
│  │         │    └───────┬────────┘    │             │         │
│  │         │            │             │             │         │
│  │         │    ¿Balón cerca?         │             │         │
│  │         │    ¿Compañero lo tiene?  │             │         │
│  │         │            │             │             │         │
│  │         │     ┌──────┴──────┐      │             │         │
│  │         │     ▼             ▼      │             │         │
│  │    ┌────────────┐  ┌────────────┐  │             │         │
│  │    │ ATACANDO   │  │DEFENDIENDO │  │             │         │
│  │    │ SIN_BALON  │  │ SIN_BALON  │  │             │         │
│  │    │            │  │            │  │             │         │
│  │    │•Desmarque  │  │•Marcar     │  │             │         │
│  │    │•Pedir pase │  │•Cerrar     │  │             │         │
│  │    │•Crear      │  │ espacio    │  │             │         │
│  │    │ espacio    │  │•Presionar  │  │             │         │
│  │    │•Correr al  │  │•Replegar   │  │             │         │
│  │    │ espacio    │  │•Interceptar│  │             │         │
│  │    └─────┬──────┘  └──────┬─────┘  │             │         │
│  │          │                │        │             │         │
│  │          │  (recibe balón)│(roba)  │             │         │
│  │          ▼                ▼        │             │         │
│  │    ┌──────────────────────────┐    │             │         │
│  │    │     CON_BALON            │    │             │         │
│  │    │                          │    │             │         │
│  │    │ Evalúa opciones:         │    │             │         │
│  │    │ ├── Pasar (a quién?)     │    │             │         │
│  │    │ ├── Disparar (si cerca)  │    │             │         │
│  │    │ ├── Regatear (si rival)  │    │             │         │
│  │    │ ├── Centrar (si banda)   │    │             │         │
│  │    │ ├── Conducir (si espacio)│    │             │         │
│  │    │ └── Retener (si no hay   │    │             │         │
│  │    │     opción clara)        │    │             │         │
│  │    │                          │    │             │         │
│  │    │ Calidad decisión =       │    │             │         │
│  │    │   f(vision, compostura,  │    │             │         │
│  │    │     presion_rival)       │    │             │         │
│  │    └────────────┬─────────────┘    │             │         │
│  │                 │                  │             │         │
│  │          (pierde balón)            │             │         │
│  │                 │                  │             │         │
│  │                 ▼                  │             │         │
│  │    ┌──────────────────────────┐    │             │         │
│  │    │  PERSIGUIENDO_BALON      │────┘             │         │
│  │    │  (transición def.)       │                  │         │
│  │    └──────────────────────────┘                  │         │
│  │                                                  │         │
│  │  ESTADOS ESPECIALES:                             │         │
│  │  ├── CELEBRANDO_GOL                              │         │
│  │  ├── ESPERANDO_BALON_PARADO                      │         │
│  │  ├── LANZANDO_FALTA                              │         │
│  │  ├── SACANDO_BANDA                               │         │
│  │  ├── LESIONADO_SUELO                             │         │
│  │  └── SALIENDO_CAMPO (sustituido)                 │         │
│  │                                                  │         │
│  └──────────────────────────────────────────────────┘         │
│                                                              │
│  ═══════════════════════════════════════                      │
│  NIVEL 3: IA DE PORTERO (GoalkeeperAI)                       │
│  ═══════════════════════════════════════                      │
│                                                              │
│  ESTADOS:                                                    │
│  ├── POSICIONANDOSE                                          │
│  │   → Se mueve en arco según posición del balón             │
│  │   → Atributo: posicionamiento_por                        │
│  │                                                           │
│  ├── PREPARADO (balón viene hacia portería)                  │
│  │   → Se agacha, listo para reaccionar                     │
│  │   → Tiempo de reacción = f(reflejos)                     │
│  │                                                           │
│  ├── ESTIRADA (disparo detectado)                            │
│  │   → Dirección de estirada basada en:                     │
│  │     ├── reflejos (tiempo para reaccionar)                │
│  │     ├── parada (alcance de la estirada)                  │
│  │     ├── posicionamiento (ya estaba bien ubicado?)        │
│  │     └── Algo de aleatoriedad (no sea infalible)          │
│  │   → Resultado: atrapa / despeja / no llega / gol         │
│  │                                                           │
│  ├── SALIDA (1 vs 1)                                         │
│  │   → Decide salir a achicar si delantero viene solo       │
│  │   → Riesgo: si falla, gol cantado                        │
│  │   → Éxito basado en: reflejos + compostura               │
│  │                                                           │
│  ├── DESPEJANDO                                              │
│  │   → Balón alto al área: sale a por él o se queda?        │
│  │   → Decide puñetazo vs atrapar                           │
│  │                                                           │
│  └── DISTRIBUYENDO                                           │
│      → Tras atrapar: saque con mano vs pie                  │
│      → Calidad del pase = f(saque_portero)                  │
│      → Puede lanzar contraataque rápido                     │
│                                                              │
│  ═══════════════════════════════════════                      │
│  DECISIONES DETALLADAS: CON_BALON                            │
│  ═══════════════════════════════════════                      │
│                                                              │
│  Cuando un jugador IA tiene el balón, evalúa:               │
│                                                              │
│  DISPARAR:                                                   │
│  ├── ¿Distancia a portería < 25m?                           │
│  ├── ¿Ángulo de tiro > 15°?                                │
│  ├── ¿Hay hueco (no hay pierna que bloquea)?                │
│  ├── Score = disparo * 0.4 + compostura * 0.2               │
│  │          + posicion * 0.2 - distancia * 0.2              │
│  └── Si score > umbral_disparo → DISPARA                    │
│                                                              │
│  PASAR:                                                      │
│  ├── Evalúa TODOS los compañeros visibles                   │
│  ├── Para cada compañero calcula:                            │
│  │   ├── ¿Está libre de marca? (+30 score)                  │
│  │   ├── ¿Está en mejor posición? (+20)                     │
│  │   ├── ¿Distancia del pase? (-1 por metro)               │
│  │   ├── ¿Hay rivales en la línea de pase? (-40)           │
│  │   ├── ¿Está en posición de gol? (+50)                    │
│  │   └── ¿Es un pase atrás/lateral/adelante?               │
│  ├── Elige el compañero con mayor score                     │
│  ├── Precisión del pase = f(pase_corto o pase_largo,        │
│  │   compostura, presión rival)                             │
│  └── Pase fallido si: random > precisión                    │
│      (balón va desviado, interceptado)                      │
│                                                              │
│  REGATEAR:                                                   │
│  ├── ¿Hay rival a <2m por delante?                          │
│  ├── ¿Regate del atacante vs defensa del rival?             │
│  ├── Éxito: atacante pasa al rival                          │
│  ├── Fracaso: pierde balón                                  │
│  └── Probabilidad = regate / (regate + defensa_rival) * 100 │
│                                                              │
│  CENTRAR:                                                    │
│  ├── Si está en banda y hay compañeros en área              │
│  ├── Calidad = f(centro, pase_largo)                        │
│  ├── Centro bueno → llega al compañero → cabezazo          │
│  └── Centro malo → despejado, fuera, portero atrapa        │
│                                                              │
│  CONDUCIR:                                                   │
│  ├── Si hay espacio libre adelante                          │
│  ├── Velocidad de conducción = velocidad * 0.85             │
│  ├── Riesgo de perder balón si rival se acerca              │
│  │   = f(regate, control, compostura)                       │
│  └── Decisión de cuándo soltar el balón                     │
│                                                              │
│  ═══════════════════════════════════════                      │
│  DIFICULTAD (afecta IA rival)                                │
│  ═══════════════════════════════════════                      │
│                                                              │
│  ┌───────────┬──────────────────────────────────────┐        │
│  │ Dificultad│ Efectos                              │        │
│  ├───────────┼──────────────────────────────────────┤        │
│  │ Fácil     │ IA toma peores decisiones            │        │
│  │           │ Portero rival reacciona más lento    │        │
│  │           │ Rivales presionan menos              │        │
│  │           │ Tus jugadores +5% en atributos       │        │
│  │           │ Más tiempo para decidir con balón    │        │
│  ├───────────┼──────────────────────────────────────┤        │
│  │ Normal    │ Sin modificadores                    │        │
│  │           │ Juego balanceado                     │        │
│  ├───────────┼──────────────────────────────────────┤        │
│  │ Difícil   │ IA toma decisiones óptimas           │        │
│  │           │ Portero rival reacciona más rápido   │        │
│  │           │ Rivales presionan más inteligente    │        │
│  │           │ Menos errores no forzados del rival  │        │
│  │           │ Tus jugadores -5% en atributos       │        │
│  ├───────────┼──────────────────────────────────────┤        │
│  │ Leyenda   │ IA casi perfecta                     │        │
│  │           │ Rivales leen tus jugadas             │        │
│  │           │ Portero rival es un muro             │        │
│  │           │ Errores de IA casi inexistentes      │        │
│  │           │ Tus jugadores -10% en atributos      │        │
│  └───────────┴──────────────────────────────────────┘        │
│                                                              │
│  ARCHIVOS:                                                   │
│  ├── core/match/team_ai.gd                                  │
│  ├── core/match/player_ai.gd                                │
│  ├── core/match/goalkeeper_ai.gd                             │
│  └── core/match/ai_decision_maker.gd                        │
│                                                              │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                   FÍSICA DEL BALÓN                            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  El balón es un RigidBody3D con física customizada.          │
│  NO usamos 100% la física de Godot porque necesitamos       │
│  control preciso para que sea "jugable y divertido".         │
│                                                              │
│  PROPIEDADES FÍSICAS:                                        │
│  ├── masa: 0.43 kg (reglamentaria)                          │
│  ├── radio: 0.11 m                                          │
│  ├── bounce: 0.6 (rebote en suelo)                          │
│  ├── friction_suelo: 0.4 (desaceleración)                   │
│  ├── friction_aire: 0.01 (resistencia)                      │
│  ├── gravity: 9.8 m/s²                                      │
│  └── max_velocity: 45 m/s (~162 km/h, disparo máximo)       │
│                                                              │
│  TIPOS DE TOQUE:                                             │
│  ┌──────────────────┬──────────┬────────┬──────────────────┐ │
│  │ Tipo             │Vel (m/s) │Altura  │ Efecto           │ │
│  ├──────────────────┼──────────┼────────┼──────────────────┤ │
│  │ Pase corto       │ 8-15     │ Raso   │ Bajo             │ │
│  │ Pase largo       │ 15-25    │ Alto   │ Medio            │ │
│  │ Centro           │ 18-28    │ Alto   │ Medio-Alto       │ │
│  │ Disparo raso     │ 20-35    │ Raso   │ Bajo-Medio       │ │
│  │ Disparo alto     │ 25-40    │ Medio  │ Medio            │ │
│  │ Disparo potente  │ 30-45    │ Medio  │ Bajo             │ │
│  │ Tiro libre       │ 20-35    │ Medio  │ Alto (curva)     │ │
│  │ Cabezazo         │ 10-25    │ Medio  │ Bajo             │ │
│  │ Volea            │ 25-40    │ Var.   │ Medio            │ │
│  │ Saque banda      │ 10-18    │ Medio  │ Ninguno          │ │
│  │ Saque puerta     │ 25-35    │ Alto   │ Bajo             │ │
│  │ Despeje          │ 15-30    │ Alto   │ Aleatorio        │ │
│  │ Control          │ 0-3      │ Raso   │ Ninguno          │ │
│  │ Regate (toque)   │ 2-5      │ Raso   │ Ninguno          │ │
│  └──────────────────┴──────────┴────────┴──────────────────┘ │
│                                                              │
│  SISTEMA DE EFECTO (SPIN):                                   │
│  ├── El efecto del balón crea curva en el aire               │
│  ├── Calculado por:                                          │
│  │   ├── atributo "efecto" del jugador                      │
│  │   ├── tipo de golpeo                                     │
│  │   └── input del jugador (dirección al disparar)          │
│  ├── Implementación:                                         │
│  │   → Fuerza lateral aplicada al balón en vuelo            │
│  │   → fuerza_curva = efecto_jugador * spin_factor          │
│  │   → Se aplica perpendicular a la dirección               │
│  └── Especialmente visible en tiros libres                   │
│                                                              │
│  DISPARO (mecánica de potencia):                             │
│  ├── Jugador presiona Shift para disparar                    │
│  ├── Barra de potencia se llena mientras mantiene            │
│  │   ┌────────────────────────────────┐                      │
│  │   │ ░░░░░░░░▓▓▓▓▓▓▓▓████████████ │                      │
│  │   │ Suave    Óptimo    Demasiado   │                      │
│  │   │          (zona verde)  fuerte  │                      │
│  │   └────────────────────────────────┘                      │
│  ├── Soltar en zona óptima = disparo preciso                │
│  ├── Soltar demasiado tarde = balón se va alto/fuera        │
│  ├── Precisión final = f(disparo, compostura, potencia,     │
│  │   presión rival, pie hábil)                              │
│  └── Dirección: combinación de hacia dónde mira el          │
│      jugador + input del joystick/flechas al soltar         │
│                                                              │
│  RECEPCIÓN/CONTROL:                                          │
│  ├── Cuando balón llega a un jugador:                       │
│  │   ├── Control perfecto: balón queda a sus pies           │
│  │   ├── Control normal: balón rebota un poco               │
│  │   ├── Mal control: balón se aleja ~2-3m                  │
│  │   └── Error: balón se va lejos, pierde posesión          │
│  ├── Probabilidad = f(control, compostura,                  │
│  │   velocidad_balon, presion_rival, pie_habil)             │
│  └── Primer toque importante: buen control = ventaja        │
│                                                              │
│  DETECCIÓN DE GOL:                                           │
│  ├── Area3D dentro de la portería                           │
│  ├── Si centro del balón cruza la línea completamente       │
│  │   → GOL                                                  │
│  ├── Trigger: señal "body_entered" del área                 │
│  └── Replay: se graba posición del balón los últimos        │
│      3 segundos para repetición                             │
│                                                              │
│  COLISIONES:                                                 │
│  ├── Balón vs Poste: rebote con sonido metálico             │
│  ├── Balón vs Red: velocidad = 0, animación de red          │
│  ├── Balón vs Jugador: basado en parte del cuerpo           │
│  │   ├── Pie: control o despeje                             │
│  │   ├── Cabeza: cabezazo                                   │
│  │   ├── Pecho: control alto                                │
│  │   ├── Mano (no portero): posible mano → falta           │
│  │   └── Cuerpo: rebote natural                             │
│  ├── Balón vs Suelo: rebote con friction                    │
│  └── Balón vs Límites: fuera de juego detectado             │
│                                                              │
│  ARCHIVO: core/match/ball_physics.gd                         │
│                                                              │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                   SISTEMA DE LESIONES                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  CAUSAS DE LESIÓN:                                           │
│  ├── En partido:                                             │
│  │   ├── Entrada dura de rival (falta)                      │
│  │   ├── Sobreesfuerzo (stamina <10%)                       │
│  │   ├── Jugador con forma física baja                      │
│  │   ├── Mal estado del césped                              │
│  │   └── Mala suerte (aleatoria, muy baja prob.)           │
│  │                                                           │
│  └── Fuera de partido:                                       │
│      ├── Entrenamiento intenso con mala preparación         │
│      └── Recaída de lesión anterior                         │
│                                                              │
│  TIPOS DE LESIÓN:                                            │
│  ┌──────────────────────┬───────────┬──────────────────────┐ │
│  │ Lesión               │ Duración  │ Probabilidad         │ │
│  ├──────────────────────┼───────────┼──────────────────────┤ │
│  │ Contractura leve     │ 3-7 días  │ Alta (40%)           │ │
│  │ Distensión muscular  │ 7-14 días │ Media (20%)          │ │
│  │ Esguince tobillo     │ 14-28 días│ Media (15%)          │ │
│  │ Rotura fibrilar      │ 21-42 días│ Media-baja (10%)     │ │
│  │ Lesión menisco       │ 30-60 días│ Baja (5%)            │ │
│  │ Rotura ligamentos    │ 120-270d  │ Muy baja (3%)        │ │
│  │ Fractura             │ 60-120 d  │ Muy baja (3%)        │ │
│  │ Rotura LCA (cruzado) │ 180-300d  │ Rara (2%)            │ │
│  │ Lesión espalda       │ 14-42 días│ Baja (2%)            │ │
│  └──────────────────────┴───────────┴──────────────────────┘ │
│                                                              │
│  FACTORES QUE AFECTAN PROBABILIDAD:                          │
│  ├── Edad (>30 = más riesgo, +2% por año)                  │
│  ├── Forma física baja (×2 riesgo)                          │
│  ├── Historial de lesiones (recidiva +30%)                  │
│  ├── Calidad del preparador físico (-20% a -50%)            │
│  ├── Calidad del césped (-10% a +20%)                       │
│  ├── Nivel del gimnasio (-10% a -30%)                       │
│  ├── Minutos jugados sin descanso (+riesgo)                 │
│  └── Profesionalismo (alto = cuida su cuerpo, -15%)        │
│                                                              │
│  FACTORES QUE AFECTAN RECUPERACIÓN:                          │
│  ├── Calidad staff médico (-10% a -40% tiempo)             │
│  ├── Nivel centro médico (-10% a -30%)                      │
│  ├── Edad (jóvenes recuperan más rápido)                    │
│  ├── Físico del jugador (alto = más rápido)                │
│  └── ¿Volvió antes de tiempo? (riesgo recaída +50%)        │
│                                                              │
│  DIAGNÓSTICO:                                                │
│  ├── El médico da un tiempo estimado                        │
│  ├── Precisión del estimado = f(calidad_staff_médico)       │
│  │   ├── Médico malo: ±40% error en estimación             │
│  │   ├── Médico normal: ±20%                               │
│  │   └── Médico top: ±5%                                   │
│  └── El jugador puede volver antes con riesgo               │
│      (el jugador puede solicitar "forzar vuelta")           │
│                                                              │
│  DURANTE LA LESIÓN:                                          │
│  ├── Jugador no disponible para partidos                    │
│  ├── No entrena con el grupo                                │
│  ├── Moral baja gradualmente                                │
│  ├── Forma física baja al volver                            │
│  └── Noticias: "X se lesiona y será baja N semanas"        │
│                                                              │
│  ARCHIVO: core/staff/medical_system.gd                       │
│                                                              │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│              SISTEMA DE MORAL Y VESTUARIO                    │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  MORAL INDIVIDUAL (0-100 por jugador):                       │
│                                                              │
│  SUBE CON:                                                   │
│  ├── +5  Victoria del equipo                                │
│  ├── +8  Victoria goleando (3+ goles diferencia)            │
│  ├── +10 Jugador marca gol                                  │
│  ├── +5  Jugador da asistencia                              │
│  ├── +8  Buena puntuación en partido (>7.5)                 │
│  ├── +15 Titular habitual (juega >70% partidos)             │
│  ├── +10 Renovación de contrato con mejora salarial         │
│  ├── +5  Victoria en derby/partido importante               │
│  ├── +10 Convocado por selección                            │
│  ├── +8  Equipo líder de la liga                            │
│  ├── +3  Buen entrenamiento (semana productiva)             │
│  └── +5  Compañero estrella fichado (ilusión)               │
│                                                              │
│  BAJA CON:                                                   │
│  ├── -5  Derrota del equipo                                 │
│  ├── -8  Derrota humillante (3+ goles)                      │
│  ├── -15 Suplente habitual (juega <20% partidos)            │
│  ├── -10 No convocado (ni en el banquillo)                  │
│  ├── -8  Solicitud de salida rechazada                      │
│  ├── -5  Oferta de renovación peor a la esperada            │
│  ├── -10 Compañero cercano vendido                          │
│  ├── -12 Lesión larga                                       │
│  ├── -8  Mala racha del equipo (3+ derrotas seguidas)       │
│  ├── -5  Ambiente malo en vestuario                         │
│  ├── -3  Sanción por tarjeta roja                           │
│  └── -20 Jugador quiere irse y no le dejan                  │
│                                                              │
│  EFECTO DE LA MORAL EN EL RENDIMIENTO:                       │
│  ┌──────────┬───────────────────────────────────────┐        │
│  │ Moral    │ Efecto                                │        │
│  ├──────────┼───────────────────────────────────────┤        │
│  │ 90-100   │ En racha: +8% en todos los atributos  │        │
│  │          │ Se le ve feliz, celebra, anima         │        │
│  ├──────────┼───────────────────────────────────────┤        │
│  │ 70-89    │ Contento: +3% atributos               │        │
│  │          │ Comportamiento normal                  │        │
│  ├──────────┼───────────────────────────────────────┤        │
│  │ 50-69    │ Normal: sin modificadores              │        │
│  ├──────────┼───────────────────────────────────────┤        │
│  │ 30-49    │ Descontento: -5% atributos            │        │
│  │          │ Puede pedir hablar contigo             │        │
│  │          │ Puede pedir salir del club             │        │
│  ├──────────┼───────────────────────────────────────┤        │
│  │ 10-29    │ Muy infeliz: -12% atributos           │        │
│  │          │ Solicita traspaso públicamente         │        │
│  │          │ Contagia mal ambiente a compañeros     │        │
│  │          │ Puede negarse a entrenar               │        │
│  ├──────────┼───────────────────────────────────────┤        │
│  │ 0-9      │ Rebelde: -20% atributos               │        │
│  │          │ Se niega a jugar                       │        │
│  │          │ La directiva te pide que lo vendas     │        │
│  │          │ Prensa lo usa contra ti                │        │
│  └──────────┴───────────────────────────────────────┘        │
│                                                              │
│  MORAL DE EQUIPO (promedio ponderado):                       │
│  ├── Promedio moral de todos los jugadores                  │
│  ├── Peso mayor para titulares y capitán                    │
│  ├── Afecta: cohesión táctica, pressing colectivo,          │
│  │   probabilidad de remontar                               │
│  ├── >80: "Vestuario unido" → bonus colectivo              │
│  ├── <40: "Crisis de vestuario" → penalización             │
│  │   → Directiva te advierte                                │
│  └── Capitán con alta moral mitiga bajadas de equipo        │
│                                                              │
│  PERSONALIDAD Y SU EFECTO:                                   │
│  ├── Profesionalismo alto:                                  │
│  │   → Moral baja menos con derrotas                        │
│  │   → Entrena siempre al máximo                            │
│  │   → Menos probable que se rebele                         │
│  │                                                           │
│  ├── Ambición alta:                                          │
│  │   → Quiere jugar en equipo grande                        │
│  │   → Moral baja si equipo no compite                      │
│  │   → Pide salir más fácilmente                            │
│  │                                                           │
│  ├── Lealtad alta:                                           │
│  │   → Moral sube más por victorias del club                │
│  │   → Menos probable que pida salir                        │
│  │   → Acepta salario menor por quedarse                    │
│  │                                                           │
│  └── Temperamento alto:                                      │
│      → Más tarjetas amarillas/rojas                         │
│      → Más probable que proteste al árbitro                 │
│      → Más probable que se pelee con compañero              │
│      → Puede ser "chispa" del equipo o problema             │
│                                                              │
│  INTERACCIONES DE VESTUARIO:                                 │
│  ├── Jugador pide reunión privada                           │
│  │   → Opciones de respuesta (afectan moral):              │
│  │     ├── "Tendrás más minutos" (compromiso)              │
│  │     ├── "Eres importante para el equipo" (motivar)      │
│  │     ├── "Debes mejorar para jugar" (honesto)            │
│  │     └── "Las decisiones las tomo yo" (autoritario)      │
│  │                                                           │
│  ├── Grupo de jugadores descontentos                        │
│  │   → Si 3+ jugadores con moral <30                       │
│  │   → "Rebelión de vestuario"                             │
│  │   → Debes resolver: vender, ceder, dar minutos          │
│  │                                                           │
│  └── Charla motivacional (pre-partido):                     │
│      ├── "Somos mejores que ellos" → +moral si verdad,     │
│      │   -moral si pierden                                  │
│      ├── "No hay presión" → estabiliza moral                │
│      ├── "Demos todo" → +moral para profesionales          │
│      └── Efecto depende del segundo entrenador              │
│         (atributo motivación)                               │
│                                                              │
│  ARCHIVO: core/match/morale_system.gd (nuevo sistema)       │
│  (Podría ir en entities/player.gd parcialmente)              │
│                                                              │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│              PIPELINE DE DATOS (Python)                       │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  FLUJO COMPLETO:                                             │
│                                                              │
│  ┌──────────────┐     ┌──────────────┐     ┌─────────────┐  │
│  │ TRANSFERMARKT│     │  SOFIFA.COM  │     │ FBREF.COM   │  │
│  │              │     │              │     │             │  │
│  │ • Plantillas │     │ • Atributos  │     │ • Estadísti │  │
│  │ • Valores    │     │   detallados │     │   cas reales│  │
│  │ • Edad, pos. │     │ • Potencial  │     │ • Goles,    │  │
│  │ • Historial  │     │ • Pie hábil  │     │   asistenci │  │
│  │ • Contratos  │     │ • Altura,    │     │   as        │  │
│  │              │     │   peso       │     │             │  │
│  └──────┬───────┘     └──────┬───────┘     └──────┬──────┘  │
│         │                    │                     │         │
│         ▼                    ▼                     ▼         │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              MERGE & MATCHING                           │ │
│  │                                                         │ │
│  │  1. Scrapear Transfermarkt → jugadores base             │ │
│  │  2. Scrapear SoFIFA → atributos detallados              │ │
│  │  3. Scrapear FBref → estadísticas temporada             │ │
│  │  4. Matching por nombre + equipo + edad                 │ │
│  │     (fuzzy matching para nombres con acentos)           │ │
│  │  5. Merge: combinar en un solo registro                 │ │
│  │  6. Para jugadores sin datos SoFIFA:                    │ │
│  │     → generar atributos basados en valor,               │ │
│  │       posición, edad y liga (algoritmo propio)          │ │
│  │                                                         │ │
│  └────────────────────────┬────────────────────────────────┘ │
│                           │                                  │
│                           ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              GENERACIÓN DE DATOS FALTANTES              │ │
│  │                                                         │ │
│  │  Para jugadores de ligas menores sin datos en SoFIFA:   │ │
│  │  ├── Estimar media basándose en:                        │ │
│  │  │   ├── Valor de mercado (Transfermarkt)               │ │
│  │  │   ├── Edad                                           │ │
│  │  │   ├── Nivel de la liga (tier 1-5)                    │ │
│  │  │   └── Posición                                       │ │
│  │  ├── Distribuir atributos según perfil posición         │ │
│  │  ├── Agregar varianza aleatoria (±5)                    │ │
│  │  └── Generar potencial:                                 │ │
│  │      ├── Edad < 21: potencial = media + rand(5,25)      │ │
│  │      ├── Edad 21-27: potencial = media + rand(0,10)     │ │
│  │      └── Edad > 27: potencial = media                   │ │
│  │                                                         │ │
│  │  Para staff, sponsors, nombres:                         │ │
│  │  ├── Bases de datos de nombres por país (web scraping)  │ │
│  │  ├── Staff generado proceduralmente                     │ │
│  │  └── Sponsors de bases de datos de marcas               │ │
│  │                                                         │ │
│  └────────────────────────┬────────────────────────────────┘ │
│                           │                                  │
│                           ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              VALIDACIÓN                                 │ │
│  │                                                         │ │
│  │  ├── ¿Cada equipo tiene 18-35 jugadores?               │ │
│  │  ├── ¿Cada equipo tiene al menos 2 porteros?           │ │
│  │  ├── ¿Todos los atributos están en rango 1-99?         │ │
│  │  ├── ¿Todas las edades son razonables (15-45)?         │ │
│  │  ├── ¿Los valores de mercado son coherentes?           │ │
│  │  ├── ¿Hay 11+ jugadores por posición genérica?        │ │
│  │  ├── ¿Los contratos tienen fechas válidas?             │ │
│  │  ├── ¿Los salarios son proporcionales al valor?        │ │
│  │  └── ¿Los IDs son únicos?                              │ │
│  │                                                         │ │
│  └────────────────────────┬────────────────────────────────┘ │
│                           │                                  │
│                           ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              EXPORTACIÓN A JSON                         │ │
│  │                                                         │ │
│  │  Genera la estructura completa de /data/ que            │ │
│  │  Godot lee al iniciar el juego                          │ │
│  │                                                         │ │
│  │  Comando final:                                         │ │
│  │  $ python tools/generators/generate_all_data.py         │ │
│  │                                                         │ │
│  │  Output:                                                │ │
│  │  ✅ 220 países generados                                │ │
│  │  ✅ 87 ligas generadas                                  │ │
│  │  ✅ 4,832 equipos generados                             │ │
│  │  ✅ 98,445 jugadores generados                          │ │
│  │  ✅ 18,230 staff generados                              │ │
│  │  ✅ 847 sponsors generados                              │ │
│  │  ✅ Validación: 0 errores, 23 warnings                  │ │
│  │  ✅ Tamaño total: ~180MB JSON                           │ │
│  │                                                         │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  SCRIPTS Y ORDEN DE EJECUCIÓN:                               │
│  ┌──────────────────────────────────────────────────┐        │
│  │                                                  │        │
│  │  # Paso 1: Scrapear datos crudos                │        │
│  │  python scrapers/scraper_transfermarkt.py        │        │
│  │  python scrapers/scraper_sofifa.py               │        │
│  │  python scrapers/scraper_fbref.py                │        │
│  │                                                  │        │
│  │  # Paso 2: Combinar y limpiar                   │        │
│  │  python converters/merge_data_sources.py         │        │
│  │  python generators/fill_missing_attributes.py    │        │
│  │                                                  │        │
│  │  # Paso 3: Generar datos adicionales             │        │
│  │  python generators/generate_staff.py             │        │
│  │  python generators/generate_sponsors.py          │        │
│  │  python generators/generate_names_db.py          │        │
│  │                                                  │        │
│  │  # Paso 4: Validar y exportar                   │        │
│  │  python generators/validate_data.py              │        │
│  │  python converters/export_to_godot_json.py       │        │
│  │                                                  │        │
│  │  # O todo junto:                                │        │
│  │  python generators/generate_all_data.py          │        │
│  │                                                  │        │
│  └──────────────────────────────────────────────────┘        │
│                                                              │
│  NOTA: Los scrapers se ejecutan UNA VEZ para generar         │
│  los datos iniciales. Después el juego funciona              │
│  100% offline con los JSONs generados.                       │
│                                                              │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│           CONFIGURACIÓN Y PARÁMETROS DE BALANCE              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Todos los valores de balance en archivos JSON editables.    │
│  Esto permite ajustar el juego sin tocar código.             │
│                                                              │
│  data/config/economy_config.json:                            │
│  {                                                           │
│    "salario_minimo_semanal": 500,                            │
│    "salario_maximo_semanal": 2000000,                        │
│    "inflacion_anual": 0.05,                                  │
│    "comision_agente_min": 0.03,                              │
│    "comision_agente_max": 0.10,                              │
│    "impuestos_sobre_fichaje": 0.0,                           │
│    "coste_despido_staff_meses": 6,                           │
│    "interes_prestamo_bancario": 0.05,                        │
│    "maximo_prestamo_porcentaje_valor_club": 0.30,            │
│    "precio_entrada_minimo": 5,                               │
│    "precio_entrada_maximo": 500,                             │
│    "porcentaje_asistencia_base": 0.75,                       │
│    "bonus_asistencia_rival_grande": 0.15,                    │
│    "bonus_asistencia_buen_momento": 0.10,                    │
│    "penalizacion_asistencia_mal_momento": -0.20,             │
│    "merchandising_base_por_socio": 50,                       │
│    "bonus_merchandising_estrella": 0.30,                     │
│    "tv_minimo_liga_top": 30000000,                           │
│    "tv_maximo_liga_top": 200000000,                          │
│    "reparto_tv": {                                           │
│      "equitativo": 0.50,                                     │
│      "por_posicion": 0.25,                                   │
│      "por_audiencia": 0.25                                   │
│    },                                                        │
│    "premios_liga": {                                         │
│      "campeon": 40000000,                                    │
│      "subcampeon": 25000000,                                 │
│      "tercero": 15000000                                     │
│    },                                                        │
│    "premios_champions": {                                    │
│      "fase_grupos": 15000000,                                │
│      "octavos": 10000000,                                    │
│      "cuartos": 12000000,                                    │
│      "semifinal": 15000000,                                  │
│      "final": 20000000,                                      │
│      "campeon": 25000000                                     │
│    }                                                         │
│  }                                                           │
│                                                              │
│  data/config/match_engine_config.json:                       │
│  {                                                           │
│    "duracion_partido_real_segundos": 360,                    │
│    "minutos_simulados": 90,                                  │
│    "velocidad_base_jugador": 6.5,                            │
│    "velocidad_sprint_multiplicador": 1.5,                    │
│    "stamina_consumo_sprint_por_segundo": 0.8,                │
│    "stamina_consumo_normal_por_segundo": 0.15,               │
│    "stamina_recuperacion_parado_por_segundo": 0.3,           │
│    "radio_control_balon": 1.5,                               │
│    "radio_tackle": 2.0,                                      │
│    "radio_pase_automatico": 3.0,                             │
│    "probabilidad_falta_por_tackle": 0.25,                    │
│    "probabilidad_amarilla_por_falta": 0.30,                  │
│    "probabilidad_roja_por_falta_dura": 0.08,                 │
│    "probabilidad_lesion_por_falta": 0.05,                    │
│    "probabilidad_lesion_por_minuto": 0.0003,                 │
│    "peso_atributos_en_disparo": {                            │
│      "disparo": 0.35,                                        │
│      "potencia_disparo": 0.25,                               │
│      "compostura": 0.20,                                     │
│      "posicionamiento_of": 0.10,                             │
│      "factor_aleatorio": 0.10                                │
│    },                                                        │
│    "peso_atributos_en_pase": {                               │
│      "pase_corto": 0.35,                                     │
│      "vision": 0.30,                                         │
│      "compostura": 0.20,                                     │
│      "factor_aleatorio": 0.15                                │
│    },                                                        │
│    "peso_atributos_en_regate": {                             │
│      "regate": 0.40,                                         │
│      "aceleracion": 0.20,                                    │
│      "compostura": 0.20,                                     │
│      "factor_aleatorio": 0.20                                │
│    },                                                        │
│    "peso_atributos_en_defensa": {                            │
│      "defensa": 0.35,                                        │
│      "entrada": 0.25,                                        │
│      "fisico": 0.20,                                         │
│      "posicionamiento_def": 0.10,                            │
│      "factor_aleatorio": 0.10                                │
│    },                                                        │
│    "modificador_local": 1.05,                                │
│    "modificador_cansancio_impacto": 0.003                    │
│  }                                                           │
│                                                              │
│  data/config/development_curves.json (continuación):         │
│  {                                                           │
│    "crecimiento_por_edad": {                                 │
│      "16": 1.8, "17": 1.7, "18": 1.5,                       │
│      "19": 1.3, "20": 1.1, "21": 0.9,                       │
│      "22": 0.7, "23": 0.5, "24": 0.3,                       │
│      "25": 0.2, "26": 0.1, "27": 0.05,                      │
│      "28": 0.0, "29": 0.0, "30": 0.0,                       │
│      "31": -0.1, "32": -0.3, "33": -0.5,                    │
│      "34": -0.8, "35": -1.2, "36": -1.8,                    │
│      "37": -2.5, "38": -3.0, "39": -4.0,                    │
│      "40": -5.0                                              │
│    },                                                        │
│    "atributos_que_suben_con_edad": [                         │
│      "vision", "compostura", "posicionamiento_of",           │
│      "posicionamiento_def", "pase_largo",                    │
│      "tiro_libre", "penaltis", "liderazgo"                   │
│    ],                                                        │
│    "atributos_que_bajan_primero": [                          │
│      "velocidad", "aceleracion", "resistencia",              │
│      "agilidad"                                              │
│    ],                                                        │
│    "atributos_que_bajan_ultimo": [                           │
│      "pase_corto", "vision", "compostura",                   │
│      "disparo", "control"                                    │
│    ],                                                        │
│    "atributos_estables": [                                   │
│      "cabeceo", "efecto", "tiro_libre",                      │
│      "pase_largo"                                            │
│    ],                                                        │
│    "factor_profesionalismo": {                               │
│      "descripcion": "Jugadores profesionales crecen         │
│       mas rapido y declinan mas lento",                      │
│      "profesionalismo_90_100": {                             │
│        "bonus_crecimiento": 0.3,                             │
│        "reduccion_declive": 0.4                              │
│      },                                                      │
│      "profesionalismo_70_89": {                              │
│        "bonus_crecimiento": 0.1,                             │
│        "reduccion_declive": 0.2                              │
│      },                                                      │
│      "profesionalismo_50_69": {                              │
│        "bonus_crecimiento": 0.0,                             │
│        "reduccion_declive": 0.0                              │
│      },                                                      │
│      "profesionalismo_0_49": {                               │
│        "bonus_crecimiento": -0.2,                            │
│        "reduccion_declive": -0.2                             │
│      }                                                       │
│    },                                                        │
│    "factor_minutos_jugados": {                               │
│      "descripcion": "Jugar partidos acelera desarrollo",     │
│      "titular_regular_75_plus": 1.3,                         │
│      "rotacion_40_74": 1.0,                                  │
│      "suplente_10_39": 0.6,                                  │
│      "no_juega_0_9": 0.2                                     │
│    },                                                        │
│    "factor_nivel_liga": {                                    │
│      "descripcion": "Ligas mejores desarrollan mas",         │
│      "tier_1_top5_europeas": 1.2,                            │
│      "tier_2_europeas_medias": 1.0,                          │
│      "tier_3_sudamericanas_top": 0.9,                        │
│      "tier_4_ligas_menores": 0.7,                            │
│      "tier_5_divisiones_bajas": 0.5                          │
│    },                                                        │
│    "factor_calidad_entrenamiento": {                         │
│      "descripcion": "Staff + instalaciones",                 │
│      "elite_nivel_9_10": 1.4,                                │
│      "bueno_nivel_7_8": 1.2,                                 │
│      "normal_nivel_5_6": 1.0,                                │
│      "bajo_nivel_3_4": 0.8,                                  │
│      "malo_nivel_1_2": 0.5                                   │
│    },                                                        │
│    "probabilidad_envejecer_bien": {                          │
│      "descripcion": "Algunos jugadores declinan muy          │
│       lento (ej: Modric, Ibrahimovic, Thiago Silva)",        │
│      "probabilidad_base": 0.08,                              │
│      "bonus_profesionalismo_alto": 0.07,                     │
│      "bonus_fisico_alto": 0.05,                              │
│      "efecto": "declive reducido en 50%"                     │
│    },                                                        │
│    "retiro": {                                               │
│      "edad_minima_retiro": 33,                               │
│      "edad_maxima_obligatoria": 42,                          │
│      "probabilidad_retiro_por_edad": {                       │
│        "33": 0.02, "34": 0.05, "35": 0.10,                  │
│        "36": 0.20, "37": 0.35, "38": 0.50,                  │
│        "39": 0.70, "40": 0.85, "41": 0.95,                  │
│        "42": 1.00                                            │
│      },                                                      │
│      "factores_retiro_anticipado": [                         │
│        "lesion_grave_repetida",                              │
│        "sin_equipo_6_meses",                                 │
│        "moral_muy_baja_prolongada"                           │
│      ]                                                       │
│    }                                                         │
│  }                                                           │
│                                                              │
│  data/config/stadium_upgrades.json:                          │
│  {                                                           │
│    "gradas": {                                               │
│      "ampliacion_pequeña": {                                 │
│        "capacidad_extra": 3000,                              │
│        "coste_base": 5000000,                                │
│        "semanas": 12,                                        │
│        "reduccion_aforo_durante_obra": 0.10                  │
│      },                                                      │
│      "ampliacion_media": {                                   │
│        "capacidad_extra": 8000,                              │
│        "coste_base": 15000000,                               │
│        "semanas": 24,                                        │
│        "reduccion_aforo_durante_obra": 0.20                  │
│      },                                                      │
│      "ampliacion_grande": {                                  │
│        "capacidad_extra": 15000,                             │
│        "coste_base": 35000000,                               │
│        "semanas": 40,                                        │
│        "reduccion_aforo_durante_obra": 0.30                  │
│      }                                                       │
│    },                                                        │
│    "vip": {                                                  │
│      "niveles": [                                            │
│        {"nivel":1, "palcos":20,  "coste":3000000,            │
│         "semanas":8,  "ingreso_palco_partido":5000},         │
│        {"nivel":2, "palcos":50,  "coste":8000000,            │
│         "semanas":14, "ingreso_palco_partido":6000},         │
│        {"nivel":3, "palcos":100, "coste":18000000,           │
│         "semanas":22, "ingreso_palco_partido":8000},         │
│        {"nivel":4, "palcos":200, "coste":40000000,           │
│         "semanas":30, "ingreso_palco_partido":10000},        │
│        {"nivel":5, "palcos":350, "coste":80000000,           │
│         "semanas":40, "ingreso_palco_partido":15000}         │
│      ]                                                       │
│    },                                                        │
│    "tienda": {                                               │
│      "niveles": [                                            │
│        {"nivel":1, "coste":400000,   "semanas":4,            │
│         "bonus_merchandising": 1.2},                         │
│        {"nivel":2, "coste":1500000,  "semanas":6,            │
│         "bonus_merchandising": 1.5},                         │
│        {"nivel":3, "coste":4000000,  "semanas":10,           │
│         "bonus_merchandising": 2.0,                          │
│         "habilita_tienda_online": true},                     │
│        {"nivel":4, "coste":10000000, "semanas":14,           │
│         "bonus_merchandising": 2.8},                         │
│        {"nivel":5, "coste":25000000, "semanas":20,           │
│         "bonus_merchandising": 4.0,                          │
│         "descripcion": "Megastore"}                          │
│      ]                                                       │
│    },                                                        │
│    "museo": {                                                │
│      "niveles": [                                            │
│        {"nivel":1, "coste":2000000,  "semanas":8,            │
│         "visitantes_semana_base": 500,                       │
│         "precio_entrada": 15},                               │
│        {"nivel":2, "coste":6000000,  "semanas":14,           │
│         "visitantes_semana_base": 1500,                      │
│         "precio_entrada": 20},                               │
│        {"nivel":3, "coste":15000000, "semanas":24,           │
│         "visitantes_semana_base": 5000,                      │
│         "precio_entrada": 30,                                │
│         "descripcion": "Tour del estadio incluido"}          │
│      ]                                                       │
│    },                                                        │
│    "iluminacion": {                                          │
│      "niveles": [                                            │
│        {"nivel":1, "coste":500000,   "semanas":4,            │
│         "cumple_requisito": "liga_nacional"},                 │
│        {"nivel":2, "coste":2000000,  "semanas":6,            │
│         "cumple_requisito": "copa_nacional"},                │
│        {"nivel":3, "coste":5000000,  "semanas":10,           │
│         "cumple_requisito": "competicion_europea",           │
│         "bonus_tv": 1.1},                                    │
│        {"nivel":4, "coste":12000000, "semanas":14,           │
│         "cumple_requisito": "champions_league",              │
│         "bonus_tv": 1.2},                                    │
│        {"nivel":5, "coste":25000000, "semanas":20,           │
│         "cumple_requisito": "final_champions",               │
│         "bonus_tv": 1.35,                                    │
│         "descripcion": "Iluminacion LED espectaculo"}        │
│      ]                                                       │
│    },                                                        │
│    "pantallas": {                                            │
│      "niveles": [                                            │
│        {"nivel":1, "coste":800000,   "semanas":4,            │
│         "descripcion": "Marcador electronico"},              │
│        {"nivel":2, "coste":4000000,  "semanas":8,            │
│         "descripcion": "Pantalla gigante",                   │
│         "bonus_sponsor_vallas": 1.2},                        │
│        {"nivel":3, "coste":12000000, "semanas":14,           │
│         "descripcion": "Anillo LED 360 grados",             │
│         "bonus_sponsor_vallas": 1.8,                         │
│         "bonus_experiencia_publico": 1.3}                    │
│      ]                                                       │
│    },                                                        │
│    "cesped": {                                               │
│      "tipos": [                                              │
│        {"tipo": "natural_basico", "coste":300000,            │
│         "semanas":3, "calidad": 60,                          │
│         "mantenimiento_semanal": 5000},                      │
│        {"tipo": "natural_premium", "coste":1000000,          │
│         "semanas":4, "calidad": 80,                          │
│         "mantenimiento_semanal": 15000},                     │
│        {"tipo": "hibrido",  "coste":3000000,                 │
│         "semanas":6, "calidad": 95,                          │
│         "mantenimiento_semanal": 25000,                      │
│         "reduce_lesiones": 0.15},                            │
│        {"tipo": "sintetico", "coste":2000000,                │
│         "semanas":5, "calidad": 70,                          │
│         "mantenimiento_semanal": 3000,                       │
│         "nota": "No permitido en algunas ligas top"}         │
│      ]                                                       │
│    },                                                        │
│    "restaurante": {                                          │
│      "niveles": [                                            │
│        {"nivel":1, "coste":1000000,  "semanas":6,            │
│         "ingreso_partido": 15000,                            │
│         "ingreso_semanal_eventos": 5000},                    │
│        {"nivel":2, "coste":3000000,  "semanas":10,           │
│         "ingreso_partido": 40000,                            │
│         "ingreso_semanal_eventos": 15000},                   │
│        {"nivel":3, "coste":8000000,  "semanas":16,           │
│         "ingreso_partido": 100000,                           │
│         "ingreso_semanal_eventos": 40000,                    │
│         "descripcion": "Restaurante gourmet con vistas"}     │
│      ]                                                       │
│    },                                                        │
│    "parking": {                                              │
│      "niveles": [                                            │
│        {"nivel":1, "plazas":500,  "coste":1500000,           │
│         "semanas":8,  "precio_plaza": 10},                   │
│        {"nivel":2, "plazas":1500, "coste":4000000,           │
│         "semanas":14, "precio_plaza": 12},                   │
│        {"nivel":3, "plazas":3000, "coste":10000000,          │
│         "semanas":22, "precio_plaza": 15,                    │
│         "bonus_satisfaccion": 1.1}                           │
│      ]                                                       │
│    },                                                        │
│    "sala_prensa": {                                          │
│      "niveles": [                                            │
│        {"nivel":1, "coste":300000,   "semanas":3,            │
│         "bonus_reputacion": 1.05},                           │
│        {"nivel":2, "coste":1200000,  "semanas":6,            │
│         "bonus_reputacion": 1.10},                           │
│        {"nivel":3, "coste":3500000,  "semanas":10,           │
│         "bonus_reputacion": 1.20,                            │
│         "descripcion": "Sala multimedia con streaming"}      │
│      ]                                                       │
│    },                                                        │
│    "estadio_nuevo": {                                        │
│      "opciones": [                                           │
│        {"capacidad":15000,  "coste":80000000,                │
│         "semanas_construccion": 78,                           │
│         "descripcion": "Estadio pequeño moderno"},           │
│        {"capacidad":30000,  "coste":200000000,               │
│         "semanas_construccion": 104,                          │
│         "descripcion": "Estadio mediano"},                   │
│        {"capacidad":50000,  "coste":450000000,               │
│         "semanas_construccion": 130,                          │
│         "descripcion": "Estadio grande"},                    │
│        {"capacidad":70000,  "coste":700000000,               │
│         "semanas_construccion": 156,                          │
│         "descripcion": "Gran estadio"},                      │
│        {"capacidad":90000,  "coste":1200000000,              │
│         "semanas_construccion": 208,                          │
│         "descripcion": "Mega estadio iconico"}               │
│      ],                                                      │
│      "naming_rights": {                                      │
│        "descripcion": "Sponsor paga parte del coste          │
│         a cambio de poner su nombre al estadio",             │
│        "porcentaje_coste_cubierto": 0.15,                    │
│        "duracion_años": 15,                                  │
│        "ingreso_anual_adicional": "variable segun sponsor"   │
│      },                                                      │
│      "alquiler_estadio_temporal": {                          │
│        "coste_semanal": 200000,                              │
│        "capacidad_reducida": 0.60,                           │
│        "descripcion": "Mientras se construye el nuevo"       │
│      }                                                       │
│    }                                                         │
│  }                                                           │
│                                                              │
│  data/config/facilities_config.json:                         │
│  {                                                           │
│    "campos_entrenamiento": {                                 │
│      "niveles": [                                            │
│        {"nivel":1, "coste":500000,   "semanas":4,            │
│         "campos":1, "calidad":"basico",                      │
│         "bonus_entrenamiento": 1.0},                         │
│        {"nivel":2, "coste":2000000,  "semanas":8,            │
│         "campos":2, "calidad":"bueno",                       │
│         "bonus_entrenamiento": 1.15},                        │
│        {"nivel":3, "coste":5000000,  "semanas":12,           │
│         "campos":3, "calidad":"muy_bueno",                   │
│         "bonus_entrenamiento": 1.30},                        │
│        {"nivel":4, "coste":12000000, "semanas":18,           │
│         "campos":4, "calidad":"excelente",                   │
│         "bonus_entrenamiento": 1.50},                        │
│        {"nivel":5, "coste":25000000, "semanas":26,           │
│         "campos":6, "calidad":"elite_mundial",               │
│         "bonus_entrenamiento": 1.80,                         │
│         "descripcion": "Valdebebas/La Masia nivel"}          │
│      ]                                                       │
│    },                                                        │
│    "gimnasio": {                                             │
│      "niveles": [                                            │
│        {"nivel":1, "coste":300000,   "semanas":3,            │
│         "bonus_fisico": 1.0,                                 │
│         "reduccion_lesiones": 0.0},                          │
│        {"nivel":2, "coste":1200000,  "semanas":6,            │
│         "bonus_fisico": 1.15,                                │
│         "reduccion_lesiones": 0.05},                         │
│        {"nivel":3, "coste":3000000,  "semanas":10,           │
│         "bonus_fisico": 1.30,                                │
│         "reduccion_lesiones": 0.10},                         │
│        {"nivel":4, "coste":7000000,  "semanas":14,           │
│         "bonus_fisico": 1.50,                                │
│         "reduccion_lesiones": 0.18},                         │
│        {"nivel":5, "coste":15000000, "semanas":20,           │
│         "bonus_fisico": 1.80,                                │
│         "reduccion_lesiones": 0.25,                          │
│         "descripcion": "Gimnasio con crioterapia,            │
│          piscinas, altitude training"}                        │
│      ]                                                       │
│    },                                                        │
│    "centro_medico": {                                        │
│      "niveles": [                                            │
│        {"nivel":1, "coste":400000,   "semanas":4,            │
│         "multiplicador_recuperacion": 1.0,                   │
│         "max_doctores": 1},                                  │
│        {"nivel":2, "coste":1500000,  "semanas":8,            │
│         "multiplicador_recuperacion": 1.15,                  │
│         "max_doctores": 2},                                  │
│        {"nivel":3, "coste":4000000,  "semanas":12,           │
│         "multiplicador_recuperacion": 1.30,                  │
│         "max_doctores": 3},                                  │
│        {"nivel":4, "coste":10000000, "semanas":18,           │
│         "multiplicador_recuperacion": 1.50,                  │
│         "max_doctores": 4,                                   │
│         "descripcion": "Crioterapia, camaras hiperbaric"},   │
│        {"nivel":5, "coste":22000000, "semanas":24,           │
│         "multiplicador_recuperacion": 1.80,                  │
│         "max_doctores": 5,                                   │
│         "descripcion": "Hospital propio del club"}           │
│      ]                                                       │
│    },                                                        │
│    "academia_cantera": {                                     │
│      "niveles": [                                            │
│        {"nivel":1, "coste":1000000,  "semanas":8,            │
│         "canteranos_generados": 3,                           │
│         "potencial_max_base": 70,                            │
│         "categorias": ["juvenil_a"]},                        │
│        {"nivel":2, "coste":4000000,  "semanas":14,           │
│         "canteranos_generados": 5,                           │
│         "potencial_max_base": 75,                            │
│         "categorias": ["juvenil_a", "juvenil_b"]},           │
│        {"nivel":3, "coste":10000000, "semanas":22,           │
│         "canteranos_generados": 8,                           │
│         "potencial_max_base": 82,                            │
│         "categorias": ["juvenil_a", "juvenil_b",             │
│                         "cadete"]},                           │
│        {"nivel":4, "coste":25000000, "semanas":32,           │
│         "canteranos_generados": 12,                          │
│         "potencial_max_base": 88,                            │
│         "categorias": ["juvenil_a", "juvenil_b",             │
│                         "cadete", "infantil"]},              │
│        {"nivel":5, "coste":50000000, "semanas":44,           │
│         "canteranos_generados": 15,                          │
│         "potencial_max_base": 95,                            │
│         "categorias": ["juvenil_a", "juvenil_b",             │
│                         "cadete", "infantil",                │
│                         "benjamin"],                         │
│         "prob_joya_generacional": 0.03,                      │
│         "descripcion": "La Masia / La Fabrica nivel"}        │
│      ]                                                       │
│    },                                                        │
│    "sala_video": {                                           │
│      "niveles": [                                            │
│        {"nivel":1, "coste":200000,   "semanas":2,            │
│         "bonus_preparacion_tactica": 1.05},                  │
│        {"nivel":2, "coste":800000,   "semanas":4,            │
│         "bonus_preparacion_tactica": 1.12},                  │
│        {"nivel":3, "coste":2500000,  "semanas":8,            │
│         "bonus_preparacion_tactica": 1.25,                   │
│         "descripcion": "IA de analisis tactico"}             │
│      ]                                                       │
│    },                                                        │
│    "cocina_nutricion": {                                     │
│      "niveles": [                                            │
│        {"nivel":1, "coste":300000,   "semanas":3,            │
│         "bonus_recuperacion": 1.05},                         │
│        {"nivel":2, "coste":1000000,  "semanas":5,            │
│         "bonus_recuperacion": 1.12},                         │
│        {"nivel":3, "coste":3000000,  "semanas":8,            │
│         "bonus_recuperacion": 1.20,                          │
│         "bonus_forma_fisica": 1.10,                          │
│         "descripcion": "Nutricionistas personalizados"}      │
│      ]                                                       │
│    },                                                        │
│    "residencia_juvenil": {                                   │
│      "niveles": [                                            │
│        {"nivel":1, "coste":800000,   "semanas":6,            │
│         "plazas": 10,                                        │
│         "atrae_extranjeros": false},                         │
│        {"nivel":2, "coste":3000000,  "semanas":12,           │
│         "plazas": 25,                                        │
│         "atrae_extranjeros": true,                           │
│         "bonus_moral_canteranos": 1.10},                     │
│        {"nivel":3, "coste":8000000,  "semanas":18,           │
│         "plazas": 50,                                        │
│         "atrae_extranjeros": true,                           │
│         "bonus_moral_canteranos": 1.25,                      │
│         "bonus_atraccion_promesas": 1.30,                    │
│         "descripcion": "Residencia de elite con             │
│          escuela, ocio y formacion integral"}                │
│      ]                                                       │
│    },                                                        │
│    "deterioro": {                                            │
│      "descripcion": "Las instalaciones se deterioran",       │
│      "deterioro_semanal_sin_mantenimiento": 0.5,             │
│      "coste_mantenimiento_porcentaje_valor": 0.001,          │
│      "umbral_deterioro_penalizacion": 50,                    │
│      "efecto_deterioro": "reduce bonus proporcionalmente"    │
│    }                                                         │
│  }                                                           │
│                                                              │
│  data/config/difficulty_presets.json:                         │
│  {                                                           │
│    "facil": {                                                │
│      "nombre": "Aficionado",                                 │
│      "descripcion": "Para disfrutar la gestion              │
│       sin demasiada presion",                                │
│      "modificadores": {                                      │
│        "atributos_tu_equipo": 1.08,                          │
│        "atributos_rival": 0.95,                              │
│        "ia_rival_calidad": 0.7,                              │
│        "ingresos_multiplicador": 1.20,                       │
│        "gastos_multiplicador": 0.90,                         │
│        "paciencia_directiva": 1.50,                          │
│        "probabilidad_lesion": 0.70,                          │
│        "probabilidad_oferta_buena": 1.30,                    │
│        "desarrollo_juveniles": 1.30,                         │
│        "moral_base": 70,                                     │
│        "error_ia_frecuencia": "alto"                         │
│      }                                                       │
│    },                                                        │
│    "normal": {                                               │
│      "nombre": "Profesional",                                │
│      "descripcion": "Experiencia equilibrada",               │
│      "modificadores": {                                      │
│        "atributos_tu_equipo": 1.0,                           │
│        "atributos_rival": 1.0,                               │
│        "ia_rival_calidad": 1.0,                              │
│        "ingresos_multiplicador": 1.0,                        │
│        "gastos_multiplicador": 1.0,                          │
│        "paciencia_directiva": 1.0,                           │
│        "probabilidad_lesion": 1.0,                           │
│        "probabilidad_oferta_buena": 1.0,                     │
│        "desarrollo_juveniles": 1.0,                          │
│        "moral_base": 60,                                     │
│        "error_ia_frecuencia": "normal"                       │
│      }                                                       │
│    },                                                        │
│    "dificil": {                                              │
│      "nombre": "Estrella",                                   │
│      "descripcion": "Para expertos en gestion futbolistica", │
│      "modificadores": {                                      │
│        "atributos_tu_equipo": 0.95,                          │
│        "atributos_rival": 1.05,                              │
│        "ia_rival_calidad": 1.3,                              │
│        "ingresos_multiplicador": 0.90,                       │
│        "gastos_multiplicador": 1.10,                         │
│        "paciencia_directiva": 0.70,                          │
│        "probabilidad_lesion": 1.20,                          │
│        "probabilidad_oferta_buena": 0.80,                    │
│        "desarrollo_juveniles": 0.85,                         │
│        "moral_base": 55,                                     │
│        "error_ia_frecuencia": "bajo"                         │
│      }                                                       │
│    },                                                        │
│    "leyenda": {                                              │
│      "nombre": "Leyenda",                                    │
│      "descripcion": "Solo para masoquistas del futbol",      │
│      "modificadores": {                                      │
│        "atributos_tu_equipo": 0.90,                          │
│        "atributos_rival": 1.10,                              │
│        "ia_rival_calidad": 1.6,                              │
│        "ingresos_multiplicador": 0.80,                       │
│        "gastos_multiplicador": 1.20,                         │
│        "paciencia_directiva": 0.50,                          │
│        "probabilidad_lesion": 1.40,                          │
│        "probabilidad_oferta_buena": 0.60,                    │
│        "desarrollo_juveniles": 0.70,                         │
│        "moral_base": 50,                                     │
│        "error_ia_frecuencia": "muy_bajo"                     │
│      }                                                       │
│    }                                                         │
│  }                                                           │
│                                                              │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│           SISTEMA DE SEÑALES / EVENT BUS                     │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Los sistemas se comunican mediante SEÑALES de Godot.        │
│  El GameManager actúa como Event Bus central.                │
│                                                              │
│  SEÑALES GLOBALES (definidas en game_manager.gd):            │
│                                                              │
│  # ═══ TIEMPO ═══                                            │
│  signal dia_avanzado(fecha: Dictionary)                      │
│  signal semana_avanzada(num_semana: int)                     │
│  signal mes_avanzado(mes: int, año: int)                     │
│  signal temporada_iniciada(año: int)                         │
│  signal temporada_finalizada(año: int)                       │
│  signal pretemporada_iniciada()                              │
│                                                              │
│  # ═══ PARTIDOS ═══                                          │
│  signal partido_programado(datos_partido: Dictionary)        │
│  signal partido_iniciado(local: String, visit: String)       │
│  signal gol_marcado(equipo: String, jugador: String,         │
│                     minuto: int, asistente: String)          │
│  signal partido_finalizado(resultado: MatchResult)           │
│  signal tarjeta_mostrada(jugador: String, tipo: String,      │
│                           minuto: int)                       │
│  signal lesion_en_partido(jugador: String, tipo: String)     │
│  signal sustitucion(sale: String, entra: String, min: int)   │
│                                                              │
│  # ═══ LIGA ═══                                              │
│  signal jornada_completada(liga_id: int, jornada: int)       │
│  signal clasificacion_actualizada(liga_id: int)              │
│  signal campeon_coronado(liga_id: int, equipo: String)       │
│  signal equipo_descendido(equipo: String, liga_id: int)      │
│  signal equipo_ascendido(equipo: String, liga_id: int)       │
│  signal plaza_europea_asegurada(equipo: String, comp: String)│
│                                                              │
│  # ═══ FICHAJES ═══                                          │
│  signal oferta_recibida(oferta: TransferOffer)               │
│  signal oferta_enviada(oferta: TransferOffer)                │
│  signal oferta_aceptada(oferta: TransferOffer)               │
│  signal oferta_rechazada(oferta: TransferOffer)              │
│  signal fichaje_completado(jugador: String,                  │
│                             de: String, a: String,           │
│                             coste: int)                      │
│  signal jugador_vendido(jugador: String, coste: int)         │
│  signal cesion_realizada(jugador: String, destino: String)   │
│  signal mercado_abierto(tipo: String)                        │
│  signal mercado_cerrado(tipo: String)                        │
│  signal deadline_day()                                       │
│                                                              │
│  # ═══ ECONOMÍA ═══                                          │
│  signal dinero_actualizado(nuevo_balance: int)               │
│  signal salarios_pagados(total: int)                         │
│  signal ingreso_recibido(tipo: String, cantidad: int)        │
│  signal gasto_realizado(tipo: String, cantidad: int)         │
│  signal sponsor_firmado(sponsor: SponsorData)                │
│  signal alerta_financiera(tipo: String, mensaje: String)     │
│  signal bancarrota_inminente()                               │
│                                                              │
│  # ═══ ESTADIO ═══                                           │
│  signal obra_iniciada(tipo: String, nivel: int)              │
│  signal obra_completada(tipo: String, nivel: int)            │
│  signal obra_retrasada(tipo: String, semanas_extra: int)     │
│  signal estadio_nuevo_iniciado(capacidad: int)               │
│  signal estadio_nuevo_completado()                           │
│                                                              │
│  # ═══ STAFF ═══                                             │
│  signal staff_contratado(persona: StaffMember)               │
│  signal staff_despedido(persona: StaffMember)                │
│  signal informe_ojeador_listo(informe: Dictionary)           │
│  signal ojeador_descubre_joya(jugador: String)               │
│                                                              │
│  # ═══ JUGADORES ═══                                         │
│  signal jugador_lesionado(jugador: String,                   │
│                            lesion: String, dias: int)        │
│  signal jugador_recuperado(jugador: String)                  │
│  signal jugador_mejorado(jugador: String,                    │
│                           atributo: String,                  │
│                           nuevo_valor: int)                  │
│  signal jugador_empeorado(jugador: String,                   │
│                            atributo: String,                 │
│                            nuevo_valor: int)                 │
│  signal jugador_pide_reunion(jugador: String,                │
│                               motivo: String)                │
│  signal jugador_pide_salir(jugador: String)                  │
│  signal jugador_se_retira(jugador: String)                   │
│  signal jugador_contrato_expira(jugador: String)             │
│  signal juvenil_promovido(jugador: String)                   │
│                                                              │
│  # ═══ CANTERA ═══                                           │
│  signal canteranos_generados(cantidad: int,                  │
│                               mejor: String)                 │
│  signal canterano_destaca(jugador: String, motivo: String)   │
│                                                              │
│  # ═══ DIRECTIVA ═══                                         │
│  signal confianza_actualizada(nueva: int)                    │
│  signal objetivo_cumplido(objetivo: Objective)               │
│  signal objetivo_fallido(objetivo: Objective)                │
│  signal advertencia_directiva(mensaje: String)               │
│  signal despido_inminente(confianza: int)                    │
│  signal despedido()                                          │
│  signal nuevo_presidente(presidente: Dictionary)             │
│  signal presupuesto_ampliado(extra: int)                     │
│  signal presupuesto_recortado(reduccion: int)                │
│                                                              │
│  # ═══ NOTICIAS ═══                                          │
│  signal noticia_generada(noticia: NewsItem)                  │
│  signal noticia_urgente(noticia: NewsItem)                   │
│  signal premio_otorgado(tipo: String, jugador: String)       │
│                                                              │
│  # ═══ SISTEMA ═══                                           │
│  signal partida_guardada(slot: int)                          │
│  signal partida_cargada(slot: int)                           │
│  signal error_sistema(mensaje: String)                       │
│                                                              │
│  EJEMPLO DE CONEXIÓN:                                        │
│                                                              │
│  # En economy_system.gd:                                     │
│  func _ready():                                              │
│      GameManager.partido_finalizado.connect(                 │
│          _on_partido_finalizado)                             │
│      GameManager.fichaje_completado.connect(                 │
│          _on_fichaje_completado)                             │
│                                                              │
│  func _on_partido_finalizado(resultado: MatchResult):        │
│      calcular_ingresos_taquilla(resultado)                   │
│      pagar_bonus_jugadores(resultado)                        │
│                                                              │
│  func _on_fichaje_completado(jugador, de, a, coste):         │
│      if a == GameManager.mi_equipo.nombre:                   │
│          registrar_gasto("fichaje", coste)                   │
│                                                              │
│                                                              │
│  ARCHIVO: autoload/game_manager.gd (señales definidas ahí)  │
│                                                              │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│              GUÍA DE ESTILO VISUAL 3D                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  REFERENCIA VISUAL: PC Fútbol 2001 + estilo "low-poly        │
│  moderno" tipo retro-3D con colores vibrantes.               │
│                                                              │
│  ┌────────────────────────────────────────────────┐          │
│  │                                                │          │
│  │   NO aspiramos a esto:        SÍ a esto:      │          │
│  │   ┌──────────────┐           ┌──────────────┐ │          │
│  │   │ FIFA 25      │           │ PC Fútbol +  │ │          │
│  │   │ (hiperrealismo│          │ Low-poly     │ │          │
│  │   │  60fps, mocap)│           │ moderno      │ │          │
│  │   │              │           │ limpio       │ │          │
│  │   │ ~100K poly   │           │ ~800-1500    │ │          │
│  │   │ por jugador  │           │ poly por     │ │          │
│  │   └──────────────┘           │ jugador      │ │          │
│  │                              └──────────────┘ │          │
│  └────────────────────────────────────────────────┘          │
│                                                              │
│  JUGADOR 3D:                                                 │
│  ├── Cuerpo: ~600-800 polígonos                             │
│  │   ├── Sin dedos individuales (manos = bloque)            │
│  │   ├── Cara simplificada (textura dibuja rasgos)          │
│  │   ├── Piernas separadas para animación                   │
│  │   └── Colores: textura UV con colores del equipo         │
│  │                                                           │
│  ├── Pelo: ~100-300 polígonos extra                         │
│  │   ├── 5-8 variantes (corto, largo, calvo, etc.)          │
│  │   └── Color variable (negro, rubio, castaño, etc.)       │
│  │                                                           │
│  ├── Botas: ~50-100 polígonos                               │
│  │   └── Color según marca (genérica)                       │
│  │                                                           │
│  ├── Equipación: sistema de colores dinámico                │
│  │   ├── Shader que colorea según equipo                    │
│  │   ├── UV map con zonas:                                  │
│  │   │   ├── zona_camiseta_principal → color1               │
│  │   │   ├── zona_camiseta_secundario → color2              │
│  │   │   ├── zona_pantalon → color3                         │
│  │   │   ├── zona_medias → color4                           │
│  │   │   └── zona_numero → shader de texto                  │
│  │   └── Patrones: liso, rayas verticales, rayas            │
│  │       horizontales, mitad-mitad, degradado               │
│  │                                                           │
│  ├── Esqueleto (rig): ~20-25 huesos                         │
│  │   ├── Pelvis (root)                                      │
│  │   ├── Espina (3 segmentos)                               │
│  │   ├── Cuello + Cabeza                                    │
│  │   ├── Hombros + Brazos + Manos (2x)                     │
│  │   ├── Caderas + Piernas + Pies (2x)                     │
│  │   └── NO necesitamos: dedos, cara, twist bones           │
│  │                                                           │
│  └── Total por jugador: ~1000-1500 polígonos                │
│      22 jugadores = ~22K-33K polígonos                      │
│      (muy ligero para cualquier PC)                          │
│                                                              │
│  CAMPO:                                                      │
│  ├── Suelo: un plano grande con textura de césped           │
│  │   ├── Shader que simula hierba (color variation)         │
│  │   ├── Líneas pintadas en textura                         │
│  │   └── NO necesitamos hierba 3D individual                │
│  │                                                           │
│  ├── Porterías: ~200 polígonos cada una                     │
│  │   ├── Postes cilíndricos                                 │
│  │   └── Red: mesh transparente o cloth simulation simple   │
│  │                                                           │
│  └── Banderines de córner: ~20 polígonos                    │
│                                                              │
│  ESTADIO (alrededores):                                      │
│  ├── Gradas: cajas simples con textura de público           │
│  │   ├── Textura animada (sprites moviéndose)               │
│  │   ├── O partículas que simulan personas                  │
│  │   └── Nivel de detalle según tamaño estadio del club     │
│  │                                                           │
│  ├── Techo de gradas: geometría simple                      │
│  │                                                           │
│  ├── Focos: 4 torres con luces                              │
│  │                                                           │
│  ├── Vallas publicitarias: planos con textura animada       │
│  │   └── Sponsor del equipo aparece en las vallas           │
│  │                                                           │
│  └── Total estadio: ~5K-10K polígonos                       │
│                                                              │
│  BALÓN:                                                      │
│  ├── Esfera UV: ~200 polígonos                              │
│  ├── Textura: patrón de pentágonos clásico                  │
│  └── Sombra: sprite circular en el suelo                    │
│                                                              │
│  TOTAL ESCENA 3D:                                            │
│  ├── Jugadores: ~33K polys                                  │
│  ├── Campo: ~2K polys                                       │
│  ├── Estadio: ~10K polys                                    │
│  ├── Balón: ~200 polys                                      │
│  ├── Otros: ~2K polys                                       │
│  └── TOTAL: ~47K polígonos                                  │
│     (Un PC de 2015 mueve esto a 200+ FPS)                   │
│                                                              │
│  CÁMARA:                                                     │
│  ├── TV (default): lateral, ligeramente elevada             │
│  │   ├── Altura: ~15-20 metros                              │
│  │   ├── Ángulo: ~30-40° respecto al suelo                 │
│  │   ├── Sigue balón en eje X                              │
│  │   ├── Zoom dinámico: más lejos si juego abierto         │
│  │   │   más cerca si concentrado en un área               │
│  │   └── Smooth follow (no brusco)                          │
│  │                                                           │
│  ├── Aérea: cenital, ve todo el campo                       │
│  │   └── Útil para ver formación                            │
│  │                                                           │
│  └── Detrás portería: para penaltis y corners               │
│                                                              │
│  DÓNDE OBTENER ASSETS:                                       │
│  ├── Crear propios en Blender (lo ideal)                    │
│  │   ├── Tutoriales "low poly character Blender"            │
│  │   └── Un modelo base → recolorear para todos             │
│  │                                                           │
│  ├── Assets gratuitos:                                       │
│  │   ├── Kenney.nl (excelentes low-poly gratuitos)          │
│  │   ├── OpenGameArt.org                                    │
│  │   ├── Sketchfab (muchos CC0)                             │
│  │   └── Godot Asset Library                                │
│  │                                                           │
│  └── Assets de pago (baratos):                               │
│      ├── itch.io (packs low-poly \$5-20)                     │
│      └── CGTrader / TurboSquid (modelos individuales)       │
│                                                              │
│  HERRAMIENTAS DE ARTE:                                       │
│  ├── Blender 4.x (modelado, rigging, animación) - GRATIS   │
│  ├── MagicaVoxel (para estilo voxel si queremos) - GRATIS  │
│  ├── Aseprite (pixel art para UI) - \$20                     │
│  └── GIMP / Krita (texturas, UI) - GRATIS                   │
│                                                              │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                 RESUMEN DEL PROYECTO                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  TECNOLOGÍA:                                                 │
│  ├── Motor: Godot 4.3                                       │
│  ├── Lenguaje juego: GDScript                               │
│  ├── Lenguaje herramientas: Python 3.11+                    │
│  ├── 3D: Low-poly (~47K polys total en escena)              │
│  ├── Modelado: Blender 4.x                                  │
│  └── Control de versiones: Git + GitHub/GitLab              │
│                                                              │
│  ESCALA DEL JUEGO:                                           │
│  ├── ~100,000 jugadores                                     │
│  ├── ~5,000 equipos                                         │
│  ├── ~200 ligas en ~50 países + COMPETENCIAS INTERNACIONALES FORMATO 2026                               │
│  ├── ~20,000 staff                                          │
│  ├── ~2,000 sponsors                                        │
│  ├── ~130 tipos de mejora de infraestructura                 │
│  ├── 16 sistemas interconectados                            │
│  ├── ~30 pantallas de UI                                    │
│  ├── ~25 animaciones 3D de jugador                          │
│  └── Infinitas temporadas (sin límite)                      │
│                                                              │
│  ARCHIVOS ESTIMADOS:                                         │
│  ├── ~80 scripts GDScript (.gd)                             │
│  ├── ~35 escenas (.tscn)                                    │
│  ├── ~50 componentes UI reutilizables                       │
│  ├── ~10 scripts Python (herramientas)                      │
│  ├── ~5,000+ archivos JSON de datos                         │
│  ├── ~30 modelos 3D (.glb)                                  │
│  ├── ~100 texturas (.png)                                   │
│  ├── ~50 archivos de audio (.ogg)                           │
│  ├── ~6 shaders (.gdshader)                                 │
│  └── ~5 fuentes (.ttf)                                      │
│                                                              │
│  PESO ESTIMADO DEL PROYECTO:                                 │
│  ├── Datos JSON: ~180MB                                     │
│  ├── Assets 3D: ~50MB                                       │
│  ├── Audio: ~80MB                                           │
│  ├── Texturas/UI: ~40MB                                     │
│  ├── Código: ~5MB                                           │
│  └── TOTAL: ~350-400MB                                      │
│                                                              │
│  TIEMPO ESTIMADO (dedicación parcial):                       │
│  ├── Fase 0 (Setup + aprender Godot): 1-2 semanas          │
│  ├── Fase 1 (Núcleo + datos): 3-4 semanas                  │
│  ├── Fase 2 (Match Engine 3D): 4-6 semanas                 │
│  ├── Fase 3 (Economía + fichajes): 3-4 semanas             │
│  ├── Fase 4 (Estadio + staff): 2-3 semanas                 │
│  ├── Fase 5 (Profundidad): 4-6 semanas                     │
│  ├── Fase 6 (Pulido): 3-4 MESES                         │
│  └── TOTAL: ~7-10 meses de desarrollo                       │
│                                                              │
│  REQUISITOS MÍNIMOS PC:                                      │
│  ├── OS: Windows 10 / Linux / macOS                         │
│  ├── CPU: Cualquier x64 (2015+)                             │
│  ├── RAM: 4GB (8GB recomendado por los JSONs)               │
│  ├── GPU: Integrada (Intel HD 4000+)                        │
│  ├── Disco: 500MB                                           │
│  └── El juego correrá en casi cualquier PC                  │
│                                                              │
│  ORDEN DE DESARROLLO RECOMENDADO:                            │
│  ┌──────────────────────────────────────────────┐            │
│  │                                              │            │
│  │  1. 🗄️  Scraper Python + generar JSONs       │            │
│  │  2. 📦 Database system (cargar datos)        │            │
│  │  3. 🖥️  Menú principal + elegir equipo       │            │
│  │  4. 📋 Despacho básico                       │            │
│  │  5. 👥 Pantalla plantilla + jugadores        │            │
│  │  6. ⚽ Motor simulación (texto)              │            │
│  │  7. 🏆 Liga + clasificación + calendario     │            │
│  │  8. 🎮 Match Engine 3D (lo gordo)            │            │
│  │  9. 🔄 Táctica y formación editor            │            │
│  │  10. 💰 Economía completa, con merchandaising, venta camisetas, modificacion de estadio, vallas publicitarias, etc                      │            │
│  │  11. 🤝 Mercado de fichajes COMPLEJO CON VARIABLES QUE INFLUYEN EN LA DECISION DE FICHAR O NO A ALGUIEN                │            │
│  │  12. 💾 Save/Load                            │            │
│  │  13. 🏟️ Estadio + infraestructura + EDIFICIOS QUE CRECEN CON EL CLUB            │            │
│  │  14. 👔 Staff + ojeadores CON ROLES DEFINIDOS                   │            │
│  │  15. 🎓 Cantera SIMULADA, TODAS LAS CATEGORIAS JUVENILES, CON COMPETENCIAS Y TORNEOS DE DIVISIONES JUVENILES. DISTINTOS NIVELES DE EDIFICIO DE JUVENILES, DESBLOQUEA POSIBLE RANGO ALEATORIO PARA CALIDAD DE JUGADOR, EJEMPLO, NIVEL 0 ENTRE 5 Y 20 DE STATS PROMEDIO SOBRE 100, NIVEL 1 DE CENTRO JUVENILES ENTRE 5 Y 28, NIVEL 2 ENTRE 5 Y 35... Y ASI... ADEMAS EL JUGADOR DESPUES PUEDE DESARROLLARSE, PERO LA IDEA ES QUE AUMENTAR EL NIVEL SUBA UN POCO LA PROBABILIDAD DE QUE TOQUE UN JUGADOR BUENO, QUE TENDRÁ VARIABLES QUE BAJAN LA POSIBILIDAD DE QUE TOQUE UNO BUENO, COMO SON LA CATEGORIA EN LA QUE ESTA EL CLUB, ETC                             │            │
│  │  16. 📈 Entrenamiento + desarrollo           │            │
│  │  17. 🏛️ Directiva + objetivos + MUSEO + HISTORIA DEL CLUB               │            │
│  │  18. 📰 Noticias + periódico + RUEDA DE PRENSA QUE AFECTA EN LA IMAGEN DEL PUBLICO               │            │
│  │  19. 🌍 Más ligas + competiciones + PREMIOS            │            │
│  │  20. 🎨 Pulido visual + audio
      21.Generar ligas juveniles, torneos juveniles, selecciones juveniles (todo para simular, pero lo gestionamos nosotros DESDE EL CLUB)
      22.Historial de enfrentamientos, continuar historial de cada club, enfrentamientos entre equipos, rivalidades, historial, palmarés, etc.
                      │            │
│  │                                              │            │
│  └──────────────────────────────────────────────┘            │
│                                                              │
└──────────────────────────────────────────────────────────────┘


