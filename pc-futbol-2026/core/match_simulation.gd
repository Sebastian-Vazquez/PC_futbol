extends Node

## S06. MATCH SIMULATION ENGINE
## Simula partidos SIN renderizado 3D.
## Usado para partidos de la IA y cuando el jugador elige "simular".

const MINUTOS := 90
const PROB_AMARILLA := 0.007
const PROB_LESION   := 0.002

func simular(local_id: int, visitante_id: int, neutral: bool = false) -> Dictionary:
	var local     = DB.obtener_equipo(local_id)
	var visitante = DB.obtener_equipo(visitante_id)
	if local.is_empty() or visitante.is_empty():
		push_error("[MatchSim] Equipo no encontrado: %d vs %d" % [local_id, visitante_id])
		return {}

	var pl_local     = DB.obtener_plantilla(local_id)
	var pl_visitante = DB.obtener_plantilla(visitante_id)

	var f_local     = _fuerza(pl_local,     local,     not neutral)
	var f_visitante = _fuerza(pl_visitante, visitante, false)

	var res = _simular_minutos(local_id, visitante_id, pl_local, pl_visitante, f_local, f_visitante)
	res["local_id"]          = local_id
	res["visitante_id"]      = visitante_id
	res["local_nombre"]      = local.get("nombre_corto", "Local")
	res["visitante_nombre"]  = visitante.get("nombre_corto", "Visitante")
	res["fecha"]             = CalendarSystem.obtener_fecha_actual().duplicate()
	return res

# ─── Cálculo de fuerza ────────────────────────────────────────────────────────

func _fuerza(plantilla: Array, equipo: Dictionary, es_local: bool) -> float:
	if plantilla.is_empty():
		return 50.0
	var ordenada = plantilla.duplicate()
	ordenada.sort_custom(func(a, b): return a.get("media", 0) > b.get("media", 0))
	var once = ordenada.slice(0, mini(11, ordenada.size()))
	var suma = 0.0
	for j in once:
		suma += float(j.get("media", 60))
	var media = suma / once.size()

	var moral   = equipo.get("moral", 75)
	var f_moral = 0.92 + (float(moral) / 75.0) * 0.08
	var f_local = 1.07 if es_local else 1.0
	return media * f_moral * f_local

# ─── Simulación minuto a minuto ───────────────────────────────────────────────

func _simular_minutos(lid: int, vid: int,
		pll: Array, plv: Array,
		fl: float, fv: float) -> Dictionary:

	var gl := 0; var gv := 0
	var disparos := [0, 0]; var corners := [0, 0]; var posesion_l := 0
	var eventos: Array = []
	var goleadores: Array = []
	var asistentes: Array = []
	var tarjetas: Array = []
	var lesiones: Array = []
	var rojos := [0, 0]

	var ft = fl + fv
	var p_posesion_l = fl / ft if ft > 0.0 else 0.5

	for min in range(1, MINUTOS + 1):
		var fm_l = maxf(0.5, 1.0 - rojos[0] * 0.15)
		var fm_v = maxf(0.5, 1.0 - rojos[1] * 0.15)

		var tiene_local = randf() < (p_posesion_l * fm_l / (p_posesion_l * fm_l + (1.0 - p_posesion_l) * fm_v))
		if tiene_local:
			posesion_l += 1

		# Ocasión
		var intensidad = (fl if tiene_local else fv) / 100.0
		if randf() < 0.055 * intensidad:
			if tiene_local:
				disparos[0] += 1
				var p_gol = 0.28 * (fl / (fl + fv * 1.1))
				if randf() < p_gol:
					gl += 1
					var scorer = _goleador(pll)
					var assist = _asistente(pll, scorer)
					_reg_gol(goleadores, asistentes, eventos, scorer, assist, lid, min, "local")
				elif randf() < 0.3:
					corners[0] += 1
			else:
				disparos[1] += 1
				var p_gol = 0.28 * (fv / (fv + fl * 1.1))
				if randf() < p_gol:
					gv += 1
					var scorer = _goleador(plv)
					var assist = _asistente(plv, scorer)
					_reg_gol(goleadores, asistentes, eventos, scorer, assist, vid, min, "visitante")
				elif randf() < 0.3:
					corners[1] += 1

		# Tarjetas
		if randf() < PROB_AMARILLA:
			var es_l = randf() < 0.5
			var pl   = pll if es_l else plv
			var eid  = lid if es_l else vid
			var lado = "local" if es_l else "visitante"
			if not pl.is_empty():
				var j = pl[randi() % pl.size()]
				var tipo = "roja" if randf() < 0.08 else "amarilla"
				tarjetas.append({
					"id": j.get("id", 0), "nombre": j.get("nombre_corto", "?"),
					"equipo_id": eid, "tipo": tipo, "minuto": min
				})
				if tipo == "roja":
					rojos[0 if es_l else 1] += 1
					eventos.append({"minuto": min, "tipo": "roja", "lado": lado})

		# Lesiones
		if randf() < PROB_LESION:
			var es_l = randf() < 0.5
			var pl   = pll if es_l else plv
			var eid  = lid if es_l else vid
			if not pl.is_empty():
				var j = pl[randi() % pl.size()]
				lesiones.append({
					"id": j.get("id", 0), "nombre": j.get("nombre_corto", "?"),
					"equipo_id": eid, "minuto": min, "semanas": randi() % 4 + 1
				})

	var pos_l = int(float(posesion_l) / float(MINUTOS) * 100.0)
	return {
		"goles_local": gl, "goles_visitante": gv,
		"goleadores": goleadores, "asistentes": asistentes,
		"tarjetas": tarjetas, "lesiones": lesiones,
		"posesion": [pos_l, 100 - pos_l],
		"disparos": disparos, "corners": corners,
		"eventos": eventos,
	}

