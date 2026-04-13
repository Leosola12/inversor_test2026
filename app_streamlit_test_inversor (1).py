import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Diagnóstico Inversor", layout="wide")

st.title("📊 Diagnóstico Integral del Inversor")
st.markdown("Este informe analiza cómo pensás, decidís y actuás al invertir.")

# -----------------------
# HELPERS
# -----------------------
def scale(v):
    return (v-1)/3*10

def idx(val, options):
    return options.index(val) + 1

# -----------------------
# RIESGO
# -----------------------
st.header("🟥 Riesgo")

q1 = st.radio("Tu cartera cae 25% en un mes:", [
    "Vendo todo","Vendo parte","Mantengo","Compro más"
])

q2 = st.radio("Elegís una inversión:", [
    "Segura","Moderada","Volátil","Alto riesgo"
])

q3 = st.radio("Pérdida tolerada:", [
    "0%","10%","25%","+25%"
])

q4 = st.radio("Sube 40%:", [
    "Vendo","Parcial","Mantengo","Compro más"
])

# -----------------------
# HORIZONTE
# -----------------------
st.header("🟨 Horizonte")

q5 = st.radio("¿Cuándo necesitás el dinero?", [
    "<6 meses","6m-2 años","2-5 años","+5 años"
])

q6 = st.radio("¿Es para emergencia?", [
    "Sí","Tal vez","Poco probable","No"
])

# -----------------------
# DISCIPLINA
# -----------------------
st.header("🟪 Disciplina")

q7 = st.radio("Frecuencia de revisión:", [
    "Varias veces al día","Diario","Semanal","Mensual"
])

q8 = st.radio("Última caída fuerte:", [
    "Vendí","Dudé","Esperé","Compré"
])

q9 = st.radio("Decisiones basadas en:", [
    "Emoción","Redes","Análisis","Estrategia"
])

q10 = st.radio("Noticias influyen:", [
    "Mucho","Algo","Poco","Nada"
])

# -----------------------
# CONOCIMIENTO
# -----------------------
st.header("🟦 Conocimiento")

q11 = st.multiselect("Instrumentos conocidos:", [
    "Bonos","Acciones","CEDEARs","ETF","Crypto"
])

q12 = st.multiselect("Instrumentos operados:", [
    "Bonos","Acciones","CEDEARs","ETF","Crypto"
])

q13 = st.radio("Una ON es:", [
    "Acción","Deuda empresa","Estado","No sé"
])

q14 = st.radio("CEDEAR cae por:", [
    "Empresa","Dólar","Ambos","No baja"
])

q15 = st.radio("Confianza en respuestas:", [
    "Baja","Media","Alta","Muy alta"
])

# -----------------------
# EXPERIENCIA
# -----------------------
st.header("🟧 Experiencia")

q16 = st.radio("Años invirtiendo:", [
    "<1","1-2","2-5","5+"
])

q17 = st.radio("Sobre pérdidas:", [
    "Nunca","No entendí","Aprendí","Varias y aprendí"
])

q18 = st.radio("Estrategia sostenida:", [
    "Nunca","A veces","Casi siempre","Siempre"
])

# -----------------------
# OBJETIVO
# -----------------------
st.header("🟩 Objetivo")

q19 = st.radio("Claridad del objetivo:", [
    "Nula","Baja","Media","Alta"
])

q20 = st.selectbox("Destino del dinero:", [
    "Emergencia","Ahorro","Objetivo","Inversión"
])

# -----------------------
# EXTRA (mejoran diagnóstico)
# -----------------------
st.header("🧠 Comportamiento")

q21 = st.radio("¿Qué te pesa más?", [
    "Perder dinero","Perder oportunidad"
])

q22 = st.radio("¿Cómo te definís?", [
    "Conservador","Moderado","Agresivo"
])

q23 = st.radio("Cuando te equivocás:", [
    "Evito","Culpo afuera","Analizo","Ajusto estrategia"
])

