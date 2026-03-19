extends Node

## S07. LEAGUE & COMPETITION SYSTEM
## Gestiona todas las ligas: calendario, clasificación, ascensos/descensos.

# Estado de todas las ligas activas
# { liga_id: { "config": {...}, "equipos": [...], "calendario": [...], "clasificacion": [...], "jornada": int } }
var _ligas: Dictionary = {}
# Historial cara a cara — persiste entre temporadas
# Clave: "minId_maxId"  |  Valor: { id_a, id_b, PJ, W_a, D, W_b, GF_a, GC_a }
var _h2h: Dictionary = {}

signal jornada_completada(liga_id: int, jornada: int, resultados: Array)
signal liga_finalizada(liga_id: int, clasificacion: Array)
signal ascenso(equipo_id: int, de_liga: int, a_liga: int)
signal descenso(equipo_id: int, de_liga: int, a_liga: int)

func _ready() -> void:
	print("[LeagueSystem] Inicializado")

# ─── Inicialización ───────────────────────────────────────────────────────────

func inicializar_todas_las_ligas() -> void:
	_ligas.clear()
	_cargar_h2h_historico()
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

func _cargar_h2h_historico() -> void:
	## Carga h2h.json si existe. No sobrescribe registros ya presentes.
	var ruta := "res://data/initial/h2h.json"
	if not FileAccess.file_exists(ruta):
		return
	var f := FileAccess.open(ruta, FileAccess.READ)
	if f == null:
		return
	var parsed = JSON.parse_string(f.get_as_text())
	f.close()
	if not parsed is Dictionary:
		return
	var cargados := 0
	for key in parsed:
		if not _h2h.has(key):
			_h2h[key] = parsed[key]
			cargados += 1
	print("[LeagueSystem] H2H histórico: %d pares cargados" % cargados)

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
	_registrar_h2h(lid, vid, gl, gv)

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
	# Detectar fin de temporada inmediatamente tras la última jornada
	if liga["jornada_actual"] >= liga["calendario"].size():
		_procesar_fin_temporada(liga_id)
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
					var pid: int = int(g.get("jugador_id", g.get("id", 0)))
					if pid == 0: continue
					var pkey: String = str(pid)
					if not conteo.has(pkey):
						conteo[pkey] = {"id": pid, "nombre": g.get("nombre", "?"), "goles": 0}
					conteo[pkey]["goles"] += 1
	var lista = conteo.values()
	lista.sort_custom(func(a, b): return a.get("goles", 0) > b.get("goles", 0))
	return lista.slice(0, n)

# ─── H2H (cara a cara) — persiste entre temporadas ───────────────────────────

func _h2h_key(a: int, b: int) -> String:
	return "%d_%d" % [mini(a, b), maxi(a, b)]

func _registrar_h2h(local_id: int, visit_id: int, gl: int, gv: int) -> void:
	var key: String = _h2h_key(local_id, visit_id)
	if not _h2h.has(key):
		_h2h[key] = {
			"id_a": mini(local_id, visit_id),
			"id_b": maxi(local_id, visit_id),
			"PJ": 0, "W_a": 0, "D": 0, "W_b": 0, "GF_a": 0, "GC_a": 0,
		}
	var rec: Dictionary = _h2h[key]
	rec["PJ"] += 1
	var id_a: int = rec["id_a"]
	var ga: int = gl if local_id == id_a else gv
	var gb: int = gv if local_id == id_a else gl
	rec["GF_a"] += ga
	rec["GC_a"] += gb
	if   ga > gb: rec["W_a"] += 1
	elif ga < gb: rec["W_b"] += 1
	else:         rec["D"]   += 1

func obtener_h2h(id_a: int, id_b: int) -> Dictionary:
	## Devuelve el historial desde la perspectiva de id_a.
	var key: String = _h2h_key(id_a, id_b)
	if not _h2h.has(key):
		return {"PJ": 0, "W": 0, "D": 0, "L": 0, "GF": 0, "GC": 0}
	var rec: Dictionary = _h2h[key]
	var base_a: int = rec["id_a"]
	if id_a == base_a:
		return {"PJ": rec["PJ"], "W": rec["W_a"], "D": rec["D"], "L": rec["W_b"],
			"GF": rec["GF_a"], "GC": rec["GC_a"]}
	else:
		return {"PJ": rec["PJ"], "W": rec["W_b"], "D": rec["D"], "L": rec["W_a"],
			"GF": rec["GC_a"], "GC": rec["GF_a"]}

# ─── Multi-temporada ──────────────────────────────────────────────────────────

func iniciar_nueva_temporada(liga_id: int, nuevos_equipos: Array = []) -> void:
	## Reinicia la liga manteniendo el historial H2H.
	## nuevos_equipos: si hay ascensos/descensos, pasar la lista actualizada.
	if not _ligas.has(liga_id): return
	var equipos_ids: Array = nuevos_equipos if not nuevos_equipos.is_empty() \
		else _ligas[liga_id]["equipos"]
	_ligas[liga_id] = {
		"config":       _ligas[liga_id]["config"],
		"equipos":      equipos_ids,
		"calendario":   _generar_calendario_rr(equipos_ids),
		"clasificacion": _clasificacion_inicial(equipos_ids),
		"jornada_actual": 0,
		"finalizada":   false,
	}
	print("[LeagueSystem] Nueva temporada iniciada para liga %d" % liga_id)

func obtener_resumen_temporada(liga_id: int) -> Dictionary:
	## Devuelve campeón, descensos y tabla final. Llamar cuando finalizada=true.
	if not _ligas.has(liga_id): return {}
	var liga: Dictionary = _ligas[liga_id]
	var tabla: Array = obtener_clasificacion(liga_id)
	var config: Dictionary = liga["config"]
	var n_des: int = config.get("descensos", 3)
	var n: int = tabla.size()
	var descendidos: Array = tabla.slice(maxi(0, n - n_des), n) if n > 0 else []
	return {
		"tabla":        tabla,
		"campeon":      tabla[0] if n > 0 else {},
		"subcampeon":   tabla[1] if n > 1 else {},
		"descendidos":  descendidos,
		"n_descensos":  n_des,
		"finalizada":   liga.get("finalizada", false),
	}
