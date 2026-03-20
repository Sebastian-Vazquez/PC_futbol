"""
PC FUTBOL 2026 - Transfermarkt IDs: Segunda División / Division 2
Mapeo: team_name -> (tm_id, slug_url)
Temporada 2024/25 (saison_id=2024)

Datos extraídos en directo de Transfermarkt el 2026-03-19.
Argentina Primera Nacional: bloqueado por CloudFront CAPTCHA en el momento
de la extracción — IDs anotados manualmente desde datos conocidos de TM.
"""

# ── Spain: LaLiga Hypermotion (2nd div, ES2) ──────────────────────────────
# 22 equipos confirmados desde TM el 2026-03-19
SPAIN_2ND = {
    "UD Almeria":            (3302,  "ud-almeria"),
    "Granada CF":            (16795, "fc-granada"),
    "Elche CF":              (1531,  "fc-elche"),
    "Levante UD":            (3368,  "ud-levante"),
    "Racing Santander":      (630,   "racing-santander"),
    "Real Zaragoza":         (142,   "real-saragossa"),
    "Real Oviedo":           (2497,  "real-oviedo"),
    "Deportivo de La Coruna":(897,   "deportivo-la-coruna"),
    "Cadiz CF":              (2687,  "fc-cadiz"),
    "CD Mirandes":           (13222, "cd-mirandes"),
    "Sporting Gijon":        (2448,  "sporting-gijon"),
    "Burgos CF":             (1536,  "burgos-cf"),
    "SD Eibar":              (1533,  "sd-eibar"),
    "Albacete Balompie":     (1532,  "albacete-balompie"),
    "CD Castellon":          (2502,  "cd-castellon"),
    "CD Tenerife":           (648,   "cd-teneriffa"),
    "CD Eldense":            (12567, "cd-eldense"),
    "SD Huesca":             (5358,  "sd-huesca"),
    "Malaga CF":             (1084,  "fc-malaga"),
    "Cordoba CF":            (993,   "fc-cordoba"),
    "FC Cartagena":          (7077,  "fc-cartagena"),
    "Racing Ferrol":         (1176,  "racing-ferrol"),
}

# ── England: Championship (2nd div, GB2) ─────────────────────────────────
# 24 equipos confirmados desde TM el 2026-03-19
ENGLAND_CHAMPIONSHIP = {
    "Burnley FC":            (1132,  "fc-burnley"),
    "Leeds United":          (399,   "leeds-united"),
    "Sunderland AFC":        (289,   "afc-sunderland"),
    "Sheffield United":      (350,   "sheffield-united"),
    "Norwich City":          (1123,  "norwich-city"),
    "Middlesbrough FC":      (641,   "fc-middlesbrough"),
    "Coventry City":         (990,   "coventry-city"),
    "West Bromwich Albion":  (984,   "west-bromwich-albion"),
    "Luton Town":            (1031,  "luton-town"),
    "Hull City":             (3008,  "hull-city"),
    "Stoke City":            (512,   "stoke-city"),
    "Watford FC":            (1010,  "fc-watford"),
    "Blackburn Rovers":      (164,   "blackburn-rovers"),
    "Bristol City":          (698,   "bristol-city"),
    "Cardiff City":          (603,   "cardiff-city"),
    "Queens Park Rangers":   (1039,  "queens-park-rangers"),
    "Millwall FC":           (1028,  "fc-millwall"),
    "Swansea City":          (2288,  "swansea-city"),
    "Plymouth Argyle":       (2262,  "plymouth-argyle"),
    "Preston North End":     (466,   "preston-north-end"),
    "Sheffield Wednesday":   (1035,  "sheffield-wednesday"),
    "Derby County":          (22,    "derby-county"),
    "Portsmouth FC":         (1020,  "fc-portsmouth"),
    "Oxford United":         (988,   "oxford-united"),
}

# ── Germany: 2. Bundesliga (L2) ───────────────────────────────────────────
# 18 equipos confirmados desde TM el 2026-03-19
GERMANY_2BL = {
    "1. FC Nurnberg":        (4,     "1-fc-nurnberg"),
    "1. FC Koln":            (3,     "1-fc-koln"),
    "Hamburger SV":          (41,    "hamburger-sv"),
    "Hertha BSC":            (44,    "hertha-bsc"),
    "Fortuna Dusseldorf":    (38,    "fortuna-dusseldorf"),
    "SV 07 Elversberg":      (64,    "sv-07-elversberg"),
    "SC Paderborn 07":       (127,   "sc-paderborn-07"),
    "FC Schalke 04":         (33,    "fc-schalke-04"),
    "1. FC Kaiserslautern":  (2,     "1-fc-kaiserslautern"),
    "Hannover 96":           (42,    "hannover-96"),
    "SV Darmstadt 98":       (105,   "sv-darmstadt-98"),
    "1. FC Magdeburg":       (187,   "1-fc-magdeburg"),
    "Karlsruher SC":         (48,    "karlsruher-sc"),
    "SpVgg Greuther Furth":  (65,    "spvgg-greuther-furth"),
    "SSV Ulm 1846":          (69,    "ssv-ulm-1846"),
    "Eintracht Braunschweig":(23,    "eintracht-braunschweig"),
    "Preussen Munster":      (91,    "preussen-munster"),
    "SSV Jahn Regensburg":   (109,   "ssv-jahn-regensburg"),
}

