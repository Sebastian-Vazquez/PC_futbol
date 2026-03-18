extends Node

## Escena de debug — Fase 3
## Prueba: simulacion de partidos + liga completa

func _ready() -> void:
	print("=".repeat(50))
	print("  PC FUTBOL 2026 -- FASE 3")
	print("=".repeat(50))

	# Cargar datos
	DB.cargar_todo()
	print("Datos cargados: %d jugadores | %d equipos | %d ligas" % [
		DB.jugadores.size(), DB.equipos.size(), DB.ligas.size()
	])

	if DB.equipos.size() < 2:
		print("ERROR: No hay suficientes equipos. Ejecuta el scraper Python primero.")
		return

	# ── Test 1: Partido individual ──────────────────────────────────────────
	print("\n--- TEST 1: Partido individual ---")
	var equipos_laliga = DB.equipos_por_liga.get(1, [])
	if equipos_laliga.size() >= 2:
		var id1 = equipos_laliga[0]
		var id2 = equipos_laliga[1]
		var eq1 = DB.obtener_equipo(id1)
		var eq2 = DB.obtener_equipo(id2)
		print("Simulando: %s vs %s" % [eq1.get("nombre_corto","?"), eq2.get("nombre_corto","?")])
		var res = MatchSim.simular(id1, id2)
		print("Resultado: %d - %d" % [res.get("goles_local",0), res.get("goles_visitante",0)])
		print("Posesion: %d%% - %d%%" % [res.get("posesion",[50,50])[0], res.get("posesion",[50,50])[1]])
		print("Disparos: %s - %s" % [str(res.get("disparos",[0,0])[0]), str(res.get("disparos",[0,0])[1])])
		if res.get("goleadores", []).size() > 0:
			print("Goleadores:")
			for g in res.get("goleadores", []):
				print("  Min %d: %s" % [g.get("minuto",0), g.get("nombre","?")])
	else:
		print("No hay equipos en LaLiga (liga_id=1). Verificar datos.")

	# ── Test 2: Temporada LaLiga completa ───────────────────────────────────
	print("\n--- TEST 2: Temporada LaLiga completa ---")
	var liga_test_id = 1  # LaLiga
	if not DB.ligas.has(liga_test_id):
		# Buscar primera liga disponible
		if not DB.ligas.is_empty():
			liga_test_id = int(DB.ligas.keys()[0])

	LeagueSystem.inicializar_todas_las_ligas()

	var n_jornadas = LeagueSystem.obtener_num_jornadas(liga_test_id)
	print("Liga ID %d: %d jornadas" % [liga_test_id, n_jornadas])

	if n_jornadas > 0:
		var t_inicio = Time.get_ticks_msec()
		LeagueSystem.simular_temporada_completa(liga_test_id)
		var t_fin = Time.get_ticks_msec()
		print("Temporada simulada en %d ms" % (t_fin - t_inicio))

		# Clasificacion final
		var tabla = LeagueSystem.obtener_clasificacion(liga_test_id)
		print("\nCLASIFICACION FINAL:")
		print("%-3s %-20s %3s %3s %3s %3s %4s %4s %4s %4s" % ["Pos", "Equipo", "PJ", "PG", "PE", "PP", "GF", "GC", "GD", "Pts"])
		print("-".repeat(60))
		for i in range(mini(tabla.size(), 20)):
			var fila = tabla[i]
			var eq   = DB.obtener_equipo(fila.equipo_id)
			var nc   = eq.get("nombre_corto", "???")
			print("%-3d %-20s %3d %3d %3d %3d %4d %4d %4d %4d" % [
				i + 1, nc,
				fila.PJ, fila.PG, fila.PE, fila.PP,
				fila.GF, fila.GC, fila.GD, fila.Pts
			])

		# Goleadores
		print("\nMAXIMOS GOLEADORES (LaLiga):")
		var goleadores = LeagueSystem.obtener_max_goleadores(5)
		for i in range(goleadores.size()):
			var g = goleadores[i]
			print("  %d. %s — %d goles" % [i+1, g.get("nombre","?"), g.get("goles",0)])
	else:
		print("No se pudo inicializar la liga. Verificar equipos.")

	# ── Test 3: Simular TODAS las ligas ─────────────────────────────────────
	print("\n--- TEST 3: Todas las ligas ---")
	var t2 = Time.get_ticks_msec()
	LeagueSystem.inicializar_todas_las_ligas()
	LeagueSystem.simular_todas_las_ligas()
	var t3 = Time.get_ticks_msec()
	print("Todas las ligas simuladas en %d ms" % (t3 - t2))

	print("\n" + "=".repeat(50))
	print("  FASE 3 COMPLETADA")
	print("=".repeat(50))
