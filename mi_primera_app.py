import streamlit as st

# Título de la app
st.title('Mi primera app')

# Autor
st.markdown('Esta app fue elaborada por Sebastián Soto Arcila.')

# Solicitar el nombre del usuario
nombre_usuario = st.text_input('¿Cuál es tu nombre?')

# Mostrar mensaje de bienvenida cuando el usuario ingresa su nombre
if nombre_usuario:
    st.write(f'{nombre_usuario}, te doy la bienvenida a mi primera app.')
