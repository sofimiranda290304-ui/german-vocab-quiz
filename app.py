"""
Deutsch Quiz - Aplicación tipo Kahoot para aprender vocabulario alemán.

Estructura de datos esperada:
    data/
        A1/
            Kapitel_01.yaml
            Kapitel_02.yaml
            ...
        A2/
            Kapitel_01.yaml
            ...
        B1/
            Kapitel_01.yaml
            ...

Cada YAML tiene este formato:

capitulo: 1
verbos:
  - aleman: "..."
    espanol: "..."
    tipo: "..."
sustantivos:
  - aleman: "..."
    espanol: "..."
    genero: "der/die/das"
    plural: "..."
adjetivos: [...]
adverbios: [...]
preposiciones: [...]
expresiones: [...]
"""

import random
from pathlib import Path

import streamlit as st
import yaml

# --------------------------------------------------------------------------
# Configuración general
# --------------------------------------------------------------------------

DATA_DIR = Path(__file__).parent / "data"
NIVELES = ["A1", "A2", "B1"]

CATEGORIAS_LABELS = {
    "verbos": "🏃 Verbos",
    "sustantivos": "📦 Sustantivos",
    "adjetivos": "🎨 Adjetivos",
    "adverbios": "🧭 Adverbios",
    "preposiciones": "🔗 Preposiciones",
    "expresiones": "💬 Expresiones",
}

OPTION_STYLES = [
    {"emoji": "🔺", "color": "#e21b3c"},  # rojo
    {"emoji": "🔷", "color": "#1368ce"},  # azul
    {"emoji": "🟡", "color": "#d89e00"},  # amarillo
    {"emoji": "🟩", "color": "#26890c"},  # verde
]

st.set_page_config(
    page_title="Deutsch Quiz",
    page_icon="🇩🇪",
    layout="centered",
)

# --------------------------------------------------------------------------
# Estilos
# --------------------------------------------------------------------------

