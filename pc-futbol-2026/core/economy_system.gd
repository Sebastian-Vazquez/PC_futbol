extends Node

## S09. ECONOMY & FINANCE SYSTEM
## Gestiona ingresos, gastos y balance financiero de todos los clubes.

signal finanzas_actualizadas(equipo_id: int, delta: int)
signal club_en_crisis(equipo_id: int, deuda: int)
signal temporada_financiera_cerrada(resumen: Dictionary)

const FILL_RATE_BASE    := 0.65   # Ocupación base del estadio
const SEMANAS_INGRESOS  := 40     # Semanas con ingresos de TV (temporada regular)

var _semana_actual: int = 0

func _ready() -> void:
	print("[EconomySystem] Inicializado")

# ─── Procesamiento semanal ────────────────────────────────────────────────────

func procesar_semana(semana: int) -> void:
	## Llamar una vez por semana desde CalendarSystem / GameManager.
	_semana_actual = semana
	for eid in DB.equipos:
		_procesar_club(int(eid), semana)

func _procesar_club(equipo_id: int, semana: int) -> void:
	var equipo: Dictionary = DB.obtener_equipo(equipo_id)
	if equipo.is_empty(): return
	var fin: Dictionary = equipo.get("finanzas", {}).duplicate()
	if fin.is_empty(): return

	# ── Ingresos ────────────────────────────────────────────────────────────
	var ing_sponsor: int = int((fin.get("sponsor_camiseta", 0) + fin.get("sponsor_estadio", 0)) / 52.0)
	var ing_merch:   int = int(fin.get("merchandising_anual", 0) / 52.0)
	var ing_tv:      int = 0
	if semana >= 5 and semana <= (5 + SEMANAS_INGRESOS):
		ing_tv = int(fin.get("ingresos_tv_anual", 0) / float(SEMANAS_INGRESOS))
	var ingresos: int = ing_sponsor + ing_merch + ing_tv

	# ── Gastos ──────────────────────────────────────────────────────────────
	var gastos_salarios: int = fin.get("masa_salarial_semanal", 0)
	var gastos_estadio:  int = int(equipo.get("estadio", {}).get("coste_mantenimiento_semanal", 0))
	var gastos: int = gastos_salarios + gastos_estadio

	# ── Aplicar ─────────────────────────────────────────────────────────────
	var delta: int = ingresos - gastos
	var balance_nuevo: int = fin.get("balance", 0) + delta

	if balance_nuevo < 0:
		fin["deuda"]   = fin.get("deuda", 0) + abs(balance_nuevo)
		balance_nuevo  = 0
		var deuda_actual: int = fin.get("deuda", 0)
		if deuda_actual > 5_000_000:
			club_en_crisis.emit(equipo_id, deuda_actual)

	fin["balance"] = balance_nuevo
	DB.actualizar_entidad("equipo", equipo_id, {"finanzas": fin})
	if delta != 0:
		finanzas_actualizadas.emit(equipo_id, delta)

# ─── Ingresos por partido (matchday) ─────────────────────────────────────────

func calcular_ingreso_partido(equipo_id: int) -> int:
	## Devuelve cuánto ingresa el equipo LOCAL por taquilla.
	var equipo: Dictionary = DB.obtener_equipo(equipo_id)
	if equipo.is_empty(): return 0
	var estadio:      Dictionary = equipo.get("estadio", {})
	var fin:          Dictionary = equipo.get("finanzas", {})
	var reputacion:   int        = equipo.get("reputacion", 60)

	var capacidad:   int   = estadio.get("capacidad", 10000)
	var precio:      int   = fin.get("precio_entrada_base", 20)
	var fill:        float = FILL_RATE_BASE + (float(reputacion - 60) / 40.0) * 0.30
	fill = clampf(fill, 0.30, 0.98)
	return int(capacidad * fill) * precio

