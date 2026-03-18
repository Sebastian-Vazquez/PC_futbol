extends Node

## S07. LEAGUE & COMPETITION SYSTEM
## Gestiona todas las ligas: calendario, clasificación, ascensos/descensos.

# Estado de todas las ligas activas
# { liga_id: { "config": {...}, "equipos": [...], "calendario": [...], "clasificacion": [...], "jornada": int } }
var _ligas: Dictionary = {}

signal jornada_completada(liga_id: int, jornada: int, resultados: Array)
signal liga_finalizada(liga_id: int, clasificacion: Array)
signal ascenso(equipo_id: int, de_liga: int, a_liga: int)
signal descenso(equipo_id: int, de_liga: int, a_liga: int)

func _ready() -> void:
	print("[LeagueSystem] Inicializado")

# ─── Inicialización ───────────────────────────────────────────────────────────

func inicializar_todas_las_ligas() -> void:
	_ligas.clear()
	for liga_data in DB.ligas.values():
		var lid: int = liga_data.get("id", 0)
		var equipos_ids = _obtener_equipos_de_liga(lid)
		if equipos_ids.size() < 4:
			continue
		_ligas[lid] = {
			"config": liga_data,
			"equipos": equipos_ids,
			"calendario": _generar_calendario_rr(equipos_ids),
			"clasificacion": _clasificacion_inicial(equipos_ids),
			"jornada_actual": 0,
			"finalizada": false,
		}
	print("[LeagueSystem] %d ligas inicializadas" % _ligas.size())

func _obtener_equipos_de_liga(liga_id: int) -> Array:
	var ids: Array = []
	for eq in DB.equipos.values():
		if eq.get("liga_id") == liga_id:
			ids.append(int(eq.get("id", 0)))
	return ids

# ─── Generación de calendario (Round-Robin) ───────────────────────────────────

func _generar_calendario_rr(equipos: Array) -> Array:
	## Algoritmo de rotación circular. Genera ida y vuelta.
	var eq = equipos.duplicate()
	if eq.size() % 2 != 0:
		eq.append(-1)  # Equipo fantasma para bye
	var n = eq.size()
	var rondas_ida: Array = []

	for ronda in range(n - 1):
		var partidos: Array = []
		for i in range(n / 2):
			var l = eq[i]
			var v = eq[n - 1 - i]
			if l != -1 and v != -1:
				if ronda % 2 == 0:
					partidos.append({"local": l, "visitante": v, "resultado": null})
				else:
					partidos.append({"local": v, "visitante": l, "resultado": null})
		rondas_ida.append(partidos)
		# Rotar: fijar eq[0], rotar el resto
		var ultimo = eq[n - 1]
		for i in range(n - 1, 1, -1):
			eq[i] = eq[i - 1]
		eq[1] = ultimo

	# Vuelta: invertir local/visitante
	var rondas_vuelta: Array = []
	for ronda in rondas_ida:
		var partidos_v: Array = []
		for p in ronda:
			partidos_v.append({"local": p.visitante, "visitante": p.local, "resultado": null})
		rondas_vuelta.append(partidos_v)

	return rondas_ida + rondas_vuelta

# ─── Clasificación ────────────────────────────────────────────────────────────

func _clasificacion_inicial(equipos: Array) -> Array:
	var tabla: Array = []
	for eid in equipos:
		tabla.append({
			"equipo_id": eid,
			"PJ": 0, "PG": 0, "PE": 0, "PP": 0,
			"GF": 0, "GC": 0, "GD": 0, "Pts": 0,
		})
	return tabla

func obtener_clasificacion(liga_id: int) -> Array:
	if not _ligas.has(liga_id):
		return []
	var tabla = _ligas[liga_id]["clasificacion"].duplicate(true)
	tabla.sort_custom(func(a, b): return _comparar_posicion(a, b))
	return tabla

func _comparar_posicion(a: Dictionary, b: Dictionary) -> bool:
	if a.Pts != b.Pts: return a.Pts > b.Pts
	if a.GD  != b.GD:  return a.GD  > b.GD
	if a.GF  != b.GF:  return a.GF  > b.GF
	return false

# ─── Registro de resultados ───────────────────────────────────────────────────

func registrar_resultado(liga_id: int, resultado: Dictionary) -> void:
	if not _ligas.has(liga_id): return
	var liga = _ligas[liga_id]
	var gl: int = resultado.get("goles_local", 0)
	var gv: int = resultado.get("goles_visitante", 0)
	var lid: int = resultado.get("local_id", 0)
	var vid: int = resultado.get("visitante_id", 0)

	_actualizar_fila(liga["clasificacion"], lid, gl, gv)
	_actualizar_fila(liga["clasificacion"], vid, gv, gl)

