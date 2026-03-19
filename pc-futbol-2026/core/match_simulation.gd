extends Node

## S06. MATCH SIMULATION ENGINE v2
## Modelo basado en xG (expected goals) con distribución realista.
## Target calibrado: ~2.6 goles/partido, ~7% de 0-0, upsets realistas.
##
## Fórmula base (equipos iguales media=75, local):
##   xG_local  = 1.20 * 1.0 * 1.08 = 1.296
##   xG_visit  = 1.20 * 1.0 * 1.00 = 1.200
##   Total     = 2.496  (+ penales 15% + sobredispersión → ~2.65 real)
##   P(0-0)   ≈ e^-1.30 × e^-1.20 ≈ 7%  ✓

const BASE_XG   := 1.20   ## xG base por equipo, equipos iguales, neutral
const HOME_MULT := 1.08   ## ventaja de local
const REF_RTG   := 75.0   ## rating de referencia para normalización

# ─── Punto de entrada ─────────────────────────────────────────────────────────

func simular(local_id: int, visitante_id: int, neutral: bool = false) -> Dictionary:
	var local: Dictionary     = DB.obtener_equipo(local_id)
	var visitante: Dictionary = DB.obtener_equipo(visitante_id)
	if local.is_empty() or visitante.is_empty():
		push_error("[MatchSim] Equipo no encontrado: %d vs %d" % [local_id, visitante_id])
		return {}

	var pll: Array = DB.obtener_plantilla(local_id)
	var plv: Array = DB.obtener_plantilla(visitante_id)
	var sl: Dictionary = _stats_equipo(pll, local)
	var sv: Dictionary = _stats_equipo(plv, visitante)

	# ── xG base (función logística suave: no explota con grandes diferencias) ─
	var ratio_l: float = clampf((sl.att / REF_RTG) / (sv.def / REF_RTG), 0.35, 3.0)
	var ratio_v: float = clampf((sv.att / REF_RTG) / (sl.def / REF_RTG), 0.35, 3.0)
	var xg_l: float = BASE_XG * _sigmoid_ratio(ratio_l) * sl.form
	var xg_v: float = BASE_XG * _sigmoid_ratio(ratio_v) * sv.form
	if not neutral:
		xg_l *= HOME_MULT

	# ── Tarjeta roja (10% de partidos tienen alguna roja) ─────────────────────
	var red_min_l: int = -1
	var red_min_v: int = -1
	if randf() < 0.10:
		var min_r: int = 15 + randi() % 70
		var frac: float = float(90 - min_r) / 90.0
		if randf() < 0.5:
			red_min_l = min_r
			xg_l = maxf(0.10, xg_l * (1.0 - 0.38 * frac))
			xg_v = minf(xg_v * 2.0, xg_v * (1.0 + 0.22 * frac))
		else:
			red_min_v = min_r
			xg_v = maxf(0.10, xg_v * (1.0 - 0.38 * frac))
			xg_l = minf(xg_l * 2.0, xg_l * (1.0 + 0.22 * frac))

	# ── Penal (15% de partidos; xG de penal real ≈ 0.76) ─────────────────────
	var penales: Array = []
	if randf() < 0.15:
		var min_p: int = 10 + randi() % 80
		if randf() < 0.52:          # locales reciben penal ligeramente más
			xg_l += 0.76
			penales.append({"lado": "local", "minuto": min_p})
		else:
			xg_v += 0.76
			penales.append({"lado": "visitante", "minuto": min_p})

	# ── Error defensivo grave (5% de partidos; +0.4 xG al atacante) ──────────
	if randf() < 0.05:
		if randf() < 0.5:
			xg_l += 0.40
		else:
			xg_v += 0.40

	# ── Sobredispersión lognormal: el fútbol tiene más varianza que Poisson ───
	# (randf()*3 - 1.5) * 0.40  →  media≈0, std≈0.20 → multiplier 0.67–1.49
	var nl: float = (randf() + randf() + randf() - 1.5) * 0.40
	var nv: float = (randf() + randf() + randf() - 1.5) * 0.40
	var xg_l_eff: float = maxf(0.05, xg_l * exp(nl))
	var xg_v_eff: float = maxf(0.05, xg_v * exp(nv))

	# ── Goles desde distribución Poisson ──────────────────────────────────────
	var gl: int = _poisson(xg_l_eff)
	var gv: int = _poisson(xg_v_eff)

	# ── Construir resultado ───────────────────────────────────────────────────
	var res: Dictionary = _construir_resultado(
		gl, gv, pll, plv, local_id, visitante_id,
		red_min_l, red_min_v, penales
	)
	res["local_id"]         = local_id
	res["visitante_id"]     = visitante_id
	res["local_nombre"]     = local.get("nombre_corto",     "Local")     as String
	res["visitante_nombre"] = visitante.get("nombre_corto", "Visitante") as String
	res["fecha"]            = CalendarSystem.obtener_fecha_actual().duplicate()
	res["xg_local"]         = snappedf(xg_l, 0.01)
	res["xg_visitante"]     = snappedf(xg_v, 0.01)
	return res

# ─── Estadísticas del equipo ──────────────────────────────────────────────────

