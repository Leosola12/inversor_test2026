import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Diagnóstico Inversor", layout="wide")

st.title("📊 Diagnóstico Integral del Inversor")
st.markdown("Este análisis evalúa cómo pensás, decidís y actuás al invertir.")

# -----------------------
# SCORING NO LINEAL
# -----------------------
def score(v):
    if v <= 2:
        return 2
    elif v == 3:
        return 5
    else:
        return 8

def idx(val, options):
    return options.index(val) + 1

# -----------------------
# RIESGO
# -----------------------
st.header("🟥 Riesgo")

q1 = st.radio("Tu cartera cae 25%:", ["Vendo todo","Vendo parte","Mantengo","Compro más"])
q2 = st.radio("Elegís inversión:", ["Segura","Moderada","Volátil","Alto riesgo"])
q3 = st.radio("Pérdida tolerada:", ["0%","10%","25%","+25%"])
q4 = st.radio("Sube 40%:", ["Vendo","Parcial","Mantengo","Compro más"])
q5 = st.radio("¿Qué te pesa más?", ["Perder dinero","Perder oportunidad"])

# -----------------------
# HORIZONTE
# -----------------------
st.header("🟨 Horizonte")

q6 = st.radio("Necesidad del dinero:", ["<6 meses","6m-2 años","2-5 años","+5 años"])
q7 = st.radio("Uso en emergencia:", ["Sí","Tal vez","Poco probable","No"])

# -----------------------
# DISCIPLINA
# -----------------------
st.header("🟪 Disciplina")

q8 = st.radio("Frecuencia de revisión:", ["Varias veces al día","Diario","Semanal","Mensual"])
q9 = st.radio("Última caída:", ["Vendí","Dudé","Esperé","Compré"])
q10 = st.radio("Decisiones:", ["Emoción","Redes","Análisis","Estrategia"])
q11 = st.radio("Noticias influyen:", ["Mucho","Algo","Poco","Nada"])
q12 = st.radio("Errores:", ["Evito","Culpo","Analizo","Ajusto"])

# -----------------------
# CONOCIMIENTO
# -----------------------
st.header("🟦 Conocimiento")

q13 = st.multiselect("Instrumentos conocidos:", ["Bonos","Acciones","CEDEARs","ETF","Crypto"])
q14 = st.multiselect("Instrumentos operados:", ["Bonos","Acciones","CEDEARs","ETF","Crypto"])
q15 = st.radio("ON:", ["Acción","Deuda empresa","Estado","No sé"])
q16 = st.radio("CEDEAR baja:", ["Empresa","Dólar","Ambos","No baja"])
q17 = st.radio("Confianza:", ["Baja","Media","Alta","Muy alta"])

# -----------------------
# EXPERIENCIA
# -----------------------
st.header("🟧 Experiencia")

q18 = st.radio("Años:", ["<1","1-2","2-5","5+"])
q19 = st.radio("Pérdidas:", ["Nunca","No entendí","Aprendí","Varias"])
q20 = st.radio("Método:", ["Redes","Noticias","Criterio propio","Sistema"])
q21 = st.radio("Estrategia sostenida:", ["Nunca","Intento","Casi siempre","Siempre"])

# -----------------------
# OBJETIVO
# -----------------------
st.header("🟩 Contexto")

q22 = st.radio("Claridad:", ["Nula","Baja","Media","Alta"])
q23 = st.selectbox("Objetivo:", ["Emergencia","Ahorro","Objetivo","Inversión"])

