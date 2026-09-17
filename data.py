# data.py
# Base de datos local de fútbol. Todo está en español.
# Puedes agregar más equipos, ligas y partidos aquí.

LIGAS = {
    "la_liga": {
        "nombre": "La Liga (España)",
        "equipos": ["Real Madrid", "Barcelona", "Atlético de Madrid", "Sevilla", "Real Sociedad", "Villarreal", "Betis", "Valencia"]
    },
    "premier": {
        "nombre": "Premier League (Inglaterra)",
        "equipos": ["Manchester City", "Arsenal", "Liverpool", "Chelsea", "Manchester United", "Tottenham", "Newcastle", "Aston Villa"]
    },
    "serie_a": {
        "nombre": "Serie A (Italia)",
        "equipos": ["Inter de Milán", "AC Milan", "Juventus", "Napoli", "Roma", "Lazio", "Atalanta", "Fiorentina"]
    },
    "bundesliga": {
        "nombre": "Bundesliga (Alemania)",
        "equipos": ["Bayern de Múnich", "Borussia Dortmund", "RB Leipzig", "Bayer Leverkusen", "Eintracht Frankfurt", "Wolfsburgo"]
    },
    "ligue_1": {
        "nombre": "Ligue 1 (Francia)",
        "equipos": ["Paris Saint-Germain", "Marsella", "Lyon", "Mónaco", "Lille", "Niza"]
    },
}

# Partidos de ejemplo (se muestran como demostración)
# Formato: fecha (YYYY-MM-DD), liga, local, visitante, marcador (None si no ha terminado)
PARTIDOS = [
    {"fecha": "2025-09-20", "liga": "la_liga", "local": "Real Madrid", "visitante": "Barcelona", "marcador": None},
    {"fecha": "2025-09-20", "liga": "premier", "local": "Manchester City", "visitante": "Arsenal", "marcador": None},
    {"fecha": "2025-09-21", "liga": "serie_a", "local": "Inter de Milán", "visitante": "Juventus", "marcador": None},
    {"fecha": "2025-09-21", "liga": "bundesliga", "local": "Bayern de Múnich", "visitante": "Borussia Dortmund", "marcador": None},
    {"fecha": "2025-09-22", "liga": "ligue_1", "local": "Paris Saint-Germain", "visitante": "Marsella", "marcador": None},
    {"fecha": "2025-09-19", "liga": "la_liga", "local": "Atlético de Madrid", "visitante": "Sevilla", "marcador": [2, 1]},
    {"fecha": "2025-09-19", "liga": "premier", "local": "Liverpool", "visitante": "Chelsea", "marcador": [1, 1]},
]

# Frases motivacionales en español para el mensaje diario
FRASES_DIARIAS = [
    "⚽ ¡El fútbol no se detiene! Aquí tienes las últimas novedades.",
    "🔥 Nuevos resultados y próximos partidos disponibles.",
    "📣 Mantente al día con toda la acción futbolística.",
    "🏟️ La jornada continúa. Esto es lo que necesitas saber.",
    "🎯 Información actualizada de las principales ligas europeas.",
]
