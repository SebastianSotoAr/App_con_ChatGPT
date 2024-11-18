import streamlit as st

# Título de la app
st.title("Conversor Universal")

# Descripción
st.write("Selecciona una categoría y luego el tipo de conversión que deseas realizar.")

# Opciones de categoría
categorias = [
    "Temperatura", "Longitud", "Peso/Masa", "Volumen", "Tiempo",
    "Velocidad", "Área", "Energía", "Presión", "Tamaño de Datos"
]

# Selección de categoría
categoria = st.selectbox("Elige una categoría:", categorias)

# Funciones de conversión
def convertir_temperatura(tipo, valor):
    if tipo == "Celsius a Fahrenheit":
        return valor * 9 / 5 + 32
    elif tipo == "Fahrenheit a Celsius":
        return (valor - 32) * 5 / 9
    elif tipo == "Celsius a Kelvin":
        return valor + 273.15
    elif tipo == "Kelvin a Celsius":
        return valor - 273.15

def convertir_longitud(tipo, valor):
    if tipo == "Pies a metros":
        return valor * 0.3048
    elif tipo == "Metros a pies":
        return valor / 0.3048
    elif tipo == "Pulgadas a centímetros":
        return valor * 2.54
    elif tipo == "Centímetros a pulgadas":
        return valor / 2.54

def convertir_peso(tipo, valor):
    if tipo == "Libras a kilogramos":
        return valor * 0.453592
    elif tipo == "Kilogramos a libras":
        return valor / 0.453592
    elif tipo == "Onzas a gramos":
        return valor * 28.3495
    elif tipo == "Gramos a onzas":
        return valor / 28.3495

# (Continúa agregando funciones de conversión para las demás categorías)

# Tipos de conversiones por categoría
conversiones = {
    "Temperatura": ["Celsius a Fahrenheit", "Fahrenheit a Celsius", "Celsius a Kelvin", "Kelvin a Celsius"],
    "Longitud": ["Pies a metros", "Metros a pies", "Pulgadas a centímetros", "Centímetros a pulgadas"],
    "Peso/Masa": ["Libras a kilogramos", "Kilogramos a libras", "Onzas a gramos", "Gramos a onzas"],
    # (Agrega las conversiones restantes aquí)
}

# Selección del tipo de conversión
if categoria in conversiones:
    tipo_conversion = st.selectbox("Elige el tipo de conversión:", conversiones[categoria])
    valor = st.number_input("Introduce el valor a convertir:", format="%.2f")

    # Realizar conversión
    if st.button("Convertir"):
        if categoria == "Temperatura":
            resultado = convertir_temperatura(tipo_conversion, valor)
        elif categoria == "Longitud":
            resultado = convertir_longitud(tipo_conversion, valor)
        elif categoria == "Peso/Masa":
            resultado = convertir_peso(tipo_conversion, valor)
        # (Agrega las categorías restantes aquí)
        
        st.write(f"El resultado de la conversión es: {resultado:.2f}")