# -----------------------
# CALCULO
# -----------------------
if st.button("Generar Informe"):

    R = np.mean([
        score(idx(q1,["Vendo todo","Vendo parte","Mantengo","Compro más"])),
        score(idx(q2,["Segura","Moderada","Volátil","Alto riesgo"])),
        score(idx(q3,["0%","10%","25%","+25%"])),
        score(idx(q4,["Vendo","Parcial","Mantengo","Compro más"]))
    ])

    H = np.mean([
        score(idx(q6,["<6 meses","6m-2 años","2-5 años","+5 años"])),
        score(idx(q7,["Sí","Tal vez","Poco probable","No"]))
    ])

    D = np.mean([
        score(idx(q8,["Varias veces al día","Diario","Semanal","Mensual"])),
        score(idx(q9,["Vendí","Dudé","Esperé","Compré"])),
        score(idx(q10,["Emoción","Redes","Análisis","Estrategia"])),
        score(idx(q11,["Mucho","Algo","Poco","Nada"])),
        score(idx(q12,["Evito","Culpo","Analizo","Ajusto"]))
    ])

    K = min(((len(q13)+len(q14)+(3 if q15=="Deuda empresa" else 0)+(3 if q16=="Ambos" else 0))/15)*10,10)

    E = np.mean([
        score(idx(q18,["<1","1-2","2-5","5+"])),
        score(idx(q19,["Nunca","No entendí","Aprendí","Varias"])),
        score(idx(q20,["Redes","Noticias","Criterio propio","Sistema"])),
        score(idx(q21,["Nunca","Intento","Casi siempre","Siempre"]))
    ])

    C = score(idx(q22,["Nula","Baja","Media","Alta"]))

    # -----------------------
    # CONSISTENCIA
    # -----------------------
    inconsistencias = 0

    if R > 7 and q9 == "Vendí":
        inconsistencias += 1

    if H > 7 and q8 == "Varias veces al día":
        inconsistencias += 1

    if q21 == "Nunca" and q10 == "Estrategia":
        inconsistencias += 1

    if inconsistencias == 0:
        CONS = "Alta"
    elif inconsistencias == 1:
        CONS = "Media"
    else:
        CONS = "Baja"

    # -----------------------
    # SESGOS
    # -----------------------
    sesgos = []

    if q9 == "Vendí":
        sesgos.append("Aversión a la pérdida")

    if K < 4 and q17 == "Muy alta":
        sesgos.append("Sobreconfianza")

    if q10 == "Redes":
        sesgos.append("Efecto manada")

    if q5 == "Perder oportunidad":
        sesgos.append("FOMO")

    # -----------------------
    # ARQUETIPOS (9)
    # -----------------------
    arche = "Perfil mixto"

    if R <= 3 and H >= 7 and q23 == "Emergencia":
        arche = "Guardián"
    elif K >= 7 and D <= 4:
        arche = "Ansioso informado"
    elif 5 <= R <= 7 and D >= 7 and K >= 6 and CONS == "Alta":
        arche = "Estratega"
    elif R >= 8 and H <= 4 and q23 == "Inversión" and C <= 5:
        arche = "Especulador puro"
    elif K >= 8 and D >= 6 and E <= 4:
        arche = "Técnico paralizado"
    elif E >= 7 and K <= 4:
        arche = "Intuitivo"
    elif K <= 4 and D >= 6 and C >= 6:
        arche = "Principiante consciente"
    elif H >= 8 and 4 <= R <= 6 and D >= 6:
        arche = "Acumulador"
    elif R >= 7 and K <= 3 and C <= 4:
        arche = "Confiado sin mapa"

    # -----------------------
    # OUTPUT
    # -----------------------

    st.header("📋 Informe del Inversor")

    st.subheader("📊 Métricas")
    st.write(f"Riesgo: {round(R,1)}")
    st.write(f"Horizonte: {round(H,1)}")
    st.write(f"Disciplina: {round(D,1)}")
    st.write(f"Conocimiento: {round(K,1)}")
    st.write(f"Experiencia: {round(E,1)}")
    st.write(f"Consistencia: {CONS}")

    st.subheader("🧬 Arquetipo")
    st.write(f"**{arche}**")

    if sesgos:
        st.subheader("⚠️ Sesgos detectados")
        st.write(", ".join(sesgos))

    st.subheader("📈 Mapa del Perfil")

    labels = ['Riesgo','Horizonte','Disciplina','Conocimiento','Experiencia']
    values = [R,H,D,K,E]
    values += values[:1]

    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(subplot_kw=dict(polar=True))
    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    st.pyplot(fig)

    # -----------------------
    # BLOQUE DIFERENCIAL
    # -----------------------
    st.header("🧠 ¿Por qué este diagnóstico es distinto?")

    st.markdown("""
Este no es un test tradicional de perfil inversor.

La mayoría de los cuestionarios clasifican a las personas en categorías simples como "conservador", "moderado" o "agresivo".  
Eso asume que el inversor es consistente en todas sus decisiones, lo cual rara vez ocurre en la práctica.

Este modelo parte de una idea distinta:

**no importa solo lo que decís que sos, sino cómo realmente actuás.**

Por eso, este diagnóstico:

- Separa comportamiento (riesgo, disciplina, horizonte) de capacidad (conocimiento, experiencia)
- Detecta inconsistencias entre lo que pensás y lo que hacés
- Identifica sesgos conductuales que afectan decisiones reales
- Integra el contexto del dinero (objetivo y claridad)

El resultado no es una etiqueta, sino un mapa de tu comportamiento como inversor.

En la práctica, dos personas con el mismo perfil de riesgo pueden tener resultados completamente distintos.  
La diferencia suele estar en la disciplina, la consistencia y la forma en que reaccionan ante la incertidumbre.

Este test intenta capturar justamente eso.
    """)
