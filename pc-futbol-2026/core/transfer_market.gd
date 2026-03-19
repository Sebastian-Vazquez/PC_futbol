extends Node

## S10. TRANSFER MARKET SYSTEM
## Gestiona fichajes, préstamos y renovaciones de contrato.

signal oferta_enviada(comprador_id: int, vendedor_id: int, jugador_id: int, cantidad: int)
signal oferta_aceptada(comprador_id: int, vendedor_id: int, jugador_id: int, cantidad: int)
signal oferta_rechazada(comprador_id: int, jugador_id: int, razon: String)
signal fichaje_completado(jugador_id: int, origen_id: int, destino_id: int, cantidad: int)
signal prestamo_completado(jugador_id: int, origen_id: int, destino_id: int)
signal contrato_renovado(jugador_id: int, equipo_id: int, nuevo_salario: int)

# Ofertas pendientes: { jugador_id: { comprador_id, vendedor_id, cantidad, salario_ofertado } }
var _ofertas: Dictionary = {}
# Historial de traspasos de la temporada
var _historial: Array = []

func _ready() -> void:
	print("[TransferMarket] Inicializado")

# ─── Estado del mercado ───────────────────────────────────────────────────────

func esta_abierto() -> bool:
	return CalendarSystem.es_mercado_abierto()

# ─── Valoración ──────────────────────────────────────────────────────────────

func valor_traspaso(jugador_id: int) -> int:
	return DB.obtener_jugador(jugador_id).get("valor_mercado", 0)

func clausula_rescision(jugador_id: int) -> int:
	var j: Dictionary = DB.obtener_jugador(jugador_id)
	return j.get("contrato", {}).get("clausula", 0)

func salario_sugerido(jugador_id: int) -> int:
	## Estima el salario que pedirá el jugador según su valor.
	var valor: int = valor_traspaso(jugador_id)
	return maxi(500, int(valor * 0.0025))  # ~0.25% del valor por semana

# ─── Envío de ofertas ─────────────────────────────────────────────────────────

func enviar_oferta(comprador_id: int, jugador_id: int,
		cantidad: int, salario_ofertado: int = -1) -> Dictionary:
	var resultado := {"exito": false, "razon": ""}

	if not esta_abierto():
		resultado.razon = "mercado_cerrado"
		oferta_rechazada.emit(comprador_id, jugador_id, "Mercado cerrado")
		return resultado

	var jugador: Dictionary = DB.obtener_jugador(jugador_id)
	if jugador.is_empty():
		resultado.razon = "jugador_no_existe"
		return resultado

	var vendedor_id: int = int(jugador.get("equipo_id", -1))
	if vendedor_id == comprador_id:
		resultado.razon = "mismo_equipo"
		return resultado

	# Verificar presupuesto
	var comp_fin: Dictionary = DB.obtener_equipo(comprador_id).get("finanzas", {})
	if cantidad > comp_fin.get("presupuesto_fichajes", 0):
		resultado.razon = "presupuesto_insuficiente"
		oferta_rechazada.emit(comprador_id, jugador_id, "Presupuesto insuficiente")
		return resultado

	# Salario sugerido si no se especifica
	if salario_ofertado < 0:
		salario_ofertado = salario_sugerido(jugador_id)

	_ofertas[jugador_id] = {
		"comprador_id":     comprador_id,
		"vendedor_id":      vendedor_id,
		"cantidad":         cantidad,
		"salario_ofertado": salario_ofertado,
	}
	resultado.exito = true
	oferta_enviada.emit(comprador_id, vendedor_id, jugador_id, cantidad)
	return resultado

# ─── Decisión IA del club vendedor ───────────────────────────────────────────

func procesar_ofertas_ia() -> void:
	## Llamar periódicamente (ej. cada semana). La IA decide si acepta/rechaza.
	for jid in _ofertas.keys():
		_ia_evaluar_oferta(int(jid))

func _ia_evaluar_oferta(jugador_id: int) -> void:
	if not _ofertas.has(jugador_id): return
	var oferta: Dictionary = _ofertas[jugador_id]
	var valor: int = valor_traspaso(jugador_id)
	var umbral: int = int(valor * 0.85)

	if oferta.cantidad >= umbral:
		_ejecutar_traspaso(jugador_id, oferta)
		oferta_aceptada.emit(oferta.comprador_id, oferta.vendedor_id, jugador_id, oferta.cantidad)
	else:
		var razon: String = "Oferta %d insuficiente (minimo ~%d)" % [oferta.cantidad, umbral]
		oferta_rechazada.emit(oferta.comprador_id, jugador_id, razon)
		_ofertas.erase(jugador_id)

# ─── Activación por cláusula ──────────────────────────────────────────────────

