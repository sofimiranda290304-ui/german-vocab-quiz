"""
Deutsch Quiz - Aplicación tipo Kahoot para aprender vocabulario alemán.

Navegación:
    1) Pantalla de NIVEL      -> tarjetas A1 / A2 / B1
    2) Pantalla de CATEGORÍA  -> tarjetas Verbos / Sustantivos / Adjetivos / ...
    3) Pantalla de CONFIG     -> capítulos + número de preguntas
    4) Pantalla de QUIZ       -> pregunta en español, opciones en alemán

Estructura de datos esperada:
    data/<NIVEL>/Kapitel_NN.yaml   (ver README.md para el formato)

Todo lo que se puede personalizar visualmente (colores, tipografía,
colores de los botones de respuesta, etc.) está reunido en el
diccionario THEME, justo debajo de esta cabecera. No hace falta tocar
el resto del código para cambiar el estilo.
"""

import random
from pathlib import Path

import streamlit as st
import yaml

# ==========================================================================
# THEME - todo lo personalizable vive aqui
# ==========================================================================

THEME = {
    # Tipografia: cualquier nombre valido de Google Fonts
    "font": "Poppins",

    # Colores generales.
    # Formato: color solido "#RRGGBB", o un degradado CSS completo, ej:
    # "linear-gradient(135deg, #FDEBF3 0%, #F6A8C4 50%, #C77DD6 100%)"
    "background": "linear-gradient(135deg, #FDEBF3 0%, #F6C8DC 50%, #E9AEE0 100%)",
    "text_color": "#1A1A1A",

    # Tarjetas de la pantalla de NIVEL (A1 / A2 / B1)
    "nivel_card_bg": "#FDF4FB",        # fondo de la tarjeta (claro)
    "nivel_card_text": "#4C1D95",      # color del texto "A1", "A2", "B1"
    "nivel_card_height": "420px",      # alto de la tarjeta
    "nivel_pill_color": "#F472B6",     # fondo de la "píldora" con el subtítulo
    "nivel_pill_text": "#4C1D95",      # texto de la píldora
    "nivel_subtitulos": {              # texto que aparece dentro de la píldora
        "A1": "Elemental",
        "A2": "Básico",
        "B1": "Intermedio",
    },

    # Tarjetas de la pantalla de CATEGORIA (Verbos / Sustantivos / ...)
    "categoria_card_color": "#7C9885",
    "categoria_card_text": "#FFFFFF",

    # Boton principal (Iniciar Quiz, Siguiente, etc.)
    "primary_button_color": "#1368CE",
    "primary_button_text": "#FFFFFF",

    # Los 4 colores de las opciones de respuesta, estilo Kahoot
    # (orden: arriba-izq, arriba-der, abajo-izq, abajo-der)
    "option_colors": ["#E21B3C", "#1368CE", "#D89E00", "#26890C"],
    "option_text": "#FFFFFF",

    # Colores de feedback al responder
    "correct_color": "#26890C",
    "wrong_color": "#E21B3C",

    # Radio de las esquinas de todos los botones/tarjetas
    "border_radius": "16px",
}

# ==========================================================================
# Configuracion general (no visual)
# ==========================================================================

DATA_DIR = Path(__file__).parent / "data"
NIVELES = ["A1", "A2", "B1"]

CATEGORIAS_LABELS = {
    "verbos": "Verbos",
    "sustantivos": "Sustantivos",
    "adjetivos": "Adjetivos",
    "adverbios": "Adverbios",
    "preposiciones": "Preposiciones",
    "expresiones": "Expresiones",
}

st.set_page_config(page_title="Deutsch Quiz", page_icon="🇩🇪", layout="centered")

