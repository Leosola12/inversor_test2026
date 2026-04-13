import streamlit as st
import numpy as np
import plotly.graph_objects as go
import math

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Diagnóstico del Inversor",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# ESTILOS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg:        #0d0f14;
    --surface:   #13161e;
    --border:    #1e2330;
    --accent:    #c8a96e;
    --accent2:   #6e9dc8;
    --danger:    #c86e6e;
    --success:   #6ec88a;
    --text:      #e8e4dc;
    --muted:     #7a7d8a;
    --card:      #161921;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}

.stApp { background-color: var(--bg); }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 4rem 2rem 2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 3rem;
}
.hero-eyebrow {
    font-size: 0.75rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 1rem;
}
.hero h1 {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2.2rem, 5vw, 3.8rem);
    font-weight: 400;
    line-height: 1.1;
    color: var(--text);
    margin-bottom: 1.2rem;
}
.hero h1 em { color: var(--accent); font-style: italic; }
.hero-sub {
    font-size: 1rem;
    color: var(--muted);
    max-width: 560px;
    margin: 0 auto 2rem;
    line-height: 1.7;
}

/* ── Step header ── */
.step-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 2.5rem 0 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border);
}
.step-num {
    font-family: 'DM Serif Display', serif;
    font-size: 2.5rem;
    color: var(--accent);
    line-height: 1;
    opacity: 0.6;
}
.step-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.5rem;
    color: var(--text);
}
.step-desc { font-size: 0.88rem; color: var(--muted); margin-top: 0.2rem; }

/* ── Info tooltip ── */
.info-box {
    background: #1a1e28;
    border-left: 2px solid var(--accent);
    border-radius: 4px;
    padding: 0.75rem 1rem;
    font-size: 0.83rem;
    color: var(--muted);
    line-height: 1.6;
    margin: -0.5rem 0 1rem;
}
.info-box strong { color: var(--accent); }

/* ── Objetivo card ── */
.obj-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 0.75rem;
    margin-bottom: 1.5rem;
}
.obj-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.1rem;
    cursor: pointer;
    transition: all 0.2s;
}
.obj-card:hover { border-color: var(--accent); }
.obj-card.selected { border-color: var(--accent); background: #1e1c14; }
.obj-icon { font-size: 1.5rem; margin-bottom: 0.5rem; }
.obj-name { font-size: 0.9rem; font-weight: 600; color: var(--text); }
.obj-desc { font-size: 0.78rem; color: var(--muted); margin-top: 0.3rem; line-height: 1.5; }

/* ── Pregunta ── */
.q-label {
    font-size: 0.95rem;
    font-weight: 500;
    color: var(--text);
    margin-bottom: 0.3rem;
}

/* ── Radio overrides ── */
div[data-testid="stRadio"] label {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    padding: 0.55rem 0.9rem !important;
    color: var(--muted) !important;
    font-size: 0.88rem !important;
    transition: all 0.15s !important;
    cursor: pointer !important;
}
div[data-testid="stRadio"] label:hover {
    border-color: var(--accent) !important;
    color: var(--text) !important;
}

/* ── Multiselect ── */
.stMultiSelect [data-baseweb="tag"] {
    background-color: var(--accent) !important;
    color: #000 !important;
}

/* ── Divider ── */
.dim-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 2rem 0;
}

/* ── Result cards ── */
.result-hero {
    text-align: center;
    padding: 3rem 2rem;
    background: linear-gradient(135deg, #13161e 0%, #0d1018 100%);
    border: 1px solid var(--border);
    border-radius: 12px;
    margin-bottom: 2rem;
}
.archetype-name {
    font-family: 'DM Serif Display', serif;
    font-size: 2.8rem;
    color: var(--accent);
    margin-bottom: 0.5rem;
}
.archetype-sub {
    font-size: 1rem;
    color: var(--muted);
    max-width: 480px;
    margin: 0 auto;
    line-height: 1.7;
}

.metric-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.metric-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.2rem;
    text-align: center;
}
.metric-label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--muted); margin-bottom: 0.4rem; }
.metric-value { font-family: 'DM Serif Display', serif; font-size: 2rem; color: var(--accent); }
.metric-range { font-size: 0.75rem; color: var(--muted); margin-top: 0.2rem; }

.inconsistency-card {
    background: #1a1214;
    border: 1px solid #3a2020;
    border-left: 3px solid var(--danger);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.75rem;
    font-size: 0.88rem;
    color: #d4a0a0;
    line-height: 1.6;
}
.inconsistency-title { font-weight: 600; color: var(--danger); margin-bottom: 0.3rem; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; }

.bias-card {
    background: #14181a;
    border: 1px solid #1e2e30;
    border-left: 3px solid var(--accent2);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.75rem;
    font-size: 0.88rem;
    color: #9abccc;
    line-height: 1.6;
}
.bias-title { font-weight: 600; color: var(--accent2); margin-bottom: 0.3rem; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; }

.rec-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.75rem;
    font-size: 0.88rem;
    color: var(--muted);
    line-height: 1.6;
}
.rec-dim { font-weight: 600; color: var(--text); margin-bottom: 0.2rem; }

.obj-result-header {
    font-family: 'DM Serif Display', serif;
    font-size: 1.3rem;
    color: var(--accent);
    margin: 2rem 0 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
}

.tag {
    display: inline-block;
    background: #1e1c14;
    border: 1px solid var(--accent);
    color: var(--accent);
    border-radius: 20px;
    padding: 0.2rem 0.7rem;
    font-size: 0.75rem;
    margin: 0.2rem;
}

.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.6rem;
    color: var(--text);
    margin: 2.5rem 0 1rem;
}

.progress-bar-bg {
    background: var(--border);
    border-radius: 4px;
    height: 6px;
    margin-top: 0.4rem;
}
.progress-bar-fill {
    height: 6px;
    border-radius: 4px;
    background: var(--accent);
}