func activar_clausula(comprador_id: int, jugador_id: int) -> Dictionary:
	var resultado := {"exito": false, "razon": ""}
	if not esta_abierto():
		resultado.razon = "mercado_cerrado"
		return resultado

	var jugador: Dictionary = DB.obtener_jugador(jugador_id)
	if jugador.is_empty():
		resultado.razon = "jugador_no_existe"
		return resultado

	var clausula: int = clausula_rescision(jugador_id)
	if clausula <= 0:
		resultado.razon = "sin_clausula"
		return resultado

	var comp_fin: Dictionary = DB.obtener_equipo(comprador_id).get("finanzas", {})
	if clausula > comp_fin.get("balance", 0):
		resultado.razon = "balance_insuficiente"
		return resultado

	var vendedor_id: int = int(jugador.get("equipo_id", -1))
	var salario: int = salario_sugerido(jugador_id)
	var oferta := {
		"comprador_id":     comprador_id,
		"vendedor_id":      vendedor_id,
		"cantidad":         clausula,
		"salario_ofertado": salario,
	}
	_ejecutar_traspaso(jugador_id, oferta)
	resultado.exito = true
	return resultado

# ─── Ejecución del traspaso ───────────────────────────────────────────────────

func _ejecutar_traspaso(jugador_id: int, oferta: Dictionary) -> void:
	var jugador:    Dictionary = DB.obtener_jugador(jugador_id)
	var comp_id:    int        = oferta.comprador_id
	var vend_id:    int        = oferta.vendedor_id
	var cantidad:   int        = oferta.cantidad
	var sal:        int        = oferta.salario_ofertado

	# Actualizar jugador
	jugador["equipo_id"] = comp_id
	jugador["contrato"]["salario_semanal"] = sal
	DB.actualizar_entidad("jugador", jugador_id, jugador)

	# Finanzas comprador
	var comp = DB.obtener_equipo(comp_id)
	var cfin: Dictionary = comp.get("finanzas", {}).duplicate()
	cfin["presupuesto_fichajes"]  = maxi(0, cfin.get("presupuesto_fichajes", 0) - cantidad)
	cfin["balance"]               = maxi(0, cfin.get("balance", 0) - cantidad)
	cfin["masa_salarial_semanal"] = cfin.get("masa_salarial_semanal", 0) + sal
	DB.actualizar_entidad("equipo", comp_id, {"finanzas": cfin})

	# Finanzas vendedor
	if vend_id > 0:
		var vend = DB.obtener_equipo(vend_id)
		var vfin: Dictionary = vend.get("finanzas", {}).duplicate()
		var sal_previo: int = jugador.get("contrato", {}).get("salario_semanal", 0)
		vfin["balance"]               = vfin.get("balance", 0) + cantidad
		vfin["presupuesto_fichajes"]  = vfin.get("presupuesto_fichajes", 0) + int(cantidad * 0.7)
		vfin["masa_salarial_semanal"] = maxi(0, vfin.get("masa_salarial_semanal", 0) - sal_previo)
		DB.actualizar_entidad("equipo", vend_id, {"finanzas": vfin})

	# Actualizar índices del DB
	_mover_jugador_indices(jugador_id, vend_id, comp_id)

	_historial.append({
		"jugador_id": jugador_id,
		"nombre":     jugador.get("nombre_corto", "?"),
		"media":      jugador.get("media", 0),
		"origen":     vend_id,
		"destino":    comp_id,
		"cantidad":   cantidad,
	})
	_ofertas.erase(jugador_id)
	fichaje_completado.emit(jugador_id, vend_id, comp_id, cantidad)

func _mover_jugador_indices(jugador_id: int, origen_id: int, destino_id: int) -> void:
	if DB.jugadores_por_equipo.has(origen_id):
		DB.jugadores_por_equipo[origen_id].erase(jugador_id)
	if not DB.jugadores_por_equipo.has(destino_id):
		DB.jugadores_por_equipo[destino_id] = []
	if not destino_id in DB.jugadores_por_equipo[destino_id]:
		DB.jugadores_por_equipo[destino_id].append(jugador_id)

# ─── Préstamos ────────────────────────────────────────────────────────────────

func prestar_jugador(jugador_id: int, origen_id: int,
		destino_id: int, semanas: int = 26) -> bool:
	var jugador: Dictionary = DB.obtener_jugador(jugador_id)
	if jugador.is_empty(): return false
	jugador["prestamo"] = {
		"equipo_propietario": origen_id,
		"equipo_destino":     destino_id,
		"semanas_restantes":  semanas,
	}
	jugador["equipo_id"] = destino_id
	DB.actualizar_entidad("jugador", jugador_id, jugador)
	_mover_jugador_indices(jugador_id, origen_id, destino_id)
	prestamo_completado.emit(jugador_id, origen_id, destino_id)
	return true

