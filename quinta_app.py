import streamlit as st
import random
import pandas as pd

# Título de la app
st.title("¡Busca Minas!")

# Descripción
st.write("Descubre las celdas sin minas. Si haces clic en una mina, pierdes. ¡Buena suerte!")

# Configuración inicial
filas = st.sidebar.slider("Número de filas:", min_value=5, max_value=15, value=8)
columnas = st.sidebar.slider("Número de columnas:", min_value=5, max_value=15, value=8)
minas = st.sidebar.slider("Número de minas:", min_value=5, max_value=filas * columnas - 1, value=10)

# Crear tablero inicial
if "tablero" not in st.session_state:
    # Generar el tablero con minas
    tablero = [[0 for _ in range(columnas)] for _ in range(filas)]
    posiciones_minas = random.sample(range(filas * columnas), minas)

    for pos in posiciones_minas:
        fila = pos // columnas
        columna = pos % columnas
        tablero[fila][columna] = -1  # -1 representa una mina

    # Calcular números en las celdas
    for fila in range(filas):
        for columna in range(columnas):
            if tablero[fila][columna] == -1:
                continue
            minas_cercanas = sum(
                tablero[fila + dx][columna + dy] == -1
                for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
                if 0 <= fila + dx < filas and 0 <= columna + dy < columnas
            )
            tablero[fila][columna] = minas_cercanas

    st.session_state.tablero = tablero
    st.session_state.revelado = [[False for _ in range(columnas)] for _ in range(filas)]
    st.session_state.juego_terminado = False

# Función para manejar clics
def revelar_celda(fila, columna):
    if st.session_state.juego_terminado or st.session_state.revelado[fila][columna]:
        return
    st.session_state.revelado[fila][columna] = True
    if st.session_state.tablero[fila][columna] == -1:
        st.session_state.juego_terminado = True
        st.error("¡Has encontrado una mina! 😢")
    elif st.session_state.tablero[fila][columna] == 0:
        # Revelar celdas adyacentes si no hay minas cercanas
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            if 0 <= fila + dx < filas and 0 <= columna + dy < columnas:
                revelar_celda(fila + dx, columna + dy)

# Mostrar el tablero
st.subheader("Tablero")
for fila in range(filas):
    cols = st.columns(columnas)
    for columna in range(columnas):
        if st.session_state.revelado[fila][columna]:
            if st.session_state.tablero[fila][columna] == -1:
                cols[columna].button("💣", disabled=True)
            else:
                cols[columna].button(
                    f"{st.session_state.tablero[fila][columna]}" if st.session_state.tablero[fila][columna] > 0 else "",
                    disabled=True
                )
        else:
            if cols[columna].button(" "):
                revelar_celda(fila, columna)

# Verificar victoria
if not st.session_state.juego_terminado:
    celdas_no_mina = filas * columnas - minas
    celdas_reveladas = sum(
        1 for fila in range(filas) for columna in range(columnas) if st.session_state.revelado[fila][columna]
    )
    if celdas_reveladas == celdas_no_mina:
        st.success("¡Felicidades! Has encontrado todas las celdas sin minas. 🎉")
        st.session_state.juego_terminado = True

# Reiniciar juego
if st.button("Reiniciar juego"):
    del st.session_state.tablero
    del st.session_state.revelado
    del st.session_state.juego_terminado
    st.experimental_rerun()