func registrar_ingreso_partido(equipo_id: int, ingreso: int) -> void:
	var equipo: Dictionary = DB.obtener_equipo(equipo_id)
	if equipo.is_empty() or ingreso <= 0: return
	var fin: Dictionary = equipo.get("finanzas", {}).duplicate()
	fin["balance"] = fin.get("balance", 0) + ingreso
	DB.actualizar_entidad("equipo", equipo_id, {"finanzas": fin})

# ─── Bonus de clasificación ───────────────────────────────────────────────────

func aplicar_bonus_clasificacion(equipo_id: int, tipo: String) -> void:
	## tipos: "champions" | "europa" | "conference" | "campeon" | "descenso"
	var bonuses: Dictionary = {
		"campeon":     10_000_000,
		"champions":    8_000_000,
		"europa":       3_000_000,
		"conference":   1_500_000,
		"descenso":    -2_000_000,
	}
	var bonus: int = bonuses.get(tipo, 0)
	if bonus == 0: return
	var equipo: Dictionary = DB.obtener_equipo(equipo_id)
	if equipo.is_empty(): return
	var fin: Dictionary = equipo.get("finanzas", {}).duplicate()
	fin["balance"] = maxi(0, fin.get("balance", 0) + bonus)
	DB.actualizar_entidad("equipo", equipo_id, {"finanzas": fin})

# ─── Consultas ────────────────────────────────────────────────────────────────

func obtener_informe(equipo_id: int) -> Dictionary:
	var equipo: Dictionary = DB.obtener_equipo(equipo_id)
	if equipo.is_empty(): return {}
	var fin: Dictionary = equipo.get("finanzas", {})
	var est: Dictionary = equipo.get("estadio", {})
	return {
		"nombre":                equipo.get("nombre_corto", "?"),
		"balance":               fin.get("balance", 0),
		"deuda":                 fin.get("deuda", 0),
		"presupuesto_fichajes":  fin.get("presupuesto_fichajes", 0),
		"masa_salarial_semanal": fin.get("masa_salarial_semanal", 0),
		"ingresos_tv_anual":     fin.get("ingresos_tv_anual", 0),
		"sponsor_total_anual":   fin.get("sponsor_camiseta", 0) + fin.get("sponsor_estadio", 0),
		"merchandising_anual":   fin.get("merchandising_anual", 0),
		"ingreso_partido":       calcular_ingreso_partido(equipo_id),
		"capacidad_estadio":     est.get("capacidad", 0),
	}

func top_ricos(n: int = 10) -> Array:
	var lista: Array = []
	for eid in DB.equipos:
		var eq: Dictionary = DB.equipos[eid]
		lista.append({
			"equipo_id": int(eid),
			"nombre":    eq.get("nombre_corto", "?"),
			"balance":   eq.get("finanzas", {}).get("balance", 0),
		})
	lista.sort_custom(func(a, b): return a.balance > b.balance)
	return lista.slice(0, n)

func calcular_masa_salarial(equipo_id: int) -> int:
	var plantilla: Array = DB.obtener_plantilla(equipo_id)
	var total: int = 0
	for j in plantilla:
		total += j.get("contrato", {}).get("salario_semanal", 0)
	return total

func porcentaje_salarios_sobre_ingresos(equipo_id: int) -> float:
	## Ratio masa salarial / ingresos anuales. Sano < 70%.
	var eq: Dictionary = DB.obtener_equipo(equipo_id)
	if eq.is_empty(): return 0.0
	var fin:  Dictionary = eq.get("finanzas", {})
	var masa: int        = fin.get("masa_salarial_semanal", 0) * 52
	var ing:  int        = (fin.get("ingresos_tv_anual", 0)
		+ fin.get("sponsor_camiseta", 0)
		+ fin.get("sponsor_estadio", 0)
		+ fin.get("merchandising_anual", 0))
	if ing == 0: return 999.0
	return float(masa) / float(ing) * 100.0
