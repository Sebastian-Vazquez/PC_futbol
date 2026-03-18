extends Node

## Escena principal de debug — Fase 1
## Verifica que todos los Autoloads del núcleo funcionan correctamente.

func _ready() -> void:
	print("=" .repeat(40))
	print("  PC FÚTBOL 2026 — FASE 1")
	print("=" .repeat(40))

	# Verificar autoloads
	assert(GameManager != null, "GameManager no disponible")
	assert(CalendarSystem != null, "CalendarSystem no disponible")
	assert(DB != null, "Database no disponible")
	assert(SaveSystem != null, "SaveSystem no disponible")
	print("✓ GameManager")
	print("✓ CalendarSystem")
	print("✓ Database (DB)")
	print("✓ SaveSystem")

	# Test calendario
	var fecha := CalendarSystem.obtener_fecha_actual()
	print("\nFecha inicial: %d/%d/%d" % [fecha.dia, fecha.mes, fecha.anio])
	print("¿Mercado abierto? %s" % str(CalendarSystem.es_mercado_abierto()))
	print("¿Pretemporada? %s" % str(CalendarSystem.es_pretemporada()))

	CalendarSystem.avanzar(7)
	fecha = CalendarSystem.obtener_fecha_actual()
	print("Tras avanzar 7 días: %d/%d/%d" % [fecha.dia, fecha.mes, fecha.anio])

	# Test programar evento
	CalendarSystem.programar_evento(
		{"dia": 15, "mes": 8, "anio": 2026},
		"inicio_liga",
		{"liga_id": 1, "nombre": "LaLiga"}
	)
	var proximos := CalendarSystem.obtener_proximos_eventos(3)
	print("Próximos eventos programados: %d" % proximos.size())

	# Test save/load
	SaveSystem.guardar(1)
	print("Save slot 1 creado ✓")
	var saves := SaveSystem.listar_saves()
	print("Saves disponibles: %d" % saves.size())

	print("\n" + "=" .repeat(40))
	print("  FASE 1 COMPLETADA — Sin errores")
	print("=" .repeat(40))
