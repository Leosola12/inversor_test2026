import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Perfil Inversor", layout="wide")

st.title("📊 Diagnóstico de Perfil Inversor")
st.markdown("Respondé con sinceridad. Este test evalúa **cómo realmente invertís**, no solo lo que creés de vos.")

# -----------------------
# HELPERS
# -----------------------
def score_map(choice, mapping):
    return mapping.get(choice, 0)

def scale(v):
    return (v-1)/3*10

# -----------------------
# RIESGO
# -----------------------
st.header("🟥 Riesgo")

q1 = st.radio("Tu cartera cae un 25% en un mes. ¿Qué hacés?", [
    "Vendo todo",
    "Vendo una parte",
    "Mantengo",
    "Compro más"
])

q2 = st.radio("Tenés que elegir una inversión:", [
    "Prefiero ganar poco pero seguro",
    "Acepto algo de riesgo",
    "Busco crecimiento con volatilidad",
    "Busco alto rendimiento aunque sea muy volátil"
])

q3 = st.radio("¿Qué pérdida permanente tolerarías?", [
    "Ninguna",
    "Hasta 10%",
    "Hasta 25%",
    "Más de 25%"
])

q4 = st.radio("Un activo sube 40% en poco tiempo:", [
    "Vendo todo",
    "Tomo ganancias parciales",
    "Mantengo",
    "Compro más"
])

risk_map = {
    "Vendo todo":1,"Prefiero ganar poco pero seguro":1,"Ninguna":1,
    "Vendo una parte":2,"Acepto algo de riesgo":2,"Hasta 10%":2,
    "Mantengo":3,"Busco crecimiento con volatilidad":3,"Hasta 25%":3,
    "Compro más":4,"Busco alto rendimiento aunque sea muy volátil":4,"Más de 25%":4,
    "Tomo ganancias parciales":2
}

# -----------------------
# HORIZONTE
# -----------------------
st.header("🟨 Horizonte y liquidez")

q5 = st.radio("¿Cuándo podrías necesitar este dinero en el peor caso?", [
    "En menos de 6 meses",
    "Entre 6 meses y 2 años",
    "Entre 2 y 5 años",
    "Más de 5 años"
])

q6 = st.radio("¿Este dinero podría ser usado en una emergencia?", [
    "Sí seguro",
    "Tal vez",
    "Poco probable",
    "No"
])

h_map = {
    "En menos de 6 meses":1,"Sí seguro":1,
    "Entre 6 meses y 2 años":2,"Tal vez":2,
    "Entre 2 y 5 años":3,"Poco probable":3,
    "Más de 5 años":4,"No":4
}

# -----------------------
# DISCIPLINA
# -----------------------
st.header("🟪 Disciplina emocional")

q7 = st.radio("¿Cada cuánto revisás tus inversiones?", [
    "Varias veces al día",
    "Todos los días",
    "Algunas veces por semana",
    "Rara vez (mensual o menos)"
])

q8 = st.radio("En una caída fuerte reciente:", [
    "Vendí",
    "Dudé mucho",
    "Esperé",
    "Aproveché para comprar"
])

q9 = st.radio("Tus decisiones se basan principalmente en:", [
    "Emoción o intuición",
    "Opiniones de otros / redes",
    "Análisis propio",
    "Estrategia definida"
])

q10 = st.radio("¿Alguna vez cambiaste decisiones por noticias recientes?", [
    "Frecuentemente",
    "A veces",
    "Rara vez",
    "Nunca"
])

d_map = {
    "Varias veces al día":1,"Vendí":1,"Emoción o intuición":1,"Frecuentemente":1,
    "Todos los días":2,"Dudé mucho":2,"Opiniones de otros / redes":1,"A veces":2,
    "Algunas veces por semana":3,"Esperé":3,"Análisis propio":3,"Rara vez":3,
    "Rara vez (mensual o menos)":4,"Aproveché para comprar":4,"Estrategia definida":4,"Nunca":4
}

# -----------------------
# CONOCIMIENTO
# -----------------------
st.header("🟦 Conocimiento")

q11 = st.multiselect("¿Qué instrumentos conocés?", [
    "Plazo fijo","Bonos","Acciones","CEDEARs","ETF","Criptomonedas"
])

q12 = st.multiselect("¿En cuáles invertiste alguna vez?", [
    "Plazo fijo","Bonos","Acciones","CEDEARs","ETF","Criptomonedas"
])

q13 = st.radio("Una Obligación Negociable (ON) es:", [
    "Una acción",
    "Una deuda de una empresa",
    "Un instrumento garantizado por el Estado",
    "No estoy seguro"
])

q14 = st.radio("¿Por qué puede bajar un CEDEAR?", [
    "Por la empresa",
    "Por el dólar",
    "Por ambos factores",
    "No puede bajar"
])

