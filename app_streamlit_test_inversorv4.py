import streamlit as st
import numpy as np
import plotly.graph_objects as go
import math
import io
import base64
from groq import Groq
from xhtml2pdf import pisa
from dotenv import load_dotenv
import os
load_dotenv()

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
.step-title { font-family: 'DM Serif Display', serif; font-size: 1.5rem; color: var(--text); }
.step-desc { font-size: 0.88rem; color: var(--muted); margin-top: 0.2rem; }
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
.q-label { font-size: 0.95rem; font-weight: 500; color: var(--text); margin-bottom: 0.3rem; }
div[data-testid="stRadio"] label {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    padding: 0.55rem 0.9rem !important;
    color: var(--muted) !important;
    font-size: 0.88rem !important;
    transition: all 0.15s !important;
}
div[data-testid="stRadio"] label:hover { border-color: var(--accent) !important; color: var(--text) !important; }
.stMultiSelect [data-baseweb="tag"] { background-color: var(--accent) !important; color: #000 !important; }
.dim-divider { border: none; border-top: 1px solid var(--border); margin: 2rem 0; }
.result-hero {
    text-align: center;
    padding: 3rem 2rem;
    background: linear-gradient(135deg, #13161e 0%, #0d1018 100%);
    border: 1px solid var(--border);
    border-radius: 12px;
    margin-bottom: 2rem;
}
.archetype-name { font-family: 'DM Serif Display', serif; font-size: 2.8rem; margin-bottom: 0.5rem; }
.archetype-sub { font-size: 1rem; color: var(--muted); max-width: 480px; margin: 0 auto; line-height: 1.7; }
.metric-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.2rem;
    text-align: center;
}
.metric-label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--muted); margin-bottom: 0.4rem; }
.metric-value { font-family: 'DM Serif Display', serif; font-size: 1.8rem; }
.metric-over { font-size: 0.85rem; color: var(--muted); }
.metric-range { font-size: 0.75rem; margin-top: 0.2rem; }
.inconsistency-card {
    background: #1a1214; border: 1px solid #3a2020; border-left: 3px solid var(--danger);
    border-radius: 8px; padding: 1rem 1.2rem; margin-bottom: 0.75rem;
    font-size: 0.88rem; color: #d4a0a0; line-height: 1.6;
}
.inconsistency-title { font-weight: 600; color: var(--danger); margin-bottom: 0.3rem; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; }
.bias-card {
    background: #14181a; border: 1px solid #1e2e30; border-left: 3px solid var(--accent2);
    border-radius: 8px; padding: 1rem 1.2rem; margin-bottom: 0.75rem;
    font-size: 0.88rem; color: #9abccc; line-height: 1.6;
}
.bias-title { font-weight: 600; color: var(--accent2); margin-bottom: 0.3rem; font-size: 0.8rem; text-transform: uppercase; }
.rec-card {
    background: var(--card); border: 1px solid var(--border); border-radius: 8px;
    padding: 1rem 1.2rem; margin-bottom: 0.75rem; font-size: 0.88rem; color: var(--muted); line-height: 1.6;
}
.rec-dim { font-weight: 600; color: var(--text); margin-bottom: 0.2rem; }
.obj-result-header {
    font-family: 'DM Serif Display', serif; font-size: 1.3rem; color: var(--accent);
    margin: 2rem 0 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border);
}
.section-title { font-family: 'DM Serif Display', serif; font-size: 1.6rem; color: var(--text); margin: 2.5rem 0 1rem; }
.progress-bar-bg { background: var(--border); border-radius: 4px; height: 6px; margin-top: 0.4rem; }
.progress-bar-fill { height: 6px; border-radius: 4px; }
.capital-card {
    background: var(--card); border: 1px solid var(--border); border-radius: 8px;
    padding: 1rem 1.2rem; margin-bottom: 0.75rem;
}
.capital-alert {
    background: #1a1214; border: 1px solid #3a2020; border-left: 3px solid var(--danger);
    border-radius: 8px; padding: 1rem 1.2rem; margin-bottom: 0.75rem;
    font-size: 0.88rem; color: #d4a0a0; line-height: 1.6;
}
.capital-ok {
    background: #141a14; border: 1px solid #1e3020; border-left: 3px solid var(--success);
    border-radius: 8px; padding: 1rem 1.2rem; margin-bottom: 0.75rem;
    font-size: 0.88rem; color: #9acca0; line-height: 1.6;
}
.stButton > button {
    background: var(--accent) !important; color: #0d0f14 !important;
    border: none !important; border-radius: 6px !important;
    font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important;
    font-size: 1rem !important; padding: 0.75rem 2.5rem !important; width: 100% !important;
}
.stButton > button:hover { opacity: 0.85 !important; }
hr { border-color: var(--border) !important; }
.footer {
    text-align: center; padding: 3rem 0 2rem; font-size: 0.78rem;
    color: var(--muted); border-top: 1px solid var(--border); margin-top: 4rem;
}
.footer strong { color: var(--accent); }
.obj-section-card {
    background: #13161e; border: 1px solid var(--border); border-radius: 10px;
    padding: 1.5rem; margin-bottom: 1.5rem;
}
.obj-section-title {
    font-family: 'DM Serif Display', serif; font-size: 1.1rem; color: var(--accent);
    margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border);
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATOS
# ─────────────────────────────────────────────
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

OBJETIVOS_OPCIONES = {
    "emergencia":  {"icon": "🛡️", "nombre": "Fondo de emergencia",  "desc": "Liquidez ante imprevistos. Inmovilizarlo es inaceptable.", "riesgo_max": 3, "horizonte_min": 0},
    "ahorro":      {"icon": "💵", "nombre": "Ahorro en dólares",    "desc": "Protección del poder adquisitivo. Objetivo: no perder.",   "riesgo_max": 5, "horizonte_min": 3},
    "objetivo":    {"icon": "🎯", "nombre": "Objetivo concreto",    "desc": "Viaje, auto, casa. Plazo definido, meta clara.",            "riesgo_max": 6, "horizonte_min": 4},
    "largo_plazo": {"icon": "🌱", "nombre": "Largo plazo",          "desc": "Jubilación o patrimonio. El tiempo es el activo.",          "riesgo_max": 8, "horizonte_min": 7},
    "especulativo":{"icon": "⚡", "nombre": "Capital especulativo", "desc": "Dinero que podés perder. Buscás alto rendimiento.",         "riesgo_max": 10,"horizonte_min": 0},
}

SESGOS_INFO = {
    "Aversión a la pérdida":      "Sentís las pérdidas con más intensidad que las ganancias equivalentes. Esto lleva a vender en caídas —cristalizando pérdidas— y a evitar activos volátiles aunque el riesgo sea razonable.",
    "Sobreconfianza":             "Tu autopercepción de conocimiento supera tu conocimiento real. Los inversores sobreconfiados toman más riesgo del que pueden gestionar.",
    "Efecto manada":              "Tus decisiones están influenciadas por lo que hacen o dicen otros. Esto lleva a comprar cuando todos compran (caro) y vender cuando todos venden (barato).",
    "FOMO":                       "El miedo a perderte una oportunidad te genera más angustia que el riesgo de perder dinero. Lleva a entrar tarde en tendencias ya maduras.",
    "Exceso de actividad":        "Revisás tu cartera con una frecuencia que no aporta información útil. La actividad excesiva suele correlacionar con peores resultados.",
    "Efecto disposición":         "Tendés a vender tus activos ganadores rápido para 'asegurar' la ganancia, mientras retenés los perdedores esperando recuperación. Es exactamente lo opuesto a lo racional: dejás correr las pérdidas y cortás las ganancias.",
    "Sesgo de disponibilidad":    "Tomás decisiones basadas en lo más reciente o memorable —un rally, una noticia, una recomendación viral— en lugar de en datos sistemáticos. Lo que recordás fácilmente distorsiona tu percepción de probabilidades.",
    "Sesgo de anclaje":           "Fijás mentalmente el precio al que compraste un activo y tomás decisiones en función de ese número en lugar del valor real actual. 'No vendo porque estoy en pérdida' es una decisión sobre el pasado, no sobre el futuro.",
    "Ilusión de control":         "Creés que tu análisis o seguimiento activo reduce el riesgo de tus inversiones más de lo que realmente lo hace. El mercado tiene una componente aleatoria que ningún nivel de análisis elimina.",
    "Sesgo de confirmación":      "Buscás y priorizás información que confirma lo que ya decidiste invertir, y descartás señales que cuestionan tu posición. Esto lleva a mantener tesis de inversión dañinas por más tiempo del razonable.",
    "Contabilidad mental":        "Tratás el dinero de distintas 'cuentas' con criterios irracionales: dinero 'ganado en el mercado' se arriesga más fácil que el ahorrado, aunque el valor sea idéntico. La plata no sabe de dónde vino.",
}

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def info(texto):
    st.markdown(f'<div class="info-box">{texto}</div>', unsafe_allow_html=True)

def q_label(texto):
    st.markdown(f'<div class="q-label">{texto}</div>', unsafe_allow_html=True)

def puntaje(respuesta, opciones):
    idx = opciones.index(respuesta) + 1
    return round((idx - 1) / 3 * 10, 2)

def nivel(valor):
    if valor <= 3:   return "Bajo",     "#c86e6e"
    if valor <= 5.5: return "Moderado", "#c8a96e"
    if valor <= 7.5: return "Alto",     "#6e9dc8"
    return "Avanzado", "#6ec88a"

def distancia_euclidiana(v1, v2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))

def asignar_arquetipo(vector):
    mejor, menor_dist = None, float('inf')
    for nombre, data in ARQUETIPOS.items():
        d = distancia_euclidiana(vector, data["vector"])
        if d < menor_dist:
            menor_dist = d
            mejor = nombre
    return mejor

