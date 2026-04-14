import streamlit as st
import numpy as np
import plotly.graph_objects as go
import math
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT

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
# PDF EXPORT
# ─────────────────────────────────────────────
def generar_pdf(arquetipo, arq_data, vector, objetivos_sel, pct_capital,
                sesgos_detectados, inconsistencias, recomendaciones,
                obj_riesgo, obj_horizonte):

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    # Colores
    GOLD   = colors.HexColor("#c8a96e")
    DARK   = colors.HexColor("#0d0f14")
    GRAY   = colors.HexColor("#7a7d8a")
    RED    = colors.HexColor("#c86e6e")
    BLUE   = colors.HexColor("#6e9dc8")
    GREEN  = colors.HexColor("#6ec88a")
    WHITE  = colors.white

    styles = getSampleStyleSheet()

    s_title = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=22,
                             textColor=GOLD, spaceAfter=6, alignment=TA_CENTER)
    s_sub   = ParagraphStyle("sub", fontName="Helvetica", fontSize=10,
                             textColor=GRAY, spaceAfter=16, alignment=TA_CENTER)
    s_h2    = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=14,
                             textColor=GOLD, spaceBefore=18, spaceAfter=6)
    s_h3    = ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=11,
                             textColor=WHITE, spaceBefore=10, spaceAfter=4)
    s_body  = ParagraphStyle("body", fontName="Helvetica", fontSize=9,
                             textColor=GRAY, spaceAfter=6, leading=14)
    s_bold  = ParagraphStyle("bold", fontName="Helvetica-Bold", fontSize=9,
                             textColor=WHITE, spaceAfter=4)
    s_arch  = ParagraphStyle("arch", fontName="Helvetica-Bold", fontSize=18,
                             textColor=colors.HexColor(arq_data["color"]),
                             spaceAfter=8, alignment=TA_CENTER)

    story = []

    # Header
    story.append(Paragraph("DIAGNÓSTICO CONDUCTUAL DEL INVERSOR", s_title))
    story.append(Paragraph("Finanzas e Inversiones en la Era IA · FCE UNLP", s_sub))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))

    # Arquetipo
    story.append(Paragraph("TU ARQUETIPO", s_h2))
    story.append(Paragraph(arquetipo, s_arch))
    story.append(Paragraph(arq_data["descripcion"], s_body))
    story.append(Spacer(1, 12))

    # Dimensiones tabla
    story.append(Paragraph("DIMENSIONES", s_h2))
    labels = ["Riesgo", "Horizonte", "Disciplina", "Conocimiento", "Experiencia"]
    dim_data_table = [["Dimensión", "Puntaje", "Nivel"]]
    for lbl, val in zip(labels, vector):
        niv, _ = nivel(val)
        dim_data_table.append([lbl, f"{round(val,1)} / 10", niv])

    t = Table(dim_data_table, colWidths=[5*cm, 4*cm, 4*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0),  colors.HexColor("#1e2330")),
        ("TEXTCOLOR",    (0,0), (-1,0),  GOLD),
        ("FONTNAME",     (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 9),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [colors.HexColor("#13161e"), colors.HexColor("#161921")]),
        ("TEXTCOLOR",    (0,1), (-1,-1), WHITE),
        ("GRID",         (0,0), (-1,-1), 0.5, colors.HexColor("#1e2330")),
        ("ALIGN",        (1,0), (-1,-1), "CENTER"),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",   (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))

    # Distribución de capital
    story.append(Paragraph("DISTRIBUCIÓN DE CAPITAL POR OBJETIVO", s_h2))
    cap_data = [["Objetivo", "% Capital", "Riesgo obj.", "Horizonte obj."]]
    for obj_key in objetivos_sel:
        obj    = OBJETIVOS_OPCIONES[obj_key]
        pct    = pct_capital.get(obj_key, 0)
        r_obj  = round(obj_riesgo.get(obj_key, 0), 1)
        h_obj  = round(obj_horizonte.get(obj_key, 0), 1)
        cap_data.append([obj["nombre"], f"{pct}%", f"{r_obj}/10", f"{h_obj}/10"])

    t2 = Table(cap_data, colWidths=[5*cm, 3*cm, 3.5*cm, 3.5*cm])
    t2.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  colors.HexColor("#1e2330")),
        ("TEXTCOLOR",     (0,0), (-1,0),  GOLD),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 9),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),  [colors.HexColor("#13161e"), colors.HexColor("#161921")]),
        ("TEXTCOLOR",     (0,1), (-1,-1), WHITE),
        ("GRID",          (0,0), (-1,-1), 0.5, colors.HexColor("#1e2330")),
        ("ALIGN",         (1,0), (-1,-1), "CENTER"),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(t2)
    story.append(Spacer(1, 12))

    # Inconsistencias
    if inconsistencias:
        story.append(Paragraph("INCONSISTENCIAS DETECTADAS", s_h2))
        for inc in inconsistencias:
            story.append(Paragraph(f"▲ {inc['titulo']}", s_bold))
            story.append(Paragraph(inc["texto"], s_body))

    # Sesgos
    if sesgos_detectados:
        story.append(Paragraph("SESGOS CONDUCTUALES", s_h2))
        for nombre, desc in sesgos_detectados.items():
            story.append(Paragraph(f"◉ {nombre}", s_bold))
            story.append(Paragraph(desc, s_body))

    # Recomendaciones
    story.append(Paragraph("PRÓXIMOS PASOS", s_h2))
    for rec in recomendaciones:
        story.append(Paragraph(f"→ {rec['dim']}", s_bold))
        story.append(Paragraph(rec["texto"], s_body))

    # Footer
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GRAY))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Basado en principios de finanzas conductuales: aversión a la pérdida, contabilidad mental, efecto manada y sesgos de exceso de confianza.",
        ParagraphStyle("footer_txt", fontName="Helvetica", fontSize=7, textColor=GRAY, alignment=TA_CENTER)
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer

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
    with st.expander("ℹ️"):
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
    with st.expander("ℹ️"):
        info("El <strong>disposition effect</strong>: los inversores tienden a vender ganadores rápido y retener perdedores. Detectar esta tendencia permite corregirla.")

