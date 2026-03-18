extends Node

## S01. GAME MANAGER - Orquestador global
## Archivo: core/game_manager.gd

enum GameState { MENU, PLAYING, MATCH, PAUSED }

var estado: GameState = GameState.MENU
var equipo_jugador_id: int = -1
var temporada_actual: int = 2026
var configuracion: Dictionary = {
	"dificultad": 1,
	"idioma": "es",
	"volumen_musica": 0.8,
	"volumen_sfx": 1.0
}

signal dia_avanzado(fecha: Dictionary)
signal semana_avanzada(num_semana: int)
signal temporada_iniciada(anio: int)
signal temporada_finalizada(anio: int)
signal evento_importante(tipo: String, datos: Dictionary)

func _ready() -> void:
	print("[GameManager] Inicializado")

func iniciar_nueva_partida(equipo_id: int, liga_id: int) -> void:
	equipo_jugador_id = equipo_id
	estado = GameState.PLAYING
	CalendarSystem.iniciar_temporada(temporada_actual)
	DB.cargar_todo()
	temporada_iniciada.emit(temporada_actual)
	print("[GameManager] Nueva partida - Equipo ID: %d, Liga ID: %d" % [equipo_id, liga_id])

func cargar_partida(slot: int) -> bool:
	return SaveSystem.cargar(slot)

func guardar_partida(slot: int) -> void:
	SaveSystem.guardar(slot)

func avanzar_dia() -> void:
	CalendarSystem.avanzar(1)
	dia_avanzado.emit(CalendarSystem.obtener_fecha_actual())

func avanzar_semana() -> void:
	CalendarSystem.avanzar(7)
	semana_avanzada.emit(CalendarSystem.obtener_semana_actual())

func avanzar_hasta_proximo_evento() -> void:
	var proximos = CalendarSystem.obtener_proximos_eventos(1)
	if proximos.is_empty():
		return
	var dias = CalendarSystem.dias_hasta(proximos[0].fecha)
	CalendarSystem.avanzar(dias)

func obtener_estado_global() -> Dictionary:
	return {
		"estado": estado,
		"equipo_jugador_id": equipo_jugador_id,
		"temporada": temporada_actual,
		"fecha": CalendarSystem.obtener_fecha_actual(),
		"configuracion": configuracion
	}

func cambiar_escena(pantalla: String) -> void:
	print("[GameManager] Cambiando a: " + pantalla)
	# TODO: get_tree().change_scene_to_file("res://ui/" + pantalla + ".tscn")
