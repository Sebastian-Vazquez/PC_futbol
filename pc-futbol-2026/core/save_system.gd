extends Node

## S04. SAVE / LOAD SYSTEM
## Archivo: core/save_system.gd

const SAVE_DIR := "user://saves/"
const MAX_SLOTS := 10
const AUTOSAVE_SLOT := 0

func _ready() -> void:
	_asegurar_directorio()
	print("[SaveSystem] Inicializado — dir: " + SAVE_DIR)

func guardar(slot_id: int) -> void:
	var datos := _serializar_estado()
	var ruta := _ruta_slot(slot_id)
	var f := FileAccess.open(ruta, FileAccess.WRITE)
	if f == null:
		push_error("[SaveSystem] No se pudo escribir en: " + ruta)
		return
	f.store_string(JSON.stringify(datos, "\t"))
	f.close()
	print("[SaveSystem] Guardado en slot %d" % slot_id)

func cargar(slot_id: int) -> bool:
	var ruta := _ruta_slot(slot_id)
	if not FileAccess.file_exists(ruta):
		print("[SaveSystem] Slot %d vacío" % slot_id)
		return false
	var f := FileAccess.open(ruta, FileAccess.READ)
	var parser := JSON.new()
	var err := parser.parse(f.get_as_text())
	f.close()
	if err != OK:
		push_error("[SaveSystem] Error al parsear slot %d" % slot_id)
		return false
	_deserializar_estado(parser.get_data())
	print("[SaveSystem] Cargado desde slot %d" % slot_id)
	return true

func autosave() -> void:
	guardar(AUTOSAVE_SLOT)

func listar_saves() -> Array:
	var lista: Array = []
	for slot in range(MAX_SLOTS + 1):
		var preview := obtener_preview(slot)
		if not preview.is_empty():
			lista.append(preview)
	return lista

func borrar_save(slot_id: int) -> void:
	var ruta := _ruta_slot(slot_id)
	if FileAccess.file_exists(ruta):
		DirAccess.remove_absolute(ruta)
		print("[SaveSystem] Slot %d borrado" % slot_id)

func obtener_preview(slot_id: int) -> Dictionary:
	var ruta := _ruta_slot(slot_id)
	if not FileAccess.file_exists(ruta):
		return {}
	var f := FileAccess.open(ruta, FileAccess.READ)
	var parser := JSON.new()
	if parser.parse(f.get_as_text()) != OK:
		f.close()
		return {}
	f.close()
	var d: Dictionary = parser.get_data()
	return {
		"slot": slot_id,
		"equipo": d.get("equipo_nombre", ""),
		"fecha": d.get("fecha", {}),
		"liga": d.get("liga_nombre", ""),
		"posicion": d.get("posicion", 0),
		"temporada": d.get("temporada", 0),
		"es_autosave": slot_id == AUTOSAVE_SLOT
	}

func _serializar_estado() -> Dictionary:
	var gm := GameManager.obtener_estado_global()
	return {
		"version": 1,
		"fecha_guardado": Time.get_datetime_string_from_system(),
		"equipo_jugador_id": gm["equipo_jugador_id"],
		"equipo_nombre": DB.obtener_equipo(gm["equipo_jugador_id"]).get("nombre", ""),
		"temporada": gm["temporada"],
		"fecha": gm["fecha"],
		"liga_nombre": "",
		"posicion": 0,
		"jugadores": DB.jugadores,
		"equipos": DB.equipos,
		"ligas": DB.ligas,
		"configuracion": gm["configuracion"]
	}

func _deserializar_estado(datos: Dictionary) -> void:
	if datos.is_empty(): return
	if datos.has("jugadores"): DB.jugadores = datos["jugadores"]
	if datos.has("equipos"): DB.equipos = datos["equipos"]
	if datos.has("ligas"): DB.ligas = datos["ligas"]
	if datos.has("equipo_jugador_id"):
		GameManager.equipo_jugador_id = datos["equipo_jugador_id"]
	if datos.has("temporada"):
		GameManager.temporada_actual = datos["temporada"]
	if datos.has("fecha"):
		var f: Dictionary = datos["fecha"]
		CalendarSystem.dia = f.get("dia", 1)
		CalendarSystem.mes = f.get("mes", 7)
		CalendarSystem.anio = f.get("anio", 2026)
	DB._construir_indices()

func _asegurar_directorio() -> void:
	if not DirAccess.dir_exists_absolute(SAVE_DIR):
		DirAccess.make_dir_recursive_absolute(SAVE_DIR)

func _ruta_slot(slot_id: int) -> String:
	return SAVE_DIR + "save_%02d.sav" % slot_id