func devolver_prestamo(jugador_id: int) -> bool:
	var jugador: Dictionary = DB.obtener_jugador(jugador_id)
	if jugador.is_empty() or not jugador.has("prestamo"): return false
	var prestamo: Dictionary = jugador["prestamo"]
	var origen_id:  int = prestamo.get("equipo_propietario", -1)
	var destino_id: int = int(jugador.get("equipo_id", -1))
	if origen_id < 0: return false
	jugador["equipo_id"] = origen_id
	jugador.erase("prestamo")
	DB.actualizar_entidad("jugador", jugador_id, jugador)
	_mover_jugador_indices(jugador_id, destino_id, origen_id)
	return true

# ─── Agentes libres ───────────────────────────────────────────────────────────

func fichar_agente_libre(jugador_id: int, equipo_id: int, salario: int = -1) -> bool:
	var jugador: Dictionary = DB.obtener_jugador(jugador_id)
	if jugador.is_empty(): return false
	if int(jugador.get("equipo_id", -1)) != -1: return false
	if salario < 0:
		salario = salario_sugerido(jugador_id)
	jugador["equipo_id"] = equipo_id
	jugador["contrato"]["salario_semanal"] = salario
	DB.actualizar_entidad("jugador", jugador_id, jugador)
	_mover_jugador_indices(jugador_id, -1, equipo_id)
	DB.jugadores_libres.erase(jugador_id)
	fichaje_completado.emit(jugador_id, -1, equipo_id, 0)
	return true

# ─── Renovación de contrato ───────────────────────────────────────────────────

func renovar_contrato(jugador_id: int, equipo_id: int,
		nuevo_salario: int, anios: int = 3) -> bool:
	var jugador: Dictionary = DB.obtener_jugador(jugador_id)
	if jugador.is_empty(): return false
	if int(jugador.get("equipo_id", -1)) != equipo_id: return false
	var contrato: Dictionary = jugador.get("contrato", {}).duplicate()
	contrato["salario_semanal"] = nuevo_salario
	contrato["fin_contrato"]    = "%d-06-30" % (CalendarSystem.obtener_fecha_actual().anio + anios)
	jugador["contrato"] = contrato
	DB.actualizar_entidad("jugador", jugador_id, jugador)
	contrato_renovado.emit(jugador_id, equipo_id, nuevo_salario)
	return true

# ─── IA: generación automática de fichajes entre clubes ──────────────────────

func simular_actividad_mercado_ia(max_traspasos: int = 10) -> int:
	## Genera transferencias IA aleatorias. Devuelve cuántas se completaron.
	if not esta_abierto(): return 0
	var completados: int = 0
	var equipos_ids: Array = DB.equipos.keys()
	equipos_ids.shuffle()

	for eid in equipos_ids:
		if completados >= max_traspasos: break
		var equipo_id: int = int(eid)
		var fin: Dictionary = DB.obtener_equipo(equipo_id).get("finanzas", {})
		var presupuesto: int = fin.get("presupuesto_fichajes", 0)
		if presupuesto < 50_000: continue

		# Buscar un jugador que pueda comprar
		var max_valor: int = int(presupuesto * 0.6)
		if max_valor < 10_000: continue

		var candidatos: Array = []
		for jid in DB.jugadores:
			var j: Dictionary = DB.jugadores[jid]
			var jval: int = j.get("valor_mercado", 0)
			var jeid: int = int(j.get("equipo_id", -1))
			if jeid == equipo_id or jeid == -1: continue
			if jval <= max_valor and jval > 0:
				candidatos.append(jid)

		if candidatos.is_empty(): continue
		candidatos.shuffle()
		var target_id: int = int(candidatos[0])
		var valor: int = valor_traspaso(target_id)
		var oferta_cantidad: int = int(valor * randf_range(0.90, 1.10))

		var res := enviar_oferta(equipo_id, target_id, oferta_cantidad)
		if res.exito:
			_ia_evaluar_oferta(target_id)
			completados += 1

	return completados

# ─── Consultas ────────────────────────────────────────────────────────────────

func obtener_historial() -> Array:
	return _historial.duplicate()

func obtener_ofertas_pendientes() -> Dictionary:
	return _ofertas.duplicate()

func jugadores_en_el_mercado(precio_max: int = -1) -> Array:
	## Todos los jugadores con valor <= precio_max, no del equipo destino.
	var lista: Array = []
	for jid in DB.jugadores:
		var j: Dictionary = DB.jugadores[jid]
		if int(j.get("equipo_id", -1)) == -1: continue
		var val: int = j.get("valor_mercado", 0)
		if precio_max > 0 and val > precio_max: continue
		lista.append(j)
	lista.sort_custom(func(a, b): return a.get("valor_mercado", 0) > b.get("valor_mercado", 0))
	return lista