# ─── Helpers ──────────────────────────────────────────────────────────────────

func _reg_gol(goleadores, asistentes, eventos, scorer, assist, eid, min, lado):
	if scorer.is_empty(): return
	goleadores.append({"id": scorer.get("id",0), "nombre": scorer.get("nombre_corto","?"), "equipo_id": eid, "minuto": min})
	if not assist.is_empty():
		asistentes.append({"id": assist.get("id",0), "nombre": assist.get("nombre_corto","?"), "equipo_id": eid, "minuto": min})
	eventos.append({"minuto": min, "tipo": "gol", "lado": lado, "goleador": scorer.get("nombre_corto","?")})

func _goleador(plantilla: Array) -> Dictionary:
	if plantilla.is_empty(): return {}
	var pesos: Array = []
	for j in plantilla:
		pesos.append(_peso_gol(j.get("posicion_principal", "MC")))
	return _ponderado(plantilla, pesos)

func _asistente(plantilla: Array, goleador: Dictionary) -> Dictionary:
	if plantilla.size() <= 1 or randf() < 0.25: return {}
	var cands = plantilla.filter(func(j): return j.get("id") != goleador.get("id"))
	if cands.is_empty(): return {}
	var pesos: Array = []
	for j in cands:
		pesos.append(_peso_asistencia(j.get("posicion_principal", "MC")))
	return _ponderado(cands, pesos)

func _peso_gol(pos: String) -> float:
	match pos:
		"DC":       return 5.0
		"ED","EI":  return 3.0
		"MCO":      return 2.5
		"MC":       return 1.5
		"DFC":      return 1.2
		"LD","LI":  return 1.0
		"MCD":      return 0.8
		"PO":       return 0.05
		_:          return 1.0

func _peso_asistencia(pos: String) -> float:
	match pos:
		"MCO":      return 3.0
		"ED","EI":  return 2.5
		"MC":       return 2.0
		"LD","LI":  return 1.8
		"DC":       return 1.5
		"MCD":      return 1.0
		"DFC":      return 0.5
		"PO":       return 0.1
		_:          return 1.0

func _ponderado(array: Array, pesos: Array) -> Dictionary:
	var total = 0.0
	for p in pesos: total += p
	var r = randf() * total
	var acum = 0.0
	for i in range(array.size()):
		acum += pesos[i]
		if r <= acum: return array[i]
	return array[-1] if not array.is_empty() else {}