# -----------------------
# CALCULO
# -----------------------
if st.button("Generar Informe Completo"):

    R = np.mean([
        scale(idx(q1,["Vendo todo","Vendo parte","Mantengo","Compro más"])),
        scale(idx(q2,["Segura","Moderada","Volátil","Alto riesgo"])),
        scale(idx(q3,["0%","10%","25%","+25%"])),
        scale(idx(q4,["Vendo","Parcial","Mantengo","Compro más"]))
    ])

    H = np.mean([
        scale(idx(q5,["<6 meses","6m-2 años","2-5 años","+5 años"])),
        scale(idx(q6,["Sí","Tal vez","Poco probable","No"]))
    ])

    D = np.mean([
        scale(idx(q7,["Varias veces al día","Diario","Semanal","Mensual"])),
        scale(idx(q8,["Vendí","Dudé","Esperé","Compré"])),
        scale(idx(q9,["Emoción","Redes","Análisis","Estrategia"])),
        scale(idx(q10,["Mucho","Algo","Poco","Nada"]))
    ])

    K = min(((len(q11)+len(q12)+(3 if q13=="Deuda empresa" else 0)+(3 if q14=="Ambos" else 0))/15)*10,10)

    E = np.mean([
        scale(idx(q16,["<1","1-2","2-5","5+"])),
        scale(idx(q17,["Nunca","No entendí","Aprendí","Varias y aprendí"])),
        scale(idx(q18,["Nunca","A veces","Casi siempre","Siempre"]))
    ])

    # CONSISTENCIA
    if R > 7 and q8 == "Vendí":
        CONS = "Baja"
    elif D > 6:
        CONS = "Alta"
    else:
        CONS = "Media"

    # SESGOS
    sesgos = []
    if q8 == "Vendí":
        sesgos.append("Aversión a la pérdida")
    if q9 == "Redes":
        sesgos.append("Efecto manada")
    if K < 4 and q15 == "Muy alta":
        sesgos.append("Sobreconfianza")
    if q21 == "Perder oportunidad":
        sesgos.append("FOMO")

    # ARQUETIPO
    if R <= 3 and q20 == "Emergencia":
        arche = "Guardián"
    elif R >= 7 and D <= 4:
        arche = "Especulador impulsivo"
    elif K >= 7 and D <= 4:
        arche = "Ansioso informado"
    elif D >= 7 and CONS == "Alta":
        arche = "Estratega"
    elif R >= 7 and K <= 4:
        arche = "Confiado sin mapa"
    else:
        arche = "Perfil mixto"

    desc = {
        "Guardián":"Priorizás la seguridad sobre el crecimiento.",
        "Especulador impulsivo":"Buscás rendimiento alto pero reaccionás emocionalmente.",
        "Ansioso informado":"Sabés, pero no siempre ejecutás bien.",
        "Estratega":"Combinás disciplina, conocimiento y consistencia.",
        "Confiado sin mapa":"Tomás riesgos sin base sólida.",
        "Perfil mixto":"Comportamiento variable según contexto."
    }

    # INSIGHT PRINCIPAL
    if CONS == "Baja":
        insight = "Tu principal debilidad es la inconsistencia entre lo que pensás y hacés."
    elif D < 5:
        insight = "Tu mayor riesgo es emocional, no de mercado."
    elif K < 5:
        insight = "Estás tomando decisiones con conocimiento insuficiente."
    elif R > 7 and D > 7:
        insight = "Tenés potencial alto si mantenés disciplina."
    else:
        insight = "Tu perfil es equilibrado pero mejorable con estrategia."

    # -----------------------
    # OUTPUT
    # -----------------------

    st.header("📋 Informe del Inversor")

    st.subheader("🧬 Arquetipo")
    st.write(f"**{arche}**")
    st.write(desc[arche])

    st.subheader("💡 Insight principal")
    st.success(insight)

    st.subheader("📊 Métricas")
    st.write(f"Riesgo: {round(R,1)}")
    st.write(f"Horizonte: {round(H,1)}")
    st.write(f"Disciplina: {round(D,1)}")
    st.write(f"Conocimiento: {round(K,1)}")
    st.write(f"Experiencia: {round(E,1)}")
    st.write(f"Consistencia: {CONS}")

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