q_label("¿Qué te genera más malestar?")
r5_opts = ["Perder dinero que ya tenía", "Perder una oportunidad de ganarlo"]
r5 = st.radio("", r5_opts, key="r5", label_visibility="collapsed")
with st.expander("ℹ️"):
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
    """)

col1, col2 = st.columns(2)
with col1:
    q_label("¿Con qué frecuencia necesitás liquidez de tus inversiones en general?")
    h_liq_opts = ["Regularmente, es parte de mis ingresos", "Ocasionalmente ante imprevistos", "Casi nunca, tengo otras fuentes", "Nunca, tengo todo cubierto aparte"]
    h_liq = st.radio("", h_liq_opts, key="h_liq", label_visibility="collapsed")

with col2:
    q_label("¿Cómo pensás cobrar los frutos de tus inversiones?")
    h3_opts = ["Necesito ingresos periódicos ya", "Mezcla de reinversión y retiros", "Reinvierto todo, no toco nada", "No tengo claro todavía"]
    h3 = st.radio("", h3_opts, key="h3", label_visibility="collapsed")
    with st.expander("ℹ️"):
        info("La <strong>estructura de retiros</strong> condiciona qué activos son adecuados. Quien necesita renta regular no puede estar 100% en activos de crecimiento.")

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
    with st.expander("ℹ️"):
        info("La <strong>brecha entre conocidos y operados</strong> revela cuánto de tu conocimiento es teórico. Operar con dinero real genera un aprendizaje que la teoría no puede reemplazar.")

with col2:
    q_label("Una Obligación Negociable (ON) es:")
    k3_opts = ["Una acción de una empresa", "Deuda emitida por una empresa privada", "Deuda emitida por el Estado", "No lo sé con certeza"]
    k3 = st.radio("", k3_opts, key="k3", label_visibility="collapsed")
    with st.expander("ℹ️"):
        info("Las <strong>ONs</strong> son instrumentos de renta fija corporativa. No confundirlas con acciones ni con bonos soberanos es fundamental para armar una cartera coherente.")

    q_label("Si el dólar sube y la empresa emisora va bien, ¿qué le pasa a tu CEDEAR?")
    k4_opts = ["Sube solo por la empresa", "Sube solo por el dólar", "Sube por ambos factores", "No varía, es renta fija"]
    k4 = st.radio("", k4_opts, key="k4", label_visibility="collapsed")
    with st.expander("ℹ️"):
        info("Los <strong>CEDEARs</strong> tienen doble exposición: al desempeño de la empresa subyacente y al tipo de cambio. Entender esto es clave para no llevarse sorpresas.")

    q_label("¿Cómo calificarías tu nivel de confianza para tomar decisiones hoy?")
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
    Estudios de comportamiento financiero muestran que los inversores pierden más dinero
    por sus propias <strong>reacciones emocionales</strong> que por elegir instrumentos incorrectos.
    La disciplina — la capacidad de sostener una estrategia bajo presión — es el diferenciador real.
    """)