func _stats_equipo(plantilla: Array, equipo: Dictionary) -> Dictionary:
	if plantilla.is_empty():
		return {"att": REF_RTG, "def": REF_RTG, "form": 1.0}

	# Top 11 jugadores por media
	var top: Array = plantilla.duplicate()
	top.sort_custom(func(a, b): return a.get("media", 0) > b.get("media", 0))
	top = top.slice(0, mini(11, top.size()))

	var s_gk: float = 0.0;  var n_gk:  int = 0
	var s_def: float = 0.0; var n_def: int = 0
	var s_mid: float = 0.0; var n_mid: int = 0
	var s_att: float = 0.0; var n_att: int = 0

	for j in top:
		var m: float = float(j.get("media", 65))
		var pos: String = j.get("posicion_principal", "MC") as String
		match pos:
			"PO":
				s_gk  += m; n_gk  += 1
			"LD", "DFC", "LI":
				s_def += m; n_def += 1
			"MCD", "MC", "MCO":
				s_mid += m; n_mid += 1
			"EI", "ED", "DC":
				s_att += m; n_att += 1
			_:
				s_mid += m; n_mid += 1

	var gk_v:  float = s_gk  / float(maxi(1, n_gk))  if n_gk  > 0 else REF_RTG
	var def_v: float = s_def / float(maxi(1, n_def)) if n_def > 0 else REF_RTG
	var mid_v: float = s_mid / float(maxi(1, n_mid)) if n_mid > 0 else REF_RTG
	var att_v: float = s_att / float(maxi(1, n_att)) if n_att > 0 else REF_RTG

	var moral: int = equipo.get("moral", 75)
	var form: float = clampf(0.90 + float(moral - 75) * 0.002, 0.87, 1.13)

	return {
		"att":  att_v * 0.55 + mid_v * 0.45,   # ofensivo = delanteros + medios
		"def":  def_v * 0.60 + gk_v  * 0.40,   # defensivo = defensas + portero
		"form": form,
	}

# Suaviza las diferencias grandes: ratio 2.0 no da el doble de xG exacto
func _sigmoid_ratio(r: float) -> float:
	# Devuelve valor en [0.40, 1.80] con punto fijo en r=1.0 → 1.0
	return 2.0 / (1.0 + exp(-1.4 * (r - 1.0)))

# ─── Construcción del resultado ───────────────────────────────────────────────

func _construir_resultado(gl: int, gv: int,
		pll: Array, plv: Array,
		lid: int, vid: int,
		red_min_l: int, red_min_v: int,
		penales: Array) -> Dictionary:

	var goleadores: Array = []
	var asistentes: Array = []
	var tarjetas:   Array = []
	var lesiones:   Array = []
	var eventos:    Array = []

	# Goles locales
	for min_g in _minutos_gol(gl):
		var sc: Dictionary = _goleador(pll)
		var as_: Dictionary = _asistente(pll, sc)
		_add_gol(goleadores, asistentes, eventos, sc, as_, lid, min_g, "local")

	# Goles visitantes
	for min_g in _minutos_gol(gv):
		var sc: Dictionary = _goleador(plv)
		var as_: Dictionary = _asistente(plv, sc)
		_add_gol(goleadores, asistentes, eventos, sc, as_, vid, min_g, "visitante")

	# Penales como eventos
	for p in penales:
		eventos.append({"minuto": int(p.get("minuto", 45)), "tipo": "penal",
			"lado": str(p.get("lado", "")), "goleador": "Penal"})

	# Rojas
	if red_min_l >= 0:
		var j: Dictionary = _rand_jugador(pll)
		tarjetas.append({"jugador_id": int(j.get("id",0)),
			"nombre": j.get("nombre_corto","?") as String,
			"equipo_id": lid, "tipo": "roja", "minuto": red_min_l})
		eventos.append({"minuto": red_min_l, "tipo": "roja", "lado": "local",
			"goleador": j.get("nombre_corto","?") as String})
	if red_min_v >= 0:
		var j: Dictionary = _rand_jugador(plv)
		tarjetas.append({"jugador_id": int(j.get("id",0)),
			"nombre": j.get("nombre_corto","?") as String,
			"equipo_id": vid, "tipo": "roja", "minuto": red_min_v})
		eventos.append({"minuto": red_min_v, "tipo": "roja", "lado": "visitante",
			"goleador": j.get("nombre_corto","?") as String})

	# Amarillas (3-5 por partido)
	for _i in range(3 + randi() % 3):
		var es_l: bool = randf() < 0.5
		var j: Dictionary = _rand_jugador(pll if es_l else plv)
		if not j.is_empty():
			tarjetas.append({"jugador_id": int(j.get("id",0)),
				"nombre": j.get("nombre_corto","?") as String,
				"equipo_id": lid if es_l else vid,
				"tipo": "amarilla", "minuto": 5 + randi() % 85})

	# Lesiones (~15% de partidos)
	if randf() < 0.15:
		var es_l: bool = randf() < 0.5
		var j: Dictionary = _rand_jugador(pll if es_l else plv)
		if not j.is_empty():
			lesiones.append({"jugador_id": int(j.get("id",0)),
				"nombre": j.get("nombre_corto","?") as String,
				"equipo_id": lid if es_l else vid,
				"minuto": 10 + randi() % 80,
				"semanas": 1 + randi() % 4})

	eventos.sort_custom(func(a, b): return int(a.get("minuto",0)) < int(b.get("minuto",0)))

	var pos_l: int = 40 + randi() % 21   # 40-60% posesión local

	return {
		"goles_local":     gl,
		"goles_visitante": gv,
		"goleadores": goleadores,
		"asistentes": asistentes,
		"tarjetas":   tarjetas,
		"lesiones":   lesiones,
		"posesion":   [pos_l, 100 - pos_l],
		"disparos":   [maxi(gl + 1, 3 + randi() % 9), maxi(gv + 1, 2 + randi() % 8)],
		"corners":    [2 + randi() % 8, 1 + randi() % 7],
		"eventos":    eventos,
	}

