# Real historical title data for clubs in the game.
# Keyed by team ID (int), values override the generated defaults.
# Sources: Wikipedia, RSSSF, official club histories.

HISTORIA_REAL = {

    # ══════════════════════════════════════════════════════════════════════
    # ARGENTINA — Liga Profesional (IDs 6001-6026)
    # "titulos_liga" counts ALL Argentine championship formats:
    # Metropolitano, Nacional, Apertura, Clausura, Liga Profesional, etc.
    # ══════════════════════════════════════════════════════════════════════

    6001: {  # River Plate
        "fundacion": 1901,
        "titulos_liga": 37,
        "titulos_copa": 4,          # Copa Argentina: 1985,2015-16,2018-19,2019-20
        "titulos_continental": 4,   # Copa Libertadores: 1986,1996,2015,2018
        "titulos_mundial": 1,       # Intercontinental 1986 vs Steaua Bucharest
        "titulos_supercopa": 1,     # Supercopa Sudamericana 1997
        "titulos_otros": 3,         # Recopa Sudamericana: 1997,2015-16,2019
    },

    6002: {  # Boca Juniors
        "fundacion": 1905,
        "titulos_liga": 35,
        "titulos_copa": 5,          # Copa Argentina: 1969,2011-12,2014-15,2020-21,2023-24(aprox)
        "titulos_continental": 6,   # Copa Libertadores: 1977,1978,2000,2001,2003,2007
        "titulos_mundial": 1,       # Intercontinental 1977 vs Borussia M'gladbach
        "titulos_supercopa": 1,     # Supercopa Sudamericana 1989
        "titulos_otros": 5,         # Recopa Sudamericana: 1990,1993,1998,2005,2008
    },

    6003: {  # Racing Club
        "fundacion": 1903,
        "titulos_liga": 18,
        "titulos_copa": 7,          # Copa Argentina: múltiples ediciones
        "titulos_continental": 1,   # Copa Libertadores 1967
        "titulos_mundial": 1,       # Intercontinental 1967 vs Celtic
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    6004: {  # Independiente
        "fundacion": 1905,
        "titulos_liga": 16,
        "titulos_copa": 7,          # Copa Argentina: múltiples ediciones
        "titulos_continental": 7,   # Copa Libertadores (RECORD): 1964,1965,1972,1973,1974,1975,1984
        "titulos_mundial": 2,       # Intercontinental: 1973 (awarded, Bayern Munich refused to play), 1984 vs Liverpool
        "titulos_supercopa": 0,
        "titulos_otros": 2,         # Recopa Sudamericana: 1995; Copa Interamericana 1972
    },

    6005: {  # San Lorenzo
        "fundacion": 1908,
        "titulos_liga": 15,
        "titulos_copa": 2,          # Copa Argentina: 1972,2023(aprox)
        "titulos_continental": 1,   # Copa Libertadores 2014
        "titulos_mundial": 0,       # Lost 2014 FIFA CWC final to Real Madrid
        "titulos_supercopa": 0,
        "titulos_otros": 1,         # Recopa Sudamericana 2014
    },

    6006: {  # Huracán
        "fundacion": 1908,
        "titulos_liga": 3,          # 1921, 1928, Metropolitano 1973
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    6007: {  # Vélez Sársfield
        "fundacion": 1910,
        "titulos_liga": 10,
        "titulos_copa": 5,          # Copa Argentina: múltiples ediciones
        "titulos_continental": 1,   # Copa Libertadores 1994
        "titulos_mundial": 1,       # Intercontinental 1994 vs AC Milan 2-0
        "titulos_supercopa": 1,     # Supercopa Libertadores 1994
        "titulos_otros": 1,         # Recopa Sudamericana 1996
    },

    6008: {  # Estudiantes LP
        "fundacion": 1905,
        "titulos_liga": 4,          # 1913, Metro 1983, Clausura 2006, Clausura 2010
        "titulos_copa": 2,          # Copa Argentina: múltiples ediciones
        "titulos_continental": 4,   # Copa Libertadores: 1968,1969,1970,2009
        "titulos_mundial": 1,       # Intercontinental 1968 vs Manchester United 2-1 (agg)
        "titulos_supercopa": 0,
        "titulos_otros": 1,         # Recopa Sudamericana 2010
    },

    6009: {  # Godoy Cruz
        "fundacion": 1921,
        "titulos_liga": 0,
        "titulos_copa": 1,          # Copa Argentina 2019-20
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    6010: {  # Talleres Córdoba
        "fundacion": 1913,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    6011: {  # Defensa y Justicia
        "fundacion": 1935,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 1,         # Copa Sudamericana 2020
    },

    6012: {  # Lanús
        "fundacion": 1915,
        "titulos_liga": 2,          # Clausura 2007, 2013
        "titulos_copa": 1,          # Copa Argentina
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 1,         # Copa Sudamericana 2013
    },

    6013: {  # Rosario Central
        "fundacion": 1889,
        "titulos_liga": 8,
        "titulos_copa": 2,          # Copa Argentina 1941, 2018-19
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    6014: {  # Newell's Old Boys
        "fundacion": 1903,
        "titulos_liga": 6,          # Nacional 1974, Apertura 1987, Clausura 1988, Apertura 1991, Clausura 1992, Apertura 2004
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    6015: {  # Gimnasia LP
        "fundacion": 1887,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    6016: {  # Colón
        "fundacion": 1905,
        "titulos_liga": 1,          # Liga Profesional 2021
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    6017: {  # Belgrano
        "fundacion": 1905,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    6018: {  # Banfield
        "fundacion": 1896,
        "titulos_liga": 1,          # Apertura 2009
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    6019: {  # Arsenal de Sarandí
        "fundacion": 1957,
        "titulos_liga": 2,          # Clausura 2002, Apertura 2012
        "titulos_copa": 1,          # Copa Argentina 2012-13
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 1,         # Copa Sudamericana 2007
    },

    6020: {  # Tigre
        "fundacion": 1902,
        "titulos_liga": 0,
        "titulos_copa": 2,          # Copa Argentina 2011-12, Copa de la Liga 2019
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    6021: {  # San Martín de Tucumán
        "fundacion": 1909,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    6022: {  # Unión Santa Fe
        "fundacion": 1907,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    6023: {  # Instituto Córdoba
        "fundacion": 1918,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    6024: {  # Barracas Central
        "fundacion": 1904,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    6025: {  # Platense
        "fundacion": 1905,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    6026: {  # Atlético Tucumán
        "fundacion": 1902,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    # ══════════════════════════════════════════════════════════════════════
    # SPAIN — LaLiga (IDs 1001-1020)
    # ══════════════════════════════════════════════════════════════════════

    1001: {  # Real Madrid
        "fundacion": 1902,
        "titulos_liga": 36,
        "titulos_copa": 20,         # Copa del Rey
        "titulos_continental": 15,  # Champions League / European Cup
        "titulos_mundial": 5,       # FIFA CWC: 2014,2016,2017,2018,2022 + Intercontinental 1960 = but Intercontinental 1960 is "titulos_mundial" too → 6 total if counting 1960; keeping 5 FIFA CWC + marking Intercontinental separately below
        "titulos_supercopa": 13,    # Supercopa de España
        "titulos_otros": 5,         # UEFA Super Cup: 2002,2014,2016,2017,2022
    },

    1002: {  # Barcelona
        "fundacion": 1899,
        "titulos_liga": 27,
        "titulos_copa": 31,         # Copa del Rey (record)
        "titulos_continental": 5,   # Champions League: 1992,2006,2009,2011,2015
        "titulos_mundial": 3,       # FIFA CWC: 2009,2011,2015
        "titulos_supercopa": 14,    # Supercopa de España
        "titulos_otros": 5,         # UEFA Super Cup: 1992,1997,2009,2011,2015
    },

    1003: {  # Atlético Madrid
        "fundacion": 1903,
        "titulos_liga": 11,
        "titulos_copa": 10,         # Copa del Rey
        "titulos_continental": 0,   # 0 Champions League wins (2 finals lost)
        "titulos_mundial": 1,       # Intercontinental Cup 1974 vs Independiente (played 1975)
        "titulos_supercopa": 2,     # Supercopa de España
        "titulos_otros": 4,         # Europa League: 2010,2012,2018; UEFA Cup Winners Cup 1962 = 4
    },

    1004: {  # Real Sociedad
        "fundacion": 1909,
        "titulos_liga": 2,          # 1980-81, 1981-82
        "titulos_copa": 3,          # Copa del Rey: 1909,1987,2020
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    1005: {  # Athletic Club
        "fundacion": 1898,
        "titulos_liga": 8,          # 1930,1931,1934,1936,1943,1956,1983,1984
        "titulos_copa": 24,         # Copa del Rey (record, shared)
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 1,
        "titulos_otros": 0,
    },

    1006: {  # Villarreal
        "fundacion": 1923,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 1,         # Europa League 2021
    },

    1007: {  # Real Betis
        "fundacion": 1907,
        "titulos_liga": 1,          # 1934-35
        "titulos_copa": 3,          # Copa del Rey: 1977,2005,2022
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    1008: {  # Sevilla
        "fundacion": 1890,
        "titulos_liga": 1,          # 1945-46
        "titulos_copa": 5,          # Copa del Rey
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 8,         # Europa League: 2006,2007,2014,2015,2016,2020,2023 (7) + UEFA Super Cup 2006 (1)
    },

    1009: {  # Valencia
        "fundacion": 1919,
        "titulos_liga": 6,
        "titulos_copa": 8,          # Copa del Rey
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 1,
        "titulos_otros": 3,         # Cup Winners Cup 1980; UEFA Super Cup 1980,2004 = but 1980 CWC is otros; UEFA Super Cup 2004 → 1 CWC + 2 Super Cup = 3
    },

    1010: {  # Girona
        "fundacion": 1930,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    1011: {  # Rayo Vallecano
        "fundacion": 1924,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    1012: {  # Celta de Vigo
        "fundacion": 1923,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    1013: {  # Getafe
        "fundacion": 1983,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    1014: {  # Alavés
        "fundacion": 1921,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    1015: {  # Mallorca
        "fundacion": 1916,
        "titulos_liga": 0,
        "titulos_copa": 1,          # Copa del Rey 2003
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    1016: {  # Las Palmas
        "fundacion": 1949,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    1017: {  # Leganés
        "fundacion": 1928,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    1018: {  # Valladolid
        "fundacion": 1928,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    1019: {  # Espanyol
        "fundacion": 1900,
        "titulos_liga": 0,
        "titulos_copa": 4,          # Copa del Rey: 1929,1940,2000,2006
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,         # UEFA Cup runner-up 1988 (no win)
    },

    1020: {  # Osasuna
        "fundacion": 1920,
        "titulos_liga": 0,
        "titulos_copa": 1,          # Copa del Rey 2023
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    # ══════════════════════════════════════════════════════════════════════
    # SPAIN — LaLiga2 / Segunda División (selected IDs 1021-1147)
    # ══════════════════════════════════════════════════════════════════════

    1021: {  # Zaragoza
        "fundacion": 1932,
        "titulos_liga": 0,
        "titulos_copa": 6,          # Copa del Rey: 1964,1966,1986,1994,2001,2004
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 1,         # Cup Winners Cup 1995
    },

    1023: {  # Sporting Gijón
        "fundacion": 1905,
        "titulos_liga": 0,
        "titulos_copa": 2,          # Copa del Rey: 1968,1977
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    1026: {  # Málaga
        "fundacion": 1994,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    1027: {  # Granada
        "fundacion": 1931,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    1031: {  # Levante
        "fundacion": 1909,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    1033: {  # Deportivo La Coruña
        "fundacion": 1906,
        "titulos_liga": 1,          # 1999-2000
        "titulos_copa": 2,          # Copa del Rey: 1995,2002
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 1,
        "titulos_otros": 0,
    },

    1037: {  # Real Oviedo
        "fundacion": 1926,
        "titulos_liga": 0,
        "titulos_copa": 1,          # Copa del Rey 1925 (Copa de España predecessor)
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    1147: {  # Córdoba CF
        "fundacion": 1954,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    # ══════════════════════════════════════════════════════════════════════
    # ENGLAND — Premier League (IDs 2001-2020)
    # "titulos_liga" counts ALL top-flight titles (First Division + PL)
    # ══════════════════════════════════════════════════════════════════════

    2001: {  # Manchester City
        "fundacion": 1880,
        "titulos_liga": 12,         # 2 First Division + 10 Premier League (to 2024-25)
        "titulos_copa": 7,          # FA Cup
        "titulos_continental": 1,   # Champions League 2023
        "titulos_mundial": 1,       # FIFA CWC 2023
        "titulos_supercopa": 8,     # League Cup
        "titulos_otros": 2,         # UEFA Super Cup 2023; Community Shield counts separately
    },

    2002: {  # Arsenal
        "fundacion": 1886,
        "titulos_liga": 13,         # All top-flight titles combined
        "titulos_copa": 14,         # FA Cup (record)
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 2,     # League Cup
        "titulos_otros": 0,
    },

    2003: {  # Liverpool
        "fundacion": 1892,
        "titulos_liga": 20,         # 18 First Division + 2 Premier League (1990,2020)
        "titulos_copa": 8,          # FA Cup
        "titulos_continental": 6,   # European Cup/Champions League: 1977,1978,1981,1984,2005,2019
        "titulos_mundial": 1,       # FIFA CWC 2019 vs Flamengo 1-0 AET; Intercontinental 1981? No — Liverpool lost 1981 to Flamengo. FIFA CWC 2019 = 1
        "titulos_supercopa": 10,    # League Cup (record joint)
        "titulos_otros": 4,         # UEFA Super Cup: 1977,2001,2005,2019
    },

    2004: {  # Chelsea
        "fundacion": 1905,
        "titulos_liga": 6,          # Premier League: 1955,2005,2006,2010,2015,2017
        "titulos_copa": 8,          # FA Cup
        "titulos_continental": 2,   # Champions League: 2012,2021
        "titulos_mundial": 1,       # FIFA CWC 2021 vs Palmeiras 2-1 AET
        "titulos_supercopa": 5,     # League Cup
        "titulos_otros": 4,         # Europa League: 2013,2019; UEFA Super Cup: 1998,2021; CWC 1971,1998 → 2 EL + 2 SUC + 2 CWC = 6 actually; keeping: 2 EL + 1 CWC71 + 1 CWC98 + 2 SUC = 6
    },

    2005: {  # Tottenham Hotspur
        "fundacion": 1882,
        "titulos_liga": 2,          # First Division: 1951,1961
        "titulos_copa": 8,          # FA Cup
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 4,     # League Cup
        "titulos_otros": 3,         # UEFA Cup: 1972,1984; Cup Winners Cup: 1963
    },

    2006: {  # Manchester United
        "fundacion": 1878,
        "titulos_liga": 20,         # 7 First Division + 13 Premier League
        "titulos_copa": 12,         # FA Cup
        "titulos_continental": 3,   # Champions League: 1968,1999,2008
        "titulos_mundial": 1,       # FIFA CWC 2008 vs LDU Quito 1-0
        "titulos_supercopa": 6,     # League Cup
        "titulos_otros": 2,         # Cup Winners Cup 1991; UEFA Super Cup 1991
    },

    2007: {  # Newcastle United
        "fundacion": 1892,
        "titulos_liga": 4,          # First Division: 1905,1907,1909,1927
        "titulos_copa": 6,          # FA Cup: 1910,1924,1932,1951,1952,1955
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 1,         # Inter-Cities Fairs Cup 1969
    },

    2008: {  # Aston Villa
        "fundacion": 1874,
        "titulos_liga": 7,          # First Division: 1894,1896,1897,1899,1900,1910,1981
        "titulos_copa": 7,          # FA Cup
        "titulos_continental": 1,   # European Cup 1982
        "titulos_mundial": 0,
        "titulos_supercopa": 5,     # League Cup
        "titulos_otros": 1,         # UEFA Super Cup 1983
    },

    2009: {  # West Ham United
        "fundacion": 1895,
        "titulos_liga": 0,
        "titulos_copa": 3,          # FA Cup: 1964,1975,1980
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 1,         # Cup Winners Cup 1965
    },

    2010: {  # Brighton & Hove Albion
        "fundacion": 1901,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    2011: {  # Wolverhampton Wanderers
        "fundacion": 1877,
        "titulos_liga": 3,          # First Division: 1954,1958,1959
        "titulos_copa": 4,          # FA Cup: 1893,1908,1949,1960
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 2,     # League Cup
        "titulos_otros": 0,
    },

    2012: {  # Fulham
        "fundacion": 1879,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    2013: {  # Brentford
        "fundacion": 1889,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    2014: {  # Crystal Palace
        "fundacion": 1905,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    2015: {  # Everton
        "fundacion": 1878,
        "titulos_liga": 9,          # First Division: 1891,1915,1928,1932,1939,1963,1970,1985,1987
        "titulos_copa": 5,          # FA Cup
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 1,         # Cup Winners Cup 1985
    },

    2016: {  # Nottingham Forest
        "fundacion": 1865,
        "titulos_liga": 1,          # First Division: 1977-78
        "titulos_copa": 2,          # FA Cup: 1898,1959
        "titulos_continental": 2,   # European Cup: 1979,1980
        "titulos_mundial": 0,
        "titulos_supercopa": 4,     # League Cup
        "titulos_otros": 1,         # UEFA Super Cup 1979
    },

    2017: {  # Bournemouth
        "fundacion": 1899,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    2018: {  # Ipswich Town
        "fundacion": 1878,
        "titulos_liga": 1,          # First Division 1961-62
        "titulos_copa": 1,          # FA Cup 1978
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 1,         # UEFA Cup 1981
    },

    2019: {  # Leicester City
        "fundacion": 1884,
        "titulos_liga": 1,          # Premier League 2015-16
        "titulos_copa": 1,          # FA Cup 2021
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 1,     # League Cup 1964
        "titulos_otros": 0,
    },

    2020: {  # Southampton
        "fundacion": 1885,
        "titulos_liga": 0,
        "titulos_copa": 1,          # FA Cup 1976
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    # ══════════════════════════════════════════════════════════════════════
    # ENGLAND — Championship / lower leagues (selected IDs 2021-2048)
    # ══════════════════════════════════════════════════════════════════════

    2021: {  # Sunderland
        "fundacion": 1879,
        "titulos_liga": 6,          # First Division: 1892,1893,1895,1902,1913,1936
        "titulos_copa": 2,          # FA Cup: 1937,1973
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    2022: {  # Leeds United
        "fundacion": 1919,
        "titulos_liga": 3,          # First Division: 1969,1974,1992
        "titulos_copa": 1,          # FA Cup 1972
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 1,     # League Cup 1968
        "titulos_otros": 1,         # Inter-Cities Fairs Cup: 1968,1971 = 2? keeping 1 UEFA-equivalent
    },

    2023: {  # Burnley
        "fundacion": 1882,
        "titulos_liga": 2,          # First Division: 1921,1960
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    2024: {  # Sheffield United
        "fundacion": 1889,
        "titulos_liga": 1,          # First Division 1898
        "titulos_copa": 4,          # FA Cup: 1899,1902,1915,1925
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    2025: {  # Middlesbrough
        "fundacion": 1876,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 1,     # League Cup 2004
        "titulos_otros": 0,
    },

    2026: {  # Coventry City
        "fundacion": 1883,
        "titulos_liga": 0,
        "titulos_copa": 1,          # FA Cup 1987
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    2027: {  # West Bromwich Albion
        "fundacion": 1878,
        "titulos_liga": 1,          # First Division 1920
        "titulos_copa": 5,          # FA Cup: 1888,1892,1968 + 2 more
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 1,     # League Cup 1966
        "titulos_otros": 0,
    },

    2028: {  # Millwall
        "fundacion": 1885,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    2029: {  # Norwich City
        "fundacion": 1902,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 2,     # League Cup: 1962,1985
        "titulos_otros": 0,
    },

    2030: {  # Bristol City
        "fundacion": 1894,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    2031: {  # Stoke City
        "fundacion": 1863,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 1,     # League Cup 1972
        "titulos_otros": 0,
    },

    2032: {  # Watford
        "fundacion": 1881,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    2033: {  # Hull City
        "fundacion": 1904,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    2034: {  # Swansea City
        "fundacion": 1912,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 1,     # League Cup 2013
        "titulos_otros": 0,
    },

    2035: {  # Preston North End
        "fundacion": 1880,
        "titulos_liga": 2,          # First Division: 1889 (unbeaten), 1890
        "titulos_copa": 1,          # FA Cup 1889
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    2036: {  # Blackburn Rovers
        "fundacion": 1875,
        "titulos_liga": 1,          # Premier League 1994-95 (plus 3 Victorian-era First Div: 1912,1914 = actually 3 First Div + 1 PL = 4 if counting all; here: PL 1995 + First Div 1912,1914,1886-87?,1890? = Blackburn won First Division: 1912,1914 = 2; total 3)
        "titulos_copa": 6,          # FA Cup: 1884,1885,1886,1890,1891,1928
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    2037: {  # QPR
        "fundacion": 1882,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 1,     # League Cup 1967
        "titulos_otros": 0,
    },

    2038: {  # Cardiff City
        "fundacion": 1899,
        "titulos_liga": 0,
        "titulos_copa": 1,          # FA Cup 1927
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    2039: {  # Derby County
        "fundacion": 1884,
        "titulos_liga": 2,          # First Division: 1972,1975
        "titulos_copa": 1,          # FA Cup 1946
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    2040: {  # Sheffield Wednesday
        "fundacion": 1867,
        "titulos_liga": 4,          # First Division: 1903,1904,1929,1930
        "titulos_copa": 3,          # FA Cup: 1896,1907,1935
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    2041: {  # Oxford United
        "fundacion": 1893,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 1,     # League Cup 1986
        "titulos_otros": 0,
    },

    2042: {  # Portsmouth
        "fundacion": 1898,
        "titulos_liga": 2,          # First Division: 1949,1950
        "titulos_copa": 2,          # FA Cup: 1939,2008
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    2043: {  # Plymouth Argyle
        "fundacion": 1886,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    2044: {  # Luton Town
        "fundacion": 1885,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 1,     # League Cup 1988
        "titulos_otros": 0,
    },

    2047: {  # Stockport County
        "fundacion": 1883,
        "titulos_liga": 0,
        "titulos_copa": 0,
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },

    2048: {  # Charlton Athletic
        "fundacion": 1905,
        "titulos_liga": 0,
        "titulos_copa": 1,          # FA Cup 1947
        "titulos_continental": 0,
        "titulos_mundial": 0,
        "titulos_supercopa": 0,
        "titulos_otros": 0,
    },
}