# ==========================================================================
# CSS global generado a partir de THEME
# ==========================================================================

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family={THEME["font"].replace(" ", "+")}:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: '{THEME["font"]}', sans-serif;
    }}
    .stApp {{
        background: {THEME["background"]};
        color: {THEME["text_color"]};
    }}

    div.stButton > button {{
        height: 4.2em;
        width: 100%;
        font-size: 1.05em;
        font-weight: 700;
        border-radius: {THEME["border_radius"]};
        border: none;
        white-space: normal;
        transition: transform 0.05s ease-in-out;
    }}
    div.stButton > button:active {{
        transform: scale(0.98);
    }}

    div.stButton > button[kind="primary"] {{
        background-color: {THEME["primary_button_color"]};
        color: {THEME["primary_button_text"]};
    }}

    .st-key-card_A1 div.stButton > button,
    .st-key-card_A2 div.stButton > button,
    .st-key-card_B1 div.stButton > button {{
        background-color: {THEME["nivel_card_bg"]};
        color: {THEME["nivel_card_text"]};
        height: {THEME["nivel_card_height"]};
        font-size: 2.1em;
        font-weight: 800;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        padding-top: 1.4em;
        box-shadow: 0 10px 25px rgba(0,0,0,0.10);
    }}
    .st-key-card_A1 div.stButton > button:hover,
    .st-key-card_A2 div.stButton > button:hover,
    .st-key-card_B1 div.stButton > button:hover {{
        box-shadow: 0 14px 30px rgba(0,0,0,0.16);
        transform: translateY(-2px);
    }}
    .st-key-card_A1 div.stButton > button::after {{
        content: "{THEME["nivel_subtitulos"].get("A1", "")}";
        margin-top: 0.6em;
        background: {THEME["nivel_pill_color"]};
        color: {THEME["nivel_pill_text"]};
        padding: 0.35em 1.1em;
        border-radius: 999px;
        font-size: 0.42em;
        font-weight: 700;
    }}
    .st-key-card_A2 div.stButton > button::after {{
        content: "{THEME["nivel_subtitulos"].get("A2", "")}";
        margin-top: 0.6em;
        background: {THEME["nivel_pill_color"]};
        color: {THEME["nivel_pill_text"]};
        padding: 0.35em 1.1em;
        border-radius: 999px;
        font-size: 0.42em;
        font-weight: 700;
    }}
    .st-key-card_B1 div.stButton > button::after {{
        content: "{THEME["nivel_subtitulos"].get("B1", "")}";
        margin-top: 0.6em;
        background: {THEME["nivel_pill_color"]};
        color: {THEME["nivel_pill_text"]};
        padding: 0.35em 1.1em;
        border-radius: 999px;
        font-size: 0.42em;
        font-weight: 700;
    }}

    .st-key-categoria_col div.stButton > button {{
        background-color: {THEME["categoria_card_color"]};
        color: {THEME["categoria_card_text"]};
        height: 4.6em;
        font-size: 1.15em;
        text-align: left;
        padding-left: 1.2em;
    }}

    .st-key-opt_row0 div[data-testid="column"]:nth-of-type(1) div.stButton > button {{
        background-color: {THEME["option_colors"][0]};
        color: {THEME["option_text"]};
    }}
    .st-key-opt_row0 div[data-testid="column"]:nth-of-type(2) div.stButton > button {{
        background-color: {THEME["option_colors"][1]};
        color: {THEME["option_text"]};
    }}
    .st-key-opt_row1 div[data-testid="column"]:nth-of-type(1) div.stButton > button {{
        background-color: {THEME["option_colors"][2]};
        color: {THEME["option_text"]};
    }}
    .st-key-opt_row1 div[data-testid="column"]:nth-of-type(2) div.stButton > button {{
        background-color: {THEME["option_colors"][3]};
        color: {THEME["option_text"]};
    }}
    [class*="st-key-opt_correct"] div.stButton > button {{
        background-color: {THEME["correct_color"]} !important;
        color: white !important;
    }}
    [class*="st-key-opt_wrong"] div.stButton > button {{
        background-color: {THEME["wrong_color"]} !important;
        color: white !important;
    }}

    .question-card {{
        background: linear-gradient(135deg, {THEME["primary_button_color"]}, #0c4ea3);
        color: white;
        padding: 1.6em 1.2em;
        border-radius: {THEME["border_radius"]};
        text-align: center;
        font-size: 1.6em;
        font-weight: 800;
        margin-bottom: 1.2em;
        box-shadow: 0 6px 14px rgba(0,0,0,0.15);
    }}
    .meta-tag {{
        display: inline-block;
        background: #eef2ff;
        color: {THEME["primary_button_color"]};
        padding: 0.15em 0.7em;
        border-radius: 999px;
        font-size: 0.8em;
        font-weight: 700;
        margin-bottom: 0.6em;
    }}
    .titulo-app {{
        text-align: center;
        font-weight: 800;
        margin-bottom: 0.1em;
    }}
    .subtitulo-app {{
        text-align: center;
        color: #666;
        margin-bottom: 1.5em;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================================================
# Carga de datos
# ==========================================================================

@st.cache_data(show_spinner=False)
def cargar_nivel(nivel: str):
    """Lee todos los YAML de un nivel y devuelve una lista plana de tarjetas."""
    carpeta = DATA_DIR / nivel
    tarjetas = []
    capitulos_encontrados = set()

    if not carpeta.exists():
        return tarjetas, capitulos_encontrados

    for archivo in sorted(carpeta.glob("*.yaml")):
        with open(archivo, "r", encoding="utf-8") as f:
            contenido = yaml.safe_load(f) or {}

        capitulo = contenido.get("capitulo", archivo.stem)
        capitulos_encontrados.add(capitulo)

        for categoria in CATEGORIAS_LABELS:
            for entrada in contenido.get(categoria, []) or []:
                tarjetas.append(
                    {
                        "nivel": nivel,
                        "capitulo": capitulo,
                        "categoria": categoria,
                        "aleman": entrada.get("aleman", ""),
                        "espanol": entrada.get("espanol", ""),
                        "genero": entrada.get("genero", ""),
                        "plural": entrada.get("plural", ""),
                        "tipo": entrada.get("tipo", ""),
                    }
                )
    return tarjetas, capitulos_encontrados


def texto_respuesta(tarjeta: dict) -> str:
    if tarjeta["categoria"] == "sustantivos" and tarjeta["genero"]:
        return f"{tarjeta['genero']} {tarjeta['aleman']}"
    return tarjeta["aleman"]


def generar_opciones(tarjeta: dict, pool: list, n: int = 4) -> list:
    correcta = texto_respuesta(tarjeta)
    candidatos = [
        c for c in pool
        if c["categoria"] == tarjeta["categoria"] and texto_respuesta(c) != correcta
    ]
    if len(candidatos) < n - 1:
        candidatos = [c for c in pool if texto_respuesta(c) != correcta]

    distractores = random.sample(candidatos, min(n - 1, len(candidatos)))
    opciones = [correcta] + [texto_respuesta(c) for c in distractores]
    while len(opciones) < n:
        opciones.append("—")
    random.shuffle(opciones)
    return opciones


# ==========================================================================
# Estado de la sesion
# ==========================================================================

def inicializar_estado():
    defaults = {
        "vista": "nivel",           # nivel | categoria | config | quiz
        "nivel_elegido": None,
        "categoria_elegida": None,
        "preguntas": [],
        "indice": 0,
        "puntaje": 0,
        "respondida": False,
        "opcion_elegida": None,
        "opciones_actuales": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


inicializar_estado()


def ir_a(vista, **kwargs):
    st.session_state.vista = vista
    for k, v in kwargs.items():
        st.session_state[k] = v


def iniciar_quiz(pool: list, cantidad: int):
    cantidad = min(cantidad, len(pool))
    st.session_state.preguntas = random.sample(pool, cantidad)
    st.session_state.indice = 0
    st.session_state.puntaje = 0
    st.session_state.respondida = False
    st.session_state.opcion_elegida = None
    st.session_state.opciones_actuales = generar_opciones(
        st.session_state.preguntas[0], pool
    )
    st.session_state.vista = "quiz"


def responder(opcion: str, correcta: str):
    if st.session_state.respondida:
        return
    st.session_state.respondida = True
    st.session_state.opcion_elegida = opcion
    if opcion == correcta:
        st.session_state.puntaje += 1


def siguiente_pregunta(pool: list):
    st.session_state.indice += 1
    st.session_state.respondida = False
    st.session_state.opcion_elegida = None
    if st.session_state.indice < len(st.session_state.preguntas):
        st.session_state.opciones_actuales = generar_opciones(
            st.session_state.preguntas[st.session_state.indice], pool
        )


def volver_al_inicio():
    inicializar_estado()
    st.session_state.vista = "nivel"


# ==========================================================================
# Encabezado
# ==========================================================================

st.markdown("<h1 class='titulo-app'>🇩🇪 Deutsch Quiz</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitulo-app'>Aprende vocabulario alemán · estilo Kahoot</p>",
    unsafe_allow_html=True,
)

# ==========================================================================
# PANTALLA 1 - Seleccion de nivel
# ==========================================================================

if st.session_state.vista == "nivel":
    cols = st.columns(3)
    for col, nivel in zip(cols, NIVELES):
        tarjetas_n, _ = cargar_nivel(nivel)
        with col:
            with st.container(key=f"card_{nivel}"):
                if st.button(nivel, key=f"btn_nivel_{nivel}"):
                    ir_a("categoria", nivel_elegido=nivel)
                    st.rerun()
            if not tarjetas_n:
                st.caption("Sin contenido todavía")
            else:
                st.caption(f"{len(tarjetas_n)} palabras")
    st.stop()

# ==========================================================================
# PANTALLA 2 - Seleccion de categoria
# ==========================================================================

if st.session_state.vista == "categoria":
    nivel = st.session_state.nivel_elegido
    tarjetas_nivel, capitulos_nivel = cargar_nivel(nivel)

    if st.button("← Cambiar nivel"):
        ir_a("nivel")
        st.rerun()

    st.markdown(f"### Vocabulario {nivel}")

    if not tarjetas_nivel:
        st.warning(f"Todavía no hay vocabulario cargado para el nivel {nivel}.")
        st.stop()

    categorias_disponibles = [
        c for c in CATEGORIAS_LABELS
        if any(t["categoria"] == c for t in tarjetas_nivel)
    ]

    with st.container(key="categoria_col"):
        for cat in categorias_disponibles:
            n_palabras = sum(1 for t in tarjetas_nivel if t["categoria"] == cat)
            etiqueta = f"{CATEGORIAS_LABELS[cat]}   ·   {n_palabras} palabras"
            if st.button(etiqueta, key=f"btn_cat_{cat}"):
                ir_a("config", categoria_elegida=cat)
                st.rerun()
    st.stop()

# ==========================================================================
# PANTALLA 3 - Configuracion (capitulos + numero de preguntas)
# ==========================================================================

if st.session_state.vista == "config":
    nivel = st.session_state.nivel_elegido
    categoria = st.session_state.categoria_elegida
    tarjetas_nivel, capitulos_nivel = cargar_nivel(nivel)
    capitulos_nivel = sorted(capitulos_nivel, key=lambda x: str(x))

    if st.button("← Cambiar categoría"):
        ir_a("categoria")
        st.rerun()

    st.markdown(f"### {CATEGORIAS_LABELS[categoria]} · {nivel}")

    capitulos_sel = st.multiselect(
        "Capítulos a incluir",
        options=capitulos_nivel,
        default=capitulos_nivel,
    )

    pool = [
        t for t in tarjetas_nivel
        if t["categoria"] == categoria and t["capitulo"] in capitulos_sel
    ]

    st.caption(f"Palabras disponibles con esta selección: {len(pool)}")

    max_preguntas = max(1, len(pool))
    num_preguntas = st.slider(
        "Número de preguntas",
        min_value=1,
        max_value=min(30, max_preguntas) if max_preguntas > 1 else 1,
        value=min(10, max_preguntas),
    )

    if st.button("🚀 Iniciar Quiz", type="primary", disabled=len(pool) < 2):
        iniciar_quiz(pool, num_preguntas)
        st.rerun()

    if len(pool) < 2:
        st.info("Selecciona al menos un capítulo con 2 o más palabras.")
    st.stop()

# ==========================================================================
# PANTALLA 4 - Quiz
# ==========================================================================

if st.session_state.vista == "quiz":
    nivel = st.session_state.nivel_elegido
    categoria = st.session_state.categoria_elegida
    tarjetas_nivel, _ = cargar_nivel(nivel)

    capitulos_usados = {p["capitulo"] for p in st.session_state.preguntas}
    pool = [
        t for t in tarjetas_nivel
        if t["categoria"] == categoria and t["capitulo"] in capitulos_usados
    ]

    preguntas = st.session_state.preguntas
    total = len(preguntas)
    indice = st.session_state.indice

    if indice >= total:
        st.balloons()
        st.markdown("## 🏁 ¡Quiz terminado!")
        porcentaje = round(100 * st.session_state.puntaje / total) if total else 0
        st.markdown(f"### Puntaje: {st.session_state.puntaje} / {total} ({porcentaje}%)")

        if porcentaje == 100:
            st.success("¡Perfecto! 🎉")
        elif porcentaje >= 70:
            st.success("¡Muy bien! 👏")
        elif porcentaje >= 40:
            st.warning("Vas por buen camino, sigue practicando 💪")
        else:
            st.error("Sigue practicando, ¡tú puedes! 📚")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Repetir"):
                iniciar_quiz(pool, total)
                st.rerun()
        with col2:
            if st.button("🏠 Volver al inicio"):
                volver_al_inicio()
                st.rerun()
        st.stop()

    tarjeta = preguntas[indice]
    opciones = st.session_state.opciones_actuales
    correcta = texto_respuesta(tarjeta)

    st.progress(indice / total, text=f"Pregunta {indice + 1} de {total}")
    st.markdown(
        f"<span class='meta-tag'>{CATEGORIAS_LABELS[tarjeta['categoria']]} · "
        f"Cap. {tarjeta['capitulo']}</span>",
        unsafe_allow_html=True,
    )
    st.markdown(f"<div class='question-card'>{tarjeta['espanol']}</div>", unsafe_allow_html=True)

    filas = [opciones[0:2], opciones[2:4]]
    for fila_idx, fila in enumerate(filas):
        key_row = f"opt_row{fila_idx}"
        with st.container(key=key_row):
            cols = st.columns(2)
            for col_idx, opcion in enumerate(fila):
                i = fila_idx * 2 + col_idx
                etiqueta = opcion

                if st.session_state.respondida:
                    if opcion == correcta:
                        etiqueta = f"✅ {opcion}"
                    elif opcion == st.session_state.opcion_elegida:
                        etiqueta = f"❌ {opcion}"

                contenedor_extra = None
                if st.session_state.respondida and opcion == correcta:
                    contenedor_extra = "opt_correct"
                elif st.session_state.respondida and opcion == st.session_state.opcion_elegida:
                    contenedor_extra = "opt_wrong"

                with cols[col_idx]:
                    if contenedor_extra:
                        with st.container(key=f"{contenedor_extra}_{indice}_{i}"):
                            st.button(
                                etiqueta,
                                key=f"op_{indice}_{i}",
                                on_click=responder,
                                args=(opcion, correcta),
                                disabled=st.session_state.respondida,
                                use_container_width=True,
                            )
                    else:
                        st.button(
                            etiqueta,
                            key=f"op_{indice}_{i}",
                            on_click=responder,
                            args=(opcion, correcta),
                            disabled=st.session_state.respondida,
                            use_container_width=True,
                        )

    if st.session_state.respondida:
        if st.session_state.opcion_elegida == correcta:
            st.success("¡Correcto! ✅")
        else:
            st.error(f"Incorrecto ❌ — la respuesta correcta era: **{correcta}**")

        st.button(
            "Siguiente ▶️",
            type="primary",
            on_click=siguiente_pregunta,
            args=(pool,),
        )

    st.caption(f"Puntaje actual: {st.session_state.puntaje} / {indice}")
    if st.button("🏠 Salir del quiz"):
        volver_al_inicio()
        st.rerun()

    st.stop()
