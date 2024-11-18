import streamlit as st
import numpy as np
import pandas as pd
import random

# Configuración inicial
st.title("Juego: Busca Minas")

# Autor
st.markdown('Esta app fue elaborada por Sebastián Soto Arcila.')

# Descripción
st.write("Encuentra las casillas sin minas. ¡Cuidado con las minas!")

# Configuración del tablero
filas = st.sidebar.slider("Número de filas:", min_value=5, max_value=10, value=8)
columnas = st.sidebar.slider("Número de columnas:", min_value=5, max_value=10, value=8)
minas = st.sidebar.slider("Número de minas:", min_value=5, max_value=(filas * columnas - 1), value=10)

# Inicialización del tablero y estado del juego
if "tablero" not in st.session_state:
    # Generar tablero con minas
    tablero = np.zeros((filas, columnas), dtype=int)
    minas_pos = random.sample(range(filas * columnas), minas)
    for pos in minas_pos:
        tablero[pos // columnas][pos % columnas] = -1

    # Agregar números (cantidad de minas alrededor)
    for i in range(filas):
        for j in range(columnas):
            if tablero[i][j] == -1:
                continue
            tablero[i][j] = sum(
                tablero[max(0, i + di)][max(0, j + dj)] == -1
                for di in [-1, 0, 1]
                for dj in [-1, 0, 1]
                if 0 <= i + di < filas and 0 <= j + dj < columnas
            )

    # Estado inicial del juego
    st.session_state["tablero"] = tablero
    st.session_state["visible"] = np.full((filas, columnas), False)
    st.session_state["game_over"] = False

# Función para revelar una celda
def revelar_celda(fila, columna):
    if st.session_state["visible"][fila][columna]:
        return

    st.session_state["visible"][fila][columna] = True

    # Si la celda es una mina, el juego termina
    if st.session_state["tablero"][fila][columna] == -1:
        st.session_state["game_over"] = True
        return

    # Si la celda es un 0, revelar las celdas vecinas
    if st.session_state["tablero"][fila][columna] == 0:
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                ni, nj = fila + di, columna + dj
                if 0 <= ni < filas and 0 <= nj < columnas:
                    revelar_celda(ni, nj)

# Mostrar el tablero en la interfaz
st.subheader("Tablero")
for i in range(filas):
    cols = st.columns(columnas)
    for j in range(columnas):
        if st.session_state["visible"][i][j]:
            if st.session_state["tablero"][i][j] == -1:
                cols[j].button("💣", disabled=True, key=f"{i}-{j}")
            else:
                cols[j].button(
                    str(st.session_state["tablero"][i][j]) if st.session_state["tablero"][i][j] > 0 else "",
                    disabled=True,
                    key=f"{i}-{j}"
                )
        else:
            if cols[j].button(" ", key=f"{i}-{j}"):
                revelar_celda(i, j)

# Estado del juego
if st.session_state["game_over"]:
    st.error("💥 ¡Has perdido! Encontraste una mina.")
    if st.button("Reiniciar juego"):
        st.session_state.clear()
        st.experimental_rerun()
else:
    # Verificar si el jugador ha ganado
    celdas_restantes = np.sum(~st.session_state["visible"])
    if celdas_restantes == minas:
        st.success("🎉 ¡Felicidades! Has ganado el juego.")
        if st.button("Reiniciar juego"):
            st.session_state.clear()
            st.experimental_rerun()