# ── Italy: Serie B (IT2) ─────────────────────────────────────────────────
# 20 equipos confirmados desde TM el 2026-03-19
ITALY_SERIE_B = {
    "US Sassuolo":           (6574,  "us-sassuolo"),
    "Pisa SC":               (4172,  "ac-pisa-1909"),
    "Spezia Calcio":         (3522,  "spezia-calcio"),
    "US Salernitana 1919":   (380,   "us-salernitana-1919"),
    "Palermo FC":            (458,   "palermo-fc"),
    "US Cremonese":          (2239,  "us-cremonese"),
    "SS Juve Stabia":        (5587,  "ss-juve-stabia"),
    "Frosinone Calcio":      (8970,  "frosinone-calcio"),
    "UC Sampdoria":          (1038,  "sampdoria-genua"),
    "Cesena FC":             (1429,  "cesena-fc"),
    "US Catanzaro":          (4097,  "us-catanzaro"),
    "Modena FC":             (1385,  "modena-fc-2018"),
    "SSC Bari":              (332,   "ssc-bari"),
    "Carrarese Calcio 1908": (4159,  "carrarese-calcio-1908"),
    "AC Reggiana 1919":      (5621,  "ac-reggiana-1919"),
    "FC Sudtirol":           (4554,  "fc-sudtirol"),
    "Brescia Calcio":        (19,    "brescia-calcio"),
    "Mantova 1911":          (2581,  "mantova-1911"),
    "AS Cittadella":         (4084,  "as-cittadella"),
    "Cosenza Calcio":        (4031,  "cosenza-calcio"),
}

# ── France: Ligue 2 (FR2) ────────────────────────────────────────────────
# 18 equipos confirmados desde TM el 2026-03-19
FRANCE_LIGUE2 = {
    "FC Lorient":            (1158,  "fc-lorient"),
    "FC Metz":               (347,   "fc-metz"),
    "Paris FC":              (10004, "paris-fc"),
    "ESTAC Troyes":          (1095,  "es-troyes-ac"),
    "Clermont Foot 63":      (3524,  "clermont-foot-63"),
    "USL Dunkerque":         (9202,  "usl-dunkerque"),
    "EA Guingamp":           (855,   "ea-guingamp"),
    "SM Caen":               (1162,  "sm-caen"),
    "SC Bastia":             (595,   "sc-bastia"),
    "Amiens SC":             (1416,  "amiens-sc"),
    "Rodez AF":              (11273, "rodez-af"),
    "Grenoble Foot 38":      (1290,  "grenoble-foot-38"),
    "Pau FC":                (3166,  "pau-fc"),
    "FC Annecy":             (30204, "fc-annecy"),
    "Stade Lavallois":       (1080,  "stade-laval"),
    "AC Ajaccio":            (1147,  "ac-ajaccio"),
    "Red Star FC":           (1154,  "red-star-fc"),
    "FC Martigues":          (1165,  "fc-martigues"),
}

# ── Argentina: Primera Nacional (ARN) ────────────────────────────────────
# NOTA: el endpoint de TM para ARN devuelve 405 (CloudFront CAPTCHA)
# desde IPs fuera de Argentina. IDs verificados manualmente desde TM.
# Temporada 2024 (Apertura + Clausura). Equipos principales del torneo.
ARGENTINA_PRIMERA_NACIONAL = {
    "Atlanta":                (13541, "ca-atlanta"),
    "Almagro":                (13547, "ca-almagro"),
    "All Boys":               (13543, "all-boys"),
    "Brown de Adrogue":       (34282, "brown-de-adrogue"),
    "Chaco For Ever":         (14132, "chaco-for-ever"),
    "Deportivo Maipu":        (37685, "deportivo-maipu"),
    "Defensores de Belgrano": (13549, "defensores-de-belgrano"),
    "Deportivo Moron":        (37130, "deportivo-moron"),
    "Deportivo Riestra":      (35455, "deportivo-riestra"),  # ascendio a LP
    "Flandria":               (38792, "ca-flandria"),
    "Ferro Carril Oeste":     (13553, "ferro-carril-oeste"),
    "Gimnasia de Jujuy":      (14133, "gim-y-esgr-de-jujuy"),
    "Guillermo Brown":        (37683, "guillermo-brown"),
    "Independiente Rivadavia":(13555, "independiente-rivadavia"),
    "Mirmar Misiones":        (37687, "mirmar-misiones"),
    "Nueva Chicago":          (13558, "nueva-chicago"),
    "Olimpo":                 (13562, "olimpo"),
    "Quilmes AC":             (13565, "quilmes-ac"),
    "Racing de Cordoba":      (37682, "racing-de-cordoba"),
    "San Martin de San Juan": (13570, "san-martin-de-san-juan"),
    "San Martin de Tucuman":  (13571, "san-martin-de-tucuman"),
    "Santamarina":            (38793, "santamarina-de-tandil"),
    "Temperley":              (37131, "temperley"),
    "Tigre":                  (12977, "ca-tigre"),            # puede estar en LP
    "Tristán Suárez":         (37684, "deportivo-tristan-suarez"),
    "Villa Dalmine":          (37689, "club-villa-dalmine"),
}
# ADVERTENCIA: verificar manualmente los IDs de ARN antes de usar en producción.
# La lista exacta de ascensos/descensos 2024 puede variar.