def radar_chart(labels, values, color="#c8a96e"):
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=labels + [labels[0]],
        fill='toself',
        fillcolor=f'rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.15)',
        line=dict(color=color, width=2),
    ))
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(
                visible=True, range=[0, 10],
                tickfont=dict(color='#7a7d8a', size=9),
                gridcolor='#1e2330', linecolor='#1e2330',
                tickvals=[2.5, 5, 7.5, 10],
                ticktext=['Bajo', 'Mod.', 'Alto', 'Avanz.'],
            ),
            angularaxis=dict(
                tickfont=dict(color='#e8e4dc', size=11, family='DM Sans'),
                gridcolor='#1e2330', linecolor='#1e2330',
            )
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=60, r=60, t=40, b=40),
        height=350,
    )
    return fig

def barra(pct, color="#c8a96e"):
    st.markdown(f"""
    <div class="progress-bar-bg">
        <div class="progress-bar-fill" style="width:{int(pct*100)}%; background:{color};"></div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SÍNTESIS IA (GROQ)
# ─────────────────────────────────────────────
def generar_sintesis_ia(arquetipo, arq_data, vector, objetivos_sel, pct_capital,
                        sesgos_detectados, inconsistencias, obj_riesgo, obj_horizonte):
    try:
        api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
        if not api_key:
            st.error("DEBUG: no se encontró GROQ_API_KEY")
            return None
        client = Groq(api_key=api_key)
    except Exception as e:
        st.error(f"DEBUG error cliente: {e}")
        return None

    labels = ["Riesgo", "Horizonte", "Disciplina", "Conocimiento", "Experiencia"]
    dim_str = ", ".join(f"{l}: {round(v,1)}/10" for l, v in zip(labels, vector))

    obj_detalle = []
    for k in objetivos_sel:
        obj = OBJETIVOS_OPCIONES[k]
        r_o = round(obj_riesgo.get(k, 0), 1)
        h_o = round(obj_horizonte.get(k, 0), 1)
        obj_detalle.append(
            f"{obj['nombre']} ({pct_capital.get(k,0)}% del capital, riesgo obj {r_o}/10, horizonte obj {h_o}/10)"
        )

    sesgos_str    = ", ".join(sesgos_detectados.keys()) if sesgos_detectados else "ninguno detectado"
    inconsist_str = "; ".join(i["titulo"] for i in inconsistencias) if inconsistencias else "ninguna"
    objetivos_str = " | ".join(obj_detalle)

    system_prompt = """Sos un analista de finanzas conductuales. Tu trabajo es escribir una síntesis personalizada del perfil de un inversor basándote en los datos de su diagnóstico.

Reglas de tono y contenido — sin excepciones:
- Directo y concreto. Cero frases de autoayuda, cero eufemismos, cero motivación vacía.
- Basate SOLO en los datos provistos. No inventes rasgos ni supongas cosas que no están en los números.
- Nombrá los sesgos y las inconsistencias detectadas por su nombre, explicando cómo se manifiestan en ESTE perfil específico.
- Si hay tensiones reales entre objetivos y perfil, decílas sin suavizarlas.
- El cierre debe ser una frase que sintetice el mayor riesgo conductual concreto de esta persona. No un consejo genérico: algo que solo tenga sentido para este perfil.
- Longitud: 180-220 palabras. Un solo bloque de texto, sin bullets ni títulos.
- Escribí en español rioplatense, tuteo."""

    user_prompt = f"""Datos del diagnóstico:

Arquetipo: {arquetipo}
Descripción del arquetipo: {arq_data['descripcion']}

Dimensiones (escala 0-10): {dim_str}

Objetivos de inversión: {objetivos_str}

Sesgos conductuales detectados: {sesgos_str}

Inconsistencias detectadas: {inconsist_str}

Escribí la síntesis personalizada."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ],
            temperature=0.6,
            max_tokens=400,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"DEBUG error llamada Groq: {e}")
        return None