st.markdown(
    """
    <style>
    div.stButton > button {
        height: 4.2em;
        width: 100%;
        font-size: 1.05em;
        font-weight: 600;
        border-radius: 14px;
        border: none;
        white-space: normal;
    }
    .question-card {
        background: linear-gradient(135deg, #1368ce, #0c4ea3);
        color: white;
        padding: 1.6em 1.2em;
        border-radius: 18px;
        text-align: center;
        font-size: 1.6em;
        font-weight: 700;
        margin-bottom: 1.2em;
        box-shadow: 0 6px 14px rgba(0,0,0,0.15);
    }
    .meta-tag {
        display: inline-block;
        background: #eef2ff;
        color: #1368ce;
        padding: 0.15em 0.7em;
        border-radius: 999px;
        font-size: 0.8em;
        font-weight: 600;
        margin-bottom: 0.6em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------------------------------
# Carga de datos
# --------------------------------------------------------------------------

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
    """Texto que se muestra como opción/respuesta en alemán."""
    if tarjeta["categoria"] == "sustantivos" and tarjeta["genero"]:
        return f"{tarjeta['genero']} {tarjeta['aleman']}"
    return tarjeta["aleman"]


def generar_opciones(tarjeta: dict, pool: list, n: int = 4) -> list:
    """Genera n opciones (1 correcta + distractores) mezcladas."""
    correcta = texto_respuesta(tarjeta)

    candidatos = [
        c for c in pool
        if c["categoria"] == tarjeta["categoria"]
        and texto_respuesta(c) != correcta
    ]
    if len(candidatos) < n - 1:
        candidatos = [c for c in pool if texto_respuesta(c) != correcta]

    distractores_tarjetas = random.sample(candidatos, min(n - 1, len(candidatos)))
    opciones = [correcta] + [texto_respuesta(c) for c in distractores_tarjetas]

    # Rellenar si aún faltan opciones (pool muy pequeño)
    while len(opciones) < n:
        opciones.append("—")

    random.shuffle(opciones)
    return opciones


# --------------------------------------------------------------------------
# Estado de la sesión
# --------------------------------------------------------------------------

def inicializar_estado():
    defaults = {
        "quiz_activo": False,
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


def iniciar_quiz(pool: list, cantidad: int):
    cantidad = min(cantidad, len(pool))
    st.session_state.preguntas = random.sample(pool, cantidad)
    st.session_state.indice = 0
    st.session_state.puntaje = 0
    st.session_state.respondida = False
    st.session_state.opcion_elegida = None
    st.session_state.quiz_activo = True
    st.session_state.opciones_actuales = generar_opciones(
        st.session_state.preguntas[0], pool
    )


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


def reiniciar():
    st.session_state.quiz_activo = False
    st.session_state.preguntas = []
    st.session_state.indice = 0
    st.session_state.puntaje = 0
    st.session_state.respondida = False
    st.session_state.opcion_elegida = None


# --------------------------------------------------------------------------
# Sidebar - configuración
# --------------------------------------------------------------------------

st.sidebar.title("⚙️ Configuración")

nivel = st.sidebar.selectbox("Nivel", NIVELES, index=NIVELES.index("A2"))

tarjetas_nivel, capitulos_disponibles = cargar_nivel(nivel)
capitulos_disponibles = sorted(capitulos_disponibles, key=lambda x: str(x))

if not tarjetas_nivel:
    st.sidebar.warning(f"Todavía no hay vocabulario cargado para el nivel {nivel}.")

capitulos_sel = st.sidebar.multiselect(
    "Capítulos",
    options=capitulos_disponibles,
    default=capitulos_disponibles,
)

categorias_sel = st.sidebar.multiselect(
    "Categorías",
    options=list(CATEGORIAS_LABELS.keys()),
    default=list(CATEGORIAS_LABELS.keys()),
    format_func=lambda c: CATEGORIAS_LABELS[c],
)

pool_filtrado = [
    t for t in tarjetas_nivel
    if t["capitulo"] in capitulos_sel and t["categoria"] in categorias_sel
]

st.sidebar.markdown(f"**Palabras disponibles:** {len(pool_filtrado)}")

max_preguntas = max(1, len(pool_filtrado))
num_preguntas = st.sidebar.slider(
    "Número de preguntas",
    min_value=1,
    max_value=min(30, max_preguntas) if max_preguntas > 1 else 1,
    value=min(10, max_preguntas),
)

iniciar = st.sidebar.button(
    "🚀 Iniciar Quiz", type="primary", disabled=len(pool_filtrado) < 2
)
if iniciar:
    iniciar_quiz(pool_filtrado, num_preguntas)

if st.session_state.quiz_activo:
    if st.sidebar.button("🔁 Reiniciar / cambiar configuración"):
        reiniciar()
        st.rerun()

# --------------------------------------------------------------------------
# Cuerpo principal
# --------------------------------------------------------------------------

st.title("🇩🇪 Deutsch Quiz")
st.caption("Español → Alemán · estilo Kahoot")

if not st.session_state.quiz_activo:
    st.info(
        "Configura el nivel, los capítulos y las categorías en la barra lateral, "
        "y pulsa **Iniciar Quiz** para comenzar."
    )
    with st.expander("📊 Vocabulario cargado por nivel"):
        for n in NIVELES:
            tarjetas_n, caps_n = cargar_nivel(n)
            st.write(
                f"**{n}**: {len(tarjetas_n)} palabras · "
                f"{len(caps_n)} capítulo(s) disponible(s)"
            )
    st.stop()

preguntas = st.session_state.preguntas
total = len(preguntas)
indice = st.session_state.indice

# Quiz terminado
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
        if st.button("🔄 Repetir con la misma configuración"):
            iniciar_quiz(pool_filtrado, total)
            st.rerun()
    with col2:
        if st.button("⚙️ Cambiar configuración"):
            reiniciar()
            st.rerun()
    st.stop()

# Pregunta actual
tarjeta = preguntas[indice]
opciones = st.session_state.opciones_actuales
correcta = texto_respuesta(tarjeta)

st.progress(indice / total, text=f"Pregunta {indice + 1} de {total}")
st.markdown(
    f"<span class='meta-tag'>{CATEGORIAS_LABELS[tarjeta['categoria']]} · "
    f"Cap. {tarjeta['capitulo']}</span>",
    unsafe_allow_html=True,
)
st.markdown(
    f"<div class='question-card'>{tarjeta['espanol']}</div>",
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)
columnas = [col1, col2, col1, col2]

for i, opcion in enumerate(opciones):
    estilo = OPTION_STYLES[i % len(OPTION_STYLES)]
    etiqueta = f"{estilo['emoji']} {opcion}"

    if st.session_state.respondida:
        if opcion == correcta:
            etiqueta = f"✅ {opcion}"
        elif opcion == st.session_state.opcion_elegida:
            etiqueta = f"❌ {opcion}"

    columnas[i].button(
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
        args=(pool_filtrado,),
    )

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Puntaje actual:** {st.session_state.puntaje} / {indice}")