col1, col2 = st.columns(2)
with col1:
    q_label("¿Con qué frecuencia revisás tu cartera?")
    d1_opts = ["Varias veces al día", "Una vez por día", "Una vez por semana", "Una vez por mes o menos"]
    d1 = st.radio("", d1_opts, key="d1", label_visibility="collapsed")
    with st.expander("ℹ️"):
        info("Revisar la cartera con alta frecuencia se asocia con <strong>mayor ansiedad y peores resultados</strong>. El ruido del corto plazo lleva a decisiones que dañan el rendimiento de largo plazo.")

    q_label("¿De dónde vienen principalmente tus decisiones de inversión?")
    d3_opts = ["Del estado de ánimo del momento", "De lo que leí en redes o grupos", "De análisis propio de cada activo", "De una estrategia definida que sigo"]
    d3 = st.radio("", d3_opts, key="d3", label_visibility="collapsed")
    with st.expander("ℹ️"):
        info("La <strong>fuente de decisión</strong> predice la consistencia mejor que el conocimiento. Un inversor con sistema mediocre suele ganarle a uno con mucho conocimiento pero sin proceso.")

    q_label("¿Cómo procesás los errores de inversión?")
    d5_opts = ["Los evito o no los reconozco", "Los atribuyo a mala suerte o al mercado", "Los analizo para entender qué falló", "Los incorporo como ajuste a mi sistema"]
    d5 = st.radio("", d5_opts, key="d5", label_visibility="collapsed")

with col2:
    q_label("En la última caída importante del mercado, ¿qué hiciste?")
    d2_opts = ["Vendí para detener las pérdidas", "Dudé mucho pero no hice nada", "Esperé sin demasiada ansiedad", "Aproveché para comprar más barato"]
    d2 = st.radio("", d2_opts, key="d2", label_visibility="collapsed")
    with st.expander("ℹ️"):
        info("El comportamiento <strong>durante una caída real</strong> es el mejor predictor de comportamiento futuro. Las respuestas a escenarios hipotéticos tienden a ser más racionales que las decisiones bajo presión.")

    q_label("¿Cuánto influyen las noticias financieras en tus decisiones?")
    d4_opts = ["Mucho — suelen cambiar mis posiciones", "Algo — las considero pero no siempre actúo", "Poco — las proceso pero tengo mis criterios", "Nada — sigo mi estrategia independientemente"]
    d4 = st.radio("", d4_opts, key="d4", label_visibility="collapsed")
    with st.expander("ℹ️"):
        info("El <strong>ruido informativo</strong> es uno de los mayores enemigos del inversor de largo plazo. La mayoría de las noticias financieras describe movimientos de corto plazo irrelevantes para una cartera bien estructurada.")

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
    H = np.mean([
        puntaje(h_liq, h_liq_opts),
        puntaje(h3, h3_opts),
    ])
    k_amplitud  = min((len(k1) + len(k2)) / 12 * 10, 10)
    k_brecha    = (len(k2) / max(len(k1), 1)) * 3
    k_correctas = (2 if k3 == "Deuda emitida por una empresa privada" else 0) + \
                  (2 if k4 == "Sube por ambos factores" else 0)
    k_confianza = puntaje(k5, k5_opts)
    K = min(k_amplitud * 0.35 + k_brecha + k_correctas + k_confianza * 0.3, 10)
    D = np.mean([puntaje(d1, d1_opts), puntaje(d2, d2_opts), puntaje(d3, d3_opts), puntaje(d4, d4_opts), puntaje(d5, d5_opts)])
    E = np.mean([puntaje(e1, e1_opts), puntaje(e2, e2_opts), puntaje(e3, e3_opts), puntaje(e4, e4_opts)])

    vector = [round(R,2), round(H,2), round(D,2), round(K,2), round(E,2)]

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
        sesgos_detectados["FOMO"] = SESGOS_INFO["FOMO"]
    if d1 in ["Varias veces al día", "Una vez por día"]:
        sesgos_detectados["Exceso de actividad"] = SESGOS_INFO["Exceso de actividad"]

    # ── Inconsistencias (incluyendo capital) ──
    inconsistencias = []
    if R > 6 and d2 == "Vendí para detener las pérdidas":
        inconsistencias.append({"titulo": "Riesgo declarado ≠ comportamiento real",
            "texto": f"Tu tolerancia al riesgo es alta ({round(R,1)}/10), pero vendiste en la última caída. Tu tolerancia real parece menor a la declarada."})
    if H > 7 and d1 in ["Varias veces al día", "Una vez por día"]:
        inconsistencias.append({"titulo": "Horizonte largo + monitoreo de corto plazo",
            "texto": f"Declarás un horizonte largo ({round(H,1)}/10), pero revisás tu cartera con alta frecuencia. El ruido de corto plazo es irrelevante para objetivos largos."})
    if e3 in ["No, voy decidiendo caso por caso", "Lo intenté pero la cambié antes"] and d3 == "De una estrategia definida que sigo":
        inconsistencias.append({"titulo": "Estrategia declarada vs. realidad",
            "texto": "Decís que seguís una estrategia definida, pero reconocés que no podés sostenerla."})
    if K < 3 and R > 7:
        inconsistencias.append({"titulo": "Alto apetito de riesgo con base de conocimiento baja",
            "texto": f"Tu tolerancia al riesgo es alta ({round(R,1)}/10) pero tu conocimiento es bajo ({round(K,1)}/10). Asumir mucho riesgo sin entender los instrumentos es la combinación más cara del mercado."})

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
            obj_riesgo, obj_horizonte
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
