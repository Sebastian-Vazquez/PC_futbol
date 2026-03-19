extends Node

## Escena de debug — Fase 4
## Prueba: economia + mercado de fichajes

func _ready() -> void:
	print("=".repeat(50))
	print("  PC FUTBOL 2026 -- FASE 4")
	print("=".repeat(50))

	DB.cargar_todo()
	print("Datos: %d jugadores | %d equipos | %d ligas" % [
		DB.jugadores.size(), DB.equipos.size(), DB.ligas.size()
	])

	if DB.equipos.size() < 2:
		print("ERROR: Sin equipos. Ejecuta el scraper primero.")
		return

	# ── Test 1: Economía semanal ────────────────────────────────────────────
	print("\n--- TEST 1: Economia semanal ---")
	CalendarSystem.iniciar_temporada(2026)

	# Simular 4 semanas de finanzas
	for sem in range(1, 5):
		EconomySystem.procesar_semana(sem)

	# Mostrar top 8 clubes más ricos
	var top = EconomySystem.top_ricos(8)
	print("TOP 8 CLUBES MAS RICOS (tras 4 semanas):")
	print("%-3s %-20s %15s" % ["Pos", "Club", "Balance"])
	print("-".repeat(40))
	for i in range(top.size()):
		var entry = top[i]
		print("%-3d %-20s %15s" % [
			i + 1,
			entry.nombre,
			_fmt_dinero(entry.balance)
		])

	# Informe detallado Real Madrid
	var eq_laliga = DB.equipos_por_liga.get(1, [])
	if eq_laliga.size() > 0:
		var rm_id: int = eq_laliga[0]
		var informe = EconomySystem.obtener_informe(rm_id)
		print("\nINFORME FINANCIERO — %s:" % informe.get("nombre", "?"))
		print("  Balance:            %s" % _fmt_dinero(informe.get("balance", 0)))
		print("  Deuda:              %s" % _fmt_dinero(informe.get("deuda", 0)))
		print("  Presup. fichajes:   %s" % _fmt_dinero(informe.get("presupuesto_fichajes", 0)))
		print("  Masa salarial/sem:  %s" % _fmt_dinero(informe.get("masa_salarial_semanal", 0)))
		print("  TV anual:           %s" % _fmt_dinero(informe.get("ingresos_tv_anual", 0)))
		print("  Ingreso por partido:%s" % _fmt_dinero(informe.get("ingreso_partido", 0)))
		print("  Ratio salarios:     %.1f%%" % EconomySystem.porcentaje_salarios_sobre_ingresos(rm_id))

	# ── Test 2: Mercado de fichajes IA ──────────────────────────────────────
	print("\n--- TEST 2: Mercado de fichajes (IA) ---")
	# Activar ventana de mercado verano (julio)
	CalendarSystem.dia = 15
	CalendarSystem.mes = 7
	CalendarSystem.anio = 2026
	print("Mercado abierto: %s" % str(TransferMarket.esta_abierto()))

	var completados = TransferMarket.simular_actividad_mercado_ia(15)
	print("Traspasos IA completados: %d" % completados)

	var historial = TransferMarket.obtener_historial()
	if historial.size() > 0:
		print("\nTRASPASOS REALIZADOS:")
		print("%-20s %5s %15s  %-18s -> %-18s" % ["Jugador", "Med", "Precio", "Origen", "Destino"])
		print("-".repeat(80))
		for t in historial:
			var orig_eq = DB.obtener_equipo(t.get("origen", 0))
			var dest_eq = DB.obtener_equipo(t.get("destino", 0))
			print("%-20s %5d %15s  %-18s -> %-18s" % [
				t.get("nombre", "?"),
				t.get("media", 0),
				_fmt_dinero(t.get("cantidad", 0)),
				orig_eq.get("nombre_corto", "?"),
				dest_eq.get("nombre_corto", "?"),
			])
	else:
		print("(Sin traspasos — los clubes no tienen presupuesto suficiente este periodo)")

	# ── Test 3: Fichar agente libre manualmente ─────────────────────────────
	print("\n--- TEST 3: Fichar agente libre ---")
	var libres = DB.obtener_agentes_libres({})
	if libres.size() > 0:
		var candidato = libres[0]
		var jid: int = int(candidato.get("id", 0))
		var dest_id: int = eq_laliga[0] if eq_laliga.size() > 0 else 1001
		var ok = TransferMarket.fichar_agente_libre(jid, dest_id)
		var dest_eq = DB.obtener_equipo(dest_id)
		print("Agente libre '%s' fichado por %s: %s" % [
			candidato.get("nombre_corto", "?"),
			dest_eq.get("nombre_corto", "?"),
			"OK" if ok else "FALLO"
		])
	else:
		print("No hay agentes libres disponibles")

	# ── Test 4: Renovación de contrato ──────────────────────────────────────
	print("\n--- TEST 4: Renovacion de contrato ---")
	if eq_laliga.size() > 0:
		var equipo_id: int = eq_laliga[0]
		var plantilla = DB.obtener_plantilla(equipo_id)
		if plantilla.size() > 0:
			var jugador = plantilla[0]
			var jid: int = int(jugador.get("id", 0))
			var sal_nuevo: int = int(jugador.get("contrato", {}).get("salario_semanal", 1000) * 1.15)
			var ok = TransferMarket.renovar_contrato(jid, equipo_id, sal_nuevo, 3)
			print("Renovacion de %s (+15%% salario): %s" % [
				jugador.get("nombre_corto", "?"),
				"OK" if ok else "FALLO"
			])
			var jugador_upd = DB.obtener_jugador(jid)
			print("  Nuevo salario: %s/semana" % _fmt_dinero(jugador_upd.get("contrato", {}).get("salario_semanal", 0)))
			print("  Fin contrato:  %s" % jugador_upd.get("contrato", {}).get("fin_contrato", "?"))

	print("\n" + "=".repeat(50))
	print("  FASE 4 COMPLETADA")
	print("=".repeat(50))

# ─── Helpers ──────────────────────────────────────────────────────────────────

func _fmt_dinero(cantidad: int) -> String:
	if cantidad >= 1_000_000_000:
		return "%.2fB" % (float(cantidad) / 1_000_000_000.0)
	if cantidad >= 1_000_000:
		return "%.2fM" % (float(cantidad) / 1_000_000.0)
	if cantidad >= 1_000:
		return "%.1fK" % (float(cantidad) / 1_000.0)
	return str(cantidad)
