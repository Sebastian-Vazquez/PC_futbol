extends Node

## S03. DATABASE SYSTEM
## Archivo: core/database.gd

var jugadores: Dictionary = {}
var equipos: Dictionary = {}
var ligas: Dictionary = {}
var paises: Dictionary = {}

# Índices de búsqueda rápida
var jugadores_por_equipo: Dictionary = {}
var jugadores_por_posicion: Dictionary = {}
var jugadores_por_pais: Dictionary = {}
var equipos_por_liga: Dictionary = {}
var jugadores_libres: Array = []

const DATA_PATH := "res://data/initial/"

func _ready() -> void:
	print("[Database] Inicializado")

func cargar_todo() -> void:
	print("[Database] Cargando datos iniciales...")
	_cargar_json("jugadores", jugadores)
	_cargar_json("equipos", equipos)
	_cargar_json("ligas", ligas)
	_cargar_json("paises", paises)
	_construir_indices()
	print("[Database] Cargados: %d jugadores | %d equipos | %d ligas" % [
		jugadores.size(), equipos.size(), ligas.size()
	])

func _cargar_json(nombre: String, destino: Dictionary) -> void:
	var ruta := DATA_PATH + nombre + ".json"
	if not FileAccess.file_exists(ruta):
		print("[Database] %s.json no encontrado — se usarán datos vacíos" % nombre)
		return
	var f := FileAccess.open(ruta, FileAccess.READ)
	var parser := JSON.new()
	if parser.parse(f.get_as_text()) != OK:
		push_error("[Database] Error al parsear %s.json" % nombre)
		f.close()
		return
	f.close()
	var data = parser.get_data()
	if data is Array:
		for item in data:
			if item.has("id"):
				destino[int(item["id"])] = item
	elif data is Dictionary:
		destino.merge(data)

func _construir_indices() -> void:
	jugadores_por_equipo.clear()
	jugadores_por_posicion.clear()
	jugadores_por_pais.clear()
	jugadores_libres.clear()

	for id in jugadores:
		var j: Dictionary = jugadores[id]
		var eid: int = int(j.get("equipo_id", -1))
		if eid == -1:
			jugadores_libres.append(id)
		else:
			if not jugadores_por_equipo.has(eid):
				jugadores_por_equipo[eid] = []
			jugadores_por_equipo[eid].append(id)
		var pos: String = j.get("posicion_principal", "")
		if not jugadores_por_posicion.has(pos):
			jugadores_por_posicion[pos] = []
		jugadores_por_posicion[pos].append(id)
		var pais: String = j.get("nacionalidad", "")
		if not jugadores_por_pais.has(pais):
			jugadores_por_pais[pais] = []
		jugadores_por_pais[pais].append(id)

	equipos_por_liga.clear()
	for id in equipos:
		var e: Dictionary = equipos[id]
		var lid: int = int(e.get("liga_id", -1))
		if lid != -1:
			if not equipos_por_liga.has(lid):
				equipos_por_liga[lid] = []
			equipos_por_liga[lid].append(int(id))

func obtener_jugador(id: int) -> Dictionary:
	return jugadores.get(id, {})

func obtener_equipo(id: int) -> Dictionary:
	return equipos.get(id, {})

func obtener_liga(id: int) -> Dictionary:
	return ligas.get(id, {})

func obtener_plantilla(equipo_id: int) -> Array:
	var ids: Array = jugadores_por_equipo.get(equipo_id, [])
	return ids.map(func(id): return jugadores[id])

func buscar_jugadores(filtros: Dictionary) -> Array:
	var resultado: Array = []
	for id in jugadores:
		if _cumple_filtros(jugadores[id], filtros):
			resultado.append(jugadores[id])
	return resultado

func obtener_agentes_libres(filtros: Dictionary = {}) -> Array:
	return jugadores_libres.map(func(id): return jugadores[id]).filter(
		func(j): return _cumple_filtros(j, filtros)
	)

func actualizar_entidad(tipo: String, id: int, datos: Dictionary) -> void:
	match tipo:
		"jugador":
			if jugadores.has(id): jugadores[id].merge(datos, true)
		"equipo":
			if equipos.has(id): equipos[id].merge(datos, true)
		"liga":
			if ligas.has(id): ligas[id].merge(datos, true)

func _cumple_filtros(j: Dictionary, filtros: Dictionary) -> bool:
	if filtros.has("posicion") and j.get("posicion_principal") != filtros["posicion"]:
		return false
	if filtros.has("nacionalidad") and j.get("nacionalidad") != filtros["nacionalidad"]:
		return false
	if filtros.has("edad_min") or filtros.has("edad_max"):
		var edad := _calcular_edad(j.get("fecha_nacimiento", ""))
		if filtros.has("edad_min") and edad < filtros["edad_min"]:
			return false
		if filtros.has("edad_max") and edad > filtros["edad_max"]:
			return false
	if filtros.has("valor_max"):
		if j.get("valor_mercado", 0) > filtros["valor_max"]:
			return false
	return true

func _calcular_edad(fecha_nac: String) -> int:
	if fecha_nac.is_empty(): return 0
	var partes := fecha_nac.split("-")
	if partes.size() < 1: return 0
	return CalendarSystem.obtener_fecha_actual().anio - int(partes[0])
