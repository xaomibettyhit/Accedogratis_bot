# data.py
# Base de datos de actrices de Hollywood. Añade tantas como quieras.
# Cada entrada: name, birth, nationality, notable_films, awards, bio, category

ACTRESSES = {
    "scarlett johansson": {
        "name": "Scarlett Johansson",
        "birth": "22 de noviembre de 1984",
        "nationality": "Estadounidense",
        "notable_films": ["Lost in Translation", "Historia de un matrimonio", "Viuda Negra", "Jojo Rabbit"],
        "awards": ["Premio Tony", "Premio BAFTA", "Múltiples nominaciones al Óscar"],
        "bio": "Una de las actrices mejor pagadas del mundo, conocida tanto por papeles taquilleros como por interpretaciones dramáticas.",
        "category": "Primera Línea"
    },
    "meryl streep": {
        "name": "Meryl Streep",
        "birth": "22 de junio de 1949",
        "nationality": "Estadounidense",
        "notable_films": ["El diablo viste de Prada", "La decisión de Sophie", "Kramer contra Kramer", "La dama de hierro"],
        "awards": ["3 Premios Óscar", "8 Globos de Oro", "2 Premios BAFTA"],
        "bio": "Considerada una de las mejores actrices de todos los tiempos, con un récord de 21 nominaciones al Óscar.",
        "category": "Ganadoras del Óscar"
    },
    "emma stone": {
        "name": "Emma Stone",
        "birth": "6 de noviembre de 1988",
        "nationality": "Estadounidense",
        "notable_films": ["La La Land", "Pobres criaturas", "La favorita", "Fácil de amar"],
        "awards": ["2 Premios Óscar", "Premio BAFTA", "Globo de Oro"],
        "bio": "Conocida por su versatilidad en musicales, comedia y papeles dramáticos.",
        "category": "Ganadoras del Óscar"
    },
    "jennifer lawrence": {
        "name": "Jennifer Lawrence",
        "birth": "15 de agosto de 1990",
        "nationality": "Estadounidense",
        "notable_films": ["El lado bueno de las cosas", "Los juegos del hambre", "Escándalo americano", "Joy"],
        "awards": ["Premio Óscar", "Premio BAFTA", "Globo de Oro"],
        "bio": "Alcanzó fama mundial gracias a la saga Los juegos del hambre y aclamados papeles dramáticos.",
        "category": "Primera Línea"
    },
    "natalie portman": {
        "name": "Natalie Portman",
        "birth": "9 de junio de 1981",
        "nationality": "Israelí-Estadounidense",
        "notable_films": ["Cisne negro", "V de Vendetta", "Jackie", "Thor"],
        "awards": ["Premio Óscar", "Globo de Oro", "Premio BAFTA"],
        "bio": "Actriz formada en Harvard, conocida por intensas interpretaciones dramáticas y papeles taquilleros.",
        "category": "Ganadoras del Óscar"
    },
    "zendaya": {
        "name": "Zendaya",
        "birth": "1 de septiembre de 1996",
        "nationality": "Estadounidense",
        "notable_films": ["Dune", "Spider-Man: No Way Home", "Euphoria", "Challengers"],
        "awards": ["2 Premios Emmy", "Globo de Oro"],
        "bio": "Una estrella definitoria de su generación, con éxito tanto en música, moda como en cine.",
        "category": "Nueva Generación"
    },
    "florence pugh": {
        "name": "Florence Pugh",
        "birth": "3 de enero de 1996",
        "nationality": "Británica",
        "notable_films": ["Mujercitas", "Midsommar", "Oppenheimer", "Viuda Negra"],
        "awards": ["Premio BAFTA a Estrella Emergente", "Nominación al Óscar"],
        "bio": "Aclamada por interpretaciones audaces y emocionalmente crudas en películas independientes y taquilleras.",
        "category": "Nueva Generación"
    },
    "margot robbie": {
        "name": "Margot Robbie",
        "birth": "2 de julio de 1990",
        "nationality": "Australiana",
        "notable_films": ["Barbie", "Yo, Tonya", "El lobo de Wall Street", "Escuadrón Suicida"],
        "awards": ["Nominaciones al Óscar", "Nominaciones al BAFTA"],
        "bio": "Actriz y productora australiana conocida tanto por éxitos comerciales como por transformaciones dramáticas.",
        "category": "Primera Línea"
    },
    "charlize theron": {
        "name": "Charlize Theron",
        "birth": "7 de agosto de 1975",
        "nationality": "Sudafricana-Estadounidense",
        "notable_films": ["Monster", "Mad Max: Furia en la carretera", "Atómica", "El escándalo"],
        "awards": ["Premio Óscar", "Globo de Oro", "Premio del Sindicato de Actores"],
        "bio": "Conocida por papeles de acción físicamente exigentes y valientes transformaciones dramáticas.",
        "category": "Ganadoras del Óscar"
    },
    "viola davis": {
        "name": "Viola Davis",
        "birth": "11 de agosto de 1965",
        "nationality": "Estadounidense",
        "notable_films": ["Fences", "Criadas y señoras", "La madre del blues", "La mujer rey"],
        "awards": ["Premio Óscar", "Premio Emmy", "Premio Tony"],
        "bio": "Una de las pocas artistas en lograr la 'Triple Corona de la Actuación': Óscar, Emmy y Tony.",
        "category": "Ganadoras del Óscar"
    },
}

CATEGORIES = ["Primera Línea", "Ganadoras del Óscar", "Nueva Generación"]