q15 = st.radio("¿Qué tan seguro estás de tus respuestas?", [
    "Nada seguro",
    "Poco seguro",
    "Bastante seguro",
    "Muy seguro"
])

k_score = (
    len(q11) + 
    len(q12) +
    (3 if q13=="Una deuda de una empresa" else 0) +
    (3 if q14=="Por ambos factores" else 0)
)

k_conf = scale(["Nada seguro","Poco seguro","Bastante seguro","Muy seguro"].index(q15)+1)

# -----------------------
# EXPERIENCIA
# -----------------------
st.header("🟧 Experiencia")

q16 = st.radio("¿Hace cuánto invertís?", [
    "Menos de 6 meses",
    "Entre 6 meses y 2 años",
    "Entre 2 y 5 años",
    "Más de 5 años"
])

q17 = st.radio("Sobre pérdidas:", [
    "Nunca tuve",
    "Perdí pero no entendí por qué",
    "Perdí y aprendí",
    "Tuve varias y aprendí de ellas"
])

q18 = st.radio("¿Seguís una estrategia a largo plazo?", [
    "Nunca",
    "A veces",
    "Casi siempre",
    "Siempre"
])

e_map = {
    "Menos de 6 meses":1,"Nunca tuve":1,"Nunca":1,
    "Entre 6 meses y 2 años":2,"Perdí pero no entendí por qué":2,"A veces":2,
    "Entre 2 y 5 años":3,"Perdí y aprendí":3,"Casi siempre":3,
    "Más de 5 años":4,"Tuve varias y aprendí de ellas":4,"Siempre":4
}

# -----------------------
# OBJETIVO
# -----------------------
st.header("🟩 Objetivo")

q19 = st.radio("¿Qué tan claro tenés tu objetivo?", [
    "No lo tengo claro",
    "Tengo una idea general",
    "Lo tengo bastante definido",
    "Está totalmente definido"
])

q20 = st.selectbox("Este dinero es principalmente para:", [
    "Fondo de emergencia",
    "Ahorro",
    "Un objetivo específico",
    "Inversión para crecimiento"
])

# -----------------------
# CALCULO
# -----------------------
if st.button("Calcular diagnóstico"):

    R = np.mean([scale(score_map(q1,risk_map)),
                 scale(score_map(q2,risk_map)),
                 scale(score_map(q3,risk_map)),
                 scale(score_map(q4,risk_map))])

    H = np.mean([scale(score_map(q5,h_map)), scale(score_map(q6,h_map))])

    D = np.mean([scale(score_map(q7,d_map)),
                 scale(score_map(q8,d_map)),
                 scale(score_map(q9,d_map)),
                 scale(score_map(q10,d_map))])

    K = min((k_score/15)*10,10)

    E = np.mean([scale(score_map(q16,e_map)),
                 scale(score_map(q17,e_map)),
                 scale(score_map(q18,e_map))])

    # -----------------------
    # CONSISTENCIA
    # -----------------------
    if R > 7 and q8 == "Vendí":
        CONS = "Baja"
    elif D > 6:
        CONS = "Alta"
    else:
        CONS = "Media"

    # -----------------------
    # SESGOS
    # -----------------------
    sesgos = []

    if q8 == "Vendí":
        sesgos.append("Aversión a la pérdida")

    if K < 4 and q15 == "Muy seguro":
        sesgos.append("Sobreconfianza")

    if q9 == "Opiniones de otros / redes":
        sesgos.append("Efecto manada")

    # -----------------------
    # INSIGHTS
    # -----------------------
    st.subheader("🧠 Diagnóstico")

    st.write(f"Riesgo: {round(R,1)}")
    st.write(f"Horizonte: {round(H,1)}")
    st.write(f"Disciplina: {round(D,1)}")
    st.write(f"Conocimiento: {round(K,1)}")
    st.write(f"Experiencia: {round(E,1)}")
    st.write(f"Consistencia: {CONS}")

    if sesgos:
        st.warning("Sesgos detectados: " + ", ".join(sesgos))

    st.subheader("💡 Insight clave")

    if D < 5:
        st.info("Tenés baja disciplina emocional. Podrías reaccionar impulsivamente ante el mercado.")

    if K < 5:
        st.info("Tu conocimiento es limitado. Es recomendable evitar decisiones complejas.")

    if CONS == "Baja":
        st.error("Hay inconsistencias entre lo que decís y cómo actuás. Esto suele generar malos resultados.")

    if R > 7 and D > 7:
        st.success("Tenés un perfil agresivo pero disciplinado. Bien ejecutado, puede generar buenos resultados.")

    # -----------------------
    # RADAR
    # -----------------------
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
