import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Perfil Inversor", layout="wide")

st.title("📊 Test de Perfil Inversor Multidimensional")
st.markdown("Completá el cuestionario para obtener un diagnóstico completo de tu perfil.")

# ------------------------
# FUNCIONES
# ------------------------

def scale(val):
    return (val - 1) / 3 * 10

# ------------------------
# PREGUNTAS
# ------------------------

st.header("1. Aversión al Riesgo")
q1 = st.radio("Tu cartera cae 25% en un mes. ¿Qué hacés?", ["Vendo todo","Vendo parte","Mantengo","Compro más"])
q2 = st.radio("Elegí un escenario", ["Ganancia segura baja","Probabilidad media","Alta volatilidad","Alto riesgo"])
q3 = st.radio("¿Cuánto estás dispuesto a perder?", ["Nada","10%","25%","Más de 25%"])
q4 = st.radio("Sube 40%. ¿Qué hacés?", ["Vendo","Vendo parcial","Mantengo","Compro más"])

map4 = {"Vendo todo":1,"Vendo parte":2,"Mantengo":3,"Compro más":4,
        "Ganancia segura baja":1,"Probabilidad media":2,"Alta volatilidad":3,"Alto riesgo":4,
        "Nada":1,"10%":2,"25%":3,"Más de 25%":4,
        "Vendo":1,"Vendo parcial":2}

st.header("2. Horizonte y Liquidez")
q5 = st.radio("¿Cuándo podrías necesitar este dinero?", ["<6 meses","6m-2 años","2-5 años",">5 años"])
q6 = st.radio("¿Podrías necesitarlo en una emergencia?", ["Sí","Tal vez","Poco probable","No"])

map_h = {"<6 meses":1,"6m-2 años":2,"2-5 años":3,">5 años":4,
         "Sí":1,"Tal vez":2,"Poco probable":3,"No":4}

st.header("3. Disciplina")
q7 = st.radio("¿Cada cuánto revisás tus inversiones?", ["Varias veces al día","Diario","Semanal","Mensual"])
q8 = st.radio("Última caída fuerte", ["Vendí","Dudé","Esperé","Compré"])
q9 = st.radio("Cómo decidís", ["Emoción","Redes","Análisis","Estrategia"])

map_d = {"Varias veces al día":1,"Diario":2,"Semanal":3,"Mensual":4,
         "Vendí":1,"Dudé":2,"Esperé":3,"Compré":4,
         "Emoción":1,"Redes":1,"Análisis":3,"Estrategia":4}

st.header("4. Conocimiento")
q10 = st.radio("Una ON es...", ["Renta variable","Deuda empresa","Garantía estatal","Ganancia neta"])
q11 = st.radio("Un CEDEAR cae porque...", ["Noticias","Tipo cambio","Ambas","No puede caer"])

map_k = {"Deuda empresa":10,"Ambas":10,"Noticias":6,"Tipo cambio":6}

st.header("5. Experiencia")
q12 = st.radio("Años invirtiendo", ["<6 meses","6m-2","2-5",">5"])
q13 = st.radio("Pérdidas", ["Nunca","Externa","Aprendí","Varias"])

map_e = {"<6 meses":1,"6m-2":2,"2-5":3,">5":4,
         "Nunca":1,"Externa":2,"Aprendí":3,"Varias":4}

st.header("6. Objetivo")
q14 = st.selectbox("Objetivo del dinero", ["Emergencia","Ahorro","Objetivo concreto","Inversión"])

# ------------------------
# CALCULO
# ------------------------

if st.button("Calcular perfil"):

    R = np.mean([scale(map4[q1]), scale(map4[q2]), scale(map4[q3]), scale(map4[q4])])
    H = np.mean([scale(map_h[q5]), scale(map_h[q6])])
    D = np.mean([scale(map_d[q7]), scale(map_d[q8]), scale(map_d[q9])])
    K = np.mean([map_k.get(q10,0), map_k.get(q11,0)])
    E = np.mean([scale(map_e[q12]), scale(map_e[q13])])

    # Consistencia
    if R > 7 and map_d[q8] == 1:
        CONS = "Baja"
    elif D > 6:
        CONS = "Alta"
    else:
        CONS = "Media"

    # Arquetipos
    if R <= 3 and q14 == "Emergencia":
        archetype = "Guardián"
    elif K >= 7 and D <= 4:
        archetype = "Ansioso Informado"
    elif R >= 8 and H <= 4:
        archetype = "Especulador Puro"
    elif D >= 7 and K >= 6:
        archetype = "Estratega"
    else:
        archetype = "Perfil Mixto"

    # Radar
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

    st.subheader("Resultado")
    st.write(f"Riesgo: {round(R,1)}")
    st.write(f"Horizonte: {round(H,1)}")
    st.write(f"Disciplina: {round(D,1)}")
    st.write(f"Conocimiento: {round(K,1)}")
    st.write(f"Experiencia: {round(E,1)}")
    st.write(f"Consistencia: {CONS}")
    st.write(f"Arquetipo: {archetype}")

    # Insight automático
    if D < 5:
        st.warning("Tenés baja disciplina emocional. Podrías tomar decisiones impulsivas.")
    if K < 5:
        st.warning("Tu conocimiento es limitado. Cuidado con sobreestimar decisiones.")
    if CONS == "Baja":
        st.warning("Tu comportamiento muestra inconsistencias entre lo que decís y hacés.")
