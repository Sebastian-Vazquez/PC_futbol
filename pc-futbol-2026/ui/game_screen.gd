extends Control

## FASE 6 — UI DE GESTIÓN COMPLETA
## 7 tabs: Despacho · Plantilla · Tácticas · Mercado · Finanzas · Clasificación · Calendario

# ═══ COLORES ══════════════════════════════════════════════════════════════════
const C_BG      := Color(0.07, 0.09, 0.13)
const C_PANEL   := Color(0.10, 0.13, 0.19)
const C_PANEL2  := Color(0.13, 0.16, 0.23)
const C_HDR     := Color(0.06, 0.08, 0.12)
const C_BORDER  := Color(0.18, 0.24, 0.34)
const C_ACCENT  := Color(0.18, 0.52, 0.90)
const C_GREEN   := Color(0.20, 0.78, 0.35)
const C_RED     := Color(0.88, 0.25, 0.25)
const C_YELLOW  := Color(0.95, 0.80, 0.10)
const C_ORANGE  := Color(0.95, 0.55, 0.10)
const C_TEXT    := Color(0.90, 0.92, 0.95)
const C_DIM     := Color(0.50, 0.56, 0.66)
const C_CAMPO   := Color(0.14, 0.44, 0.14)
const C_CAMPO2  := Color(0.17, 0.50, 0.17)
const C_CHAMP   := Color(0.10, 0.35, 0.75)
const C_EUROPA  := Color(0.10, 0.60, 0.30)
const C_PROMO   := Color(0.70, 0.50, 0.10)
const C_RELEGA  := Color(0.70, 0.15, 0.15)

# ═══ TABS ══════════════════════════════════════════════════════════════════════
const TABS := ["despacho","plantilla","tactica","mercado","finanzas","clasificacion","calendario"]
const TAB_NAMES := {
	"despacho":      "Despacho",
	"plantilla":     "Plantilla",
	"tactica":       "Tácticas",
	"mercado":       "Mercado",
	"finanzas":      "Finanzas",
	"clasificacion": "Clasificación",
	"calendario":    "Calendario",
}

# ═══ FORMACIONES ══════════════════════════════════════════════════════════════
const FORMACIONES: Dictionary = {
	"4-4-2":   [[0.50,0.90],[0.12,0.70],[0.37,0.70],[0.63,0.70],[0.88,0.70],[0.12,0.47],[0.37,0.47],[0.63,0.47],[0.88,0.47],[0.35,0.20],[0.65,0.20]],
	"4-3-3":   [[0.50,0.90],[0.12,0.70],[0.37,0.70],[0.63,0.70],[0.88,0.70],[0.25,0.47],[0.50,0.47],[0.75,0.47],[0.20,0.18],[0.50,0.15],[0.80,0.18]],
	"4-2-3-1": [[0.50,0.90],[0.12,0.70],[0.37,0.70],[0.63,0.70],[0.88,0.70],[0.35,0.57],[0.65,0.57],[0.20,0.38],[0.50,0.36],[0.80,0.38],[0.50,0.15]],
	"4-1-4-1": [[0.50,0.90],[0.12,0.70],[0.37,0.70],[0.63,0.70],[0.88,0.70],[0.50,0.58],[0.12,0.40],[0.37,0.40],[0.63,0.40],[0.88,0.40],[0.50,0.16]],
	"3-5-2":   [[0.50,0.90],[0.25,0.70],[0.50,0.70],[0.75,0.70],[0.10,0.47],[0.30,0.47],[0.50,0.47],[0.70,0.47],[0.90,0.47],[0.35,0.18],[0.65,0.18]],
	"5-3-2":   [[0.50,0.90],[0.08,0.70],[0.28,0.70],[0.50,0.70],[0.72,0.70],[0.92,0.70],[0.25,0.47],[0.50,0.47],[0.75,0.47],[0.35,0.18],[0.65,0.18]],
	"4-5-1":   [[0.50,0.90],[0.12,0.70],[0.37,0.70],[0.63,0.70],[0.88,0.70],[0.10,0.47],[0.30,0.47],[0.50,0.47],[0.70,0.47],[0.90,0.47],[0.50,0.16]],
	"3-4-3":   [[0.50,0.90],[0.25,0.70],[0.50,0.70],[0.75,0.70],[0.15,0.47],[0.40,0.47],[0.60,0.47],[0.85,0.47],[0.20,0.16],[0.50,0.14],[0.80,0.16]],
}
const POSICIONES_FORM: Dictionary = {
	"4-4-2":   ["PO","LI","DFC","DFC","LD","MI","MC","MC","MD","DC","DC"],
	"4-3-3":   ["PO","LI","DFC","DFC","LD","MI","MC","MD","EI","DC","ED"],
	"4-2-3-1": ["PO","LI","DFC","DFC","LD","MCD","MCD","EI","MCO","ED","DC"],
	"4-1-4-1": ["PO","LI","DFC","DFC","LD","MC","EI","MCO","MCO","ED","DC"],
	"3-5-2":   ["PO","DFC","DFC","DFC","MI","MC","MCO","MC","MD","DC","DC"],
	"5-3-2":   ["PO","LI","DFC","DFC","DFC","LD","MI","MC","MD","DC","DC"],
	"4-5-1":   ["PO","LI","DFC","DFC","LD","MI","MC","MCO","MC","MD","DC"],
	"3-4-3":   ["PO","DFC","DFC","DFC","MI","MCD","MCO","MD","EI","DC","ED"],
}

# ═══ ESTADO ═══════════════════════════════════════════════════════════════════
var _eq_id:         int    = -1
var _liga_id:       int    = -1
var _sem:           int    = 0
var _hist:          Array  = []
var _tab_activa:    String = "despacho"
var _formacion:     String = "4-3-3"
var _titulares:     Array  = []   # [jugador_id x11]
var _noticias:      Array  = []
var _mercado_pos:   String = "TODOS"
var _mercado_valor: int    = 0
var _confianza:     int    = 70
var _sueldo_mgr:    int    = 0
var _reputacion:    int    = 50
var _capitan_id:    int    = -1
var _pateador_id:   int    = -1
var _temporada:     int    = 2026

# ═══ NODOS UI ══════════════════════════════════════════════════════════════════
var _lbl_club:    Label
var _lbl_fecha:   Label
var _lbl_balance: Label
var _lbl_pos:     Label
var _bodies:      Dictionary = {}
var _scrolls:     Dictionary = {}
var _tab_btns:    Dictionary = {}
var _fondos:      Dictionary = {}   # key -> TextureRect (fondo de pestaña)
var _content_area: Control
var _menu_root:   Control
var _selector_root: Control
var _sel_opt:     OptionButton
var _sel_vb:      VBoxContainer

const SAVE_PATH := "user://ft2026_save.json"

# ══════════════════════════════════════════════════════════════════════════════
# READY
# ══════════════════════════════════════════════════════════════════════════════

func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	DB.cargar_todo()
	_mostrar_menu_principal()

# ══════════════════════════════════════════════════════════════════════════════
# MENÚ PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

func _mostrar_menu_principal() -> void:
	_menu_root = Control.new()
	_menu_root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(_menu_root)

	# ── Fondo portada ────────────────────────────────────────────────────────
	var bg := TextureRect.new()
	bg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	bg.stretch_mode = TextureRect.STRETCH_COVER
	var tex := load("res://assets/backgrounds/portada_final.jpg")
	if tex:
		bg.texture = tex
	else:
		var cr := ColorRect.new()
		cr.color = C_BG
		cr.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		_menu_root.add_child(cr)
	_menu_root.add_child(bg)

	# ── Overlay oscuro general ────────────────────────────────────────────────
	var ov := ColorRect.new()
	ov.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	ov.color = Color(0.0, 0.01, 0.05, 0.52)
	_menu_root.add_child(ov)

	# ── Layout principal ─────────────────────────────────────────────────────
	var vb := VBoxContainer.new()
	vb.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	vb.add_theme_constant_override("separation", 0)
	_menu_root.add_child(vb)

	# Espacio superior
	var sp_top := Control.new()
	sp_top.size_flags_vertical = Control.SIZE_EXPAND_FILL
	sp_top.size_flags_stretch_ratio = 0.8
	vb.add_child(sp_top)

	# ── Título ───────────────────────────────────────────────────────────────
	var title_c := CenterContainer.new()
	vb.add_child(title_c)
	var title_vb := VBoxContainer.new()
	title_vb.add_theme_constant_override("separation", 6)
	title_c.add_child(title_vb)

	var title := Label.new()
	title.text = "FÚTBOL TYCOON 2026"
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.add_theme_font_size_override("font_size", 70)
	title.add_theme_color_override("font_color", Color(0.96, 0.97, 1.0))
	title.add_theme_color_override("font_outline_color", Color(0.05, 0.15, 0.45, 0.95))
	title.add_theme_constant_override("outline_size", 4)
	title.add_theme_color_override("font_shadow_color", Color(0.0, 0.0, 0.0, 0.85))
	title.add_theme_constant_override("shadow_offset_x", 3)
	title.add_theme_constant_override("shadow_offset_y", 4)
	title_vb.add_child(title)

	var sub := Label.new()
	sub.text = "EL CLÁSICO DEL FÚTBOL MANAGER"
	sub.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	sub.add_theme_font_size_override("font_size", 15)
	sub.add_theme_color_override("font_color", Color(0.72, 0.82, 1.0, 0.88))
	sub.add_theme_color_override("font_outline_color", Color(0, 0, 0, 0.7))
	sub.add_theme_constant_override("outline_size", 2)
	title_vb.add_child(sub)

	# Separador decorativo
	var sep_c := CenterContainer.new()
	vb.add_child(sep_c)
	var sep_line := ColorRect.new()
	sep_line.custom_minimum_size = Vector2(380, 2)
	sep_line.color = Color(0.35, 0.55, 0.90, 0.6)
	sep_c.add_child(sep_line)

	# Espacio
	var sp_mid := Control.new()
	sp_mid.custom_minimum_size = Vector2(0, 28)
	vb.add_child(sp_mid)

	# ── Botones ──────────────────────────────────────────────────────────────
	var btn_c := CenterContainer.new()
	vb.add_child(btn_c)
	var btn_vb := VBoxContainer.new()
	btn_vb.add_theme_constant_override("separation", 14)
	btn_c.add_child(btn_vb)

	var btn1 := _btn_metalico("⚽   INICIAR NUEVA PARTIDA")
	btn1.pressed.connect(_menu_iniciar_nueva)
	btn_vb.add_child(btn1)

	var btn2 := _btn_metalico("💾   CARGAR PARTIDA")
	btn2.pressed.connect(_cargar_partida_menu)
	if not FileAccess.file_exists(SAVE_PATH):
		btn2.disabled = true
		btn2.modulate = Color(1, 1, 1, 0.45)
	btn_vb.add_child(btn2)

	var btn3 := _btn_metalico("📋   BASE DE DATOS")
	btn3.pressed.connect(_menu_base_datos)
	btn_vb.add_child(btn3)

	# Espacio inferior
	var sp_bot := Control.new()
	sp_bot.size_flags_vertical = Control.SIZE_EXPAND_FILL
	sp_bot.size_flags_stretch_ratio = 1.2
	vb.add_child(sp_bot)

	# ── Footer ────────────────────────────────────────────────────────────────
	var footer_bg := ColorRect.new()
	footer_bg.custom_minimum_size = Vector2(0, 52)
	footer_bg.color = Color(0.0, 0.02, 0.06, 0.82)
	vb.add_child(footer_bg)

	var footer_mg := MarginContainer.new()
	footer_mg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_set_margins(footer_mg, 0, 6, 0, 6)
	footer_bg.add_child(footer_mg)

	var footer_vb := VBoxContainer.new()
	footer_vb.add_theme_constant_override("separation", 2)
	footer_vb.alignment = BoxContainer.ALIGNMENT_CENTER
	footer_mg.add_child(footer_vb)

	var f1 := Label.new()
	f1.text = "BY NEURAL AETHER  ·  MADE WITH GODOT ENGINE"
	f1.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	f1.add_theme_font_size_override("font_size", 11)
	f1.add_theme_color_override("font_color", Color(0.75, 0.82, 1.0, 0.90))
	footer_vb.add_child(f1)

	var f2 := Label.new()
	f2.text = "© 2026 Neural Aether · Todos los derechos reservados"
	f2.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	f2.add_theme_font_size_override("font_size", 10)
	f2.add_theme_color_override("font_color", Color(0.48, 0.54, 0.66, 0.75))
	footer_vb.add_child(f2)


func _btn_metalico(texto: String) -> Button:
	var btn := Button.new()
	btn.text = texto
	btn.custom_minimum_size = Vector2(420, 62)
	btn.alignment = HORIZONTAL_ALIGNMENT_CENTER

	# Estado normal — gris metalizado con sombra profunda
	var sn := StyleBoxFlat.new()
	sn.bg_color          = Color(0.36, 0.39, 0.44)
	sn.set_border_width_all(2)
	sn.border_color      = Color(0.62, 0.66, 0.74)
	sn.border_width_top  = 3   # highlight superior (borde más brillante arriba)
	sn.set_corner_radius_all(6)
	sn.shadow_color      = Color(0.0, 0.0, 0.0, 0.70)
	sn.shadow_size       = 8
	sn.shadow_offset     = Vector2(2, 5)
	sn.expand_margin_bottom = 4
	btn.add_theme_stylebox_override("normal", sn)

	# Hover — más luminoso
	var sh := sn.duplicate() as StyleBoxFlat
	sh.bg_color      = Color(0.46, 0.50, 0.57)
	sh.border_color  = Color(0.80, 0.86, 0.96)
	sh.shadow_size   = 12
	sh.shadow_color  = Color(0.0, 0.0, 0.0, 0.80)
	btn.add_theme_stylebox_override("hover", sh)

	# Pressed — hundido
	var sp := sn.duplicate() as StyleBoxFlat
	sp.bg_color          = Color(0.28, 0.31, 0.35)
	sp.border_color      = Color(0.42, 0.45, 0.52)
	sp.shadow_size       = 2
	sp.shadow_offset     = Vector2(0, 1)
	sp.expand_margin_bottom = 0
	btn.add_theme_stylebox_override("pressed", sp)

	# Focus (sin recuadro molesto)
	btn.add_theme_stylebox_override("focus", sn.duplicate())

	# Texto
	btn.add_theme_font_size_override("font_size", 21)
	btn.add_theme_color_override("font_color",         Color(0.93, 0.95, 0.99))
	btn.add_theme_color_override("font_hover_color",   Color(1.00, 1.00, 1.00))
	btn.add_theme_color_override("font_pressed_color", Color(0.78, 0.82, 0.92))
	btn.add_theme_color_override("font_outline_color", Color(0.0, 0.0, 0.0, 0.55))
	btn.add_theme_constant_override("outline_size", 1)
	return btn