# ─────────────────────────────────────────────
# PDF EXPORT (WeasyPrint)
# ─────────────────────────────────────────────
def generar_pdf(arquetipo, arq_data, vector, objetivos_sel, pct_capital,
                sesgos_detectados, inconsistencias, recomendaciones,
                obj_riesgo, obj_horizonte, sintesis_ia=None):

    color = arq_data["color"]

    # ── Radar SVG (sin dependencia de kaleido/Chrome) ──
    labels = ["Riesgo", "Horizonte", "Disciplina", "Conocimiento", "Experiencia"]
    n = len(labels)
    cx, cy, r_max = 200, 200, 150
    angles = [math.pi / 2 - 2 * math.pi * i / n for i in range(n)]

    def polar_pt(val, angle, scale=1):
        r = (val / 10) * r_max * scale
        return cx + r * math.cos(angle), cy - r * math.sin(angle)

    # Grillas
    grid_lines = ""
    for level in [0.25, 0.5, 0.75, 1.0]:
        pts = " ".join(f"{cx + level*r_max*math.cos(a):.1f},{cy - level*r_max*math.sin(a):.1f}" for a in angles)
        grid_lines += f'<polygon points="{pts}" fill="none" stroke="#ddd" stroke-width="1"/>\n'

    # Ejes
    axis_lines = "".join(
        f'<line x1="{cx}" y1="{cy}" x2="{cx + r_max*math.cos(a):.1f}" y2="{cy - r_max*math.sin(a):.1f}" stroke="#ddd" stroke-width="1"/>\n'
        for a in angles
    )

    # Polígono de datos
    data_pts = " ".join(f"{polar_pt(v, a)[0]:.1f},{polar_pt(v, a)[1]:.1f}" for v, a in zip(vector, angles))
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    data_poly = f'<polygon points="{data_pts}" fill="rgba({r},{g},{b},0.18)" stroke="{color}" stroke-width="2"/>\n'

    # Puntos
    data_dots = "".join(
        f'<circle cx="{polar_pt(v,a)[0]:.1f}" cy="{polar_pt(v,a)[1]:.1f}" r="4" fill="{color}"/>\n'
        for v, a in zip(vector, angles)
    )

    # Etiquetas
    label_offset = 22
    label_texts = ""
    for i, (lbl, a) in enumerate(zip(labels, angles)):
        lx = cx + (r_max + label_offset) * math.cos(a)
        ly = cy - (r_max + label_offset) * math.sin(a)
        anchor = "middle" if abs(math.cos(a)) < 0.3 else ("start" if math.cos(a) > 0 else "end")
        label_texts += f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" dominant-baseline="middle" font-size="11" font-family="Helvetica" fill="#333">{lbl}</text>\n'

    radar_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400">
      <rect width="400" height="400" fill="white"/>
      {grid_lines}{axis_lines}{data_poly}{data_dots}{label_texts}
    </svg>'''
    radar_b64 = base64.b64encode(radar_svg.encode()).decode()
    radar_src = f"data:image/svg+xml;base64,{radar_b64}"

    # ── Helpers HTML ──
    def nivel_color(v):
        if v <= 3:   return "#c86e6e"
        if v <= 5.5: return "#c8a96e"
        if v <= 7.5: return "#6e9dc8"
        return "#6ec88a"

    def nivel_label(v):
        if v <= 3:   return "Bajo"
        if v <= 5.5: return "Moderado"
        if v <= 7.5: return "Alto"
        return "Avanzado"

    def barra_html(v):
        c = nivel_color(v)
        pct = int(v / 10 * 100)
        return f'''<div style="background:#eee;border-radius:4px;height:6px;margin-top:4px;">
                     <div style="width:{pct}%;height:6px;border-radius:4px;background:{c};"></div>
                   </div>'''

    # ── Secciones opcionales ──
    sintesis_html = ""
    if sintesis_ia:
        sintesis_html = f'''
        <div class="sintesis-block">
            <div class="sintesis-label">Sintesis conductual &nbsp;·&nbsp; IA</div>
            <div class="ia-body">{sintesis_ia}</div>
        </div>'''

    # Dimensiones
    dims = list(zip(labels, vector))
    dims_rows = "".join(f'''
        <tr>
            <td class="dim-name">{lbl}</td>
            <td class="dim-score" style="color:{nivel_color(v)};">{round(v,1)}/10</td>
            <td class="dim-nivel" style="color:{nivel_color(v)};">{nivel_label(v)}</td>
        </tr>''' for lbl, v in dims)

    # Objetivos
    obj_rows = "".join(f'''
        <tr>
            <td>{OBJETIVOS_OPCIONES[k]["icon"]} {OBJETIVOS_OPCIONES[k]["nombre"]}</td>
            <td class="center">{pct_capital.get(k,0)}%</td>
            <td class="center" style="color:{nivel_color(obj_riesgo.get(k,0))};">{round(obj_riesgo.get(k,0),1)}/10</td>
            <td class="center" style="color:{nivel_color(obj_horizonte.get(k,0))};">{round(obj_horizonte.get(k,0),1)}/10</td>
        </tr>''' for k in objetivos_sel)

    # Inconsistencias
    inconsist_html = ""
    if inconsistencias:
        items = "".join(f'''
            <div class="alert-card">
                <div class="alert-title">⚠ {i["titulo"]}</div>
                <div class="alert-body">{i["texto"]}</div>
            </div>''' for i in inconsistencias)
        inconsist_html = f'<div class="section" style="page-break-before: always;"><div class="section-title">Inconsistencias detectadas</div>{items}</div>'

    # Sesgos
    sesgos_html = ""
    if sesgos_detectados:
        items = "".join(f'''
            <div class="sesgo-card">
                <div class="sesgo-title">◉ {nombre}</div>
                <div class="sesgo-body">{desc}</div>
            </div>''' for nombre, desc in sesgos_detectados.items())
        sesgos_html = f'<div class="section" style="page-break-before: always;"><div class="section-title">Sesgos conductuales identificados</div>{items}</div>'

    # Recomendaciones
    recs_html = "".join(f'''
        <div class="rec-card">
            <div class="rec-dim">→ {r["dim"]}</div>
            <div class="rec-body">{r["texto"]}</div>
        </div>''' for r in recomendaciones)

    # ── Página 3: bloques pre-construidos ──
    p3_inconsistencias = ""
    if inconsistencias:
        items = "".join(
            f'<div class="alert-card"><div class="alert-title">{i["titulo"]}</div><div class="alert-body">{i["texto"]}</div></div>'
            for i in inconsistencias
        )
        p3_inconsistencias = f'<div class="block"><div class="section-title">Inconsistencias detectadas</div>{items}</div>'

    p3_sesgos = ""
    if sesgos_detectados:
        items = "".join(
            f'<div class="sesgo-card"><div class="sesgo-title">{nombre}</div><div class="sesgo-body">{desc}</div></div>'
            for nombre, desc in sesgos_detectados.items()
        )
        p3_sesgos = f'<div class="block"><div class="section-title">Sesgos conductuales identificados</div>{items}</div>'

    p3_recomendaciones = "".join(
        f'<div class="rec-card"><div class="rec-dim">{r["dim"]}</div><div class="rec-body">{r["texto"]}</div></div>'
        for r in recomendaciones
    )

    # ── HTML completo ──
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: Helvetica, sans-serif; color: #1a1a2e; background: white; font-size: 10pt; line-height: 1.6; }}

  @page {{ margin: 2cm 2.2cm; }}

  /* ── PÁGINA 1 ── */

  .header {{
    text-align: center;
    padding-bottom: 1.2rem;
    border-bottom: 1px solid #e0e0e0;
    margin-bottom: 2rem;
  }}
  .header-eyebrow {{
    font-size: 6.5pt; letter-spacing: 0.3em; text-transform: uppercase;
    color: #aaa; margin-bottom: 0.6rem;
  }}
  .header-title {{
    font-size: 26pt; font-weight: bold; color: #1a1a2e;
    margin-bottom: 0.3rem; letter-spacing: -0.01em;
  }}
  .header-sub {{ font-size: 8pt; color: #bbb; }}

  /* Arquetipo: solo línea superior, sin caja */
  .arquetipo-block {{
    text-align: center;
    padding: 1.8rem 0 1.6rem;
    border-top: 4px solid {color};
    margin-bottom: 2rem;
    page-break-inside: avoid;
  }}
  .arquetipo-label {{
    font-size: 12.5pt; letter-spacing: 0.3em; text-transform: uppercase;
    color: #aaa; margin-bottom: 0.7rem;
  }}
  .arquetipo-name {{
    font-size: 30pt; font-weight: bold; color: {color};
    margin-bottom: 0.8rem; line-height: 1.15;
  }}
  .arquetipo-desc {{
    font-size: 10pt; color: #444; line-height: 1.8;
    max-width: 420px; margin: 0 auto;
  }}

  /* Síntesis IA */
  .sintesis-block {{ margin-bottom: 0; page-break-inside: avoid; }}
  .sintesis-label {{
    font-size: 12.5pt; letter-spacing: 0.3em; text-transform: uppercase;
    color: #aaa; margin-bottom: 0.5rem;
  }}
  .ia-body {{
    font-style: italic; font-size: 9.5pt; color: #444; line-height: 1.9;
    padding: 1rem 1.2rem;
    border-left: 3px solid {color};
  }}

  /* ── PÁGINA 2 ── */

  .p2 {{ page-break-before: always; }}

  .section-title {{
    font-size: 11pt; font-weight: bold; color: {color};
    margin-bottom: 0.9rem;
    padding-bottom: 0.4rem;
    border-bottom: 1.5px solid {color};
    text-transform: uppercase;
    letter-spacing: 0.2em;
  }}

  .radar-wrap {{ text-align: center; margin: 0.3rem 0 1rem; page-break-inside: avoid; }}
  .radar-wrap img {{ width: 250px; }}

  .dim-table {{ width: 100%; border-collapse: collapse; margin-bottom: 1.8rem; page-break-inside: avoid; }}
  .dim-table th {{ background: {color}; color: white; font-size: 7.5pt; text-transform: uppercase; letter-spacing: 0.08em; padding: 6px 10px; text-align: left; }}
  .dim-table td {{ padding: 6px 10px; border-bottom: 1px solid #f0f0f0; font-size: 9pt; }}
  .dim-table tr:nth-child(even) td {{ background: #fafafa; }}
  .dim-name {{ font-weight: 600; color: #1a1a2e; width: 130px; }}
  .dim-score {{ font-weight: 700; font-size: 10pt; width: 65px; text-align: right; }}
  .dim-nivel {{ font-size: 8pt; width: 80px; text-align: right; color: #888; }}

  .obj-table {{ width: 100%; border-collapse: collapse; page-break-inside: avoid; }}
  .obj-table th {{ background: {color}; color: white; font-size: 7.5pt; text-transform: uppercase; letter-spacing: 0.08em; padding: 6px 10px; text-align: left; }}
  .obj-table td {{ padding: 6px 10px; border-bottom: 1px solid #f0f0f0; font-size: 9pt; }}
  .obj-table tr:nth-child(even) td {{ background: #fafafa; }}
  .center {{ text-align: center; }}

  /* ── PÁGINA 3 ── */

  .p3 {{ page-break-before: always; }}
  .block {{ margin-bottom: 1.8rem; }}

  /* Cards sin fondo — solo borde izquierdo + separador inferior */
  .alert-card {{
    border-left: 3px solid #c86e6e;
    padding: 0.5rem 0 0.5rem 0.9rem;
    margin-bottom: 0.7rem;
    border-bottom: 1px solid #f5f5f5;
    page-break-inside: avoid;
  }}
  .alert-title {{
    font-weight: 700; font-size: 8.5pt; color: #c86e6e;
    text-transform: uppercase; letter-spacing: 0.05em;
    margin-bottom: 0.25rem;
  }}
  .alert-body {{ font-size: 9pt; color: #555; line-height: 1.65; }}

  .sesgo-card {{
    border-left: 3px solid #6e9dc8;
    padding: 0.5rem 0 0.5rem 0.9rem;
    margin-bottom: 0.7rem;
    border-bottom: 1px solid #f5f5f5;
    page-break-inside: avoid;
  }}
  .sesgo-title {{
    font-weight: 700; font-size: 8.5pt; color: #4a7fa8;
    text-transform: uppercase; letter-spacing: 0.05em;
    margin-bottom: 0.25rem;
  }}
  .sesgo-body {{ font-size: 9pt; color: #555; line-height: 1.65; }}

  .rec-card {{
    border-left: 3px solid {color};
    padding: 0.5rem 0 0.5rem 0.9rem;
    margin-bottom: 0.7rem;
    border-bottom: 1px solid #f5f5f5;
    page-break-inside: avoid;
  }}
  .rec-dim {{
    font-weight: 700; font-size: 8.5pt; color: {color};
    text-transform: uppercase; letter-spacing: 0.05em;
    margin-bottom: 0.25rem;
  }}
  .rec-body {{ font-size: 9pt; color: #555; line-height: 1.65; }}

  .footer {{
    margin-top: 2.5rem; padding-top: 0.7rem;
    border-top: 1px solid #e8e8e8;
    text-align: center; font-size: 7pt; color: #ccc;
  }}
  .footer strong {{ color: {color}; }}
</style>
</head>
<body>

  <!-- ══ PÁGINA 1 ══ -->
  <div class="header">
    <div class="header-eyebrow">SEMINARIO - FINANZAS E INVERSIONES EN LA ERA DE LA IA &nbsp;·&nbsp; FCE UNLP · 2026</div>
    <div class="header-title">Diagnóstico Conductual del Inversor</div>
  </div>

  <div class="arquetipo-block">
    <div class="arquetipo-label">Tu arquetipo inversor</div>
    <div class="arquetipo-name">{arquetipo}</div>
    <div class="arquetipo-desc">{arq_data["descripcion"]}</div>
  </div>

  {sintesis_html}

  <!-- ══ PÁGINA 2 ══ -->
  <div class="p2">
    <div class="section-title">Perfil dimensional</div>
    <div class="radar-wrap">
      <img src="{radar_src}" />
    </div>
    <table class="dim-table">
      <tr>
        <th>Dimension</th>
        <th style="text-align:right;">Puntaje</th>
        <th style="text-align:right;">Nivel</th>
      </tr>
      {dims_rows}
    </table>

    <div class="section-title">Distribucion de capital por objetivo</div>
    <table class="obj-table">
      <tr>
        <th>Objetivo</th>
        <th class="center">% Capital</th>
        <th class="center">Riesgo obj.</th>
        <th class="center">Horizonte obj.</th>
      </tr>
      {obj_rows}
    </table>
  </div>

  <!-- ══ PÁGINA 3 ══ -->
  <div class="p3">
    {p3_inconsistencias}
    {p3_sesgos}

    <div class="block">
      <div class="section-title">Proximos pasos</div>
      {p3_recomendaciones}
    </div>

    <div class="footer">
      <strong>Diagnostico Conductual del Inversor</strong> · FCE UNLP · 2026<br>
      Basado en principios de finanzas conductuales: aversion a la perdida, contabilidad mental, efecto manada y sesgos de exceso de confianza.
    </div>
  </div>

</body>
</html>"""

    pdf_bytes = io.BytesIO()
    pisa.CreatePDF(io.StringIO(html), dest=pdf_bytes)
    pdf_bytes.seek(0)
    return pdf_bytes

# ─────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">◈ Diagnóstico Conductual del Inversor</div>
    <h1>No sos un solo<br><em>perfil inversor</em></h1>
    <div class="hero-sub">
        Los tests tradicionales te definen en una única etiqueta. Nuestro diagnóstico parte de una premisa distinta:
        el mismo inversor puede ser conservador con su fondo de emergencia y especulativo con otro capital.
        Eso no es inconsistencia — es racionalidad.
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PASO 0 — OBJETIVOS + % CAPITAL
# ─────────────────────────────────────────────
st.markdown("""
<div class="step-header">
    <div class="step-num">00</div>
    <div>
        <div class="step-title">Tus objetivos de inversión</div>
        <div class="step-desc">El punto de partida que derivó en la creación de este Test — y la distribución real de tu capital</div>
    </div>
</div>
""", unsafe_allow_html=True)

with st.expander("ℹ️ ¿Por qué empezamos por los objetivos?"):
    info("""
    <strong>Contabilidad mental:</strong> las personas naturalmente segmentan su dinero en 'cuentas'
    con distintas tolerancias al riesgo. Un inversor puede ser absolutamente conservador con el dinero
    destinado a emergencias y simultáneamente especulativo con una porción menor de su capital.
    Tratarte como un único perfil ignora (o simplifica DEMASIADO) esta realidad. Ese es nuestro mayor principio.
    """)

objetivos_sel = st.multiselect(
    "Seleccioná todos tus objetivos activos:",
    options=list(OBJETIVOS_OPCIONES.keys()),
    format_func=lambda k: f"{OBJETIVOS_OPCIONES[k]['icon']} {OBJETIVOS_OPCIONES[k]['nombre']}",
    default=["ahorro", "largo_plazo"],
)
# ── Mostrar descripción de objetivos seleccionados ──
if objetivos_sel:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 📌 Tus objetivos seleccionados")

    for obj_key in objetivos_sel:
        obj = OBJETIVOS_OPCIONES[obj_key]

        st.markdown(
            f"""
            <div style="margin-bottom:0.6rem;">
                <span style="font-size:1.1rem;">{obj['icon']}</span>
                <strong>{obj['nombre']}</strong><br>
                <span style="font-size:0.85rem; color:var(--muted);">
                    {obj['desc']}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )
pct_capital = {}
total_pct   = 0

if objetivos_sel:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.95rem; font-weight:500; color:var(--text); margin-bottom:0.5rem;">¿Qué porcentaje de tu capital total destinás a cada objetivo?</div>', unsafe_allow_html=True)

    with st.expander("ℹ️ ¿Por qué importa cuánto capital va a cada objetivo?"):
        info("""
        La distribución de capital <strong>es una decisión de inversión en sí misma</strong>.
        Alguien que destina el 70% de su capital a especulación con bajo conocimiento financiero
        está asumiendo un riesgo que no puede gestionar, sin importar cómo lo llame.
        Este análisis cruza el porcentaje asignado con el perfil de cada objetivo para detectar
        esas tensiones.
        """)

    cols = st.columns(len(objetivos_sel))
    for i, obj_key in enumerate(objetivos_sel):
        obj = OBJETIVOS_OPCIONES[obj_key]
        with cols[i]:
            st.markdown(f'<div style="text-align:center; font-size:1.5rem;">{obj["icon"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="text-align:center; font-size:0.8rem; color:var(--muted); margin-bottom:0.3rem;">{obj["nombre"]}</div>', unsafe_allow_html=True)
            pct = st.number_input(
                f"% {obj_key}", min_value=0, max_value=100, value=round(100//len(objetivos_sel)),
                step=5, label_visibility="collapsed", key=f"pct_{obj_key}"
            )
            pct_capital[obj_key] = pct

    total_pct = sum(pct_capital.values())
    if total_pct != 100:
        color_total = "#c86e6e" if total_pct != 100 else "#6ec88a"
        st.markdown(f'<div style="color:{color_total}; font-size:0.88rem; margin-top:0.5rem;">Total asignado: <strong>{total_pct}%</strong> {"✓" if total_pct==100 else "— debe sumar 100%"}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="color:#6ec88a; font-size:0.88rem; margin-top:0.5rem;">Total asignado: <strong>100%</strong> ✓</div>', unsafe_allow_html=True)

st.markdown('<hr class="dim-divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PASO 1 — RIESGO (general + por objetivo)
# ─────────────────────────────────────────────
st.markdown("""
<div class="step-header">
    <div class="step-num">01</div>
    <div>
        <div class="step-title">Tolerancia al riesgo</div>
        <div class="step-desc">Primero tu perfil general, luego cómo varía por objetivo</div>
    </div>
</div>
""", unsafe_allow_html=True)

with st.expander("ℹ️ Riesgo general vs. riesgo por objetivo"):
    info("""
    Tu tolerancia al riesgo <strong>no es la misma para todos tus objetivos</strong>.
    Primero medimos tu perfil base como inversor. Luego, para cada objetivo que tengas,
    te hacemos 2 preguntas clave que capturan cómo esa tolerancia se modifica
    según el propósito del capital.
    """)

col1, col2 = st.columns(2)
with col1:
    q_label("Tu cartera cae un 25% en 30 días. ¿Qué hacés?")
    r1_opts = ["Vendo todo, no puedo con esto", "Vendo una parte para reducir exposición", "No hago nada, el mercado se recupera", "Compro más, es una oportunidad"]
    r1 = st.radio("", r1_opts, key="r1", label_visibility="collapsed")
    with st.expander("ℹ️ Clickeá aquí para más información"):
        info("Este escenario distingue la <strong>aversión a la pérdida real</strong> de la declarada. Vender en la baja cristaliza la pérdida y suele perderse la recuperación.")

    q_label("¿Cuánta pérdida temporal podés aceptar sin perder el sueño?")
    r3_opts = ["Prefiero no perder nada", "Hasta un 10%", "Hasta un 25%", "Más del 25%, lo asumo"]
    r3 = st.radio("", r3_opts, key="r3", label_visibility="collapsed")

with col2:
    q_label("¿Qué tipo de inversión preferís?")
    r2_opts = ["Segura aunque rinda poco", "Equilibrio riesgo-retorno", "Volátil pero con potencial alto", "Máximo potencial, acepto grandes caídas"]
    r2 = st.radio("", r2_opts, key="r2", label_visibility="collapsed")

    q_label("Un activo que compraste sube un 40%. ¿Qué hacés?")
    r4_opts = ["Vendo todo, ya gané suficiente", "Vendo la mitad y aseguro ganancias", "Mantengo, puede seguir subiendo", "Compro más, la tendencia es tu amiga"]
    r4 = st.radio("", r4_opts, key="r4", label_visibility="collapsed")
    with st.expander("ℹ️ ¿Por qué me preguntan esto?"):
        info("El <strong>disposition effect</strong> (o 'efecto disposición'): los inversores tienden a vender sus posiciones ganadoras rápido y sostener por más tiempo sus posiciones con pérdidas. Detectar esta tendencia permite corregirla.")

q_label("¿Qué te genera más malestar?")
r5_opts = ["Perder dinero que ya tenía", "Perder una oportunidad de ganarlo"]
r5 = st.radio("", r5_opts, key="r5", label_visibility="collapsed")
with st.expander("ℹ️ ¿Por qué me preguntan esto?"):
    info("Distingue <strong>aversión a la pérdida</strong> de <strong>FOMO</strong>. Ambos son sesgos, pero llevan a errores opuestos: uno a vender en pánico, el otro a comprar en euforia.")

# Riesgo por objetivo
obj_riesgo = {}
if objetivos_sel:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:1rem; font-weight:600; color:var(--text); margin-bottom:1rem;">Riesgo específico por objetivo</div>', unsafe_allow_html=True)

    r_base_opts = {
        "emergencia":  ("¿Tolerarías que tu fondo de emergencia caiga un 5% aunque sea temporalmente?",
                        ["Jamás, necesito ese dinero intacto", "Con mucha incomodidad", "Podría tolerarlo", "Sin problema, es temporal"]),
        "ahorro":      ("Para tu ahorro en dólares, ¿qué prioridad tiene preservar el capital vs. hacerlo crecer?",
                        ["Preservar ante todo, aunque no crezca", "Preservar primero, algo de crecimiento", "Equilibrio entre ambos", "Crecer es la prioridad"]),
        "objetivo":    ("Para tu objetivo concreto, si falta 1 año y la cartera cae 15%, ¿qué hacés?",
                        ["Vendo todo y paso a algo seguro", "Reduzco el riesgo parcialmente", "Mantengo y confío en recuperación", "Aprovecho y compro más"]),
        "largo_plazo": ("Para tu capital de largo plazo, ¿cuánta volatilidad anual tolerás sin cambiar de estrategia?",
                        ["Menos del 10%", "Hasta un 20%", "Hasta un 35%", "Sin límite, es largo plazo"]),
        "especulativo":("Para tu capital especulativo, ¿cuánto de ese capital aceptás perder en un escenario malo?",
                        ["Hasta un 20%", "Hasta un 40%", "Hasta un 70%", "Todo, sé que es posible"]),
    }

    for obj_key in objetivos_sel:
        obj = OBJETIVOS_OPCIONES[obj_key]
        pregunta, opciones = r_base_opts[obj_key]
        st.markdown(f'<div class="obj-section-card"><div class="obj-section-title">{obj["icon"]} {obj["nombre"]}</div>', unsafe_allow_html=True)
        q_label(pregunta)
        resp = st.radio("", opciones, key=f"robj_{obj_key}", label_visibility="collapsed")
        obj_riesgo[obj_key] = puntaje(resp, opciones)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<hr class="dim-divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PASO 2 — HORIZONTE (general + por objetivo)
# ─────────────────────────────────────────────
st.markdown("""
<div class="step-header">
    <div class="step-num">02</div>
    <div>
        <div class="step-title">Horizonte temporal</div>
        <div class="step-desc">Cuándo y cómo necesitás el dinero de cada objetivo</div>
    </div>
</div>
""", unsafe_allow_html=True)

with st.expander("ℹ️ ¿Por qué el horizonte lo cambia todo?"):
    info("""
    Un inversor con horizonte de 10 años puede y debería tolerar más volatilidad que uno que necesita
    el dinero en 18 meses. El error más común: <strong>invertir en activos de largo plazo con capital
    que en realidad se necesita pronto</strong>. Cuando el mercado cae, ese inversor está forzado
    a vender en el peor momento.
    <br><br>El horizonte se mide <strong>por objetivo</strong>: cada porción de tu capital tiene su propio
    plazo, y el análisis refleja esa realidad en lugar de colapsarla en un único número.
    """)

# Horizonte por objetivo
obj_horizonte = {}
if objetivos_sel:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:1rem; font-weight:600; color:var(--text); margin-bottom:1rem;">Horizonte específico por objetivo</div>', unsafe_allow_html=True)

    h_base_opts = {
        "emergencia":  ("¿En cuánto tiempo necesitarías usar tu fondo de emergencia si surgiera algo?",
                        ["Mañana mismo si hiciera falta", "En menos de 1 semana", "En 1 a 4 semanas", "Podría esperar hasta 2 meses"]),
        "ahorro":      ("¿Cuánto tiempo podés dejar inmovilizado tu ahorro en dólares sin tocarlo?",
                        ["Menos de 6 meses", "Entre 6 meses y 1 año", "Entre 1 y 3 años", "Más de 3 años"]),
        "objetivo":    ("¿En cuánto tiempo necesitás el dinero de tu objetivo concreto?",
                        ["En menos de 1 año", "Entre 1 y 2 años", "Entre 2 y 4 años", "En más de 4 años"]),
        "largo_plazo": ("¿En cuántos años planeás empezar a usar el capital de largo plazo?",
                        ["En 5 a 7 años", "En 7 a 10 años", "En 10 a 15 años", "En más de 15 años"]),
        "especulativo":("¿Cuánto tiempo le das a una posición especulativa antes de tomar ganancias o pérdidas?",
                        ["Días o semanas", "1 a 3 meses", "3 a 12 meses", "Más de 1 año"]),
    }

    for obj_key in objetivos_sel:
        obj = OBJETIVOS_OPCIONES[obj_key]
        pregunta, opciones = h_base_opts[obj_key]
        st.markdown(f'<div class="obj-section-card"><div class="obj-section-title">{obj["icon"]} {obj["nombre"]}</div>', unsafe_allow_html=True)
        q_label(pregunta)
        resp = st.radio("", opciones, key=f"hobj_{obj_key}", label_visibility="collapsed")
        obj_horizonte[obj_key] = puntaje(resp, opciones)
        st.markdown('</div>', unsafe_allow_html=True)

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
    preguntas que verifican si realmente entendés cómo funcionan. La brecha entre ambas
    es el indicador de <strong>sobreconfianza</strong> más relevante para un inversor.
    """)

col1, col2 = st.columns(2)
with col1:
    q_label("¿Con qué instrumentos tenés familiaridad?")
    k1 = st.multiselect("Conocimiento", ["Plazos fijos / FCI", "Bonos soberanos", "Acciones locales", "CEDEARs", "ETFs", "Opciones / Futuros", "Criptomonedas", "ONs (Obligaciones Negociables)"], label_visibility="collapsed", key="k1")

    q_label("¿Cuáles operaste realmente alguna vez?")
    k2 = st.multiselect("Operados", ["Plazos fijos / FCI", "Bonos soberanos", "Acciones locales", "CEDEARs", "ETFs", "Opciones / Futuros", "Criptomonedas", "ONs (Obligaciones Negociables)"], label_visibility="collapsed", key="k2")
    with st.expander("ℹ️ ¿Por qué me preguntan esto?"):
        info("La <strong>brecha entre conocidos y operados</strong> revela cuánto de tu conocimiento es teórico. Operar con dinero real genera un aprendizaje que la teoría no puede reemplazar.")

with col2:
    q_label("Una Obligación Negociable (ON) es:")
    k3_opts = ["Una acción de una empresa", "Deuda emitida por una empresa privada", "Deuda emitida por el Estado", "No lo sé con certeza"]
    k3 = st.radio("", k3_opts, key="k3", label_visibility="collapsed")
    with st.expander("ℹ️ ¿Para qué sirve esta pregunta?"):
        info("Las <strong>ONs</strong> son instrumentos de renta fija corporativa. No confundirlas con acciones ni con bonos soberanos es fundamental para armar una cartera coherente.")

    q_label("Si el dólar sube y la empresa emisora va bien, ¿qué le pasa a tu CEDEAR?")
    k4_opts = ["Sube solo por la empresa", "Sube solo por el dólar", "Sube por ambos factores", "No varía, es renta fija"]
    k4 = st.radio("", k4_opts, key="k4", label_visibility="collapsed")
    with st.expander("ℹ️ Clickeá acá para más información"):
        info("Los <strong>CEDEARs</strong> tienen doble exposición: al desempeño de la empresa subyacente y al tipo de cambio. Entender esto es clave para no llevarse sorpresas.")

    q_label("¿Cómo calificarías tu nivel de confianza para tomar decisiones hoy?")
    k5_opts = ["Muy baja — necesito ayuda para todo", "Baja — entiendo lo básico", "Media — me manejo solo en lo habitual", "Alta — tomo decisiones fundamentadas"]
    k5 = st.radio("", k5_opts, key="k5", label_visibility="collapsed")

    q_label("Compraste un activo a $100. Hoy vale $60. ¿Qué hacés?")
    k6_opts = ["Espero a que vuelva a $100 para vender sin pérdida", "Evalúo si el activo sigue siendo válido; si no, vendo", "Promedio a la baja y compro más barato", "Vendo de inmediato para no perder más"]
    k6 = st.radio("", k6_opts, key="k6", label_visibility="collapsed")
    with st.expander("ℹ️ Clickeá acá para más información"):
        info("El precio de compra es <strong>irrelevante para la decisión de hoy</strong>. El mercado no sabe ni le importa cuánto pagaste. Anclar decisiones al precio de entrada es uno de los sesgos más costosos.")

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
    Estudios de comportamiento financiero muestran que los inversores pierden más dinero
    por sus propias <strong>reacciones emocionales</strong> que por elegir instrumentos incorrectos.
    La disciplina — la capacidad de sostener una estrategia bajo presión — es el diferenciador real.
    """)

col1, col2 = st.columns(2)
with col1:
    q_label("¿Con qué frecuencia revisás tu cartera?")
    d1_opts = ["Varias veces al día", "Una vez por día", "Una vez por semana", "Una vez por mes o menos"]
    d1 = st.radio("", d1_opts, key="d1", label_visibility="collapsed")
    with st.expander("ℹ️ ¡Click acá!"):
        info("Revisar la cartera con alta frecuencia se asocia con <strong>mayor ansiedad y peores resultados</strong>. El ruido del corto plazo lleva a decisiones que dañan el rendimiento de largo plazo.")

    q_label("¿De dónde vienen principalmente tus decisiones de inversión?")
    d3_opts = ["Del estado de ánimo del momento", "De lo que leí en redes o grupos", "De análisis propio de cada activo", "De una estrategia definida que sigo"]
    d3 = st.radio("", d3_opts, key="d3", label_visibility="collapsed")
    with st.expander("ℹ️ ¿Qué es una 'fuente de decisión'?"):
        info("La <strong>fuente de decisión</strong> predice la consistencia mejor que el conocimiento. Un inversor con sistema mediocre suele ganarle a uno con mucho conocimiento pero sin proceso.")

    q_label("¿Cómo procesás los errores de inversión?")
    d5_opts = ["Los evito o no los reconozco", "Los atribuyo a mala suerte o al mercado", "Los analizo para entender qué falló", "Los incorporo como ajuste a mi sistema"]
    d5 = st.radio("", d5_opts, key="d5", label_visibility="collapsed")

    q_label("Antes de tomar una decisión de inversión, ¿qué hacés con la información que la contradice?")
    d6_opts = ["Generalmente no la busco o no la encuentro", "La veo pero le doy menos peso que a la que me da la razón", "La evalúo por igual que la información favorable", "La busco activamente para poner a prueba mi tesis"]
    d6 = st.radio("", d6_opts, key="d6", label_visibility="collapsed")
    with st.expander("ℹ️ ¿Qué es el sesgo de confirmación?"):
        info("El <strong>sesgo de confirmación</strong> es invisible porque se activa antes de la decisión. No es que ignoremos la evidencia contraria: es que directamente no la buscamos.")

with col2:
    q_label("En la última caída importante del mercado, ¿qué hiciste?")
    d2_opts = ["Vendí para detener las pérdidas", "Dudé mucho pero no hice nada", "Esperé sin demasiada ansiedad", "Aproveché para comprar más barato"]
    d2 = st.radio("", d2_opts, key="d2", label_visibility="collapsed")
    with st.expander("ℹ️ ¿Para qué sirve esta pregunta?"):
        info("El comportamiento <strong>durante una caída real</strong> es el mejor predictor de comportamiento futuro. Las respuestas a escenarios hipotéticos tienden a ser más racionales que las decisiones bajo presión.")

    q_label("¿Cuánto influyen las noticias financieras en tus decisiones?")
    d4_opts = ["Mucho — suelen cambiar mis posiciones", "Algo — las considero pero no siempre actúo", "Poco — las proceso pero tengo mis criterios", "Nada — sigo mi estrategia independientemente"]
    d4 = st.radio("", d4_opts, key="d4", label_visibility="collapsed")
    with st.expander("ℹ️ ¿Qué es el ruido informativo?"):
        info("El <strong>ruido informativo</strong> es uno de los mayores enemigos del inversor de largo plazo. La mayoría de las noticias financieras describe movimientos de corto plazo irrelevantes para una cartera bien estructurada.")

    q_label("¿Cuánto creés que tu análisis personal reduce el riesgo real de tus inversiones?")
    d7_opts = ["Mucho — el análisis detallado me protege de pérdidas", "Bastante — me ayuda a evitar errores grandes", "Algo — reduce ciertos riesgos pero no todos", "Poco — el mercado tiene mucha aleatoriedad que ningún análisis controla"]
    d7 = st.radio("", d7_opts, key="d7", label_visibility="collapsed")
    with st.expander("ℹ️ ¿Para qué sirve esta pregunta?"):
        info("El análisis es valioso, pero <strong>no elimina el riesgo</strong>. Creer que sí lo hace lleva a asumir posiciones más grandes de lo razonable. Los mejores inversores distinguen entre riesgo gestionable y aleatoriedad irreducible.")

    q_label("Cuando ganás dinero operando, ¿cómo tratás esas ganancias?")
    d8_opts = ["Las arriesgo más fácil — ya las 'gané en el mercado'", "Las reinvierto pero con los mismos criterios que el resto de mi capital", "Las paso a instrumentos más seguros para no perderlas", "No distingo de dónde vino el dinero — todo es el mismo capital"]
    d8 = st.radio("", d8_opts, key="d8", label_visibility="collapsed")
    with st.expander("ℹ️ ¿Por qué es importante el origen del dinero?"):
        info("Tratar las ganancias del mercado como 'dinero de la casa' es <strong>contabilidad mental</strong>. $1.000 ganados en una operación valen exactamente lo mismo que $1.000 ahorrados. El origen del dinero no debería cambiar el nivel de riesgo que aceptás.</p>")

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
        info("Haber atravesado una pérdida real y <strong>procesarla conscientemente</strong> es una de las experiencias formativas más valiosas. El mercado enseña lo que los libros no pueden.")

with col2:
    q_label("¿Tenés una estrategia de inversión que puedas describir en 2 oraciones?")
    e3_opts = ["No, voy decidiendo caso por caso", "Tengo algunas ideas pero no un sistema claro", "Sí, aunque no siempre la sigo", "Sí, y la aplico consistentemente"]
    e3 = st.radio("", e3_opts, key="e3", label_visibility="collapsed")
    with st.expander("ℹ️"):
        info("Poder <strong>articular tu estrategia</strong> es señal de que existe. Los inversores sin estrategia explícita suelen operar desde el ruido del momento.")

    q_label("¿Pudiste sostener una estrategia por más de 6 meses sin cambiarla fundamentalmente?")
    e4_opts = ["Nunca llegué a sostener una", "Lo intenté pero la cambié antes", "Casi siempre — con algunos desvíos", "Siempre — la consistencia es mi base"]
    e4 = st.radio("", e4_opts, key="e4", label_visibility="collapsed")

st.markdown('<hr class="dim-divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# BOTÓN
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
        st.error("Seleccioná al menos un objetivo de inversión.")
        st.stop()

    if total_pct != 100:
        st.error(f"La distribución de capital debe sumar 100%. Ahora suma {total_pct}%.")
        st.stop()

    # ── Scores ──
    R = np.mean([puntaje(r1, r1_opts), puntaje(r2, r2_opts), puntaje(r3, r3_opts), puntaje(r4, r4_opts)])

    # H = promedio ponderado de horizontes por objetivo (ponderado por % de capital)
    if objetivos_sel and sum(pct_capital.values()) > 0:
        H = sum(obj_horizonte.get(k, 0) * pct_capital.get(k, 0) for k in objetivos_sel) / sum(pct_capital.values())
    else:
        H = 5.0

    k_amplitud  = min((len(k1) + len(k2)) / 12 * 10, 10)
    k_brecha    = (len(k2) / max(len(k1), 1)) * 3
    k_correctas = (2 if k3 == "Deuda emitida por una empresa privada" else 0) + \
                  (2 if k4 == "Sube por ambos factores" else 0)
    k_confianza = puntaje(k5, k5_opts)
    # k6: ancla — la respuesta racional es evaluar el activo (opción 2), no esperar al precio de compra
    k_anclaje_ok = 1.5 if k6 == "Evalúo si el activo sigue siendo válido; si no, vendo" else 0
    K = min(k_amplitud * 0.35 + k_brecha + k_correctas + k_confianza * 0.3 + k_anclaje_ok, 10)

    D = np.mean([puntaje(d1, d1_opts), puntaje(d2, d2_opts), puntaje(d3, d3_opts),
                 puntaje(d4, d4_opts), puntaje(d5, d5_opts), puntaje(d6, d6_opts),
                 puntaje(d7, d7_opts), puntaje(d8, d8_opts)])
    E = np.mean([puntaje(e1, e1_opts), puntaje(e2, e2_opts), puntaje(e3, e3_opts), puntaje(e4, e4_opts)])

    vector = [round(R,2), round(H,2), round(D,2), round(K,2), round(E,2)]

    arquetipo = asignar_arquetipo(vector)
    arq_data  = ARQUETIPOS[arquetipo]

    # ── Sesgos ──
    sesgos_detectados = {}

    # Aversión a la pérdida: vendió en caída + no tolera pérdidas
    if d2 == "Vendí para detener las pérdidas" or (r1 == "Vendo todo, no puedo con esto" and r3 == "Prefiero no perder nada"):
        sesgos_detectados["Aversión a la pérdida"] = SESGOS_INFO["Aversión a la pérdida"]

    # Sobreconfianza: score de conocimiento bajo pero autoconfianza alta
    if K < 4 and k5 in ["Media — me manejo solo en lo habitual", "Alta — tomo decisiones fundamentadas"]:
        sesgos_detectados["Sobreconfianza"] = SESGOS_INFO["Sobreconfianza"]

    # Efecto manada: fuente de decisiones son redes/grupos
    if d3 == "De lo que leí en redes o grupos":
        sesgos_detectados["Efecto manada"] = SESGOS_INFO["Efecto manada"]

    # FOMO: prefiere angustia por oportunidad perdida sobre pérdida real
    if r5 == "Perder una oportunidad de ganarlo":
        sesgos_detectados["FOMO"] = SESGOS_INFO["FOMO"]

    # Exceso de actividad: revisa cartera muy seguido
    if d1 in ["Varias veces al día", "Una vez por día"]:
        sesgos_detectados["Exceso de actividad"] = SESGOS_INFO["Exceso de actividad"]

    # Efecto disposición: vende ganadores rápido (r4) Y/O vendió en caída (d2)
    if r4 == "Vendo todo, ya gané suficiente" and d2 == "Vendí para detener las pérdidas":
        sesgos_detectados["Efecto disposición"] = SESGOS_INFO["Efecto disposición"]
    elif r4 == "Vendo todo, ya gané suficiente" and d2 in ["Dudé mucho pero no hice nada", "Vendí para detener las pérdidas"]:
        sesgos_detectados["Efecto disposición"] = SESGOS_INFO["Efecto disposición"]

    # Sesgo de disponibilidad: decisiones muy influidas por noticias recientes
    if d4 == "Mucho — suelen cambiar mis posiciones" and d3 in ["Del estado de ánimo del momento", "De lo que leí en redes o grupos"]:
        sesgos_detectados["Sesgo de disponibilidad"] = SESGOS_INFO["Sesgo de disponibilidad"]

    # Sesgo de anclaje: espera volver al precio de compra antes de vender
    if k6 == "Espero a que vuelva a $100 para vender sin pérdida":
        sesgos_detectados["Sesgo de anclaje"] = SESGOS_INFO["Sesgo de anclaje"]

    # Ilusión de control: cree que su análisis elimina el riesgo, K moderado-alto (no es ignorancia)
    if d7 == "Mucho — el análisis detallado me protege de pérdidas" and K >= 4:
        sesgos_detectados["Ilusión de control"] = SESGOS_INFO["Ilusión de control"]

    # Sesgo de confirmación: no busca ni evalúa información contraria
    if d6 in ["Generalmente no la busco o no la encuentro", "La veo pero le doy menos peso que a la que me da la razón"]:
        sesgos_detectados["Sesgo de confirmación"] = SESGOS_INFO["Sesgo de confirmación"]

    # Contabilidad mental: trata ganancias del mercado como dinero para arriesgar más
    if d8 == "Las arriesgo más fácil — ya las 'gané en el mercado'":
        sesgos_detectados["Contabilidad mental"] = SESGOS_INFO["Contabilidad mental"]

    # ── Inconsistencias (incluyendo capital) ──
    inconsistencias = []
    if R > 6 and d2 == "Vendí para detener las pérdidas":
        inconsistencias.append({"titulo": "Riesgo declarado ≠ comportamiento real",
            "texto": f"Tu tolerancia al riesgo es alta ({round(R,1)}/10), pero vendiste en la última caída. Tu tolerancia real parece menor a la declarada."})

    # Horizonte: ahora detectamos inconsistencias a nivel objetivo
    for obj_key in objetivos_sel:
        h_obj = obj_horizonte.get(obj_key, 0)
        if obj_key == "largo_plazo" and h_obj < 5:
            inconsistencias.append({"titulo": "Largo plazo con horizonte corto",
                "texto": f"Declarás un objetivo de largo plazo, pero tu horizonte para ese capital es bajo ({round(h_obj,1)}/10). El largo plazo requiere capacidad real de no tocar el dinero por años."})
        if obj_key == "especulativo" and h_obj > 7:
            inconsistencias.append({"titulo": "Capital especulativo con horizonte muy largo",
                "texto": f"El capital especulativo suele tener horizontes cortos. Declarás un horizonte alto ({round(h_obj,1)}/10) para ese objetivo: revisá si realmente es especulativo o es largo plazo con otro nombre."})

    # Revisión frecuente contra horizonte agregado largo
    if H > 6 and d1 in ["Varias veces al día", "Una vez por día"]:
        inconsistencias.append({"titulo": "Horizonte largo + monitoreo de corto plazo",
            "texto": f"Tu horizonte agregado es largo ({round(H,1)}/10), pero revisás tu cartera con alta frecuencia. El ruido de corto plazo es irrelevante para objetivos largos — y genera decisiones emocionales."})

    if e3 in ["No, voy decidiendo caso por caso", "Lo intenté pero la cambié antes"] and d3 == "De una estrategia definida que sigo":
        inconsistencias.append({"titulo": "Estrategia declarada vs. realidad",
            "texto": "Decís que seguís una estrategia definida, pero reconocés que no podés sostenerla."})
    if K < 3 and R > 7:
        inconsistencias.append({"titulo": "Alto apetito de riesgo con base de conocimiento baja",
            "texto": f"Tu tolerancia al riesgo es alta ({round(R,1)}/10) pero tu conocimiento es bajo ({round(K,1)}/10). Asumir mucho riesgo sin entender los instrumentos es la combinación más cara del mercado."})

    # Ilusión de control + alta actividad + resultado mediocre
    if d7 == "Mucho — el análisis detallado me protege de pérdidas" and d1 in ["Varias veces al día", "Una vez por día"] and D < 5:
        inconsistencias.append({"titulo": "Ilusión de control + baja disciplina",
            "texto": "Creés que tu análisis te protege, pero tu disciplina conductual es baja. El seguimiento activo sin sistema genera la ilusión de control sin los beneficios."})

    # Confirmación + manada: combinación especialmente peligrosa
    if d6 in ["Generalmente no la busco o no la encuentro"] and d3 == "De lo que leí en redes o grupos":
        inconsistencias.append({"titulo": "Confirmación + efecto manada combinados",
            "texto": "Tomás decisiones desde redes y grupos, y no buscás información que las cuestione. Esta combinación es la más vulnerable a burbujas y narrativas de mercado."})

    # Contabilidad mental + capital especulativo alto
    if d8 == "Las arriesgo más fácil — ya las 'gané en el mercado'" and "especulativo" in objetivos_sel and pct_capital.get("especulativo", 0) > 25:
        inconsistencias.append({"titulo": "Contabilidad mental amplificando riesgo especulativo",
            "texto": f"Tratás las ganancias del mercado como dinero para arriesgar libremente, y tenés el {pct_capital.get('especulativo',0)}% en capital especulativo. Esta combinación escala el riesgo real muy por encima de lo que el perfil sugiere."})

    # Inconsistencias de capital
    for obj_key in objetivos_sel:
        obj    = OBJETIVOS_OPCIONES[obj_key]
        pct    = pct_capital.get(obj_key, 0)
        r_max  = obj["riesgo_max"]
        r_obj  = obj_riesgo.get(obj_key, R)
        if obj_key == "especulativo" and pct > 30 and K < 5:
            inconsistencias.append({
                "titulo": f"Concentración alta en especulativo con conocimiento bajo",
                "texto": f"Destinás el {pct}% de tu capital a objetivos especulativos, pero tu conocimiento financiero es {round(K,1)}/10. Esta combinación amplifica el riesgo real más allá de lo que el perfil sugiere."
            })
        if obj_key == "emergencia" and r_obj > 4:
            inconsistencias.append({
                "titulo": f"Tolerancia de riesgo alta para un fondo de emergencia",
                "texto": f"Para tu fondo de emergencia ({pct}% del capital), declarás una tolerancia al riesgo de {round(r_obj,1)}/10. Un fondo de emergencia debería estar en activos prácticamente sin riesgo."
            })
        if obj_key in ["largo_plazo"] and pct < 10 and E > 5:
            inconsistencias.append({
                "titulo": f"Poca exposición al largo plazo teniendo experiencia",
                "texto": f"Solo destinás el {pct}% de tu capital al largo plazo, pese a tener experiencia ({round(E,1)}/10). El horizonte largo es donde la experiencia genera más valor."
            })

    # ── Recomendaciones ──
    recomendaciones = []
    dims = {"Riesgo": R, "Horizonte": H, "Disciplina": D, "Conocimiento": K, "Experiencia": E}
    dim_mas_baja = min(dims, key=dims.get)
    rec_map = {
        "Riesgo":       "Tu tolerancia al riesgo es baja. Priorizá renta fija y fondos de bajo riesgo mientras construís experiencia. No asumas más riesgo del que podés mantener en una caída.",
        "Horizonte":    "Tu horizonte es corto. Asegurate de que el capital invertido sea el que realmente podés inmovilizar. El error clásico es invertir dinero que en realidad se necesita pronto.",
        "Disciplina":   "Tu disciplina conductual tiene margen de mejora. Definí reglas de entrada y salida antes de invertir, y revisiones periódicas programadas — no reactivas. Un sistema es tu mejor defensa contra el ruido del mercado.",
        "Conocimiento": "Tu base de conocimiento financiero es el área de mayor oportunidad. Antes de ampliar tu exposición, entendé cómo funciona cada instrumento que operás. El conocimiento reduce el riesgo real.",
        "Experiencia":  "La experiencia práctica lleva tiempo. Empezá con posiciones pequeñas en instrumentos simples, documentá tus decisiones y resultados. Aprender con poco capital es mucho más barato que aprender con mucho.",
    }
    recomendaciones.append({"dim": dim_mas_baja, "texto": rec_map[dim_mas_baja]})
    if D < 5:
        recomendaciones.append({"dim": "Disciplina (adicional)", "texto": "Establecé un ritual de revisión semanal o mensual — no más frecuente. Escribí tus tesis de inversión antes de invertir. Si no podés explicar en dos oraciones por qué compraste algo, la decisión fue emocional."})

    # ─────────────────────────────────────────────
    # OUTPUT
    # ─────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-title">◈ Tu diagnóstico</div>', unsafe_allow_html=True)

    # Arquetipo hero
    st.markdown(f"""
    <div class="result-hero">
        <div style="font-size:0.75rem; letter-spacing:0.2em; text-transform:uppercase; color:{arq_data['color']}; margin-bottom:0.8rem;">Tu arquetipo inversor</div>
        <div class="archetype-name" style="color:{arq_data['color']};">{arquetipo}</div>
        <div class="archetype-sub">{arq_data['descripcion']}</div>
    </div>
    """, unsafe_allow_html=True)

    # Radar
    labels = ["Riesgo", "Horizonte", "Disciplina", "Conocimiento", "Experiencia"]
    st.plotly_chart(radar_chart(labels, vector, color=arq_data['color']), use_container_width=True)

    # ── Síntesis IA ──
    with st.spinner("Generando síntesis conductual..."):
        sintesis_ia = generar_sintesis_ia(
            arquetipo, arq_data, vector, objetivos_sel, pct_capital,
            sesgos_detectados, inconsistencias, obj_riesgo, obj_horizonte
        )
    if sintesis_ia:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #13161e 0%, #0d1018 100%);
            border: 1px solid {arq_data['color']}40;
            border-left: 3px solid {arq_data['color']};
            border-radius: 10px;
            padding: 1.5rem 1.8rem;
            margin: 1.5rem 0 2rem;
        ">
            <div style="font-size:0.68rem; letter-spacing:0.2em; text-transform:uppercase;
                        color:{arq_data['color']}; margin-bottom:0.8rem; opacity:0.8;">
                ◈ Síntesis conductual · IA
            </div>
            <div style="font-size:0.95rem; color:#c8c4bc; line-height:1.8; font-style:italic;">
                {sintesis_ia}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Dimensiones con puntaje explícito ──
    st.markdown('<div class="section-title" style="font-size:1.2rem;">Tus dimensiones</div>', unsafe_allow_html=True)

    dim_data = [
        ("Riesgo",        R, "Tolerancia a la volatilidad"),
        ("Horizonte",     H, "Plazo y liquidez"),
        ("Disciplina",    D, "Control conductual"),
        ("Conocimiento",  K, "Base técnica"),
        ("Experiencia",   E, "Recorrido práctico"),
    ]

    cols = st.columns(5)
    for i, (nombre, valor, desc) in enumerate(dim_data):
        niv, col = nivel(valor)
        with cols[i]:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{nombre}</div>
                <div class="metric-value" style="color:{col};">{round(valor,1)}<span class="metric-over" style="font-size:1rem; color:var(--muted);"> /10</span></div>
                <div class="metric-range" style="color:{col};">{niv}</div>
            </div>
            """, unsafe_allow_html=True)
            barra(valor/10, col)
            st.markdown(f'<div style="font-size:0.72rem; color:var(--muted); margin-top:0.4rem; text-align:center;">{desc}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Distribución de capital ──
    st.markdown('<div class="section-title">Distribución de tu capital</div>', unsafe_allow_html=True)
    with st.expander("ℹ️ ¿Por qué analizamos la distribución de capital?"):
        info("""
        La <strong>distribución entre objetivos es una decisión de inversión en sí misma</strong>.
        El mismo perfil de riesgo se vuelve problemático si está mal asignado: mucho capital especulativo
        con poco conocimiento, o poco capital de largo plazo con mucha experiencia, son tensiones que
        este análisis pone en evidencia.
        """)

    # Gráfico de torta de distribución
    fig_pie = go.Figure(data=[go.Pie(
        labels=[f"{OBJETIVOS_OPCIONES[k]['icon']} {OBJETIVOS_OPCIONES[k]['nombre']}" for k in objetivos_sel],
        values=[pct_capital[k] for k in objetivos_sel],
        hole=0.55,
        marker=dict(colors=["#c8a96e","#6e9dc8","#6ec88a","#a96ec8","#c86e6e"][:len(objetivos_sel)]),
        textinfo="label+percent",
        textfont=dict(color="#e8e4dc", size=11),
    )])
    fig_pie.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
        height=280,
    )
    col_pie, col_cap = st.columns([1, 1])
    with col_pie:
        st.plotly_chart(fig_pie, use_container_width=True)
    with col_cap:
        st.markdown("<br>", unsafe_allow_html=True)
        for obj_key in objetivos_sel:
            obj   = OBJETIVOS_OPCIONES[obj_key]
            pct   = pct_capital[obj_key]
            r_obj = round(obj_riesgo.get(obj_key, R), 1)
            h_obj = round(obj_horizonte.get(obj_key, H), 1)
            r_max = obj["riesgo_max"]
            alerta = r_obj > r_max

            card_class = "capital-alert" if alerta else "capital-ok"
            icon_alert = "⚠" if alerta else "✓"
            msg = f"Riesgo declarado ({r_obj}/10) supera el máximo recomendado para este objetivo ({r_max}/10)." if alerta else f"Riesgo ({r_obj}/10) dentro del rango apropiado para este objetivo."

            st.markdown(f"""
            <div class="{card_class}">
                <div style="font-weight:600; margin-bottom:0.3rem;">{obj['icon']} {obj['nombre']} — {pct}%</div>
                <div style="font-size:0.8rem;">{icon_alert} {msg}</div>
                <div style="font-size:0.78rem; margin-top:0.2rem; opacity:0.8;">Horizonte: {h_obj}/10</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Por objetivo ──
    st.markdown('<div class="section-title">Análisis por objetivo</div>', unsafe_allow_html=True)

    interps = {
        "emergencia": {
            "afin":    "Tu perfil es compatible con este objetivo. Preservación de capital y liquidez inmediata es exactamente lo que un fondo de emergencia necesita.",
            "tension": f"Tu tolerancia al riesgo general ({round(R,1)}/10) es alta para un fondo de emergencia. Este capital no debería estar en activos volátiles, sin importar tu perfil general.",
            "neutro":  "Este objetivo requiere máxima liquidez y mínima volatilidad. Priorizá instrumentos como cuentas remuneradas, FCI money market o plazos fijos renovables."
        },
        "ahorro": {
            "afin":    "Tu perfil se alinea bien con un objetivo de ahorro en dólares. Priorizá preservación del poder adquisitivo con exposición controlada al riesgo cambiario.",
            "tension": f"Con riesgo {round(R,1)}/10, tendés a buscar más retorno del que un objetivo de ahorro justifica. Separar el capital de ahorro del capital de inversión ayuda a no mezclar criterios.",
            "neutro":  "Para ahorro en dólares considerá CEDEARs defensivos, ONs dollar-linked o FCI en dólares. La consistencia de aportes importa más que el instrumento."
        },
        "objetivo": {
            "afin":    "Tenés horizonte y disciplina compatibles con un objetivo concreto. La clave es no cambiar la estrategia cuando el mercado se ponga volátil cerca de la fecha.",
            "tension": f"El mayor riesgo es tu horizonte ({round(H,1)}/10). Si la fecha del objetivo es cercana, reducí la exposición al riesgo progresivamente.",
            "neutro":  "Con objetivo concreto y plazo definido, la cartera debería ir reduciendo riesgo a medida que se acerca la fecha. Definí hoy cuándo y cómo vas a hacer ese ajuste."
        },
        "largo_plazo": {
            "afin":    f"Tu horizonte ({round(H,1)}/10) y disciplina ({round(D,1)}/10) son activos clave para largo plazo. El interés compuesto requiere exactamente lo que tenés: tiempo y paciencia.",
            "tension": f"La inversión de largo plazo es tu objetivo más desafiante. El riesgo: que la baja disciplina ({round(D,1)}/10) te lleve a cambios de estrategia en el momento equivocado.",
            "neutro":  "Para largo plazo: activos de crecimiento diversificados, aportes periódicos, revisión anual. La frecuencia de decisiones debería ser mínima."
        },
        "especulativo": {
            "afin":    f"Tu apetito de riesgo ({round(R,1)}/10) es compatible con capital especulativo. Asegurate de que este capital sea una porción pequeña que podés perder sin que afecte tu vida.",
            "tension": "El capital especulativo requiere tolerancia real a pérdidas del 30-50% o más. Si tu comportamiento en caídas muestra ansiedad o venta de pánico, puede hacerte daño.",
            "neutro":  "Para capital especulativo, el tamaño de la posición importa más que el instrumento. Definí antes de invertir cuánto máximo podés perder en esa posición."
        },
    }

    for obj_key in objetivos_sel:
        obj        = OBJETIVOS_OPCIONES[obj_key]
        es_afin    = obj_key in arq_data["objetivos_afines"]
        es_tension = obj_key in arq_data["objetivos_tension"]
        tipo       = "afin" if es_afin else ("tension" if es_tension else "neutro")
        tag_color  = "#6ec88a" if es_afin else ("#c86e6e" if es_tension else "#c8a96e")
        tag_texto  = "Afinidad alta" if es_afin else ("Tensión detectada" if es_tension else "Compatible")

        r_obj = round(obj_riesgo.get(obj_key, R), 1)
        h_obj = round(obj_horizonte.get(obj_key, H), 1)

        st.markdown(f'<div class="obj-result-header">{obj["icon"]} {obj["nombre"]} — {pct_capital[obj_key]}% del capital</div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns([3, 1, 1])
        with c1:
            border = "#3a2020" if es_tension else ("#1e3020" if es_afin else "var(--border)")
            bg     = "#1a1214" if es_tension else ("#141a14" if es_afin else "var(--card)")
            st.markdown(f"""
            <div style="background:{bg}; border:1px solid {border}; border-radius:8px; padding:1rem 1.2rem; font-size:0.88rem; color:var(--muted); line-height:1.7;">
                {interps[obj_key][tipo]}
            </div>
            """, unsafe_allow_html=True)
        with c2:
            niv_r, col_r = nivel(r_obj)
            st.markdown(f"""
            <div class="metric-card" style="text-align:center;">
                <div class="metric-label">Riesgo obj.</div>
                <div class="metric-value" style="color:{col_r}; font-size:1.6rem;">{r_obj}<span style="font-size:0.85rem; color:var(--muted);"> /10</span></div>
                <div class="metric-range" style="color:{col_r};">{niv_r}</div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            niv_h, col_h = nivel(h_obj)
            st.markdown(f"""
            <div class="metric-card" style="text-align:center;">
                <div class="metric-label">Horizonte obj.</div>
                <div class="metric-value" style="color:{col_h}; font-size:1.6rem;">{h_obj}<span style="font-size:0.85rem; color:var(--muted);"> /10</span></div>
                <div class="metric-range" style="color:{col_h};">{niv_h}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Inconsistencias ──
    if inconsistencias:
        st.markdown('<div class="section-title">⚠️ Inconsistencias detectadas</div>', unsafe_allow_html=True)
        with st.expander("ℹ️ ¿Qué es una inconsistencia conductual?"):
            info("Una inconsistencia aparece cuando dos respuestas apuntan en direcciones opuestas. <strong>La brecha entre lo que creemos que somos y cómo actuamos en realidad</strong> es exactamente lo que los tests tradicionales no detectan.")
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
            info("Los sesgos son <strong>patrones sistemáticos de pensamiento</strong> que desvían nuestras decisiones de lo racional. Identificarlos no los elimina, pero permite diseñar sistemas que los compensen.")
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

    # ── Por qué es diferente ──
    st.markdown('<div class="section-title" style="margin-top:3rem;">¿Por qué este diagnóstico es diferente?</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:var(--card); border:1px solid var(--border); border-radius:12px; padding:2rem; font-size:0.9rem; color:var(--muted); line-height:1.8;">
        <p>Los tests de perfil inversor convencionales tienen un problema estructural: colapsan toda la complejidad de una persona en una única dimensión — la aversión al riesgo — y producen una etiqueta. El 99% de los inversores termina clasificado como "moderado", lo cual no ayuda a nadie.</p>
        <p><strong style="color:var(--accent)">1. Comportamiento ≠ autopercepción.</strong> No alcanza con saber cómo te describís. Importa cómo actuaste en la última caída real, con qué frecuencia revisás tu cartera, de dónde vienen tus decisiones.</p>
        <p><strong style="color:var(--accent)">2. Un inversor no es un único perfil.</strong> La misma persona puede ser conservadora con su fondo de emergencia y especulativa con otro capital — y eso es completamente racional. La distribución de capital entre objetivos es una decisión de inversión en sí misma.</p>
        <p><strong style="color:var(--accent)">3. Las inconsistencias son la información más valiosa.</strong> La brecha entre lo que creemos que somos y cómo actuamos en realidad es lo que los tests tradicionales no capturan — y lo que este modelo pone en el centro.</p>
        <p>El resultado no es una etiqueta. Es un mapa. Ahora depende de vos caminarlo y avanzar.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── EXPORT PDF ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title" style="font-size:1.2rem;">Exportar diagnóstico</div>', unsafe_allow_html=True)

    with st.spinner("Generando PDF..."):
        pdf_buffer = generar_pdf(
            arquetipo, arq_data, vector, objetivos_sel, pct_capital,
            sesgos_detectados, inconsistencias, recomendaciones,
            obj_riesgo, obj_horizonte, sintesis_ia
        )

    st.download_button(
        label="⬇  Descargar reporte en PDF",
        data=pdf_buffer,
        file_name="diagnostico_inversor.pdf",
        mime="application/pdf",
    )

st.markdown("""
<div class="footer">
    <strong>Diagnóstico Conductual del Inversor</strong><br>
     FCE UNLP · Seminario de Finanzas e Inversiones en la Era IA · 2026<br><br>
    <span style="opacity:0.5;">Conceptos aplicados: Aversión a la pérdida, Contabilidad mental, Efecto manada, FOMO, Exceso de actividad, disposition effect (venta prematura)</span>
</div>
""", unsafe_allow_html=True)