# ─── Poisson (algoritmo de Knuth) ────────────────────────────────────────────

func _poisson(lam: float) -> int:
	if lam <= 0.0: return 0
	var L: float = exp(-minf(lam, 15.0))
	var k: int   = 0
	var p: float = 1.0
	while true:
		k += 1
		p *= randf()
		if p <= L: break
	return k - 1

# ─── Distribución de minutos de gol ──────────────────────────────────────────
# Distribución empírica de la Premier/La Liga: más goles 60-90 que 0-30

func _minutos_gol(n: int) -> Array:
	var mins: Array = []
	for _i in range(n):
		var r: float = randf()
		var m: int
		if   r < 0.07: m = 1  + randi() % 14  # 1-14 min   7%
		elif r < 0.22: m = 15 + randi() % 15  # 15-29 min  15%
		elif r < 0.40: m = 30 + randi() % 15  # 30-44 min  18%
		elif r < 0.55: m = 45 + randi() % 15  # 45-59 min  15%
		elif r < 0.77: m = 60 + randi() % 20  # 60-79 min  22%
		elif r < 0.93: m = 80 + randi() % 10  # 80-89 min  16%
		else:          m = 90 + randi() % 6   # 90+  min   7%
		mins.append(m)
	mins.sort()
	return mins

# ─── Helpers ──────────────────────────────────────────────────────────────────

func _add_gol(goleadores: Array, asistentes: Array, eventos: Array,
		sc: Dictionary, as_: Dictionary, eid: int, min_g: int, lado: String) -> void:
	if sc.is_empty(): return
	goleadores.append({
		"jugador_id": int(sc.get("id", 0)),
		"nombre":     sc.get("nombre_corto", "?") as String,
		"equipo_id":  eid, "minuto": min_g,
	})
	if not as_.is_empty():
		asistentes.append({
			"jugador_id": int(as_.get("id", 0)),
			"nombre":     as_.get("nombre_corto", "?") as String,
			"equipo_id":  eid, "minuto": min_g,
		})
	eventos.append({"minuto": min_g, "tipo": "gol", "lado": lado,
		"goleador": sc.get("nombre_corto", "?") as String})

func _goleador(pl: Array) -> Dictionary:
	if pl.is_empty(): return {}
	var pw: Array = []
	for j in pl: pw.append(_peso_gol(j.get("posicion_principal", "MC") as String))
	return _ponderado(pl, pw)

func _asistente(pl: Array, gol: Dictionary) -> Dictionary:
	if pl.size() <= 1 or randf() < 0.22: return {}
	var cands: Array = []
	var gid: int = int(gol.get("id", -999))
	for j in pl:
		if int(j.get("id", 0)) != gid: cands.append(j)
	if cands.is_empty(): return {}
	var pw: Array = []
	for j in cands: pw.append(_peso_asistencia(j.get("posicion_principal", "MC") as String))
	return _ponderado(cands, pw)

func _rand_jugador(pl: Array) -> Dictionary:
	if pl.is_empty(): return {}
	return pl[randi() % pl.size()]

func _peso_gol(pos: String) -> float:
	match pos:
		"DC":      return 5.0
		"ED","EI": return 3.0
		"MCO":     return 2.5
		"MC":      return 1.5
		"DFC":     return 1.2
		"LD","LI": return 1.0
		"MCD":     return 0.8
		"PO":      return 0.05
		_:         return 1.0

func _peso_asistencia(pos: String) -> float:
	match pos:
		"MCO":     return 3.0
		"ED","EI": return 2.5
		"MC":      return 2.0
		"LD","LI": return 1.8
		"DC":      return 1.5
		"MCD":     return 1.0
		"DFC":     return 0.5
		"PO":      return 0.1
		_:         return 1.0

func _ponderado(arr: Array, pesos: Array) -> Dictionary:
	var total: float = 0.0
	for p in pesos: total += float(p)
	if total <= 0.0: return arr[0] if not arr.is_empty() else {}
	var r: float = randf() * total
	var acum: float = 0.0
	for i in range(arr.size()):
		acum += float(pesos[i])
		if r <= acum: return arr[i]
	return arr[-1] if not arr.is_empty() else {}