func _menu_iniciar_nueva() -> void:
	if _menu_root:
		_menu_root.queue_free()
		_menu_root = null
	_mostrar_selector()


func _menu_base_datos() -> void:
	push_warning("Base de datos: por implementar")


# ── GUARDAR / CARGAR ─────────────────────────────────────────────────────────

func _guardar_partida() -> void:
	var data := {
		"version":    1,
		"eq_id":      _eq_id,
		"liga_id":    _liga_id,
		"sem":        _sem,
		"temporada":  _temporada,
		"formacion":  _formacion,
		"titulares":  _titulares,
		"confianza":  _confianza,
		"sueldo_mgr": _sueldo_mgr,
		"reputacion": _reputacion,
	}
	var f := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if f:
		f.store_string(JSON.stringify(data, "\t"))
		f.close()
		_mostrar_notif_guardado()
	else:
		push_error("No se pudo guardar la partida en " + SAVE_PATH)


func _mostrar_notif_guardado() -> void:
	var lbl := Label.new()
	lbl.text = "✔ Partida guardada"
	lbl.add_theme_font_size_override("font_size", 14)
	lbl.add_theme_color_override("font_color", C_GREEN)
	lbl.position = Vector2(get_viewport_rect().size.x - 220, 8)
	add_child(lbl)
	var tw := create_tween()
	tw.tween_property(lbl, "modulate:a", 0.0, 1.8).set_delay(1.5)
	tw.tween_callback(lbl.queue_free)


func _cargar_partida_menu() -> void:
	if not FileAccess.file_exists(SAVE_PATH):
		return
	var f := FileAccess.open(SAVE_PATH, FileAccess.READ)
	if not f:
		return
	var parsed := JSON.parse_string(f.get_as_text())
	f.close()
	if not parsed is Dictionary:
		return
	var d: Dictionary = parsed
	_eq_id      = int(d.get("eq_id",      -1))
	_liga_id    = int(d.get("liga_id",    -1))
	_sem        = int(d.get("sem",         0))
	_temporada  = int(d.get("temporada", 2026))
	_formacion  = str(d.get("formacion", "4-3-3"))
	_confianza  = int(d.get("confianza",  70))
	_sueldo_mgr = int(d.get("sueldo_mgr", 10000))
	_reputacion = int(d.get("reputacion", 50))
	var tit_raw = d.get("titulares", [])
	_titulares = []
	for v in tit_raw:
		_titulares.append(int(v))
	if _eq_id < 0 or _liga_id < 0:
		return
	CalendarSystem.iniciar_temporada(_temporada)
	LeagueSystem.inicializar_todas_las_ligas()
	if _titulares.is_empty():
		_inicializar_titulares()
	if _menu_root:
		_menu_root.queue_free()
		_menu_root = null
	_construir_juego()


# ══════════════════════════════════════════════════════════════════════════════
# SELECTOR DE EQUIPO
# ══════════════════════════════════════════════════════════════════════════════

func _mostrar_selector() -> void:
	var cr := ColorRect.new()
	cr.color = C_BG
	_selector_root = cr
	_selector_root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(_selector_root)

	var center := CenterContainer.new()
	center.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_selector_root.add_child(center)

	var vb := VBoxContainer.new()
	vb.custom_minimum_size = Vector2(560, 0)
	vb.add_theme_constant_override("separation", 10)
	center.add_child(vb)

	var title := _mk_lbl("PC FÚTBOL 2026", 32, true)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.add_theme_color_override("font_color", C_ACCENT)
	vb.add_child(title)

	var sub := _mk_lbl("Elige tu equipo y comienza tu carrera como mánager", 13)
	sub.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	sub.add_theme_color_override("font_color", C_DIM)
	vb.add_child(sub)

	vb.add_child(_mk_sep())

	# Liga selector
	var hb_liga := HBoxContainer.new()
	hb_liga.add_theme_constant_override("separation", 10)
	vb.add_child(hb_liga)
	var lbl_liga := _mk_lbl("Liga:", 13, true)
	lbl_liga.custom_minimum_size = Vector2(60, 0)
	hb_liga.add_child(lbl_liga)
	_sel_opt = OptionButton.new()
	_sel_opt.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	hb_liga.add_child(_sel_opt)
	for lid in DB.ligas:
		var liga: Dictionary = DB.ligas[lid]
		_sel_opt.add_item(liga.get("nombre", str(lid)), int(lid))
	_sel_opt.item_selected.connect(_on_liga_sel)

	# Team list
	var sc := ScrollContainer.new()
	sc.custom_minimum_size = Vector2(560, 380)
	vb.add_child(sc)
	_sel_vb = VBoxContainer.new()
	_sel_vb.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_sel_vb.add_theme_constant_override("separation", 3)
	sc.add_child(_sel_vb)

	if DB.ligas.size() > 0:
		_on_liga_sel(0)

func _on_liga_sel(idx: int) -> void:
	var liga_id: int = _sel_opt.get_item_id(idx)
	for c in _sel_vb.get_children():
		c.queue_free()
	var equipos_ids: Array = DB.equipos_por_liga.get(liga_id, [])
	var equipos_data: Array = []
	for eid in equipos_ids:
		var eq: Dictionary = DB.obtener_equipo(int(eid))
		if not eq.is_empty():
			equipos_data.append(eq)
	equipos_data.sort_custom(func(a, b): return a.get("reputacion", 0) > b.get("reputacion", 0))
	for eq in equipos_data:
		var eid: int = int(eq.get("id", 0))
		var rep: int = eq.get("reputacion", 0)
		var bal: int = eq.get("finanzas", {}).get("balance", 0)
		var txt := "%-22s  Rep:%d  %s" % [eq.get("nombre_corto","?"), rep, _fmt_m(bal)]
		var btn := Button.new()
		btn.text = txt
		btn.alignment = HORIZONTAL_ALIGNMENT_LEFT
		btn.custom_minimum_size = Vector2(540, 32)
		_estilo_btn(btn, C_PANEL)
		btn.pressed.connect(_comenzar.bind(eid, liga_id))
		_sel_vb.add_child(btn)

func _comenzar(equipo_id: int, liga_id: int) -> void:
	var eq: Dictionary = DB.obtener_equipo(equipo_id)
	if eq.is_empty():
		return
	_eq_id   = equipo_id
	_liga_id = liga_id
	CalendarSystem.iniciar_temporada(2026)
	LeagueSystem.inicializar_todas_las_ligas()
	_sem = CalendarSystem.obtener_semana_actual()
	_hist.clear()
	_noticias.clear()
	_sueldo_mgr = int(eq.get("reputacion", 50)) * 500 + 5000
	_reputacion  = 50
	_confianza   = 70
	_inicializar_titulares()
	_selector_root.queue_free()
	_construir_juego()

# ══════════════════════════════════════════════════════════════════════════════
# UI PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

func _construir_juego() -> void:
	var bg := ColorRect.new()
	bg.color = C_BG
	bg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(bg)

	var root_vb := VBoxContainer.new()
	root_vb.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	root_vb.add_theme_constant_override("separation", 0)
	add_child(root_vb)

	root_vb.add_child(_build_hud())
	root_vb.add_child(_build_nav())
	_content_area = _build_content_area()
	root_vb.add_child(_content_area)

	_refresh_all()
	_mostrar_tab("despacho")

func _build_hud() -> Control:
	var hud := ColorRect.new()
	hud.color = C_HDR
	hud.custom_minimum_size = Vector2(0, 52)

	var mg := MarginContainer.new()
	mg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_set_margins(mg, 12, 6, 12, 6)
	hud.add_child(mg)

	var hb := HBoxContainer.new()
	hb.add_theme_constant_override("separation", 16)
	mg.add_child(hb)

	_lbl_club = _mk_lbl("---", 15, true)
	_lbl_club.add_theme_color_override("font_color", C_ACCENT)
	hb.add_child(_lbl_club)

	var sep1 := VSeparator.new()
	hb.add_child(sep1)

	_lbl_fecha = _mk_lbl("---", 12)
	_lbl_fecha.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	hb.add_child(_lbl_fecha)

	_lbl_balance = _mk_lbl("---", 13, true)
	hb.add_child(_lbl_balance)

	var sep2 := VSeparator.new()
	hb.add_child(sep2)

	_lbl_pos = _mk_lbl("---", 12)
	hb.add_child(_lbl_pos)

	var sep3 := VSeparator.new()
	hb.add_child(sep3)

	var btn_av := Button.new()
	btn_av.text = "▶  Avanzar Semana"
	btn_av.custom_minimum_size = Vector2(160, 36)
	_estilo_btn(btn_av, C_ACCENT)
	btn_av.pressed.connect(_on_avanzar_semana)
	hb.add_child(btn_av)

	var sep4 := VSeparator.new()
	hb.add_child(sep4)

	var btn_save := Button.new()
	btn_save.text = "💾 Guardar"
	btn_save.custom_minimum_size = Vector2(110, 36)
	_estilo_btn(btn_save, Color(0.25, 0.45, 0.25))
	btn_save.pressed.connect(_guardar_partida)
	hb.add_child(btn_save)

	return hud

func _build_nav() -> Control:
	var nav := ColorRect.new()
	nav.color = C_HDR
	nav.custom_minimum_size = Vector2(0, 38)

	var hb := HBoxContainer.new()
	hb.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	hb.add_theme_constant_override("separation", 0)
	nav.add_child(hb)

	for key in TABS:
		var btn := Button.new()
		btn.text = TAB_NAMES[key]
		btn.custom_minimum_size = Vector2(0, 38)
		btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		_estilo_btn_nav(btn, false)
		btn.pressed.connect(_mostrar_tab.bind(key))
		_tab_btns[key] = btn
		hb.add_child(btn)

	return nav

func _build_content_area() -> Control:
	var area := Control.new()
	area.size_flags_vertical = Control.SIZE_EXPAND_FILL
	area.size_flags_horizontal = Control.SIZE_EXPAND_FILL

	for key in TABS:
		var sc := ScrollContainer.new()
		sc.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		sc.visible = false

		var mg := MarginContainer.new()
		mg.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		_set_margins(mg, 18, 14, 18, 14)
		sc.add_child(mg)

		var vb := VBoxContainer.new()
		vb.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		vb.add_theme_constant_override("separation", 8)
		mg.add_child(vb)

		_scrolls[key] = sc
		_bodies[key]  = vb
		area.add_child(sc)

		# Fondo DESPUÉS de añadir al árbol para que get_parent() funcione.
		# Se añade al área padre, NO al ScrollContainer (si no se scrollea).
		_cargar_fondo_tab(area, key)

	return area

func _mostrar_tab(key: String) -> void:
	_tab_activa = key
	for k in _scrolls:
		(_scrolls[k] as ScrollContainer).visible = (k == key)
	for k in _tab_btns:
		_estilo_btn_nav(_tab_btns[k] as Button, k == key)
	for k in _fondos:
		(_fondos[k] as TextureRect).visible = (k == key)

# ══════════════════════════════════════════════════════════════════════════════
# HUD UPDATE
# ══════════════════════════════════════════════════════════════════════════════