func _actualizar_fila(tabla: Array, equipo_id: int, gf: int, gc: int) -> void:
	for fila in tabla:
		if fila["equipo_id"] == equipo_id:
			fila["PJ"] += 1
			fila["GF"] += gf
			fila["GC"] += gc
			fila["GD"] = fila["GF"] - fila["GC"]
			if gf > gc:
				fila["PG"] += 1; fila["Pts"] += 3
			elif gf == gc:
				fila["PE"] += 1; fila["Pts"] += 1
			else:
				fila["PP"] += 1
			return

# ─── Simulación de jornadas ───────────────────────────────────────────────────

func simular_jornada(liga_id: int) -> Array:
	## Simula la siguiente jornada pendiente de una liga. Devuelve los resultados.
	if not _ligas.has(liga_id): return []
	var liga = _ligas[liga_id]
	if liga.finalizada: return []

	var jornada_idx: int = liga["jornada_actual"]
	if jornada_idx >= liga["calendario"].size():
		_procesar_fin_temporada(liga_id)
		return []

	var partidos: Array = liga["calendario"][jornada_idx]
	var resultados: Array = []

	for partido in partidos:
		var res = MatchSim.simular(partido.local, partido.visitante)
		if not res.is_empty():
			partido["resultado"] = res
			registrar_resultado(liga_id, res)
			resultados.append(res)

	liga["jornada_actual"] += 1
	jornada_completada.emit(liga_id, jornada_idx + 1, resultados)
	return resultados

func simular_temporada_completa(liga_id: int) -> void:
	## Simula TODAS las jornadas restantes de una liga.
	if not _ligas.has(liga_id): return
	var liga = _ligas[liga_id]
	var total = liga["calendario"].size()
	while liga["jornada_actual"] < total and not liga.finalizada:
		simular_jornada(liga_id)

func simular_todas_las_ligas() -> void:
	## Simula una temporada completa de TODAS las ligas.
	for liga_id in _ligas.keys():
		simular_temporada_completa(liga_id)

# ─── Fin de temporada ─────────────────────────────────────────────────────────

func _procesar_fin_temporada(liga_id: int) -> void:
	var liga = _ligas[liga_id]
	if liga.finalizada: return
	liga.finalizada = true

	var config = liga["config"]
	var tabla  = obtener_clasificacion(liga_id)
	var n      = tabla.size()

	liga_finalizada.emit(liga_id, tabla)

	# Ascensos
	var plazas_ascenso: int = config.get("descensos", 3)  # Las que ascienden = las que bajan de arriba
	# (Se maneja entre ligas, aquí solo emitimos señales)

	# Descensos
	var descensos: int = config.get("descensos", 3)
	for i in range(descensos):
		var idx = n - 1 - i
		if idx >= 0:
			var eid = tabla[idx]["equipo_id"]
			descenso.emit(eid, liga_id, -1)  # -1 = liga inferior (se resuelve en GameManager)

# ─── Consultas ────────────────────────────────────────────────────────────────

func obtener_proxima_jornada(liga_id: int) -> Array:
	if not _ligas.has(liga_id): return []
	var liga = _ligas[liga_id]
	var idx  = liga["jornada_actual"]
	if idx >= liga["calendario"].size(): return []
	return liga["calendario"][idx]

func obtener_num_jornadas(liga_id: int) -> int:
	if not _ligas.has(liga_id): return 0
	return _ligas[liga_id]["calendario"].size()

func jornada_actual(liga_id: int) -> int:
	if not _ligas.has(liga_id): return 0
	return _ligas[liga_id]["jornada_actual"]

func liga_finalizada_estado(liga_id: int) -> bool:
	if not _ligas.has(liga_id): return true
	return _ligas[liga_id].get("finalizada", false)

func obtener_max_goleadores(n: int = 10) -> Array:
	## Devuelve los N máximos goleadores globales.
	var conteo: Dictionary = {}
	for liga_id in _ligas:
		var liga = _ligas[liga_id]
		for jornada in liga["calendario"]:
			for partido in jornada:
				var res = partido.get("resultado")
				if res == null: continue
				for g in res.get("goleadores", []):
					var pid = g.get("id", 0)
					if pid == 0: continue
					conteo[pid] = conteo.get(pid, {"id": pid, "nombre": g.get("nombre","?"), "goles": 0})
					conteo[pid]["goles"] += 1
	var lista = conteo.values()
	lista.sort_custom(func(a, b): return a.goles > b.goles)
	return lista.slice(0, n)
