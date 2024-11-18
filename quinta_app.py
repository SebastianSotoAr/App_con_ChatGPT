import streamlit as st
import time

# Título de la app
st.title("Animación con Emojis 🎉")

# Autor
st.markdown('Esta app fue elaborada por Sebastián Soto Arcila.')

# Descripción
st.write("Disfruta de esta simple animación usando emojis. ¡Relájate y diviértete!")

# Parámetros de la animación
emojis = ["😀", "😎", "🤩", "🥳", "😜", "😂", "🌟", "🔥", "🌈", "✨"]
intervalo = st.sidebar.slider("Velocidad de la animación (segundos):", min_value=0.1, max_value=1.0, value=0.3)

# Mensaje animado
st.write("### Animación:")
placeholder = st.empty()

# Botón de inicio
if st.button("Iniciar Animación"):
    for _ in range(50):  # Duración de la animación (número de ciclos)
        for emoji in emojis:
            placeholder.markdown(f"<h1 style='text-align: center;'>{emoji}</h1>", unsafe_allow_html=True)
            time.sleep(intervalo)

    st.success("¡La animación ha terminado! 🎉")
