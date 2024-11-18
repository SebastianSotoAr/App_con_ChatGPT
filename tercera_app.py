import streamlit as st
import pandas as pd
import datetime as dt

# Título de la app
st.title("Registro de Finanzas Personales")

# Autor
st.markdown('Esta app fue elaborada por Sebastián Soto Arcila.')

# Secciones principales de la app
menu = ["Presupuesto", "Ingresos", "Gastos", "Metas de Ahorro", "Reportes"]
opcion = st.sidebar.selectbox("Elige una sección:", menu)

# Diccionario para almacenar datos
if "finanzas" not in st.session_state:
    st.session_state["finanzas"] = {
        "presupuesto": [],
        "ingresos": [],
        "gastos": [],
        "metas": []
    }

# Función para calcular diferencias
def calcular_diferencias(presupuestado, real):
    return real - presupuestado

# Sección: Presupuesto
if opcion == "Presupuesto":
    st.header("Configurar Presupuesto")
    categoria = st.text_input("Categoría del presupuesto (e.g., Alimentación, Transporte):")
    monto_presupuesto = st.number_input("Monto presupuestado:", min_value=0.0, format="%.2f")

    if st.button("Guardar Presupuesto"):
        st.session_state["finanzas"]["presupuesto"].append({"categoría": categoria, "monto": monto_presupuesto})
        st.success(f"Presupuesto para {categoria} guardado con éxito.")

    if st.session_state["finanzas"]["presupuesto"]:
        st.subheader("Presupuestos Guardados")
        st.write(pd.DataFrame(st.session_state["finanzas"]["presupuesto"]))

# Sección: Ingresos
elif opcion == "Ingresos":
    st.header("Registrar Ingresos")
    fuente = st.text_input("Fuente del ingreso:")
    monto_ingreso = st.number_input("Monto del ingreso:", min_value=0.0, format="%.2f")
    fecha_ingreso = st.date_input("Fecha del ingreso:", dt.date.today())

    if st.button("Guardar Ingreso"):
        st.session_state["finanzas"]["ingresos"].append({"fuente": fuente, "monto": monto_ingreso, "fecha": fecha_ingreso})
        st.success(f"Ingreso de {monto_ingreso:.2f} guardado con éxito.")

    if st.session_state["finanzas"]["ingresos"]:
        st.subheader("Ingresos Registrados")
        st.write(pd.DataFrame(st.session_state["finanzas"]["ingresos"]))

# Sección: Gastos
elif opcion == "Gastos":
    st.header("Registrar Gastos")
    categoria_gasto = st.text_input("Categoría del gasto:")
    monto_gasto = st.number_input("Monto del gasto:", min_value=0.0, format="%.2f")
    fecha_gasto = st.date_input("Fecha del gasto:", dt.date.today())

    if st.button("Guardar Gasto"):
        st.session_state["finanzas"]["gastos"].append({"categoría": categoria_gasto, "monto": monto_gasto, "fecha": fecha_gasto})
        st.success(f"Gasto de {monto_gasto:.2f} guardado con éxito.")

    if st.session_state["finanzas"]["gastos"]:
        st.subheader("Gastos Registrados")
        st.write(pd.DataFrame(st.session_state["finanzas"]["gastos"]))

# Sección: Metas de Ahorro
elif opcion == "Metas de Ahorro":
    st.header("Configurar Metas de Ahorro")
    meta = st.text_input("Descripción de la meta:")
    monto_meta = st.number_input("Monto objetivo:", min_value=0.0, format="%.2f")
    fecha_meta = st.date_input("Fecha objetivo:", dt.date.today())

    if st.button("Guardar Meta"):
        st.session_state["finanzas"]["metas"].append({"meta": meta, "monto": monto_meta, "fecha": fecha_meta})
        st.success(f"Meta de ahorro guardada con éxito.")

    if st.session_state["finanzas"]["metas"]:
        st.subheader("Metas de Ahorro Registradas")
        st.write(pd.DataFrame(st.session_state["finanzas"]["metas"]))

# Sección: Reportes
elif opcion == "Reportes":
    st.header("Generar Reportes")

    # Crear DataFrame de presupuestos y gastos
    presupuestos = pd.DataFrame(st.session_state["finanzas"]["presupuesto"])
    gastos = pd.DataFrame(st.session_state["finanzas"]["gastos"])

    if not presupuestos.empty and not gastos.empty:
        # Agregar diferencias a los presupuestos
        gastos_por_categoria = gastos.groupby("categoría")["monto"].sum().reset_index()
        reportes = pd.merge(presupuestos, gastos_por_categoria, on="categoría", how="left").fillna(0)
        reportes["diferencia"] = reportes.apply(
            lambda x: calcular_diferencias(x["monto"], x["monto_y"]), axis=1
        )
        reportes = reportes.rename(columns={"monto": "Presupuestado", "monto_y": "Gastado"})
        st.subheader("Reporte Mensual")
        st.write(reportes)
    else:
        st.write("No hay datos suficientes para generar reportes.")