.stButton > button {
    background: var(--accent) !important;
    color: #0d0f14 !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.75rem 2.5rem !important;
    cursor: pointer !important;
    transition: opacity 0.2s !important;
    width: 100% !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

.stSelectbox > div > div {
    background: var(--card) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}

hr { border-color: var(--border) !important; }

.footer {
    text-align: center;
    padding: 3rem 0 2rem;
    font-size: 0.78rem;
    color: var(--muted);
    border-top: 1px solid var(--border);
    margin-top: 4rem;
}
.footer strong { color: var(--accent); }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATOS: ARQUETIPOS
# ─────────────────────────────────────────────
# Cada arquetipo es un vector [Riesgo, Horizonte, Disciplina, Conocimiento, Experiencia] en escala 0-10

ARQUETIPOS = {
    "El Guardián": {
        "vector": [2, 4, 7, 5, 4],
        "descripcion": "Priorizás la preservación del capital por encima de todo. Tu fortaleza es la disciplina y la prudencia; tu desafío, no dejar que el miedo te cueste oportunidades de largo plazo.",
        "objetivos_afines": ["emergencia", "ahorro"],
        "objetivos_tension": ["especulativo"],
        "color": "#6ec88a"
    },
    "El Estratega": {
        "vector": [6, 8, 8, 7, 7],
        "descripcion": "Combinás visión de largo plazo con control emocional y conocimiento sólido. Tomás decisiones desde un sistema, no desde el estado de ánimo del mercado.",
        "objetivos_afines": ["largo_plazo", "objetivo"],
        "objetivos_tension": ["emergencia"],
        "color": "#c8a96e"
    },
    "El Acumulador": {
        "vector": [5, 9, 7, 5, 5],
        "descripcion": "Tu mayor activo es el tiempo. Invertís con constancia y horizonte largo, aunque tu conocimiento técnico todavía tiene margen de crecimiento.",
        "objetivos_afines": ["largo_plazo", "ahorro"],
        "objetivos_tension": ["especulativo"],
        "color": "#6e9dc8"
    },
    "El Intuitivo": {
        "vector": [7, 5, 4, 3, 7],
        "descripcion": "Tenés experiencia real en el mercado, pero operás más por intuición que por sistema. Eso funciona en mercados alcistas; se vuelve costoso cuando el mercado te pone a prueba.",
        "objetivos_afines": ["objetivo", "especulativo"],
        "objetivos_tension": ["emergencia"],
        "color": "#a96ec8"
    },
    "El Especulador": {
        "vector": [9, 3, 3, 5, 6],
        "descripcion": "Buscás rendimientos altos en plazos cortos. Tu mayor riesgo no es el mercado: es la disciplina. Sin un sistema claro, la especulación se convierte en juego.",
        "objetivos_afines": ["especulativo"],
        "objetivos_tension": ["emergencia", "largo_plazo"],
        "color": "#c86e6e"
    },
    "El Principiante Consciente": {
        "vector": [4, 6, 6, 2, 1],
        "descripcion": "Reconocés tus límites y tenés una actitud sana hacia el aprendizaje. Tu desafío es construir conocimiento antes de asumir más riesgo del que podés gestionar.",
        "objetivos_afines": ["ahorro", "emergencia"],
        "objetivos_tension": ["especulativo"],
        "color": "#6ec8b8"
    },
    "El Ansioso Informado": {
        "vector": [4, 6, 2, 8, 6],
        "descripcion": "Sabés mucho sobre los mercados, pero ese conocimiento no te da tranquilidad: te genera más dudas. El exceso de información puede paralizarte en momentos clave.",
        "objetivos_afines": ["ahorro", "largo_plazo"],
        "objetivos_tension": ["especulativo"],
        "color": "#c8b46e"
    },
    "El Confiado sin Mapa": {
        "vector": [8, 4, 4, 2, 3],
        "descripcion": "Tenés apetito de riesgo alto pero base técnica baja. Esta combinación es la más peligrosa: actuás con convicción en territorios que no conocés bien.",
        "objetivos_afines": ["especulativo"],
        "objetivos_tension": ["emergencia", "largo_plazo"],
        "color": "#c87a6e"
    },
}

# Sesgos con descripción completa
SESGOS_INFO = {
    "Aversión a la pérdida": "Sentís las pérdidas con más intensidad que las ganancias equivalentes. Esto lleva a vender en caídas (cristalizando pérdidas) y a evitar activos volátiles aunque el riesgo sea razonable.",
    "Sobreconfianza": "Tu autopercepción de conocimiento supera tu conocimiento real. Los inversores sobreconfiados toman más riesgo del que pueden gestionar y atribuyen los aciertos a habilidad y los errores al mercado.",
    "Efecto manada": "Tus decisiones están influenciadas por lo que hacen o dicen otros. Esto lleva a comprar cuando todos compran (caro) y vender cuando todos venden (barato).",
    "FOMO (Fear of Missing Out)": "El miedo a perderte una oportunidad te genera más angustia que el riesgo de perder dinero. Lleva a entrar tarde en tendencias ya maduras o a tomar posiciones apresuradas.",
    "Anclaje": "Tomás decisiones en base a un precio de referencia arbitrario (precio de compra, máximo histórico) en lugar de la situación actual del activo.",
    "Exceso de actividad": "Revisás tu cartera con una frecuencia que no aporta información útil. La actividad excesiva suele correlacionar con peores resultados por costos de transacción y decisiones emocionales.",
}

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def info(texto):
    st.markdown(f'<div class="info-box">{texto}</div>', unsafe_allow_html=True)

def q_label(texto):
    st.markdown(f'<div class="q-label">{texto}</div>', unsafe_allow_html=True)

def puntaje(respuesta, opciones):
    """Convierte respuesta a escala 1-4 y normaliza a 0-10"""
    idx = opciones.index(respuesta) + 1
    return round((idx - 1) / 3 * 10, 2)

def nivel(valor):
    if valor <= 3:   return "Bajo", "#c86e6e"
    if valor <= 5.5: return "Moderado", "#c8a96e"
    if valor <= 7.5: return "Alto", "#6e9dc8"
    return "Avanzado", "#6ec88a"

def distancia_euclidiana(v1, v2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))

def asignar_arquetipo(vector):
    mejor = None
    menor_dist = float('inf')
    for nombre, data in ARQUETIPOS.items():
        d = distancia_euclidiana(vector, data["vector"])
        if d < menor_dist:
            menor_dist = d
            mejor = nombre
    return mejor

