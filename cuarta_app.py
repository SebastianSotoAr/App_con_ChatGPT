import streamlit as st
import pandas as pd

# Título de la app
st.title("Calculadora de PAPA")

# Autor
st.markdown('Esta app fue elaborada por Sebastián Soto Arcila.')

# Descripción
st.write("Esta app permite calcular el PAPA global y por tipología de asignatura. "
         "Por favor, ingresa las materias con sus respectivas calificaciones y créditos.")

# Inicializar el estado de las materias
if "materias" not in st.session_state:
    st.session_state["materias"] = []

# Función para calcular el PAPA
def calcular_papa(data):
    total_puntos = sum(row["calificación"] * row["créditos"] for row in data)
    total_créditos = sum(row["créditos"] for row in data)
    return total_puntos / total_créditos if total_créditos > 0 else 0

# Función para calcular el PAPA por tipología
def calcular_papa_por_tipologia(data):
    data_df = pd.DataFrame(data)
    papa_por_tipologia = data_df.groupby("tipología").apply(
        lambda x: sum(x["calificación"] * x["créditos"]) / sum(x["créditos"])
    )
    return papa_por_tipologia

# Formulario para agregar materias
with st.form("Agregar Materia"):
    col1, col2, col3 = st.columns(3)
    with col1:
        nombre = st.text_input("Nombre de la materia:")
    with col2:
        calificación = st.number_input("Calificación (0.0 - 5.0):", min_value=0.0, max_value=5.0, step=0.1)
    with col3:
        créditos = st.number_input("Créditos:", min_value=1, step=1)
    tipología = st.selectbox("Tipología de la asignatura:", ["Obligatoria", "Electiva", "Optativa"])
    agregar = st.form_submit_button("Agregar")

    if agregar and nombre and créditos > 0:
        st.session_state["materias"].append({
            "materia": nombre,
            "calificación": calificación,
            "créditos": créditos,
            "tipología": tipología
        })
        st.success(f"Materia '{nombre}' agregada con éxito.")

# Mostrar materias registradas
if st.session_state["materias"]:
    st.subheader("Materias Registradas")
    materias_df = pd.DataFrame(st.session_state["materias"])
    st.write(materias_df)

    # Calcular PAPA global
    papa_global = calcular_papa(st.session_state["materias"])
    st.subheader(f"PAPA Global: {papa_global:.2f}")

    # Calcular PAPA por tipología
    st.subheader("PAPA por Tipología")
    papa_por_tipologia = calcular_papa_por_tipologia(st.session_state["materias"])
    st.write(papa_por_tipologia)

    # Botón para reiniciar datos
    if st.button("Reiniciar Datos"):
        st.session_state["materias"] = []
        st.success("Datos reiniciados con éxito.")
else:
    st.info("No se han registrado materias. Agrega materias en el formulario.")
