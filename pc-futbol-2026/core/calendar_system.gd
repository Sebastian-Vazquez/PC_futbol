extends Node

## S02. CALENDAR & TIME SYSTEM
## Archivo: core/calendar_system.gd

var dia: int = 1
var mes: int = 7
var anio: int = 2026
var semana_actual: int = 1

var _eventos: Array = []  # Array de {fecha: {d,m,a}, tipo: String, datos: Dictionary}

func _ready() -> void:
	print("[CalendarSystem] Inicializado")

func iniciar_temporada(anio_inicio: int) -> void:
	anio = anio_inicio
	mes = 7
	dia = 1
	semana_actual = 1
	_eventos.clear()
	print("[CalendarSystem] Temporada %d iniciada (1/7/%d)" % [anio, anio])

func obtener_fecha_actual() -> Dictionary:
	return {"dia": dia, "mes": mes, "anio": anio}

func obtener_semana_actual() -> int:
	return semana_actual

func avanzar(dias: int) -> void:
	for i in range(dias):
		_avanzar_un_dia()
	_procesar_eventos_pendientes()

func _avanzar_un_dia() -> void:
	dia += 1
	var tope = _dias_del_mes(mes, anio)
	if dia > tope:
		dia = 1
		mes += 1
		if mes > 12:
			mes = 1
			anio += 1
	if (dia - 1) % 7 == 0 and dia > 1:
		semana_actual += 1

func programar_evento(fecha: Dictionary, tipo: String, datos: Dictionary) -> void:
	_eventos.append({"fecha": fecha, "tipo": tipo, "datos": datos})
	_eventos.sort_custom(func(a, b): return _comparar_fechas(a.fecha, b.fecha) < 0)

func obtener_proximos_eventos(n: int) -> Array:
	var hoy = obtener_fecha_actual()
	var futuros = _eventos.filter(func(e): return _comparar_fechas(e.fecha, hoy) > 0)
	return futuros.slice(0, n)

func dias_hasta(fecha_objetivo: Dictionary) -> int:
	var dias_hoy = _fecha_a_dias(obtener_fecha_actual())
	var dias_obj = _fecha_a_dias(fecha_objetivo)
	return max(0, dias_obj - dias_hoy)

func es_mercado_abierto() -> bool:
	return mes in [1, 7, 8]

func es_pretemporada() -> bool:
	return mes == 7

func obtener_jornada_actual(_liga_id: int) -> int:
	# TODO: calcular jornada según calendario de liga
	return 0

func _procesar_eventos_pendientes() -> void:
	var hoy = obtener_fecha_actual()
	var procesados = []
	for evento in _eventos:
		if _comparar_fechas(evento.fecha, hoy) <= 0:
			GameManager.evento_importante.emit(evento.tipo, evento.datos)
			procesados.append(evento)
	for e in procesados:
		_eventos.erase(e)

func _comparar_fechas(a: Dictionary, b: Dictionary) -> int:
	if a.anio != b.anio: return a.anio - b.anio
	if a.mes != b.mes: return a.mes - b.mes
	return a.dia - b.dia

func _fecha_a_dias(f: Dictionary) -> int:
	return f.anio * 365 + f.mes * 30 + f.dia

func _dias_del_mes(m: int, a: int) -> int:
	var tabla = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	if m == 2 and (a % 4 == 0 and (a % 100 != 0 or a % 400 == 0)):
		return 29
	return tabla[m]