def radar_chart(labels, values, title="", color="#c8a96e"):
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=labels + [labels[0]],
        fill='toself',
        fillcolor=f'rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.15)',
        line=dict(color=color, width=2),
        name=title
    ))
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                tickfont=dict(color='#7a7d8a', size=9),
                gridcolor='#1e2330',
                linecolor='#1e2330',
                tickvals=[2.5, 5, 7.5, 10],
                ticktext=['Bajo', 'Mod.', 'Alto', 'Avanz.'],
            ),
            angularaxis=dict(
                tickfont=dict(color='#e8e4dc', size=11, family='DM Sans'),
                gridcolor='#1e2330',
                linecolor='#1e2330',
            )
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=60, r=60, t=40, b=40),
        height=350,
    )
    return fig

def barra(valor, color="#c8a96e"):
    pct = int(valor * 10)
    st.markdown(f"""
    <div class="progress-bar-bg">
        <div class="progress-bar-fill" style="width:{pct}%; background:{color};"></div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">◈ Diagnóstico Conductual del Inversor</div>
    <h1>No sos un solo<br><em>perfil inversor</em></h1>
    <div class="hero-sub">
        Los tests tradicionales te colapsan en una etiqueta. Este diagnóstico parte de una premisa distinta: 
        el mismo inversor puede ser conservador con su fondo de emergencia y especulativo con otro capital. 
        Eso no es inconsistencia — es racionalidad.
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PASO 0 — OBJETIVOS
# ─────────────────────────────────────────────
st.markdown("""
<div class="step-header">
    <div class="step-num">00</div>
    <div>
        <div class="step-title">Tus objetivos de inversión</div>
        <div class="step-desc">El punto de partida de todo diagnóstico real</div>
    </div>
</div>
""", unsafe_allow_html=True)

with st.expander("ℹ️ ¿Por qué empezamos por los objetivos?"):
    st.markdown("""
    **Mental Accounting (Thaler, 1985):** las personas naturalmente segmentan su dinero en 'cuentas mentales' 
    con distintas tolerancias al riesgo. Un inversor puede ser absolutamente conservador con el dinero 
    destinado a emergencias y simultáneamente especulativo con una porción menor de su capital.
    
    Tratarte como un único perfil ignora esta realidad. Por eso, este diagnóstico analiza tus dimensiones 
    como inversor **una sola vez** (son tuyas, no del objetivo), pero interpreta el resultado en función 
    de **cada objetivo que tengas activo**.
    """)

OBJETIVOS_OPCIONES = {
    "emergencia": {"icon": "🛡️", "nombre": "Fondo de emergencia", "desc": "Liquidez ante imprevistos. Inmovilizarlo es inaceptable."},
    "ahorro":     {"icon": "💵", "nombre": "Ahorro en dólares",   "desc": "Protección del poder adquisitivo. Objetivo: no perder."},
    "objetivo":   {"icon": "🎯", "nombre": "Objetivo concreto",   "desc": "Viaje, auto, casa. Plazo definido, meta clara."},
    "largo_plazo":{"icon": "🌱", "nombre": "Largo plazo",         "desc": "Jubilación o patrimonio. El tiempo es el activo."},
    "especulativo":{"icon":"⚡", "nombre": "Capital especulativo","desc": "Dinero que podés perder. Buscás alto rendimiento."},
}

objetivos_sel = st.multiselect(
    "Seleccioná todos tus objetivos activos:",
    options=list(OBJETIVOS_OPCIONES.keys()),
    format_func=lambda k: f"{OBJETIVOS_OPCIONES[k]['icon']} {OBJETIVOS_OPCIONES[k]['nombre']}",
    default=["ahorro", "largo_plazo"],
    help="Podés seleccionar más de uno. El diagnóstico se interpretará para cada objetivo por separado."
)

if objetivos_sel:
    cols = st.columns(len(objetivos_sel))
    for i, obj_key in enumerate(objetivos_sel):
        obj = OBJETIVOS_OPCIONES[obj_key]
        cols[i].markdown(f"""
        <div class="obj-card selected">
            <div class="obj-icon">{obj['icon']}</div>
            <div class="obj-name">{obj['nombre']}</div>
            <div class="obj-desc">{obj['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<hr class="dim-divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PASO 1 — RIESGO
# ─────────────────────────────────────────────
st.markdown("""
<div class="step-header">
    <div class="step-num">01</div>
    <div>
        <div class="step-title">Tolerancia al riesgo</div>
        <div class="step-desc">Cómo reaccionás ante la volatilidad — en la práctica, no en la teoría</div>
    </div>
</div>
""", unsafe_allow_html=True)

with st.expander("ℹ️ Por qué esto importa más de lo que parece"):
    info("""
    <strong>La mayoría de los tests preguntan "¿cuánto riesgo tolerás?" en abstracto.</strong> El problema es que 
    la respuesta cambia radicalmente cuando el mercado cae de verdad. Este bloque usa escenarios concretos 
    (caídas numéricas, decisiones reales) para capturar tu comportamiento probable bajo presión, 
    no tu autopercepción en un momento de calma.
    """)

col1, col2 = st.columns(2)

with col1:
    q_label("Tu cartera cae un 25% en 30 días. ¿Qué hacés?")
    r1_opts = ["Vendo todo, no puedo con esto", "Vendo una parte para reducir exposición", "No hago nada, el mercado se recupera", "Compro más, es una oportunidad"]
    r1 = st.radio("", r1_opts, key="r1", label_visibility="collapsed")
    with st.expander("ℹ️"):
        info("Este escenario distingue la <strong>aversión a la pérdida real</strong> de la declarada. Vender en la baja es el error más costoso del inversor promedio (Odean, 1998): cristaliza la pérdida y suele perderse la recuperación.")

    q_label("¿Cuánta pérdida temporal podés aceptar sin perder el sueño?")
    r3_opts = ["Prefiero no perder nada", "Hasta un 10%", "Hasta un 25%", "Más del 25%, lo asumo"]
    r3 = st.radio("", r3_opts, key="r3", label_visibility="collapsed")
    with st.expander("ℹ️"):
        info("La <strong>pérdida máxima tolerable</strong> es un indicador más honesto que la preferencia de riesgo abstracta. Un 25% de caída en acciones es completamente normal en un mercado bajista.")

with col2:
    q_label("¿Qué tipo de inversión preferís?")
    r2_opts = ["Segura aunque rinda poco", "Equilibrio riesgo-retorno", "Volátil pero con potencial alto", "Máximo potencial, acepto grandes caídas"]
    r2 = st.radio("", r2_opts, key="r2", label_visibility="collapsed")
    with st.expander("ℹ️"):
        info("Esta pregunta captura tu <strong>preferencia declarada</strong>, que luego cruzamos con tu comportamiento real. La brecha entre ambas es un dato clave del diagnóstico.")

    q_label("Un activo que compraste sube un 40%. ¿Qué hacés?")
    r4_opts = ["Vendo todo, ya gané suficiente", "Vendo la mitad y aseguro ganancias", "Mantengo, puede seguir subiendo", "Compro más, la tendencia es tu amiga"]
    r4 = st.radio("", r4_opts, key="r4", label_visibility="collapsed")
    with st.expander("ℹ️"):
        info("El <strong>disposition effect</strong> (Shefrin & Statman, 1985): los inversores tienden a vender ganadores rápido y retener perdedores. Detectar esta tendencia permite corregirla.")

q_label("¿Qué te genera más malestar?")
r5_opts = ["Perder dinero que ya tenía", "Perder una oportunidad de ganarlo"]
r5 = st.radio("", r5_opts, key="r5", label_visibility="collapsed")
with st.expander("ℹ️"):
    info("Esta pregunta distingue <strong>aversión a la pérdida</strong> (loss aversion) de <strong>FOMO</strong> (Fear of Missing Out). Ambos son sesgos, pero llevan a errores opuestos: uno a vender en pánico, el otro a comprar en euforia.")

st.markdown('<hr class="dim-divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PASO 2 — HORIZONTE
# ─────────────────────────────────────────────
st.markdown("""
<div class="step-header">
    <div class="step-num">02</div>
    <div>
        <div class="step-title">Horizonte temporal</div>
        <div class="step-desc">Cuándo y cómo necesitás el dinero — la variable más subestimada</div>
    </div>
</div>
""", unsafe_allow_html=True)

with st.expander("ℹ️ Por qué el horizonte lo cambia todo"):
    info("""
    Un inversor con horizonte de 10 años puede y debería tolerar más volatilidad que uno que necesita 
    el dinero en 18 meses. El error más común: <strong>invertir en activos de largo plazo con capital 
    que en realidad se necesita en el corto plazo</strong>. Cuando el mercado cae, ese inversor está 
    forzado a vender en el peor momento.
    """)

col1, col2 = st.columns(2)

with col1:
    q_label("¿En cuánto tiempo podrías necesitar este capital?")
    h1_opts = ["En menos de 6 meses", "Entre 6 meses y 2 años", "Entre 2 y 5 años", "En más de 5 años"]
    h1 = st.radio("", h1_opts, key="h1", label_visibility="collapsed")

    q_label("¿Usarías este capital ante una emergencia?")
    h2_opts = ["Sí, es mi único respaldo", "Probablemente sí", "Poco probable", "No, tengo otras reservas"]
    h2 = st.radio("", h2_opts, key="h2", label_visibility="collapsed")
    with st.expander("ℹ️"):
        info("Si este capital cumple función de <strong>fondo de emergencia</strong>, no debería estar en activos volátiles. Confundir el rol del capital con el perfil del inversor es uno de los errores más frecuentes.")

with col2:
    q_label("¿Cómo pensás cobrar los frutos de esta inversión?")
    h3_opts = ["Necesito ingresos periódicos ya", "Mezcla de reinversión y retiros", "Reinvierto todo, no toco nada", "No tengo claro todavía"]
    h3 = st.radio("", h3_opts, key="h3", label_visibility="collapsed")
    with st.expander("ℹ️"):
        info("La <strong>estructura de retiros</strong> condiciona qué activos son adecuados. Un inversor que necesita renta regular no puede estar 100% en activos de crecimiento que no distribuyen.")

st.markdown('<hr class="dim-divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PASO 3 — CONOCIMIENTO
# ─────────────────────────────────────────────
st.markdown("""
<div class="step-header">
    <div class="step-num">03</div>
    <div>
        <div class="step-title">Conocimiento financiero</div>
        <div class="step-desc">Lo que sabés realmente — no lo que creés saber</div>
    </div>
</div>
""", unsafe_allow_html=True)

with st.expander("ℹ️ Conocimiento declarado vs. conocimiento validado"):
    info("""
    Los tests tradicionales preguntan qué instrumentos <em>conocés</em>. Este test cruza eso con 
    preguntas que verifican si realmente entendés cómo funcionan. La brecha entre ambas es el indicador 
    de <strong>sobreconfianza</strong> más relevante para un inversor.
    """)

col1, col2 = st.columns(2)

with col1:
    q_label("¿Con qué instrumentos tenés familiaridad? (podés marcar varios)")
    k1 = st.multiselect("Conocimiento", ["Plazos fijos / FCI", "Bonos soberanos", "Acciones locales", "CEDEARs", "ETFs", "Opciones / Futuros", "Criptomonedas", "ONs (Obligaciones Negociables)"], label_visibility="collapsed", key="k1")

    q_label("¿Cuáles operaste realmente alguna vez?")
    k2 = st.multiselect("Operados", ["Plazos fijos / FCI", "Bonos soberanos", "Acciones locales", "CEDEARs", "ETFs", "Opciones / Futuros", "Criptomonedas", "ONs (Obligaciones Negociables)"], label_visibility="collapsed", key="k2")
    with st.expander("ℹ️"):
        info("Operar un instrumento de verdad — con dinero real, en mercados reales — genera un tipo de aprendizaje que la teoría no puede reemplazar. La <strong>brecha entre conocidos y operados</strong> revela cuánto de tu conocimiento es teórico.")

with col2:
    q_label("Una Obligación Negociable (ON) es:")
    k3_opts = ["Una acción de una empresa", "Deuda emitida por una empresa privada", "Deuda emitida por el Estado", "No lo sé con certeza"]
    k3 = st.radio("", k3_opts, key="k3", label_visibility="collapsed")
    with st.expander("ℹ️"):
        info("Las <strong>ONs</strong> son instrumentos de renta fija emitidos por empresas. No confundirlas con acciones (renta variable) ni con bonos soberanos es fundamental para armar una cartera coherente.")

    q_label("Si el dólar sube y la empresa emisora va bien, ¿qué le pasa a tu CEDEAR?")
    k4_opts = ["Sube por la empresa", "Sube por el dólar", "Sube por ambos factores", "No varía, es renta fija"]
    k4 = st.radio("", k4_opts, key="k4", label_visibility="collapsed")
    with st.expander("ℹ️"):
        info("Los <strong>CEDEARs</strong> tienen doble exposición: al desempeño de la empresa subyacente y al tipo de cambio. Entender esto es clave para no llevarse sorpresas en carteras en pesos.")

    q_label("¿Cómo calificarías tu nivel de confianza para tomar decisiones de inversión hoy?")
    k5_opts = ["Muy baja — necesito ayuda para todo", "Baja — entiendo lo básico", "Media — me manejo solo en lo habitual", "Alta — tomo decisiones fundamentadas"]
    k5 = st.radio("", k5_opts, key="k5", label_visibility="collapsed")

st.markdown('<hr class="dim-divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PASO 4 — DISCIPLINA
# ─────────────────────────────────────────────
st.markdown("""
<div class="step-header">
    <div class="step-num">04</div>
    <div>
        <div class="step-title">Disciplina conductual</div>
        <div class="step-desc">Cómo actuás cuando el mercado pone a prueba tus convicciones</div>
    </div>
</div>
""", unsafe_allow_html=True)

with st.expander("ℹ️ Por qué la disciplina importa más que el conocimiento"):
    info("""
    Estudios de comportamiento financiero muestran consistentemente que los inversores pierden más dinero 
    por sus propias <strong>reacciones emocionales</strong> que por elegir los instrumentos incorrectos. 
    La disciplina — la capacidad de sostener una estrategia bajo presión — es el diferenciador real 
    entre inversores que crecen y los que no.
    """)

col1, col2 = st.columns(2)

with col1:
    q_label("¿Con qué frecuencia revisás tu cartera?")
    d1_opts = ["Varias veces al día", "Una vez por día", "Una vez por semana", "Una vez por mes o menos"]
    d1 = st.radio("", d1_opts, key="d1", label_visibility="collapsed")
    with st.expander("ℹ️"):
        info("Revisar la cartera con alta frecuencia se asocia con <strong>mayor ansiedad y peores resultados</strong> (Barber & Odean, 2000). El ruido del corto plazo lleva a decisiones que dañan el rendimiento de largo plazo.")

    q_label("¿De dónde vienen principalmente tus decisiones de inversión?")
    d3_opts = ["Del estado de ánimo del momento", "De lo que leí en redes o grupos", "De análisis propio de cada activo", "De una estrategia definida que sigo"]
    d3 = st.radio("", d3_opts, key="d3", label_visibility="collapsed")
    with st.expander("ℹ️"):
        info("La <strong>fuente de decisión</strong> predice la consistencia mejor que el conocimiento. Un inversor con sistema mediocre suele ganarle a uno con mucho conocimiento pero sin proceso.")

    q_label("¿Cómo procesás los errores de inversión?")
    d5_opts = ["Los evito o no los reconozco", "Los atribuyo a mala suerte o al mercado", "Los analizo para entender qué falló", "Los incorporo como ajuste a mi sistema"]
    d5 = st.radio("", d5_opts, key="d5", label_visibility="collapsed")
    with st.expander("ℹ️"):
        info("La <strong>atribución causal</strong> de errores es un predictor de aprendizaje. Atribuir errores al mercado (locus externo) impide mejora; asumirlos y ajustar (locus interno) es el ciclo del inversor que evoluciona.")

with col2:
    q_label("En la última caída importante del mercado, ¿qué hiciste?")
    d2_opts = ["Vendí para detener las pérdidas", "Dudé mucho pero no hice nada", "Esperé sin demasiada ansiedad", "Aproveché para comprar más barato"]
    d2 = st.radio("", d2_opts, key="d2", label_visibility="collapsed")
    with st.expander("ℹ️"):
        info("El comportamiento <strong>durante una caída real</strong> es el mejor predictor de comportamiento futuro. Las respuestas a escenarios hipotéticos tienden a ser más racionales que las decisiones bajo presión real.")

    q_label("¿Cuánto influyen las noticias financieras en tus decisiones?")
    d4_opts = ["Mucho — suelen cambiar mis posiciones", "Algo — las considero pero no siempre actúo", "Poco — las proceso pero tengo mis criterios", "Nada — sigo mi estrategia independientemente"]
    d4 = st.radio("", d4_opts, key="d4", label_visibility="collapsed")
    with st.expander("ℹ️"):
        info("El <strong>ruido informativo</strong> es uno de los mayores enemigos del inversor de largo plazo. La mayoría de las noticias financieras describen movimientos de corto plazo irrelevantes para una cartera bien estructurada.")

st.markdown('<hr class="dim-divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PASO 5 — EXPERIENCIA
# ─────────────────────────────────────────────
st.markdown("""
<div class="step-header">
    <div class="step-num">05</div>
    <div>
        <div class="step-title">Experiencia práctica</div>
        <div class="step-desc">Lo que el mercado te enseñó — y lo que todavía no</div>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    q_label("¿Cuántos años llevás invirtiendo con dinero real?")
    e1_opts = ["Menos de 1 año", "Entre 1 y 2 años", "Entre 2 y 5 años", "Más de 5 años"]
    e1 = st.radio("", e1_opts, key="e1", label_visibility="collapsed")

    q_label("¿Viviste alguna pérdida significativa en tu cartera?")
    e2_opts = ["Nunca tuve pérdidas relevantes", "Sí, pero no entendí bien qué pasó", "Sí, y aprendí algo concreto de eso", "Varias veces — es parte del proceso"]
    e2 = st.radio("", e2_opts, key="e2", label_visibility="collapsed")
    with st.expander("ℹ️"):
        info("Haber atravesado una pérdida real — y <strong>procesarla conscientemente</strong> — es una de las experiencias formativas más valiosas para un inversor. El mercado enseña lo que los libros no pueden.")

with col2:
    q_label("¿Tenés una estrategia de inversión que puedas describir en 2 oraciones?")
    e3_opts = ["No, voy decidiendo caso por caso", "Tengo algunas ideas pero no un sistema claro", "Sí, aunque no siempre la sigo", "Sí, y la aplico consistentemente"]
    e3 = st.radio("", e3_opts, key="e3", label_visibility="collapsed")
    with st.expander("ℹ️"):
        info("Poder <strong>articular tu estrategia</strong> es señal de que existe. Los inversores sin estrategia explícita suelen operar desde el ruido del momento, lo que genera resultados inconsistentes.")

    q_label("¿Pudiste sostener una estrategia de inversión por más de 6 meses sin cambiarla fundamentalmente?")
    e4_opts = ["Nunca llegué a sostener una", "Lo intenté pero la cambié antes", "Casi siempre — con algunos desvíos", "Siempre — la consistencia es mi base"]
    e4 = st.radio("", e4_opts, key="e4", label_visibility="collapsed")

st.markdown('<hr class="dim-divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# BOTÓN GENERAR
# ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col_btn = st.columns([1, 2, 1])
with col_btn[1]:
    generar = st.button("◈  Generar mi diagnóstico")

# ─────────────────────────────────────────────
# RESULTADOS
# ─────────────────────────────────────────────
if generar:

    if not objetivos_sel:
        st.error("Seleccioná al menos un objetivo de inversión para continuar.")
        st.stop()

    # ── Scores dimensiones ──
    R = np.mean([
        puntaje(r1, r1_opts),
        puntaje(r2, r2_opts),
        puntaje(r3, r3_opts),
        puntaje(r4, r4_opts),
    ])

    H = np.mean([
        puntaje(h1, h1_opts),
        puntaje(h2, ["Sí, es mi único respaldo","Probablemente sí","Poco probable","No, tengo otras reservas"]),
        puntaje(h3, h3_opts),
    ])

    # Conocimiento: mix de respuestas correctas + amplitud + confianza
    k_amplitud = min((len(k1) + len(k2)) / 12 * 10, 10)
    k_brecha   = len(k2) / max(len(k1), 1)  # operados/conocidos
    k_correctas = (2 if k3 == "Deuda emitida por una empresa privada" else 0) + \
                  (2 if k4 == "Sube por ambos factores" else 0)
    k_confianza = puntaje(k5, k5_opts)
    K = min((k_amplitud * 0.35 + k_brecha * 3 + k_correctas + k_confianza * 0.3), 10)

    D = np.mean([
        puntaje(d1, d1_opts),
        puntaje(d2, d2_opts),
        puntaje(d3, d3_opts),
        puntaje(d4, d4_opts),
        puntaje(d5, d5_opts),
    ])

    E = np.mean([
        puntaje(e1, e1_opts),
        puntaje(e2, e2_opts),
        puntaje(e3, e3_opts),
        puntaje(e4, e4_opts),
    ])

    vector = [round(R, 2), round(H, 2), round(D, 2), round(K, 2), round(E, 2)]

    # ── Arquetipo ──
    arquetipo = asignar_arquetipo(vector)
    arq_data  = ARQUETIPOS[arquetipo]

    # ── Sesgos ──
    sesgos_detectados = {}

    if d2 == "Vendí para detener las pérdidas":
        sesgos_detectados["Aversión a la pérdida"] = SESGOS_INFO["Aversión a la pérdida"]

    if K < 4 and k5 in ["Media — me manejo solo en lo habitual", "Alta — tomo decisiones fundamentadas"]:
        sesgos_detectados["Sobreconfianza"] = SESGOS_INFO["Sobreconfianza"]

    if d3 == "De lo que leí en redes o grupos":
        sesgos_detectados["Efecto manada"] = SESGOS_INFO["Efecto manada"]

    if r5 == "Perder una oportunidad de ganarlo":
        sesgos_detectados["FOMO (Fear of Missing Out)"] = SESGOS_INFO["FOMO (Fear of Missing Out)"]

    if d1 in ["Varias veces al día", "Una vez por día"]:
        sesgos_detectados["Exceso de actividad"] = SESGOS_INFO["Exceso de actividad"]

    # ── Inconsistencias ──
    inconsistencias = []

    if R > 6 and d2 == "Vendí para detener las pérdidas":
        inconsistencias.append({
            "titulo": "Riesgo declarado ≠ comportamiento real",
            "texto": f"Tu puntaje de tolerancia al riesgo es alto ({round(R,1)}/10), pero vendiste en la última caída. Eso sugiere que tu tolerancia real es menor a la declarada — o que actuaste desde el pánico en lugar de tu estrategia."
        })

    if H > 7 and d1 in ["Varias veces al día", "Una vez por día"]:
        inconsistencias.append({
            "titulo": "Horizonte largo + monitoreo de corto plazo",
            "texto": f"Declarás un horizonte de inversión largo ({round(H,1)}/10), pero revisás tu cartera con alta frecuencia. El ruido de corto plazo es irrelevante para objetivos largos — y genera decisiones que los dañan."
        })

    if e3 in ["Sí, aunque no siempre la sigo", "No, voy decidiendo caso por caso"] and d3 == "De una estrategia definida que sigo":
        inconsistencias.append({
            "titulo": "Estrategia declarada vs. realidad",
            "texto": "Decís que seguís una estrategia definida, pero también reconocés que no podés sostenerla. Hay una brecha entre cómo te describís y cómo actuás en la práctica."
        })

    if K < 3 and R > 7:
        inconsistencias.append({
            "titulo": "Alto apetito de riesgo con base de conocimiento baja",
            "texto": f"Tu tolerancia al riesgo es alta ({round(R,1)}/10) pero tu conocimiento financiero es bajo ({round(K,1)}/10). Asumir mucho riesgo sin entender los instrumentos es la combinación más cara del mercado."
        })

    # ── Recomendaciones ──
    recomendaciones = []

    dims = {"Riesgo": R, "Horizonte": H, "Disciplina": D, "Conocimiento": K, "Experiencia": E}
    dim_mas_baja = min(dims, key=dims.get)
    val_mas_baja = dims[dim_mas_baja]

    rec_map = {
        "Riesgo":       "Tu tolerancia al riesgo es baja. Priorizá instrumentos de renta fija y fondos de bajo riesgo mientras construís experiencia. No asumas más riesgo del que podés mantener en una caída.",
        "Horizonte":    "Tu horizonte es corto. Asegurate de que el capital invertido sea el que realmente podés inmovilizar. El error clásico es invertir dinero que en realidad se necesita en 12 meses.",
        "Disciplina":   "Tu disciplina conductual tiene margen de mejora. Considerá definir reglas de entrada y salida antes de invertir, y revisiones periódicas programadas (no reactivas). Un sistema es tu mejor defensa contra el ruido del mercado.",
        "Conocimiento": "Tu base de conocimiento financiero es el área de mayor oportunidad. Antes de ampliar tu exposición, es clave entender cómo funciona cada instrumento que operás. El conocimiento reduce el riesgo real.",
        "Experiencia":  "La experiencia práctica lleva tiempo. Empezá con posiciones pequeñas en instrumentos simples, documentá tus decisiones y tus resultados. Aprender con poco capital es mucho más barato que aprender con mucho.",
    }
    recomendaciones.append({"dim": dim_mas_baja, "texto": rec_map[dim_mas_baja]})

    if D < 5:
        recomendaciones.append({"dim": "Disciplina (adicional)", "texto": "Establecé un ritual de revisión semanal o mensual — no más frecuente. Escribí tus tesis de inversión antes de invertir. Si no podés explicar en dos oraciones por qué compraste algo, es una señal de que la decisión fue emocional."})

    # ─────────────────────────────────────────────
    # OUTPUT
    # ─────────────────────────────────────────────

    st.markdown("---")
    st.markdown('<div class="section-title">◈ Tu diagnóstico</div>', unsafe_allow_html=True)

    # Arquetipo hero
    st.markdown(f"""
    <div class="result-hero">
        <div style="font-size:0.75rem; letter-spacing:0.2em; text-transform:uppercase; color:{arq_data['color']}; margin-bottom:0.8rem;">
            Tu arquetipo inversor
        </div>
        <div class="archetype-name" style="color:{arq_data['color']};">{arquetipo}</div>
        <div class="archetype-sub">{arq_data['descripcion']}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Radar ──
    labels = ["Riesgo", "Horizonte", "Disciplina", "Conocimiento", "Experiencia"]
    fig = radar_chart(labels, vector, title=arquetipo, color=arq_data['color'])
    st.plotly_chart(fig, use_container_width=True)

    # ── Métricas ──
    st.markdown('<div class="section-title" style="font-size:1.2rem;">Tus dimensiones</div>', unsafe_allow_html=True)

    dim_data = [
        ("Riesgo", R, "Tolerancia a la volatilidad"),
        ("Horizonte", H, "Plazo y liquidez"),
        ("Disciplina", D, "Control conductual"),
        ("Conocimiento", K, "Base técnica"),
        ("Experiencia", E, "Recorrido práctico"),
    ]

    cols = st.columns(5)
    for i, (nombre, valor, desc) in enumerate(dim_data):
        niv, col = nivel(valor)
        with cols[i]:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{nombre}</div>
                <div class="metric-value" style="color:{col};">{round(valor,1)}</div>
                <div class="metric-range" style="color:{col};">{niv}</div>
            </div>
            """, unsafe_allow_html=True)
            barra(valor/10, col)
            st.markdown(f'<div style="font-size:0.72rem; color:var(--muted); margin-top:0.4rem; text-align:center;">{desc}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Por objetivo ──
    st.markdown('<div class="section-title">Por objetivo de inversión</div>', unsafe_allow_html=True)
    with st.expander("ℹ️ ¿Por qué el mismo perfil se lee distinto según el objetivo?"):
        info("""
        <strong>Mental Accounting (Thaler, 1985):</strong> la misma tolerancia al riesgo tiene implicancias 
        completamente distintas según el propósito del capital. Un puntaje de riesgo de 7/10 es saludable 
        para un capital especulativo y potencialmente peligroso para un fondo de emergencia. 
        Esta sección muestra ese cruce.
        """)

    for obj_key in objetivos_sel:
        obj = OBJETIVOS_OPCIONES[obj_key]
        es_afin    = obj_key in arq_data["objetivos_afines"]
        es_tension = obj_key in arq_data["objetivos_tension"]

        tag_color  = "#6ec88a" if es_afin else ("#c86e6e" if es_tension else "#c8a96e")
        tag_texto  = "Afinidad alta" if es_afin else ("Posible tensión" if es_tension else "Compatible")

        st.markdown(f"""
        <div class="obj-result-header">{obj['icon']} {obj['nombre']}</div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([3, 1])
        with col1:
            # Interpretación específica por objetivo
            interps = {
                "emergencia": {
                    "afin":    "Tu perfil es compatible con este objetivo. Un puntaje de riesgo bajo es exactamente lo que necesita un fondo de emergencia: preservación de capital y liquidez inmediata.",
                    "tension": f"Tu tolerancia al riesgo ({round(R,1)}/10) es alta para un fondo de emergencia. Este capital no debería estar en activos volátiles, sin importar tu perfil general. El fondo de emergencia tiene su propia lógica.",
                    "neutro":  "Este objetivo requiere máxima liquidez y mínima volatilidad. Revisá que el capital destinado a emergencias no esté inmovilizado en activos de plazo."
                },
                "ahorro": {
                    "afin":    "Tu perfil se alinea bien con un objetivo de ahorro en dólares. La prioridad es preservación del poder adquisitivo con exposición controlada al riesgo cambiario.",
                    "tension": f"Con un riesgo de {round(R,1)}/10, tendés a buscar más retorno del que un objetivo de ahorro justifica. Separar el capital de ahorro del capital de inversión ayuda a no mezclar los criterios.",
                    "neutro":  "Para ahorro en dólares, priorizá instrumentos como CEDEARs defensivos, ONs dollar-linked o FCI en dólares. La consistencia de aportes importa más que el instrumento elegido."
                },
                "objetivo": {
                    "afin":    "Tenés un horizonte y disciplina compatibles con un objetivo concreto. La clave es no cambiar la estrategia cuando el mercado se ponga volátil cerca de la fecha objetivo.",
                    "tension": f"El mayor riesgo para este objetivo es tu horizonte temporal ({round(H,1)}/10). Si la fecha del objetivo es cercana, reducí la exposición al riesgo progresivamente.",
                    "neutro":  "Con un objetivo concreto y plazo definido, la cartera debería ir reduciendo riesgo a medida que se acerca la fecha. Definí hoy cuándo y cómo vas a hacer ese ajuste."
                },
                "largo_plazo": {
                    "afin":    f"Tu horizonte ({round(H,1)}/10) y disciplina ({round(D,1)}/10) son activos clave para inversión de largo plazo. La magia del interés compuesto requiere precisamente lo que tenés: tiempo y paciencia.",
                    "tension": f"La inversión de largo plazo es tu objetivo más desafiante dado tu perfil. El mayor riesgo: que la baja disciplina ({round(D,1)}/10) te lleve a cambios de estrategia en el momento equivocado.",
                    "neutro":  "Para largo plazo, la estrategia más robusta es simple: activos de crecimiento diversificados, aportes periódicos, y revisión anual. La frecuencia de decisiones debería ser mínima."
                },
                "especulativo": {
                    "afin":    f"Tu apetito de riesgo ({round(R,1)}/10) es compatible con capital especulativo. Asegurate de que este capital sea una porción pequeña de tu patrimonio total — la que podés perder sin que afecte tu vida.",
                    "tension": "El capital especulativo requiere tolerancia real a pérdidas del 30-50% o más. Si tu comportamiento en caídas muestra ansiedad o venta de pánico, el capital especulativo puede hacerte daño.",
                    "neutro":  "Para capital especulativo, el tamaño de la posición importa más que el instrumento. Definí antes de invertir cuánto máximo podés perder en esa posición sin que afecte tu estrategia general."
                },
            }

            tipo = "afin" if es_afin else ("tension" if es_tension else "neutro")
            border = "#3a2020" if es_tension else ("#1e3020" if es_afin else "var(--border)")
            bg     = "#1a1214" if es_tension else ("#141a14" if es_afin else "var(--card)")
            st.markdown(f"""
            <div style="background:{bg}; border:1px solid {border}; border-radius:8px; padding:1rem 1.2rem; font-size:0.88rem; color:var(--muted); line-height:1.7;">
                {interps[obj_key][tipo]}
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="text-align:center; padding-top:0.5rem;">
                <div style="font-size:2rem;">{obj['icon']}</div>
                <div style="margin-top:0.5rem;">
                    <span style="background:#1a1a1a; border:1px solid {tag_color}; color:{tag_color}; border-radius:20px; padding:0.2rem 0.8rem; font-size:0.75rem;">
                        {tag_texto}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Inconsistencias ──
    if inconsistencias:
        st.markdown('<div class="section-title">⚠️ Inconsistencias detectadas</div>', unsafe_allow_html=True)
        with st.expander("ℹ️ ¿Qué es una inconsistencia conductual?"):
            info("""
            Una inconsistencia aparece cuando dos respuestas tuyas apuntan en direcciones opuestas. 
            No es un juicio — es información. <strong>La brecha entre lo que creemos que somos y cómo actuamos 
            en realidad</strong> es exactamente lo que los tests tradicionales no detectan. Conocerla es el 
            primer paso para gestionarla.
            """)
        for inc in inconsistencias:
            st.markdown(f"""
            <div class="inconsistency-card">
                <div class="inconsistency-title">⚠ {inc['titulo']}</div>
                {inc['texto']}
            </div>
            """, unsafe_allow_html=True)

    # ── Sesgos ──
    if sesgos_detectados:
        st.markdown('<div class="section-title">🧠 Sesgos conductuales identificados</div>', unsafe_allow_html=True)
        with st.expander("ℹ️ ¿Qué son los sesgos conductuales?"):
            info("""
            Los sesgos son <strong>patrones sistemáticos de pensamiento</strong> que desvían nuestras 
            decisiones de lo racional. No son fallas de inteligencia — son características de cómo el 
            cerebro humano procesa la incertidumbre. Identificarlos no los elimina, pero te da la 
            posibilidad de diseñar sistemas que los compensen.
            """)
        for nombre, desc in sesgos_detectados.items():
            st.markdown(f"""
            <div class="bias-card">
                <div class="bias-title">◉ {nombre}</div>
                {desc}
            </div>
            """, unsafe_allow_html=True)

    # ── Recomendaciones ──
    st.markdown('<div class="section-title">→ Próximos pasos</div>', unsafe_allow_html=True)
    for rec in recomendaciones:
        st.markdown(f"""
        <div class="rec-card">
            <div class="rec-dim">{rec['dim']}</div>
            {rec['texto']}
        </div>
        """, unsafe_allow_html=True)

    # ── Por qué este diagnóstico es distinto ──
    st.markdown('<div class="section-title" style="margin-top:3rem;">¿Por qué este diagnóstico es diferente?</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:var(--card); border:1px solid var(--border); border-radius:12px; padding:2rem; font-size:0.9rem; color:var(--muted); line-height:1.8;">
        <p>Los tests de perfil inversor convencionales tienen un problema estructural: colapsan toda la complejidad de una persona en una única dimensión — la aversión al riesgo — y producen una etiqueta como resultado. El 99% de los inversores termina siendo clasificado como "moderado", lo cual no ayuda a nadie a tomar mejores decisiones.</p>
        <p>Este diagnóstico parte de tres principios distintos:</p>
        <p><strong style="color:var(--accent)">1. Comportamiento ≠ autopercepción.</strong> No alcanza con saber cómo te describís. Importa cómo actuaste en la última caída real, con qué frecuencia revisás tu cartera, de dónde vienen tus decisiones.</p>
        <p><strong style="color:var(--accent)">2. Un inversor no es un único perfil.</strong> La misma persona puede ser conservadora con su fondo de emergencia y especulativa con otro capital. Tratarla como un perfil único es una simplificación que distorsiona (Mental Accounting, Thaler 1985).</p>
        <p><strong style="color:var(--accent)">3. Las inconsistencias son la información más valiosa.</strong> La brecha entre lo que creemos que somos y cómo actuamos en realidad es exactamente lo que los tests tradicionales no capturan — y lo que este modelo pone en el centro.</p>
        <p>El resultado no es una etiqueta. Es un mapa.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    <strong>Diagnóstico Conductual del Inversor</strong><br>
    Finanzas e Inversiones en la Era IA · FCE UNLP · 2025<br><br>
    <span style="opacity:0.5;">Basado en finanzas conductuales: Kahneman & Tversky (1979), Thaler (1985), Barber & Odean (2000), Shefrin & Statman (1985)</span>
</div>
""", unsafe_allow_html=True)