func _update_hud() -> void:
	var eq: Dictionary = DB.obtener_equipo(_eq_id)
	_lbl_club.text = eq.get("nombre_corto", "?") as String
	var fecha: Dictionary = CalendarSystem.obtener_fecha_actual()
	var dia: int = fecha.get("dia", 1)
	var mes: int = fecha.get("mes", 1)
	var anio: int = fecha.get("anio", 2026)
	var meses: Array = ["","Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
	var mes_str: String = meses[mes] if mes >= 1 and mes <= 12 else "?"
	_lbl_fecha.text = "%d %s %d  —  Semana %d" % [dia, mes_str, anio, _sem]
	var bal: int = eq.get("finanzas", {}).get("balance", 0)
	var c_bal: Color = C_GREEN if bal >= 0 else C_RED
	_lbl_balance.text = _fmt_m(bal)
	_lbl_balance.add_theme_color_override("font_color", c_bal)
	var pos: int = _posicion_liga()
	_lbl_pos.text = "Posición: %s" % (str(pos) + "°" if pos > 0 else "--")

# ══════════════════════════════════════════════════════════════════════════════
# PANEL: DESPACHO
# ══════════════════════════════════════════════════════════════════════════════

func _refresh_despacho() -> void:
	_clear_body("despacho")
	var vb: VBoxContainer = _bodies["despacho"]
	var eq: Dictionary = DB.obtener_equipo(_eq_id)

	vb.add_child(_mk_titulo("DESPACHO DEL MÁNAGER"))

	# ── Fila superior: 3 cards ──────────────────────────────────────────────
	var hb_cards := HBoxContainer.new()
	hb_cards.add_theme_constant_override("separation", 10)
	vb.add_child(hb_cards)

	var pos: int = _posicion_liga()
	var bal: int = eq.get("finanzas", {}).get("balance", 0)
	var pj: int = _hist.size()
	var pg: int = 0
	var pe: int = 0
	var pp: int = 0
	for r in _hist:
		var gl: int = r.get("goles_local", 0)
		var gv: int = r.get("goles_visitante", 0)
		var es_local: bool = int(r.get("local_id", 0)) == _eq_id
		if gl == gv:
			pe += 1
		elif (es_local and gl > gv) or (not es_local and gv > gl):
			pg += 1
		else:
			pp += 1

	hb_cards.add_child(_mk_card("POSICIÓN", str(pos) + "°" if pos > 0 else "--", C_ACCENT))
	hb_cards.add_child(_mk_card("BALANCE", _fmt_m(bal), C_GREEN if bal >= 0 else C_RED))
	var racha_txt: String = str(pg) + "V " + str(pe) + "E " + str(pp) + "D"
	hb_cards.add_child(_mk_card("TEMPORADA", racha_txt, C_TEXT))
	hb_cards.add_child(_mk_card("SUELDO MÁN.", _fmt_m(_sueldo_mgr) + "/sem", C_YELLOW))

	vb.add_child(_mk_sep())

	# ── Confianza directiva ─────────────────────────────────────────────────
	vb.add_child(_mk_seccion("CONFIANZA DE LA DIRECTIVA"))
	_confianza = _calcular_confianza()
	var hb_conf := HBoxContainer.new()
	hb_conf.add_theme_constant_override("separation", 10)
	vb.add_child(hb_conf)
	var lbl_conf := _mk_lbl("%d%%" % _confianza, 15, true)
	var c_conf: Color = C_GREEN if _confianza >= 70 else (C_YELLOW if _confianza >= 40 else C_RED)
	lbl_conf.add_theme_color_override("font_color", c_conf)
	lbl_conf.custom_minimum_size = Vector2(55, 0)
	hb_conf.add_child(lbl_conf)
	var barra_bg := ColorRect.new()
	barra_bg.color = C_PANEL2
	barra_bg.custom_minimum_size = Vector2(300, 18)
	hb_conf.add_child(barra_bg)
	var barra_fill := ColorRect.new()
	barra_fill.color = c_conf
	barra_fill.custom_minimum_size = Vector2(int(3.0 * float(_confianza)), 18)
	barra_bg.add_child(barra_fill)
	var lbl_estado: String
	if _confianza >= 80:
		lbl_estado = "Excelente — La directiva confía plenamente en tu gestión"
	elif _confianza >= 60:
		lbl_estado = "Buena — Sigues contando con el apoyo de la directiva"
	elif _confianza >= 40:
		lbl_estado = "Regular — La directiva empieza a cuestionar tus resultados"
	else:
		lbl_estado = "¡CRISIS! — Tu puesto está en peligro"
	var lbl_e := _mk_lbl(lbl_estado, 11)
	lbl_e.add_theme_color_override("font_color", c_conf)
	vb.add_child(lbl_e)

	vb.add_child(_mk_sep())

	# ── Objetivos de temporada ──────────────────────────────────────────────
	vb.add_child(_mk_seccion("OBJETIVOS DE TEMPORADA"))
	var obj_data: Array = _generar_objetivos(eq)
	for o in obj_data:
		var cumplido: bool = o.get("cumplido", false)
		var icono: String = "✓ " if cumplido else "○ "
		var l := _mk_lbl(icono + o.get("texto", ""), 13)
		l.add_theme_color_override("font_color", C_GREEN if cumplido else C_TEXT)
		vb.add_child(l)

	vb.add_child(_mk_sep())

	# ── Próximo partido ─────────────────────────────────────────────────────
	vb.add_child(_mk_seccion("PRÓXIMO PARTIDO"))
	var proxima: Array = LeagueSystem.obtener_proxima_jornada(_liga_id)
	var jor_num: int = LeagueSystem.jornada_actual(_liga_id) + 1
	var encontrado: bool = false
	for p in proxima:
		if int(p.get("local", 0)) == _eq_id or int(p.get("visitante", 0)) == _eq_id:
			var eql: Dictionary = DB.obtener_equipo(int(p.get("local", 0)))
			var eqv: Dictionary = DB.obtener_equipo(int(p.get("visitante", 0)))
			var txt_p: String = "Jornada %d  —  %s  vs  %s" % [
				jor_num,
				eql.get("nombre_corto", "?"),
				eqv.get("nombre_corto", "?"),
			]
			var lp := _mk_lbl(txt_p, 14, true)
			lp.add_theme_color_override("font_color", C_ACCENT)
			vb.add_child(lp)
			encontrado = true
			break
	if not encontrado:
		vb.add_child(_mk_lbl("Temporada finalizada", 13))

	vb.add_child(_mk_sep())

	# ── Últimos resultados ──────────────────────────────────────────────────
	vb.add_child(_mk_seccion("ÚLTIMOS RESULTADOS"))
	if _hist.is_empty():
		vb.add_child(_mk_lbl("Sin partidos jugados aún.", 12))
	else:
		var recientes: Array = _hist.slice(max(0, _hist.size() - 5), _hist.size())
		recientes.reverse()
		for r in recientes:
			var eql: Dictionary = DB.obtener_equipo(int(r.get("local_id", 0)))
			var eqv: Dictionary = DB.obtener_equipo(int(r.get("visitante_id", 0)))
			var gl: int = r.get("goles_local", 0)
			var gv: int = r.get("goles_visitante", 0)
			var es_local: bool = int(r.get("local_id", 0)) == _eq_id
			var gano: bool  = (es_local and gl > gv) or (not es_local and gv > gl)
			var empate: bool = gl == gv
			var cr: Color = C_GREEN if gano else (C_YELLOW if empate else C_RED)
			var res_txt: String = "  %s  %d – %d  %s" % [
				eql.get("nombre_corto","?"), gl, gv, eqv.get("nombre_corto","?")
			]
			var l := _mk_lbl(res_txt, 13)
			l.add_theme_color_override("font_color", cr)
			vb.add_child(l)

	vb.add_child(_mk_sep())

	# ── Noticias ────────────────────────────────────────────────────────────
	vb.add_child(_mk_seccion("NOTICIAS RECIENTES"))
	if _noticias.is_empty():
		vb.add_child(_mk_lbl("No hay noticias. Avanza una semana para empezar.", 12))
	else:
		var ultimas: Array = _noticias.slice(max(0, _noticias.size() - 6), _noticias.size())
		ultimas.reverse()
		for n in ultimas:
			var l := _mk_lbl("• " + str(n), 12)
			l.add_theme_color_override("font_color", C_DIM)
			l.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
			vb.add_child(l)

	vb.add_child(_mk_sep())

	# ── Info del club ───────────────────────────────────────────────────────
	vb.add_child(_mk_seccion("PERFIL DEL CLUB"))
	var estadio: Dictionary = eq.get("estadio", {})
	var grid := GridContainer.new()
	grid.columns = 4
	grid.add_theme_constant_override("h_separation", 24)
	grid.add_theme_constant_override("v_separation", 5)
	vb.add_child(grid)
	var info_data: Array = [
		["País", eq.get("pais", "?")],
		["Reputación", str(eq.get("reputacion", 0)) + "/100"],
		["Estadio", estadio.get("nombre", "?")],
		["Aforo", str(estadio.get("capacidad", 0))],
		["Nivel médico", str(eq.get("nivel_medicina", 0)) + "/5"],
		["Nivel cantera", str(eq.get("nivel_cantera", 0)) + "/5"],
		["Ojeadores", str(eq.get("nivel_ojeadores", 0)) + " asignados"],
		["Tu sueldo", _fmt_m(_sueldo_mgr) + "/sem"],
	]
	for pair in info_data:
		var lk := _mk_lbl(str(pair[0]), 11)
		lk.add_theme_color_override("font_color", C_DIM)
		grid.add_child(lk)
		var lv := _mk_lbl(str(pair[1]), 12, true)
		grid.add_child(lv)

# ══════════════════════════════════════════════════════════════════════════════
# PANEL: PLANTILLA
# ══════════════════════════════════════════════════════════════════════════════

func _refresh_plantilla() -> void:
	_clear_body("plantilla")
	var vb: VBoxContainer = _bodies["plantilla"]
	var eq: Dictionary = DB.obtener_equipo(_eq_id)

	vb.add_child(_mk_titulo("PLANTILLA — %s" % eq.get("nombre_corto", "?")))

	var plantilla: Array = DB.obtener_plantilla(_eq_id)
	if plantilla.is_empty():
		vb.add_child(_mk_lbl("Plantilla vacía.", 12))
		return

	# Ordenar por posición + media
	var orden: Dictionary = {
		"PO":0,"LD":1,"DFC":1,"LI":1,"MCD":2,"MC":2,"MCO":2,"EI":3,"ED":3,"DC":4
	}
	plantilla.sort_custom(func(a, b):
		var pa: int = orden.get(a.get("posicion_principal",""), 5)
		var pb: int = orden.get(b.get("posicion_principal",""), 5)
		if pa != pb:
			return pa < pb
		return a.get("media", 0) > b.get("media", 0)
	)

	# Stats de plantilla
	var total: int = plantilla.size()
	var masa: int = eq.get("finanzas", {}).get("masa_salarial_semanal", 0)
	var hb_stats := HBoxContainer.new()
	hb_stats.add_theme_constant_override("separation", 20)
	vb.add_child(hb_stats)
	hb_stats.add_child(_mk_card("JUGADORES", str(total), C_TEXT))
	hb_stats.add_child(_mk_card("MASA SALARIAL", _fmt_m(masa) + "/sem", C_RED))
	var media_pl: float = 0.0
	for j in plantilla:
		media_pl += float(j.get("media", 0))
	if total > 0:
		media_pl = media_pl / float(total)
	hb_stats.add_child(_mk_card("MEDIA PLANTILLA", "%.1f" % media_pl, C_ACCENT))

	vb.add_child(_mk_sep())

	# Cabecera tabla
	vb.add_child(_mk_fila_tabla(["Pos","Jugador","Nac","Edad","Med","Pot","Forma","Valor","Salario/sem","Contrato",""], true, [44,170,40,38,38,38,52,80,90,70,100]))
	vb.add_child(_mk_sep())

	var anio_actual: int = CalendarSystem.obtener_fecha_actual().anio
	for j in plantilla:
		var edad: int     = _calcular_edad(j.get("fecha_nacimiento", ""))
		var fin_c: String = j.get("contrato", {}).get("fin_contrato", "?")
		var anio_fin: String = fin_c.split("-")[0] if "-" in fin_c else fin_c
		var sal: int      = j.get("contrato", {}).get("salario_semanal", 0)
		var val: int      = j.get("valor_mercado", 0)
		var forma: int    = j.get("forma_fisica", 75)
		var pot: int      = j.get("potencial", 0)
		var c_cont: Color = C_RED if (anio_fin != "?" and int(anio_fin) <= anio_actual + 1) else C_TEXT

		var hb_j := HBoxContainer.new()
		hb_j.add_theme_constant_override("separation", 0)

		var widths: Array = [44,170,40,38,38,38,52,80,90,70,100]
		var cols: Array = [
			j.get("posicion_principal","?"),
			j.get("nombre_corto","?"),
			j.get("nacionalidad","?"),
			str(edad),
			str(j.get("media",0)),
			str(pot),
			str(forma) + "%",
			_fmt_m(val),
			_fmt_m(sal),
			anio_fin,
			"",
		]
		for ci in range(cols.size()):
			var w: int = widths[ci] if ci < widths.size() else 80
			var l := _mk_lbl(str(cols[ci]), 11)
			l.custom_minimum_size = Vector2(w, 22)
			if ci == 9:
				l.add_theme_color_override("font_color", c_cont)
			hb_j.add_child(l)

		# Botones de acción
		var hb_acc := HBoxContainer.new()
		hb_acc.add_theme_constant_override("separation", 4)
		hb_acc.custom_minimum_size = Vector2(100, 0)
		var btn_ren := Button.new()
		btn_ren.text = "Renovar"
		btn_ren.custom_minimum_size = Vector2(62, 20)
		_estilo_btn(btn_ren, C_ACCENT)
		var jid: int = int(j.get("id", 0))
		btn_ren.pressed.connect(_renovar_rapido.bind(jid))
		hb_acc.add_child(btn_ren)
		hb_j.add_child(hb_acc)

		vb.add_child(hb_j)

	vb.add_child(_mk_sep())

	# Jugadores libres disponibles para fichar (resumen)
	vb.add_child(_mk_seccion("AGENTES LIBRES DESTACADOS"))
	var libres: Array = DB.obtener_agentes_libres({})
	libres.sort_custom(func(a, b): return a.get("media", 0) > b.get("media", 0))
	var top_libres: Array = libres.slice(0, min(5, libres.size()))
	if top_libres.is_empty():
		vb.add_child(_mk_lbl("No hay agentes libres disponibles.", 12))
	else:
		for j in top_libres:
			var txt_l: String = "  %-20s  %s  Media:%d  Valor:%s" % [
				j.get("nombre_corto","?"),
				j.get("posicion_principal","?"),
				j.get("media",0),
				_fmt_m(j.get("valor_mercado",0)),
			]
			var bl := Button.new()
			bl.text = txt_l
			bl.alignment = HORIZONTAL_ALIGNMENT_LEFT
			_estilo_btn(bl, C_PANEL)
			var jid2: int = int(j.get("id", 0))
			bl.pressed.connect(_fichar_libre_directo.bind(jid2))
			vb.add_child(bl)

# ══════════════════════════════════════════════════════════════════════════════
# PANEL: TÁCTICAS
# ══════════════════════════════════════════════════════════════════════════════

func _refresh_tactica() -> void:
	_clear_body("tactica")
	var vb: VBoxContainer = _bodies["tactica"]

	vb.add_child(_mk_titulo("TÁCTICAS Y ALINEACIÓN"))

	# ── Selector de formación ────────────────────────────────────────────────
	vb.add_child(_mk_seccion("FORMACIÓN: " + _formacion))
	var hb_form := HBoxContainer.new()
	hb_form.add_theme_constant_override("separation", 6)
	hb_form.add_child(_mk_lbl("Elegir: ", 12))
	vb.add_child(hb_form)

	for f in FORMACIONES.keys():
		var bf := Button.new()
		bf.text = f
		bf.custom_minimum_size = Vector2(70, 28)
		if f == _formacion:
			_estilo_btn(bf, C_ACCENT)
		else:
			_estilo_btn(bf, C_PANEL2)
		bf.pressed.connect(_cambiar_formacion.bind(f))
		hb_form.add_child(bf)

	vb.add_child(_mk_sep())

	# ── Campo visual ─────────────────────────────────────────────────────────
	var campo_container := _build_campo_tactico()
	vb.add_child(campo_container)

	vb.add_child(_mk_sep())

	# ── Lista de titulares ───────────────────────────────────────────────────
	vb.add_child(_mk_seccion("ONCE TITULAR"))
	var posiciones_form: Array = POSICIONES_FORM.get(_formacion, [])
	for i in range(min(11, _titulares.size())):
		var jid: int = _titulares[i]
		var j: Dictionary = DB.obtener_jugador(jid) if jid > 0 else {}
		var pos_nombre: String = posiciones_form[i] if i < posiciones_form.size() else "?"
		var nombre: String = j.get("nombre_corto", "(vacío)") as String
		var media: int = j.get("media", 0)

		var hb_t := HBoxContainer.new()
		hb_t.add_theme_constant_override("separation", 10)
		var lbl_i := _mk_lbl(str(i + 1) + ".", 12, true)
		lbl_i.custom_minimum_size = Vector2(24, 0)
		var lbl_pos := _mk_lbl(pos_nombre, 12, true)
		lbl_pos.custom_minimum_size = Vector2(44, 0)
		lbl_pos.add_theme_color_override("font_color", C_ACCENT)
		var lbl_n := _mk_lbl(nombre, 12)
		lbl_n.custom_minimum_size = Vector2(180, 0)
		var lbl_m := _mk_lbl("Med: " + str(media), 11)
		lbl_m.custom_minimum_size = Vector2(70, 0)
		lbl_m.add_theme_color_override("font_color", C_DIM)

		var btn_sw := Button.new()
		btn_sw.text = "Cambiar"
		btn_sw.custom_minimum_size = Vector2(70, 22)
		_estilo_btn(btn_sw, C_PANEL2)
		btn_sw.pressed.connect(_mostrar_cambio_titular.bind(i, vb))

		hb_t.add_child(lbl_i)
		hb_t.add_child(lbl_pos)
		hb_t.add_child(lbl_n)
		hb_t.add_child(lbl_m)
		hb_t.add_child(btn_sw)
		vb.add_child(hb_t)

	vb.add_child(_mk_sep())

	# ── Instrucciones tácticas ───────────────────────────────────────────────
	vb.add_child(_mk_seccion("INSTRUCCIONES TÁCTICAS"))
	var instrucciones: Array = [
		["Presión alta", "Robar balón arriba, gasta más físico"],
		["Posesión", "Mantener balón, juego pausado"],
		["Contraataque", "Defender y salir rápido"],
		["Juego directo", "Pases largos al delantero"],
	]
	var hb_inst := HBoxContainer.new()
	hb_inst.add_theme_constant_override("separation", 8)
	vb.add_child(hb_inst)
	for inst in instrucciones:
		var bi := Button.new()
		bi.text = str(inst[0])
		bi.custom_minimum_size = Vector2(130, 30)
		bi.tooltip_text = str(inst[1])
		_estilo_btn(bi, C_PANEL2)
		hb_inst.add_child(bi)

	vb.add_child(_mk_sep())

	# ── Roles especiales ─────────────────────────────────────────────────────
	vb.add_child(_mk_seccion("ROLES ESPECIALES"))
	var grid_roles := GridContainer.new()
	grid_roles.columns = 4
	grid_roles.add_theme_constant_override("h_separation", 20)
	grid_roles.add_theme_constant_override("v_separation", 6)
	vb.add_child(grid_roles)

	var cap_j: Dictionary = DB.obtener_jugador(_capitan_id) if _capitan_id > 0 else {}
	var pat_j: Dictionary = DB.obtener_jugador(_pateador_id) if _pateador_id > 0 else {}

	var lk1 := _mk_lbl("Capitán:", 11)
	lk1.add_theme_color_override("font_color", C_DIM)
	grid_roles.add_child(lk1)
	grid_roles.add_child(_mk_lbl(cap_j.get("nombre_corto", "(sin asignar)") as String, 12, true))
	var lk2 := _mk_lbl("Pateador TL:", 11)
	lk2.add_theme_color_override("font_color", C_DIM)
	grid_roles.add_child(lk2)
	grid_roles.add_child(_mk_lbl(pat_j.get("nombre_corto", "(sin asignar)") as String, 12, true))

func _build_campo_tactico() -> Control:
	var pw: float = 380.0
	var ph: float = 250.0

	var outer := PanelContainer.new()
	var sty := StyleBoxFlat.new()
	sty.bg_color = Color(0.05, 0.07, 0.10)
	sty.border_color = C_BORDER
	sty.border_width_left = 1
	sty.border_width_right = 1
	sty.border_width_top = 1
	sty.border_width_bottom = 1
	outer.add_theme_stylebox_override("panel", sty)
	outer.size_flags_horizontal = Control.SIZE_SHRINK_CENTER

	var campo := Control.new()
	campo.custom_minimum_size = Vector2(pw, ph)
	outer.add_child(campo)

	# Fondo verde con franjas
	for i in range(7):
		var franja := ColorRect.new()
		franja.color = C_CAMPO if i % 2 == 0 else C_CAMPO2
		franja.position = Vector2(float(i) * float(pw) / 7.0, 0)
		franja.size = Vector2(float(pw) / 7.0, ph)
		campo.add_child(franja)

	# Líneas del campo
	_linea_campo(campo, pw / 2, 0, 2, ph, Color(1,1,1,0.5))  # línea central
	_linea_campo(campo, pw / 2 - 6, ph / 2 - 6, 12, 12, Color(1,1,1,0.5))  # punto central

	# Círculo central (aproximado con línea horizontal y vertical)
	var radio_c: int = 30
	_linea_campo(campo, pw/2 - radio_c, ph/2, radio_c*2, 2, Color(1,1,1,0.3))
	_linea_campo(campo, pw/2, ph/2 - radio_c, 2, radio_c*2, Color(1,1,1,0.3))

	# Áreas
	_linea_campo(campo, 0, ph/2 - 35, 50, 2, Color(1,1,1,0.5))  # área izq sup
	_linea_campo(campo, 0, ph/2 + 35, 50, 2, Color(1,1,1,0.5))  # área izq inf
	_linea_campo(campo, 50, ph/2 - 35, 2, 70, Color(1,1,1,0.5)) # área izq vert
	_linea_campo(campo, pw - 50, ph/2 - 35, 50, 2, Color(1,1,1,0.5))
	_linea_campo(campo, pw - 50, ph/2 + 35, 50, 2, Color(1,1,1,0.5))
	_linea_campo(campo, pw - 52, ph/2 - 35, 2, 70, Color(1,1,1,0.5))

	# Porterías
	_linea_campo(campo, 0, ph/2 - 15, 8, 2, Color(1,1,1,0.8))
	_linea_campo(campo, 0, ph/2 + 15, 8, 2, Color(1,1,1,0.8))
	_linea_campo(campo, 8, ph/2 - 15, 2, 30, Color(1,1,1,0.8))
	_linea_campo(campo, pw - 8, ph/2 - 15, 8, 2, Color(1,1,1,0.8))
	_linea_campo(campo, pw - 8, ph/2 + 15, 8, 2, Color(1,1,1,0.8))
	_linea_campo(campo, pw - 10, ph/2 - 15, 2, 30, Color(1,1,1,0.8))

	# Jugadores en el campo
	var posiciones: Array = FORMACIONES.get(_formacion, FORMACIONES["4-3-3"])

	for i in range(min(11, posiciones.size())):
		var pos_arr: Array = posiciones[i] as Array
		var rx: float = float(pos_arr[0])
		var ry: float = float(pos_arr[1])
		var px: int = int(rx * float(pw))
		var py: int = int(ry * float(ph))

		var jid: int = _titulares[i] if i < _titulares.size() else -1
		var j: Dictionary = DB.obtener_jugador(jid) if jid > 0 else {}
		var nombre: String = j.get("nombre_corto", "---") as String
		if nombre.length() > 8:
			nombre = nombre.substr(0, 8)
		var media: int = j.get("media", 0)

		var btn := Button.new()
		btn.text = nombre + "\n" + str(media)
		btn.custom_minimum_size = Vector2(62, 34)
		btn.position = Vector2(px - 31, py - 17)

		var sty_btn := StyleBoxFlat.new()
		var media_color: Color = C_GREEN if media >= 80 else (C_ACCENT if media >= 70 else C_YELLOW)
		sty_btn.bg_color = media_color.darkened(0.5)
		sty_btn.border_color = media_color
		sty_btn.border_width_left = 2
		sty_btn.border_width_right = 2
		sty_btn.border_width_top = 2
		sty_btn.border_width_bottom = 2
		sty_btn.corner_radius_top_left = 4
		sty_btn.corner_radius_top_right = 4
		sty_btn.corner_radius_bottom_left = 4
		sty_btn.corner_radius_bottom_right = 4
		btn.add_theme_stylebox_override("normal", sty_btn)
		btn.add_theme_stylebox_override("hover", sty_btn)
		btn.add_theme_color_override("font_color", Color.WHITE)
		btn.add_theme_font_size_override("font_size", 9)

		campo.add_child(btn)

	return outer

func _linea_campo(campo: Control, x: int, y: int, w: int, h: int, color: Color) -> void:
	var r := ColorRect.new()
	r.color = color
	r.position = Vector2(x, y)
	r.size = Vector2(w, h)
	campo.add_child(r)

func _cambiar_formacion(nueva: String) -> void:
	_formacion = nueva
	_inicializar_titulares()
	_refresh_tactica()

func _mostrar_cambio_titular(slot: int, _vb: VBoxContainer) -> void:
	# Popup para elegir jugador en ese slot
	var overlay := ColorRect.new()
	overlay.color = Color(0, 0, 0, 0.7)
	overlay.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	overlay.z_index = 100
	add_child(overlay)

	var center := CenterContainer.new()
	center.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	overlay.add_child(center)

	var panel := PanelContainer.new()
	panel.custom_minimum_size = Vector2(400, 350)
	var ps := StyleBoxFlat.new()
	ps.bg_color = C_PANEL
	ps.border_color = C_BORDER
	ps.border_width_left = 2
	ps.border_width_right = 2
	ps.border_width_top = 2
	ps.border_width_bottom = 2
	panel.add_theme_stylebox_override("panel", ps)
	center.add_child(panel)

	var pvb := VBoxContainer.new()
	pvb.add_theme_constant_override("separation", 6)
	panel.add_child(pvb)

	var pvb_mg := MarginContainer.new()
	_set_margins(pvb_mg, 12, 10, 12, 10)
	panel.add_child(pvb_mg)
	var pvb2 := VBoxContainer.new()
	pvb2.add_theme_constant_override("separation", 6)
	pvb_mg.add_child(pvb2)

	var pos_nombre: String = POSICIONES_FORM.get(_formacion, [])[slot] if slot < POSICIONES_FORM.get(_formacion, []).size() else "?"
	pvb2.add_child(_mk_lbl("Seleccionar jugador para posición: " + pos_nombre, 13, true))
	pvb2.add_child(_mk_sep())

	var sc_pop := ScrollContainer.new()
	sc_pop.custom_minimum_size = Vector2(380, 250)
	pvb2.add_child(sc_pop)
	var vb_pop := VBoxContainer.new()
	vb_pop.add_theme_constant_override("separation", 3)
	sc_pop.add_child(vb_pop)

	var plantilla: Array = DB.obtener_plantilla(_eq_id)
	plantilla.sort_custom(func(a, b): return a.get("media", 0) > b.get("media", 0))

	for j in plantilla:
		var jid: int = int(j.get("id", 0))
		var ya_titular: bool = jid in _titulares
		var txt_j: String = "%-20s  %s  Med:%d%s" % [
			j.get("nombre_corto","?"),
			j.get("posicion_principal","?"),
			j.get("media",0),
			"  (titular)" if ya_titular else "",
		]
		var bj := Button.new()
		bj.text = txt_j
		bj.alignment = HORIZONTAL_ALIGNMENT_LEFT
		_estilo_btn(bj, C_PANEL2 if ya_titular else C_PANEL)
		bj.pressed.connect(func():
			_titulares[slot] = jid
			overlay.queue_free()
			_refresh_tactica()
		)
		vb_pop.add_child(bj)

	var btn_cerrar := Button.new()
	btn_cerrar.text = "Cancelar"
	_estilo_btn(btn_cerrar, C_RED)
	btn_cerrar.pressed.connect(func(): overlay.queue_free())
	pvb2.add_child(btn_cerrar)

# ══════════════════════════════════════════════════════════════════════════════
# PANEL: MERCADO
# ══════════════════════════════════════════════════════════════════════════════

func _refresh_mercado() -> void:
	_clear_body("mercado")
	var vb: VBoxContainer = _bodies["mercado"]

	vb.add_child(_mk_titulo("MERCADO DE FICHAJES"))

	# Estado del mercado
	var abierto: bool = TransferMarket.esta_abierto()
	var estado_lbl := _mk_lbl(
		"● MERCADO " + ("ABIERTO" if abierto else "CERRADO"),
		14, true
	)
	estado_lbl.add_theme_color_override("font_color", C_GREEN if abierto else C_RED)
	vb.add_child(estado_lbl)

	var eq: Dictionary = DB.obtener_equipo(_eq_id)
	var presupuesto: int = eq.get("finanzas", {}).get("presupuesto_fichajes", 0)
	var hb_budget := HBoxContainer.new()
	hb_budget.add_theme_constant_override("separation", 20)
	vb.add_child(hb_budget)
	hb_budget.add_child(_mk_card("PRESUPUESTO FICHAJES", _fmt_m(presupuesto), C_ACCENT))

	vb.add_child(_mk_sep())

	# ── Filtros de búsqueda ──────────────────────────────────────────────────
	vb.add_child(_mk_seccion("BUSCAR JUGADORES"))
	var hb_filtros := HBoxContainer.new()
	hb_filtros.add_theme_constant_override("separation", 10)
	vb.add_child(hb_filtros)

	var lbl_pf := _mk_lbl("Posición:", 12)
	hb_filtros.add_child(lbl_pf)
	var opt_pos := OptionButton.new()
	opt_pos.custom_minimum_size = Vector2(90, 28)
	var posiciones_filtro: Array = ["TODOS","PO","LD","DFC","LI","MCD","MC","MCO","EI","ED","DC"]
	for pf in posiciones_filtro:
		opt_pos.add_item(pf)
	opt_pos.item_selected.connect(func(i: int):
		_mercado_pos = posiciones_filtro[i]
		_refresh_mercado()
	)
	for pi in range(posiciones_filtro.size()):
		if posiciones_filtro[pi] == _mercado_pos:
			opt_pos.select(pi)
	hb_filtros.add_child(opt_pos)

	var lbl_v := _mk_lbl("Valor máx:", 12)
	hb_filtros.add_child(lbl_v)
	var vals: Array = [0, 1_000_000, 5_000_000, 20_000_000, 50_000_000, 100_000_000]
	var val_labels: Array = ["Sin límite","1M","5M","20M","50M","100M"]
	var opt_val := OptionButton.new()
	opt_val.custom_minimum_size = Vector2(90, 28)
	for vi in range(val_labels.size()):
		opt_val.add_item(str(val_labels[vi]))
	opt_val.item_selected.connect(func(i: int):
		_mercado_valor = vals[i]
		_refresh_mercado()
	)
	for vi in range(vals.size()):
		if vals[vi] == _mercado_valor:
			opt_val.select(vi)
	hb_filtros.add_child(opt_val)

	vb.add_child(_mk_sep())

	# ── Resultados de búsqueda ───────────────────────────────────────────────
	var candidatos: Array = []
	for jid in DB.jugadores:
		var j: Dictionary = DB.jugadores[jid]
		var jeid: int = int(j.get("equipo_id", -1))
		if jeid == _eq_id or jeid == -1:
			continue
		var jpos: String = j.get("posicion_principal", "") as String
		if _mercado_pos != "TODOS" and jpos != _mercado_pos:
			continue
		var jval: int = j.get("valor_mercado", 0)
		if _mercado_valor > 0 and jval > _mercado_valor:
			continue
		candidatos.append(j)

	candidatos.sort_custom(func(a, b): return a.get("media", 0) > b.get("media", 0))
	var mostrar: Array = candidatos.slice(0, min(30, candidatos.size()))

	var lbl_res := _mk_lbl("Resultados: %d jugadores encontrados (mostrando %d)" % [candidatos.size(), mostrar.size()], 12)
	lbl_res.add_theme_color_override("font_color", C_DIM)
	vb.add_child(lbl_res)

	vb.add_child(_mk_fila_tabla(["Jugador","Pos","País","Edad","Med","Valor","Club","Acción"], true, [160,44,40,36,36,80,130,90]))
	vb.add_child(_mk_sep())

	for j in mostrar:
		var jid: int = int(j.get("id", 0))
		var edad: int = _calcular_edad(j.get("fecha_nacimiento", ""))
		var jval: int = j.get("valor_mercado", 0)
		var jeq: Dictionary = DB.obtener_equipo(int(j.get("equipo_id", 0)))

		var hb_j := HBoxContainer.new()
		hb_j.add_theme_constant_override("separation", 0)

		var wcols: Array = [160,44,40,36,36,80,130]
		var cols2: Array = [
			j.get("nombre_corto","?"),
			j.get("posicion_principal","?"),
			j.get("nacionalidad","?"),
			str(edad),
			str(j.get("media",0)),
			_fmt_m(jval),
			jeq.get("nombre_corto","?"),
		]
		for ci in range(cols2.size()):
			var w: int = wcols[ci] if ci < wcols.size() else 80
			var l := _mk_lbl(str(cols2[ci]), 11)
			l.custom_minimum_size = Vector2(w, 22)
			hb_j.add_child(l)

		var btn_of := Button.new()
		btn_of.text = "Ofertar"
		btn_of.custom_minimum_size = Vector2(86, 22)
		_estilo_btn(btn_of, C_ACCENT if abierto else C_PANEL2)
		btn_of.disabled = not abierto
		btn_of.pressed.connect(_enviar_oferta_ui.bind(jid, jval))
		hb_j.add_child(btn_of)
		vb.add_child(hb_j)

	vb.add_child(_mk_sep())

	# ── Agentes libres ───────────────────────────────────────────────────────
	vb.add_child(_mk_seccion("AGENTES LIBRES"))
	var libres: Array = DB.obtener_agentes_libres({})
	libres.sort_custom(func(a, b): return a.get("media", 0) > b.get("media", 0))
	if libres.is_empty():
		vb.add_child(_mk_lbl("No hay agentes libres.", 12))
	else:
		for j in libres.slice(0, min(10, libres.size())):
			var jid: int = int(j.get("id", 0))
			var txt_l: String = "  %-20s  %s  Edad:%d  Med:%d  Sal.sug:%s/sem" % [
				j.get("nombre_corto","?"),
				j.get("posicion_principal","?"),
				_calcular_edad(j.get("fecha_nacimiento","")),
				j.get("media",0),
				_fmt_m(TransferMarket.salario_sugerido(jid)),
			]
			var bl := Button.new()
			bl.text = txt_l
			bl.alignment = HORIZONTAL_ALIGNMENT_LEFT
			_estilo_btn(bl, C_PANEL)
			bl.pressed.connect(_fichar_libre_directo.bind(jid))
			vb.add_child(bl)

	vb.add_child(_mk_sep())

	# ── Historial ────────────────────────────────────────────────────────────
	vb.add_child(_mk_seccion("HISTORIAL DE FICHAJES"))
	var historial: Array = TransferMarket.obtener_historial()
	if historial.is_empty():
		vb.add_child(_mk_lbl("Sin traspasos realizados aún.", 12))
	else:
		var recientes_h: Array = historial.slice(max(0, historial.size() - 8), historial.size())
		recientes_h.reverse()
		for t in recientes_h:
			var orig_eq: Dictionary = DB.obtener_equipo(int(t.get("origen", 0)))
			var dest_eq: Dictionary = DB.obtener_equipo(int(t.get("destino", 0)))
			var txt_h: String = "  %-20s  Med:%d  %s  %s → %s" % [
				t.get("nombre","?"),
				t.get("media",0),
				_fmt_m(t.get("cantidad",0)),
				orig_eq.get("nombre_corto","?"),
				dest_eq.get("nombre_corto","?"),
			]
			var lh := _mk_lbl(txt_h, 11)
			var dest_id: int = int(t.get("destino", 0))
			lh.add_theme_color_override("font_color", C_GREEN if dest_id == _eq_id else C_DIM)
			vb.add_child(lh)

# ══════════════════════════════════════════════════════════════════════════════
# PANEL: FINANZAS
# ══════════════════════════════════════════════════════════════════════════════

func _refresh_finanzas() -> void:
	_clear_body("finanzas")
	var vb: VBoxContainer = _bodies["finanzas"]
	var eq: Dictionary = DB.obtener_equipo(_eq_id)
	var fin: Dictionary = eq.get("finanzas", {})
	var inf: Dictionary = EconomySystem.obtener_informe(_eq_id)

	vb.add_child(_mk_titulo("FINANZAS DEL CLUB"))

	# ── Cards superiores ─────────────────────────────────────────────────────
	var hb_top := HBoxContainer.new()
	hb_top.add_theme_constant_override("separation", 10)
	vb.add_child(hb_top)

	var bal: int = fin.get("balance", 0)
	var deuda: int = fin.get("deuda", 0)
	var pres: int = fin.get("presupuesto_fichajes", 0)
	var masa: int = fin.get("masa_salarial_semanal", 0)

	hb_top.add_child(_mk_card("BALANCE", _fmt_m(bal), C_GREEN if bal >= 0 else C_RED))
	hb_top.add_child(_mk_card("DEUDA", _fmt_m(deuda), C_RED if deuda > 0 else C_DIM))
	hb_top.add_child(_mk_card("PRESUPUESTO FICHAJES", _fmt_m(pres), C_ACCENT))
	hb_top.add_child(_mk_card("MASA SALARIAL/SEM", _fmt_m(masa), C_YELLOW))

	vb.add_child(_mk_sep())

	# ── Ingresos ─────────────────────────────────────────────────────────────
	vb.add_child(_mk_seccion("INGRESOS"))
	var tv_anual: int = inf.get("ingresos_tv_anual", fin.get("ingresos_tv_anual", 0))
	var sponsor: int = fin.get("sponsor_camiseta", 0) + fin.get("sponsor_estadio", 0)
	var merch: int = fin.get("merchandising_anual", 0)
	var ticket: int = inf.get("ingreso_partido", 0) * 19

	var ing_data: Array = [
		["Derechos TV (anual)", tv_anual],
		["Sponsors (anual)", sponsor],
		["Merchandising (anual)", merch],
		["Taquilla (estimado temporada)", ticket],
	]
	var max_ing: int = 1
	for d in ing_data:
		if int(d[1]) > max_ing:
			max_ing = int(d[1])

	for d in ing_data:
		var cant: int = int(d[1])
		_barra_finanzas(vb, str(d[0]), cant, max_ing, C_GREEN)

	vb.add_child(_mk_sep())

	# ── Gastos ───────────────────────────────────────────────────────────────
	vb.add_child(_mk_seccion("GASTOS"))
	var salarios_anual: int = masa * 52
	var mantenimiento: int = eq.get("estadio", {}).get("coste_mantenimiento_semanal", 0) * 52

	var gas_data: Array = [
		["Salarios (anual)", salarios_anual],
		["Mantenimiento estadio (anual)", mantenimiento],
		["Intereses deuda (anual)", int(float(deuda) * 0.05)],
	]
	var max_gas: int = 1
	for d in gas_data:
		if int(d[1]) > max_gas:
			max_gas = int(d[1])
	for d in gas_data:
		_barra_finanzas(vb, str(d[0]), int(d[1]), max_gas, C_RED)

	var ratio: float = EconomySystem.porcentaje_salarios_sobre_ingresos(_eq_id)
	var c_ratio: Color = C_GREEN if ratio < 70.0 else (C_YELLOW if ratio < 90.0 else C_RED)
	var lbl_r := _mk_lbl("Ratio salarios/ingresos: %.1f%%" % ratio, 13, true)
	lbl_r.add_theme_color_override("font_color", c_ratio)
	vb.add_child(lbl_r)

	vb.add_child(_mk_sep())

	# ── Estadio ──────────────────────────────────────────────────────────────
	vb.add_child(_mk_seccion("ESTADIO"))
	var estadio: Dictionary = eq.get("estadio", {})
	var grid_st := GridContainer.new()
	grid_st.columns = 4
	grid_st.add_theme_constant_override("h_separation", 24)
	grid_st.add_theme_constant_override("v_separation", 5)
	vb.add_child(grid_st)

	var st_data: Array = [
		["Nombre", estadio.get("nombre", "?")],
		["Capacidad", str(estadio.get("capacidad", 0)) + " espectadores"],
		["Estado", str(estadio.get("estado", 0)) + "%"],
		["Nivel VIP", str(estadio.get("nivel_vip", 0)) + "/5"],
		["Tienda oficial", str(estadio.get("nivel_tienda", 0)) + "/5"],
		["Museo", str(estadio.get("nivel_museo", 0)) + "/3"],
		["Parking", str(estadio.get("nivel_parking", 0)) + "/3"],
		["Mant./sem", _fmt_m(estadio.get("coste_mantenimiento_semanal", 0))],
	]
	for pair in st_data:
		var lk := _mk_lbl(str(pair[0]), 11)
		lk.add_theme_color_override("font_color", C_DIM)
		grid_st.add_child(lk)
		grid_st.add_child(_mk_lbl(str(pair[1]), 12, true))

	vb.add_child(_mk_sep())

	# ── Sponsors ─────────────────────────────────────────────────────────────
	vb.add_child(_mk_seccion("SPONSORS"))
	var sponsors_data: Array = [
		["Camiseta (frente)",    fin.get("sponsor_camiseta", 0), "Renegociar"],
		["Estadio (naming)",     fin.get("sponsor_estadio",  0), "Renegociar"],
		["Sponsor TV",           int(float(tv_anual) * 0.1),     "Buscar nuevo"],
	]
	for s in sponsors_data:
		var hb_s := HBoxContainer.new()
		hb_s.add_theme_constant_override("separation", 12)
		var lbl_s := _mk_lbl("%-25s  %s/año" % [str(s[0]), _fmt_m(int(s[1]))], 12)
		lbl_s.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		hb_s.add_child(lbl_s)
		var btn_s := Button.new()
		btn_s.text = str(s[2])
		btn_s.custom_minimum_size = Vector2(100, 24)
		_estilo_btn(btn_s, C_PANEL2)
		btn_s.pressed.connect(func(): _mostrar_notif("Los sponsors se renegocian al final de temporada."))
		hb_s.add_child(btn_s)
		vb.add_child(hb_s)

	vb.add_child(_mk_sep())

	# ── Solicitar préstamo ───────────────────────────────────────────────────
	vb.add_child(_mk_seccion("BANCO"))
	var hb_pr := HBoxContainer.new()
	hb_pr.add_theme_constant_override("separation", 12)
	vb.add_child(hb_pr)
	var lbl_pr := _mk_lbl("Solicitar préstamo (interés 5% anual):", 12)
	lbl_pr.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	hb_pr.add_child(lbl_pr)
	for monto in [5_000_000, 20_000_000, 50_000_000]:
		var bp := Button.new()
		bp.text = _fmt_m(monto)
		bp.custom_minimum_size = Vector2(70, 28)
		_estilo_btn(bp, C_PANEL2)
		bp.pressed.connect(_solicitar_prestamo.bind(monto))
		hb_pr.add_child(bp)

# ══════════════════════════════════════════════════════════════════════════════
# PANEL: CLASIFICACIÓN
# ══════════════════════════════════════════════════════════════════════════════

func _refresh_clasificacion() -> void:
	_clear_body("clasificacion")
	var vb: VBoxContainer = _bodies["clasificacion"]

	var liga: Dictionary = DB.ligas.get(_liga_id, {})
	vb.add_child(_mk_titulo("CLASIFICACIÓN — " + str(liga.get("nombre", "Liga"))))

	# Leyenda de colores
	var hb_ley := HBoxContainer.new()
	hb_ley.add_theme_constant_override("separation", 16)
	vb.add_child(hb_ley)
	for par in [["■ Champions", C_CHAMP], ["■ Europa", C_EUROPA], ["■ Promoción", C_PROMO], ["■ Descenso", C_RELEGA]]:
		var ll := _mk_lbl(str(par[0]), 11)
		ll.add_theme_color_override("font_color", par[1] as Color)
		hb_ley.add_child(ll)

	vb.add_child(_mk_sep())

	var tabla: Array = LeagueSystem.obtener_clasificacion(_liga_id)
	var n: int = tabla.size()

	# Cabecera
	vb.add_child(_mk_fila_tabla(["Pos","Equipo","PJ","PG","PE","PP","GF","GC","GD","Pts"], true, [32,180,32,32,32,32,32,32,32,40]))
	vb.add_child(_mk_sep())

	for i in range(n):
		var fila = tabla[i]
		var eid: int = int(fila.get("equipo_id", 0))
		var eq_fila: Dictionary = DB.obtener_equipo(eid)
		var nombre: String = eq_fila.get("nombre_corto", "?") as String
		var pj: int = fila.get("PJ", 0)
		var pg: int = fila.get("PG", 0)
		var pe: int = fila.get("PE", 0)
		var pp: int = fila.get("PP", 0)
		var gf: int = fila.get("GF", 0)
		var gc: int = fila.get("GC", 0)
		var gd: int = gf - gc
		var pts: int = fila.get("Pts", 0)
		var pos_num: int = i + 1

		var c_fondo: Color = Color(0, 0, 0, 0)
		if pos_num <= 4:
			c_fondo = Color(C_CHAMP.r, C_CHAMP.g, C_CHAMP.b, 0.12)
		elif pos_num <= 6:
			c_fondo = Color(C_EUROPA.r, C_EUROPA.g, C_EUROPA.b, 0.12)
		elif pos_num >= n - 2:
			c_fondo = Color(C_RELEGA.r, C_RELEGA.g, C_RELEGA.b, 0.12)
		elif pos_num == n - 3:
			c_fondo = Color(C_PROMO.r, C_PROMO.g, C_PROMO.b, 0.12)

		var hb_f := HBoxContainer.new()
		hb_f.add_theme_constant_override("separation", 0)
		if c_fondo.a > 0:
			var bg_r := ColorRect.new()
			bg_r.color = c_fondo
			bg_r.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
			hb_f.add_child(bg_r)
			bg_r.z_index = -1

		var gd_str: String = ("+" if gd >= 0 else "") + str(gd)
		var wcols: Array = [32,180,32,32,32,32,32,32,32,40]
		var cols3: Array = [str(pos_num), nombre, str(pj), str(pg), str(pe), str(pp), str(gf), str(gc), gd_str, str(pts)]

		for ci in range(cols3.size()):
			var w: int = wcols[ci] if ci < wcols.size() else 40
			var l := _mk_lbl(str(cols3[ci]), 12 if ci == 9 else 11, ci == 9)
			l.custom_minimum_size = Vector2(w, 22)
			if eid == _eq_id:
				l.add_theme_color_override("font_color", C_ACCENT)
			elif ci == 9:
				l.add_theme_color_override("font_color", C_TEXT)
			hb_f.add_child(l)

		vb.add_child(hb_f)

	vb.add_child(_mk_sep())

	# ── Top Goleadores ────────────────────────────────────────────────────────
	vb.add_child(_mk_seccion("TOP GOLEADORES"))
	var goleadores: Array = LeagueSystem.obtener_max_goleadores(10)
	if goleadores.is_empty():
		vb.add_child(_mk_lbl("Sin goles registrados.", 12))
	else:
		var hb_gol := HBoxContainer.new()
		hb_gol.add_theme_constant_override("separation", 40)
		vb.add_child(hb_gol)

		var vb_gol := VBoxContainer.new()
		vb_gol.add_theme_constant_override("separation", 4)
		hb_gol.add_child(vb_gol)

		for i in range(goleadores.size()):
			var g = goleadores[i]
			var j: Dictionary = DB.obtener_jugador(int(g.get("id", 0)))
			var eqg: Dictionary = DB.obtener_equipo(int(j.get("equipo_id", 0)))
			var txt_g: String = "%2d.  %-22s  %-18s  %d goles" % [
				i + 1,
				g.get("nombre", "?"),
				eqg.get("nombre_corto", "?"),
				g.get("goles", 0),
			]
			var lg := _mk_lbl(txt_g, 12)
			if int(j.get("equipo_id", 0)) == _eq_id:
				lg.add_theme_color_override("font_color", C_ACCENT)
			vb_gol.add_child(lg)

# ══════════════════════════════════════════════════════════════════════════════
# PANEL: CALENDARIO
# ══════════════════════════════════════════════════════════════════════════════

func _refresh_calendario() -> void:
	_clear_body("calendario")
	var vb: VBoxContainer = _bodies["calendario"]

	var liga: Dictionary = DB.ligas.get(_liga_id, {})
	vb.add_child(_mk_titulo("CALENDARIO — " + str(liga.get("nombre", "Liga"))))

	var jor_actual: int = LeagueSystem.jornada_actual(_liga_id)
	var total_j: int   = 38

	var j_inicio: int = max(0, jor_actual - 3)
	var j_fin: int    = min(total_j, jor_actual + 8)

	for jor in range(j_inicio, j_fin):
		var l_jor: Array = []
		if LeagueSystem._ligas.has(_liga_id):
			var liga_data: Dictionary = LeagueSystem._ligas[_liga_id]
			var cal: Array = liga_data.get("calendario", [])
			if jor < cal.size():
				l_jor = cal[jor]

		var es_pasada: bool = jor < jor_actual
		var es_actual: bool = jor == jor_actual

		var color_jor: Color = C_DIM if es_pasada else (C_ACCENT if es_actual else C_TEXT)
		var hdr_jor := _mk_lbl("── Jornada %d %s──" % [jor + 1, "▶ " if es_actual else ""], 12, true)
		hdr_jor.add_theme_color_override("font_color", color_jor)
		vb.add_child(hdr_jor)

		if l_jor.is_empty():
			var lv := _mk_lbl("   (sin partidos programados)", 11)
			lv.add_theme_color_override("font_color", C_DIM)
			vb.add_child(lv)
			continue

		for p in l_jor:
			var lid: int = int(p.get("local", 0))
			var vid: int = int(p.get("visitante", 0))
			var eql: Dictionary = DB.obtener_equipo(lid)
			var eqv: Dictionary = DB.obtener_equipo(vid)
			var es_nuestro: bool = lid == _eq_id or vid == _eq_id

			var res_str: String = ""
			if es_pasada and p.has("goles_local"):
				var gl: int = int(p.get("goles_local", 0))
				var gv: int = int(p.get("goles_visitante", 0))
				res_str = "  %d – %d" % [gl, gv]
				var ganamos: bool = (lid == _eq_id and gl > gv) or (vid == _eq_id and gv > gl)
				var empatamos: bool = gl == gv
				var txt_p: String = "   %-20s%s  %-20s" % [eql.get("nombre_corto","?"), res_str, eqv.get("nombre_corto","?")]
				var lp := _mk_lbl(txt_p, 12 if es_nuestro else 11)
				if es_nuestro:
					lp.add_theme_color_override("font_color", C_GREEN if ganamos else (C_YELLOW if empatamos else C_RED))
				vb.add_child(lp)
			else:
				var txt_p: String = "   %-20s  vs  %-20s" % [eql.get("nombre_corto","?"), eqv.get("nombre_corto","?")]
				var lp := _mk_lbl(txt_p, 12 if es_nuestro else 11)
				if es_nuestro:
					lp.add_theme_color_override("font_color", C_ACCENT)
				vb.add_child(lp)

# ══════════════════════════════════════════════════════════════════════════════
# AVANZAR SEMANA
# ══════════════════════════════════════════════════════════════════════════════

func _on_avanzar_semana() -> void:
	# Si la temporada ya terminó, mostrar resumen en lugar de simular
	if LeagueSystem.liga_finalizada_estado(_liga_id):
		_mostrar_fin_temporada()
		return

	# Preview del próximo partido antes de simular
	var proxima: Array = LeagueSystem.obtener_proxima_jornada(_liga_id)
	var rival_id: int = -1
	var es_local_partido: bool = false
	for p in proxima:
		var lid: int = int(p.get("local", 0))
		var vid: int = int(p.get("visitante", 0))
		if lid == _eq_id:
			rival_id = vid; es_local_partido = true; break
		elif vid == _eq_id:
			rival_id = lid; es_local_partido = false; break

	if rival_id >= 0:
		_mostrar_preview_partido(rival_id, es_local_partido)
	else:
		# Sin partido propio esta jornada (ej. bye), simular directamente
		_ejecutar_semana()

func _mostrar_preview_partido(rival_id: int, es_local: bool) -> void:
	var rival: Dictionary = DB.obtener_equipo(rival_id)
	var eq:    Dictionary = DB.obtener_equipo(_eq_id)
	var h2h:   Dictionary = LeagueSystem.obtener_h2h(_eq_id, rival_id)
	var jor:   int = LeagueSystem.jornada_actual(_liga_id) + 1
	var tabla: Array = LeagueSystem.obtener_clasificacion(_liga_id)
	var pos_rival: int = 0
	for i in range(tabla.size()):
		if int(tabla[i].get("equipo_id", 0)) == rival_id:
			pos_rival = i + 1; break

	var overlay := ColorRect.new()
	overlay.color = Color(0, 0, 0, 0.78)
	overlay.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	overlay.z_index = 60
	add_child(overlay)

	var center := CenterContainer.new()
	center.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	overlay.add_child(center)

	var panel := PanelContainer.new()
	panel.custom_minimum_size = Vector2(480, 0)
	var ps := StyleBoxFlat.new()
	ps.bg_color = C_PANEL
	ps.border_color = C_ACCENT
	ps.border_width_left = 2; ps.border_width_right = 2
	ps.border_width_top  = 2; ps.border_width_bottom = 2
	ps.corner_radius_top_left = 8; ps.corner_radius_top_right = 8
	ps.corner_radius_bottom_left = 8; ps.corner_radius_bottom_right = 8
	panel.add_theme_stylebox_override("panel", ps)
	center.add_child(panel)

	var mg := MarginContainer.new()
	_set_margins(mg, 28, 22, 28, 22)
	panel.add_child(mg)

	var vb := VBoxContainer.new()
	vb.add_theme_constant_override("separation", 10)
	mg.add_child(vb)

	# Jornada
	var lbl_jor := _mk_lbl("JORNADA %d — TEMPORADA %d" % [jor, _temporada], 11)
	lbl_jor.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	lbl_jor.add_theme_color_override("font_color", C_DIM)
	vb.add_child(lbl_jor)

	# Enfrentamiento
	var nombre_local:   String = eq.get("nombre_corto","?")     as String if es_local else rival.get("nombre_corto","?") as String
	var nombre_visit:   String = rival.get("nombre_corto","?")   as String if es_local else eq.get("nombre_corto","?")   as String
	var lbl_match := _mk_lbl("%s  vs  %s" % [nombre_local, nombre_visit], 20, true)
	lbl_match.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	lbl_match.add_theme_color_override("font_color", C_TEXT)
	vb.add_child(lbl_match)

	var cond := _mk_lbl("[ %s ]" % ("LOCAL" if es_local else "VISITANTE"), 12, true)
	cond.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	cond.add_theme_color_override("font_color", C_ACCENT)
	vb.add_child(cond)

	vb.add_child(_mk_sep())

	# Datos del rival
	vb.add_child(_mk_seccion("RIVAL"))
	var grid_r := GridContainer.new()
	grid_r.columns = 4
	grid_r.add_theme_constant_override("h_separation", 20)
	grid_r.add_theme_constant_override("v_separation", 4)
	vb.add_child(grid_r)
	var pl_rival: Array = DB.obtener_plantilla(rival_id)
	var media_rival: float = 0.0
	for j in pl_rival: media_rival += float(j.get("media", 0))
	if not pl_rival.is_empty(): media_rival /= float(pl_rival.size())
	var rival_tabla: Dictionary = {}
	for fila in tabla:
		if int(fila.get("equipo_id",0)) == rival_id: rival_tabla = fila; break
	for par in [
		["Posición", "%d°" % pos_rival if pos_rival > 0 else "--"],
		["Media equipo", "%.0f" % media_rival],
		["PJ/PG/PE/PP", "%d/%d/%d/%d" % [rival_tabla.get("PJ",0), rival_tabla.get("PG",0), rival_tabla.get("PE",0), rival_tabla.get("PP",0)]],
		["Reputación", str(rival.get("reputacion",0))],
	]:
		var lk := _mk_lbl(str(par[0]), 11); lk.add_theme_color_override("font_color", C_DIM)
		grid_r.add_child(lk)
		grid_r.add_child(_mk_lbl(str(par[1]), 12, true))

	vb.add_child(_mk_sep())

	# Historial H2H
	vb.add_child(_mk_seccion("HISTORIAL CARA A CARA"))
	var h2h_vb := VBoxContainer.new()
	h2h_vb.add_theme_constant_override("separation", 4)
	vb.add_child(h2h_vb)
	if h2h.get("PJ", 0) == 0:
		var lbl_h := _mk_lbl("Primer enfrentamiento histórico entre estos clubes.", 12)
		lbl_h.add_theme_color_override("font_color", C_DIM)
		h2h_vb.add_child(lbl_h)
	else:
		var pj_h: int  = h2h.get("PJ", 0)
		var wh: int    = h2h.get("W",  0)
		var dh: int    = h2h.get("D",  0)
		var lh: int    = h2h.get("L",  0)
		var gfh: int   = h2h.get("GF", 0)
		var gch: int   = h2h.get("GC", 0)
		var txt_h: String = "%d partidos:  %dV  %dE  %dD  |  %d-%d en goles" % [pj_h, wh, dh, lh, gfh, gch]
		var lbl_h := _mk_lbl(txt_h, 13, true)
		var c_h: Color = C_GREEN if wh > lh else (C_YELLOW if wh == lh else C_RED)
		lbl_h.add_theme_color_override("font_color", c_h)
		h2h_vb.add_child(lbl_h)

	vb.add_child(_mk_sep())

	# Botones
	var hb_btn := HBoxContainer.new()
	hb_btn.add_theme_constant_override("separation", 12)
	hb_btn.alignment = BoxContainer.ALIGNMENT_CENTER
	vb.add_child(hb_btn)

	var btn_sim := Button.new()
	btn_sim.text = "▶  Simular partido"
	btn_sim.custom_minimum_size = Vector2(180, 38)
	_estilo_btn(btn_sim, C_ACCENT)
	btn_sim.pressed.connect(func():
		overlay.queue_free()
		_ejecutar_semana()
	)
	hb_btn.add_child(btn_sim)

	var btn_can := Button.new()
	btn_can.text = "Cancelar"
	btn_can.custom_minimum_size = Vector2(100, 38)
	_estilo_btn(btn_can, C_PANEL2)
	btn_can.pressed.connect(func(): overlay.queue_free())
	hb_btn.add_child(btn_can)

func _ejecutar_semana() -> void:
	_sem += 1
	var resultados: Array = LeagueSystem.simular_jornada(_liga_id)
	EconomySystem.procesar_semana(_sem)
	CalendarSystem.avanzar(7)

	var res_propio: Dictionary = {}
	for r in resultados:
		var lid: int = int(r.get("local_id", 0))
		var vid: int = int(r.get("visitante_id", 0))
		if lid == _eq_id or vid == _eq_id:
			res_propio = r
			_hist.append(r)

	if TransferMarket.esta_abierto():
		TransferMarket.simular_actividad_mercado_ia(3)

	_generar_noticias_semana(resultados)
	_refresh_all()

	# ¿Terminó la temporada tras esta jornada?
	var temporada_terminada: bool = LeagueSystem.liga_finalizada_estado(_liga_id)

	if not res_propio.is_empty():
		# Mostrar resultado; al cerrar, si terminó la temporada mostrar resumen
		_mostrar_popup_resultado(res_propio, temporada_terminada)
	elif temporada_terminada:
		_mostrar_fin_temporada()

func _mostrar_fin_temporada() -> void:
	var resumen: Dictionary = LeagueSystem.obtener_resumen_temporada(_liga_id)
	var tabla: Array = resumen.get("tabla", [])
	var campeon: Dictionary = resumen.get("campeon", {})
	var descendidos: Array = resumen.get("descendidos", [])

	var overlay := ColorRect.new()
	overlay.color = Color(0, 0, 0, 0.82)
	overlay.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	overlay.z_index = 70
	add_child(overlay)

	var sc := ScrollContainer.new()
	sc.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	overlay.add_child(sc)

	var center := CenterContainer.new()
	center.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	sc.add_child(center)

	var panel := PanelContainer.new()
	panel.custom_minimum_size = Vector2(560, 0)
	var ps := StyleBoxFlat.new()
	ps.bg_color = C_PANEL
	ps.border_color = Color(0.9, 0.75, 0.1)
	ps.border_width_left = 3; ps.border_width_right = 3
	ps.border_width_top  = 3; ps.border_width_bottom = 3
	ps.corner_radius_top_left = 10; ps.corner_radius_top_right = 10
	ps.corner_radius_bottom_left = 10; ps.corner_radius_bottom_right = 10
	panel.add_theme_stylebox_override("panel", ps)
	center.add_child(panel)

	var mg := MarginContainer.new()
	_set_margins(mg, 28, 24, 28, 24)
	panel.add_child(mg)

	var vb := VBoxContainer.new()
	vb.add_theme_constant_override("separation", 10)
	mg.add_child(vb)

	# Título
	var lbl_t := _mk_lbl("TEMPORADA %d — FIN" % _temporada, 22, true)
	lbl_t.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	lbl_t.add_theme_color_override("font_color", Color(0.95, 0.80, 0.10))
	vb.add_child(lbl_t)

	# Campeón
	if not campeon.is_empty():
		var eq_c: Dictionary = DB.obtener_equipo(int(campeon.get("equipo_id", 0)))
		var lbl_c := _mk_lbl("🏆 CAMPEÓN: %s  (%d pts)" % [
			eq_c.get("nombre_corto","?"), campeon.get("Pts",0)], 16, true)
		lbl_c.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		lbl_c.add_theme_color_override("font_color", Color(0.95, 0.80, 0.10))
		vb.add_child(lbl_c)

	vb.add_child(_mk_sep())

	# Tabla final
	vb.add_child(_mk_seccion("CLASIFICACIÓN FINAL"))
	vb.add_child(_mk_fila_tabla(["Pos","Equipo","PJ","PG","PE","PP","GD","Pts"], true, [32,190,32,32,32,32,40,40]))
	for i in range(tabla.size()):
		var fila = tabla[i]
		var eid: int = int(fila.get("equipo_id",0))
		var eq_f: Dictionary = DB.obtener_equipo(eid)
		var gd: int = fila.get("GF",0) - fila.get("GC",0)
		var gd_str: String = ("+" if gd >= 0 else "") + str(gd)
		var pos_n: int = i + 1
		var c_fila: Color
		if   pos_n <= 4:              c_fila = Color(C_CHAMP.r,  C_CHAMP.g,  C_CHAMP.b,  0.15)
		elif pos_n <= 6:              c_fila = Color(C_EUROPA.r, C_EUROPA.g, C_EUROPA.b, 0.15)
		elif pos_n >= tabla.size()-2: c_fila = Color(C_RELEGA.r, C_RELEGA.g, C_RELEGA.b, 0.20)
		else:                         c_fila = Color(0,0,0,0)
		var hb_f := HBoxContainer.new()
		hb_f.add_theme_constant_override("separation", 0)
		if c_fila.a > 0:
			var bg_r := ColorRect.new()
			bg_r.color = c_fila
			bg_r.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
			bg_r.z_index = -1
			hb_f.add_child(bg_r)
		var cols_fin: Array = [str(pos_n), eq_f.get("nombre_corto","?"), str(fila.get("PJ",0)),
			str(fila.get("PG",0)), str(fila.get("PE",0)), str(fila.get("PP",0)), gd_str, str(fila.get("Pts",0))]
		var ws_fin: Array = [32,190,32,32,32,32,40,40]
		for ci in range(cols_fin.size()):
			var lc := _mk_lbl(str(cols_fin[ci]), 11 if ci != 7 else 12, ci == 7)
			lc.custom_minimum_size = Vector2(ws_fin[ci] if ci < ws_fin.size() else 40, 22)
			if eid == _eq_id:
				lc.add_theme_color_override("font_color", C_ACCENT)
			hb_f.add_child(lc)
		vb.add_child(hb_f)

	vb.add_child(_mk_sep())

	# Descensos
	if not descendidos.is_empty():
		vb.add_child(_mk_seccion("DESCENSOS"))
		for d in descendidos:
			var eq_d: Dictionary = DB.obtener_equipo(int(d.get("equipo_id",0)))
			var lbl_d := _mk_lbl("▼  %s" % eq_d.get("nombre_corto","?"), 13)
			lbl_d.add_theme_color_override("font_color", C_RED)
			vb.add_child(lbl_d)
		vb.add_child(_mk_sep())

	# Tu desempeño
	var pos_final: int = _posicion_liga()
	var pg_t: int = 0; var pe_t: int = 0; var pp_t: int = 0
	for r in _hist:
		var gl: int = r.get("goles_local",0); var gv: int = r.get("goles_visitante",0)
		var esl: bool = int(r.get("local_id",0)) == _eq_id
		if gl == gv: pe_t += 1
		elif (esl and gl > gv) or (not esl and gv > gl): pg_t += 1
		else: pp_t += 1
	vb.add_child(_mk_seccion("TU TEMPORADA"))
	var lbl_tu := _mk_lbl("Posición final: %d°  |  %dV %dE %dD" % [pos_final, pg_t, pe_t, pp_t], 14, true)
	lbl_tu.add_theme_color_override("font_color", C_ACCENT)
	vb.add_child(lbl_tu)
	vb.add_child(_mk_sep())

	# Botón Nueva Temporada
	var btn_nt := Button.new()
	btn_nt.text = "▶  Iniciar Temporada %d" % (_temporada + 1)
	btn_nt.custom_minimum_size = Vector2(260, 42)
	_estilo_btn(btn_nt, Color(0.9, 0.75, 0.1))
	btn_nt.add_theme_color_override("font_color", Color(0.05, 0.05, 0.05))
	btn_nt.pressed.connect(func():
		overlay.queue_free()
		_iniciar_nueva_temporada()
	)
	var c_btn := CenterContainer.new()
	c_btn.add_child(btn_nt)
	vb.add_child(c_btn)

func _iniciar_nueva_temporada() -> void:
	_temporada += 1
	_sem = 0
	_hist.clear()
	CalendarSystem.iniciar_temporada(_temporada)
	LeagueSystem.iniciar_nueva_temporada(_liga_id)
	_noticias.append("── Temporada %d iniciada ──" % _temporada)
	_refresh_all()

func _generar_noticias_semana(resultados: Array) -> void:
	var liga: Dictionary = DB.ligas.get(_liga_id, {})
	var _nombre_liga: String = liga.get("nombre", "Liga") as String

	# Goleada más llamativa
	var max_goles: int = 0
	var noticia_goleada: String = ""
	for r in resultados:
		var gl: int = r.get("goles_local", 0)
		var gv: int = r.get("goles_visitante", 0)
		var total_g: int = gl + gv
		if total_g > max_goles:
			max_goles = total_g
			var eql: Dictionary = DB.obtener_equipo(int(r.get("local_id", 0)))
			var eqv: Dictionary = DB.obtener_equipo(int(r.get("visitante_id", 0)))
			noticia_goleada = "Jornada %d: %s %d-%d %s" % [
				LeagueSystem.jornada_actual(_liga_id),
				eql.get("nombre_corto","?"), gl, gv,
				eqv.get("nombre_corto","?"),
			]

	if noticia_goleada != "":
		_noticias.append(noticia_goleada)

	# Resultado del equipo del jugador
	for r in resultados:
		var lid: int = int(r.get("local_id", 0))
		var vid: int = int(r.get("visitante_id", 0))
		if lid == _eq_id or vid == _eq_id:
			var gl: int = r.get("goles_local", 0)
			var gv: int = r.get("goles_visitante", 0)
			var eql: Dictionary = DB.obtener_equipo(lid)
			var eqv: Dictionary = DB.obtener_equipo(vid)
			var es_local: bool = lid == _eq_id
			var gano: bool = (es_local and gl > gv) or (not es_local and gv > gl)
			var empate: bool = gl == gv
			var desc: String = "Victoria" if gano else ("Empate" if empate else "Derrota")
			_noticias.append("%s del equipo: %s %d-%d %s" % [
				desc, eql.get("nombre_corto","?"), gl, gv, eqv.get("nombre_corto","?")
			])

	# Limite de noticias
	if _noticias.size() > 40:
		_noticias = _noticias.slice(_noticias.size() - 40, _noticias.size())

func _refresh_all() -> void:
	_update_hud()
	_refresh_despacho()
	_refresh_plantilla()
	_refresh_tactica()
	_refresh_mercado()
	_refresh_finanzas()
	_refresh_clasificacion()
	_refresh_calendario()

# ══════════════════════════════════════════════════════════════════════════════
# POPUP RESULTADO
# ══════════════════════════════════════════════════════════════════════════════

func _mostrar_popup_resultado(r: Dictionary, fin_temporada: bool = false) -> void:
	var overlay := ColorRect.new()
	overlay.color = Color(0, 0, 0, 0.75)
	overlay.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	overlay.z_index = 50
	add_child(overlay)

	var center := CenterContainer.new()
	center.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	overlay.add_child(center)

	var panel := PanelContainer.new()
	panel.custom_minimum_size = Vector2(420, 0)
	var ps := StyleBoxFlat.new()
	ps.bg_color = C_PANEL
	ps.border_color = C_BORDER
	ps.border_width_left = 2
	ps.border_width_right = 2
	ps.border_width_top = 2
	ps.border_width_bottom = 2
	ps.corner_radius_top_left = 8
	ps.corner_radius_top_right = 8
	ps.corner_radius_bottom_left = 8
	ps.corner_radius_bottom_right = 8
	panel.add_theme_stylebox_override("panel", ps)
	center.add_child(panel)

	var mg := MarginContainer.new()
	_set_margins(mg, 24, 20, 24, 20)
	panel.add_child(mg)

	var vb_p := VBoxContainer.new()
	vb_p.add_theme_constant_override("separation", 10)
	mg.add_child(vb_p)

	var eql: Dictionary = DB.obtener_equipo(int(r.get("local_id", 0)))
	var eqv: Dictionary = DB.obtener_equipo(int(r.get("visitante_id", 0)))
	var gl: int = r.get("goles_local", 0)
	var gv: int = r.get("goles_visitante", 0)
	var es_local: bool = int(r.get("local_id", 0)) == _eq_id
	var gano: bool  = (es_local and gl > gv) or (not es_local and gv > gl)
	var empate: bool = gl == gv

	var res_color: Color = C_GREEN if gano else (C_YELLOW if empate else C_RED)
	var res_txt: String  = "VICTORIA" if gano else ("EMPATE" if empate else "DERROTA")

	var lbl_res := _mk_lbl(res_txt, 22, true)
	lbl_res.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	lbl_res.add_theme_color_override("font_color", res_color)
	vb_p.add_child(lbl_res)

	var lbl_marcador := _mk_lbl(
		"%s  %d – %d  %s" % [eql.get("nombre_corto","?"), gl, gv, eqv.get("nombre_corto","?")],
		18, true
	)
	lbl_marcador.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	vb_p.add_child(lbl_marcador)

	vb_p.add_child(_mk_sep())

	# Goleadores
	var goleadores: Array = r.get("goleadores", [])
	if not goleadores.is_empty():
		var lbl_g := _mk_lbl("Goles:", 12, true)
		lbl_g.add_theme_color_override("font_color", C_DIM)
		vb_p.add_child(lbl_g)
		for gol in goleadores:
			var j_g: Dictionary = DB.obtener_jugador(int(gol.get("jugador_id", 0)))
			var min_g: int = gol.get("minuto", 0)
			var gl_txt: String = "  %d'  %s" % [min_g, j_g.get("nombre_corto","?")]
			vb_p.add_child(_mk_lbl(gl_txt, 12))

	vb_p.add_child(_mk_sep())

	# xG info
	var xg_l: float = r.get("xg_local", 0.0)
	var xg_v: float = r.get("xg_visitante", 0.0)
	if xg_l + xg_v > 0.0:
		var lbl_xg := _mk_lbl("xG: %.2f — %.2f" % [xg_l, xg_v], 11)
		lbl_xg.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		lbl_xg.add_theme_color_override("font_color", C_DIM)
		vb_p.add_child(lbl_xg)

	var btn_ok := Button.new()
	btn_ok.text = "Ver Fin de Temporada" if fin_temporada else "Continuar"
	btn_ok.custom_minimum_size = Vector2(200, 36)
	_estilo_btn(btn_ok, Color(0.9, 0.75, 0.1) if fin_temporada else C_ACCENT)
	if fin_temporada:
		btn_ok.add_theme_color_override("font_color", Color(0.05,0.05,0.05))
	btn_ok.pressed.connect(func():
		overlay.queue_free()
		if fin_temporada:
			_mostrar_fin_temporada()
	)
	var c_btn := CenterContainer.new()
	c_btn.add_child(btn_ok)
	vb_p.add_child(c_btn)

# ══════════════════════════════════════════════════════════════════════════════
# ACCIONES
# ══════════════════════════════════════════════════════════════════════════════

func _renovar_rapido(jug_id: int) -> void:
	var j: Dictionary = DB.obtener_jugador(jug_id)
	if j.is_empty():
		return
	var sal_actual: int = j.get("contrato", {}).get("salario_semanal", 1000)
	var sal_nuevo: int = int(float(sal_actual) * 1.10)
	var ok: bool = TransferMarket.renovar_contrato(jug_id, _eq_id, sal_nuevo, 3)
	_mostrar_notif("Renovación de %s: %s" % [j.get("nombre_corto","?"), "✓ OK (+10%% sal.)" if ok else "✗ Fallo"])
	_refresh_plantilla()

func _fichar_libre_directo(jug_id: int) -> void:
	var ok: bool = TransferMarket.fichar_agente_libre(jug_id, _eq_id)
	var j: Dictionary = DB.obtener_jugador(jug_id)
	_mostrar_notif("Fichaje de %s: %s" % [j.get("nombre_corto","?"), "✓ Completado" if ok else "✗ Fallo"])
	_refresh_plantilla()
	_refresh_mercado()

func _enviar_oferta_ui(jug_id: int, valor: int) -> void:
	var cantidad: int = int(float(valor) * 1.0)
	var res: Dictionary = TransferMarket.enviar_oferta(_eq_id, jug_id, cantidad)
	if res.get("exito", false):
		TransferMarket.procesar_ofertas_ia()
		_mostrar_notif("Oferta enviada por " + _fmt_m(cantidad))
		_noticias.append("Oferta de %s por jugador (%s)" % [DB.obtener_equipo(_eq_id).get("nombre_corto","?"), _fmt_m(cantidad)])
	else:
		_mostrar_notif("Oferta rechazada: " + str(res.get("razon", "error")))
	_refresh_mercado()

func _solicitar_prestamo(monto: int) -> void:
	var eq: Dictionary = DB.obtener_equipo(_eq_id)
	var fin: Dictionary = eq.get("finanzas", {}).duplicate()
	fin["balance"] = fin.get("balance", 0) + monto
	fin["deuda"]   = fin.get("deuda", 0) + monto
	DB.actualizar_entidad("equipo", _eq_id, {"finanzas": fin})
	_mostrar_notif("Préstamo aprobado: %s (interés 5%% anual)" % _fmt_m(monto))
	_refresh_finanzas()

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS DE JUEGO
# ══════════════════════════════════════════════════════════════════════════════

func _inicializar_titulares() -> void:
	_titulares.clear()
	var plantilla: Array = DB.obtener_plantilla(_eq_id)
	plantilla.sort_custom(func(a, b): return a.get("media", 0) > b.get("media", 0))

	var posiciones_form: Array = POSICIONES_FORM.get(_formacion, [])
	var usados: Array = []

	for pos_nombre in posiciones_form:
		var mejor_id: int = -1
		var mejor_media: int = -1
		for j in plantilla:
			var jid: int = int(j.get("id", -1))
			if jid in usados:
				continue
			var media: int = j.get("media", 0)
			if _es_pos_compatible(j.get("posicion_principal", "") as String, pos_nombre) and media > mejor_media:
				mejor_media = media
				mejor_id = jid
		# Si no hay compatible, tomar cualquiera disponible
		if mejor_id == -1:
			for j in plantilla:
				var jid: int = int(j.get("id", -1))
				if jid not in usados:
					mejor_id = jid
					break
		_titulares.append(mejor_id)
		if mejor_id != -1:
			usados.append(mejor_id)

	while _titulares.size() < 11:
		_titulares.append(-1)

	# Capitán y pateador = mejor jugador de campo
	if plantilla.size() > 0:
		_capitan_id  = int(plantilla[0].get("id", -1))
		_pateador_id = int(plantilla[min(1, plantilla.size() - 1)].get("id", -1))

func _es_pos_compatible(pos_jugador: String, pos_buscada: String) -> bool:
	var compatibles: Dictionary = {
		"PO":  ["PO"],
		"LD":  ["LD","DFC"],
		"DFC": ["DFC","LD","LI"],
		"LI":  ["LI","DFC"],
		"MCD": ["MCD","MC"],
		"MC":  ["MC","MCD","MCO"],
		"MCO": ["MCO","MC","EI","ED"],
		"EI":  ["EI","ED","DC","MCO"],
		"ED":  ["ED","EI","DC","MCO"],
		"DC":  ["DC","EI","ED"],
	}
	var lista: Array = compatibles.get(pos_buscada, [pos_buscada])
	return pos_jugador in lista

func _calcular_confianza() -> int:
	if _hist.is_empty():
		return 70
	var pg: int = 0
	var pe: int = 0
	for r in _hist:
		var gl: int = r.get("goles_local", 0)
		var gv: int = r.get("goles_visitante", 0)
		var es_local: bool = int(r.get("local_id", 0)) == _eq_id
		if gl == gv:
			pe += 1
		elif (es_local and gl > gv) or (not es_local and gv > gl):
			pg += 1
	var puntos: float = float(pg * 3 + pe) / float(max(1, _hist.size()) * 3)
	return int(clampf(40.0 + puntos * 60.0, 10.0, 100.0))

func _generar_objetivos(eq: Dictionary) -> Array:
	var rep: int = eq.get("reputacion", 50)
	var pos: int = _posicion_liga()
	var resultado: Array = []
	if rep >= 75:
		resultado.append({"texto": "Terminar en el Top 4 de la liga", "cumplido": pos > 0 and pos <= 4})
		resultado.append({"texto": "Llegar a cuartos de Champions", "cumplido": false})
	elif rep >= 55:
		resultado.append({"texto": "Clasificar a competición europea (Top 7)", "cumplido": pos > 0 and pos <= 7})
		resultado.append({"texto": "No caer en la primera mitad de la tabla", "cumplido": pos > 0 and pos <= 10})
	else:
		resultado.append({"texto": "Evitar el descenso", "cumplido": pos > 0 and pos <= 14})
		resultado.append({"texto": "Mejorar 3 posiciones respecto al año pasado", "cumplido": false})
	resultado.append({"texto": "Mantener ratio salarios < 70% de ingresos",
		"cumplido": EconomySystem.porcentaje_salarios_sobre_ingresos(_eq_id) < 70.0})
	return resultado

func _posicion_liga() -> int:
	var tabla: Array = LeagueSystem.obtener_clasificacion(_liga_id)
	for i in range(tabla.size()):
		if int(tabla[i].get("equipo_id", 0)) == _eq_id:
			return i + 1
	return 0

func _fila_equipo(tabla: Array, equipo_id: int) -> Dictionary:
	for fila in tabla:
		if int(fila.get("equipo_id", 0)) == equipo_id:
			return fila
	return {}

func _calcular_edad(fecha_nac: String) -> int:
	if fecha_nac.is_empty() or "-" not in fecha_nac:
		return 0
	var partes: PackedStringArray = fecha_nac.split("-")
	if partes.size() < 1:
		return 0
	var anio_n: int = partes[0].to_int()
	var anio_a: int = CalendarSystem.obtener_fecha_actual().get("anio", 2026)
	return anio_a - anio_n

func _barra_finanzas(vb: VBoxContainer, nombre: String, valor: int, maximo: int, color: Color) -> void:
	var hb := HBoxContainer.new()
	hb.add_theme_constant_override("separation", 10)
	vb.add_child(hb)

	var lbl_n := _mk_lbl(nombre, 11)
	lbl_n.custom_minimum_size = Vector2(240, 0)
	lbl_n.add_theme_color_override("font_color", C_DIM)
	hb.add_child(lbl_n)

	var lbl_v := _mk_lbl(_fmt_m(valor), 12, true)
	lbl_v.custom_minimum_size = Vector2(80, 0)
	lbl_v.add_theme_color_override("font_color", color)
	hb.add_child(lbl_v)

	var barra_w: int = 200
	var bg := ColorRect.new()
	bg.color = C_PANEL2
	bg.custom_minimum_size = Vector2(barra_w, 12)
	hb.add_child(bg)

	if maximo > 0:
		var fill_w: int = int(float(barra_w) * float(valor) / float(maximo))
		var fill := ColorRect.new()
		fill.color = color
		fill.custom_minimum_size = Vector2(fill_w, 12)
		bg.add_child(fill)

func _mostrar_notif(texto: String) -> void:
	var overlay := ColorRect.new()
	overlay.color = Color(0, 0, 0, 0.6)
	overlay.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	overlay.z_index = 200
	add_child(overlay)

	var center := CenterContainer.new()
	center.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	overlay.add_child(center)

	var panel := PanelContainer.new()
	panel.custom_minimum_size = Vector2(380, 0)
	var ps := StyleBoxFlat.new()
	ps.bg_color = C_PANEL
	ps.border_color = C_ACCENT
	ps.border_width_left = 2
	ps.border_width_right = 2
	ps.border_width_top = 2
	ps.border_width_bottom = 2
	ps.corner_radius_top_left = 6
	ps.corner_radius_top_right = 6
	ps.corner_radius_bottom_left = 6
	ps.corner_radius_bottom_right = 6
	panel.add_theme_stylebox_override("panel", ps)
	center.add_child(panel)

	var mg := MarginContainer.new()
	_set_margins(mg, 20, 16, 20, 16)
	panel.add_child(mg)

	var pvb := VBoxContainer.new()
	pvb.add_theme_constant_override("separation", 12)
	mg.add_child(pvb)

	var lbl := _mk_lbl(texto, 13)
	lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	pvb.add_child(lbl)

	var btn := Button.new()
	btn.text = "OK"
	btn.custom_minimum_size = Vector2(100, 32)
	_estilo_btn(btn, C_ACCENT)
	btn.pressed.connect(func(): overlay.queue_free())
	var c := CenterContainer.new()
	c.add_child(btn)
	pvb.add_child(c)

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS UI
# ══════════════════════════════════════════════════════════════════════════════

func _cargar_fondo_tab(area: Control, key: String) -> void:
	## Carga la imagen de fondo y la añade al área contenedora (NO al ScrollContainer).
	## Así el fondo queda fijo detrás del contenido aunque el usuario haga scroll.
	var extensiones: Array = ["png", "jpg", "jpeg", "webp"]
	for ext in extensiones:
		var ruta: String = "res://assets/backgrounds/%s.%s" % [key, ext]
		if ResourceLoader.exists(ruta):
			var tex = load(ruta) as Texture2D
			if tex:
				var bg := TextureRect.new()
				bg.texture = tex
				bg.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
				bg.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
				bg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
				bg.modulate = Color(1, 1, 1, 0.18)   # opacidad 18% — decorativo
				bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
				bg.visible = false   # se activa en _mostrar_tab
				area.add_child(bg)
				# Colocar DEBAJO del ScrollContainer en el árbol de renderizado
				area.move_child(bg, 0)
				_fondos[key] = bg
				break

func _clear_body(key: String) -> void:
	var vb: VBoxContainer = _bodies[key]
	for c in vb.get_children():
		c.queue_free()

func _mk_lbl(texto: String, font_size: int, bold: bool = false) -> Label:
	var l := Label.new()
	l.text = texto
	l.add_theme_font_size_override("font_size", font_size)
	if bold:
		l.add_theme_color_override("font_color", C_TEXT)
	else:
		l.add_theme_color_override("font_color", C_TEXT)
	return l

func _mk_titulo(texto: String) -> Label:
	var l := _mk_lbl(texto, 18, true)
	l.add_theme_color_override("font_color", C_TEXT)
	return l

func _mk_seccion(texto: String) -> Label:
	var l := _mk_lbl(texto, 12, true)
	l.add_theme_color_override("font_color", C_ACCENT)
	return l

func _mk_sep() -> HSeparator:
	var s := HSeparator.new()
	var st := StyleBoxFlat.new()
	st.bg_color = C_BORDER
	st.content_margin_top = 1
	st.content_margin_bottom = 1
	s.add_theme_stylebox_override("separator", st)
	return s

func _estilo_btn(btn: Button, bg: Color) -> void:
	var style := StyleBoxFlat.new()
	style.bg_color = bg
	style.border_width_left   = 1
	style.border_width_right  = 1
	style.border_width_top    = 1
	style.border_width_bottom = 1
	style.border_color               = C_BORDER
	style.corner_radius_top_left     = 4
	style.corner_radius_top_right    = 4
	style.corner_radius_bottom_left  = 4
	style.corner_radius_bottom_right = 4
	style.set_content_margin(SIDE_LEFT, 8)
	style.set_content_margin(SIDE_RIGHT, 8)
	style.set_content_margin(SIDE_TOP, 4)
	style.set_content_margin(SIDE_BOTTOM, 4)
	btn.add_theme_stylebox_override("normal", style)
	var hover := style.duplicate()
	hover.bg_color = bg.lightened(0.15)
	btn.add_theme_stylebox_override("hover", hover)
	var pressed := style.duplicate()
	pressed.bg_color = bg.darkened(0.15)
	btn.add_theme_stylebox_override("pressed", pressed)
	btn.add_theme_color_override("font_color", C_TEXT)

func _estilo_btn_nav(btn: Button, activo: bool) -> void:
	var style := StyleBoxFlat.new()
	style.bg_color            = C_ACCENT.darkened(0.2) if activo else Color(0, 0, 0, 0)
	style.border_width_bottom = 3 if activo else 0
	style.border_color        = C_ACCENT
	style.set_content_margin(SIDE_LEFT, 4)
	style.set_content_margin(SIDE_RIGHT, 4)
	style.set_content_margin(SIDE_TOP, 6)
	style.set_content_margin(SIDE_BOTTOM, 6)
	btn.add_theme_stylebox_override("normal",  style)
	btn.add_theme_stylebox_override("hover",   style)
	btn.add_theme_stylebox_override("pressed", style)
	btn.add_theme_color_override("font_color", C_TEXT if activo else C_DIM)

func _mk_card(titulo: String, valor: String, color_val: Color) -> PanelContainer:
	var card  := PanelContainer.new()
	var style := StyleBoxFlat.new()
	style.bg_color            = C_PANEL
	style.border_width_left   = 1
	style.border_width_right  = 1
	style.border_width_top    = 1
	style.border_width_bottom = 1
	style.border_color               = C_BORDER
	style.corner_radius_top_left     = 6
	style.corner_radius_top_right    = 6
	style.corner_radius_bottom_left  = 6
	style.corner_radius_bottom_right = 6
	card.add_theme_stylebox_override("panel", style)
	card.size_flags_horizontal = Control.SIZE_EXPAND_FILL

	var mg := MarginContainer.new()
	_set_margins(mg, 12, 8, 12, 8)
	card.add_child(mg)

	var vb := VBoxContainer.new()
	vb.add_theme_constant_override("separation", 3)
	mg.add_child(vb)

	var lbl_t := _mk_lbl(titulo, 10)
	lbl_t.add_theme_color_override("font_color", C_DIM)
	vb.add_child(lbl_t)

	var lbl_v := _mk_lbl(valor, 15, true)
	lbl_v.add_theme_color_override("font_color", color_val)
	vb.add_child(lbl_v)

	return card

func _mk_fila_tabla(cols: Array, cabecera: bool, widths: Array = []) -> HBoxContainer:
	var hb := HBoxContainer.new()
	hb.add_theme_constant_override("separation", 0)
	var default_widths: Array = [44,160,60,38,38,80,90,70,44,44,44,80]
	var w_arr: Array = widths if not widths.is_empty() else default_widths
	for i in range(cols.size()):
		var w: int = w_arr[i] if i < w_arr.size() else 70
		var l := _mk_lbl(str(cols[i]), 11 if cabecera else 12, cabecera)
		l.custom_minimum_size = Vector2(w, 22)
		if cabecera:
			l.add_theme_color_override("font_color", C_DIM)
		hb.add_child(l)
	return hb

func _set_margins(node: MarginContainer, l: int, t: int, r: int, b: int) -> void:
	node.add_theme_constant_override("margin_left",   l)
	node.add_theme_constant_override("margin_top",    t)
	node.add_theme_constant_override("margin_right",  r)
	node.add_theme_constant_override("margin_bottom", b)

func _fmt_m(cantidad: int) -> String:
	if cantidad >= 1_000_000_000:
		return "%.2fB" % (float(cantidad) / 1_000_000_000.0)
	if cantidad >= 1_000_000:
		return "%.2fM" % (float(cantidad) / 1_000_000.0)
	if cantidad >= 1_000:
		return "%.1fK" % (float(cantidad) / 1_000.0)
	return str(cantidad)
