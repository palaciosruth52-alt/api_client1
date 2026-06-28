import streamlit as st 
import pandas as pd 
from api_client import obtener_usuarios_api
from database import crear_tabla, guardar_usuarios, consultar_usuarios, eliminar_datos

st.set_page_config(page_title="API-SQLITE", page_icon=":guardsman:", layout="wide")

crear_tabla()

st.title("API-SQLITE-STREAMLITE")
st.write("Esta aplicación permite obtener datos de una API y almacenarlos en una base de datos SQLite, así como consultar y eliminar los datos almacenados.")

menu=st.sidebar.selectbox (
    "Selecccione una opción",
    [
        "Inicio",
        "Consumir API",
        "Ver la base de datos",
        "Buscar los usuarios",
        "Eliminar los datos"
            
    ]
       
)

if menu=="Inicio":
    st.header("Bienvenido a la aplicación API-SQLITE-STREAMLITE")

    st.write("Esta aplicación permite obtener datos de una API y almacenarlos en una base de datos SQLite, así como consultar y eliminar los datos almacenados.")

    st.info("Seleccione una opción en el menú lateral para comenzar a utilizar la aplicación.")

elif menu=="Consumir API":
    st.header ("Consumir API pública")
    st.write ("API Utilziada")
    st.code("https://jsonplaceholder.typicode.com/users")
    
    if st.button("Obtener usuarios de la API"):
        usuarios=obtener_usuarios_api()
        if usuarios:
            guardar_usuarios(usuarios)
            st.success("Usuarios obtenidos y guardados en la base de datos.")
            st.json(usuarios[0])
        else:
            st.error("No se pudieron obtener los usuarios de la API.")

elif menu == "Ver la base de datos":
    st.header("Tabla almacenada en nuestro SQLite")

    df = consultar_usuarios()

    if df.empty:
        st.warning("La base de datos está vacía. Primero consuma la API.")
    else:
        st.dataframe(df, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total usuarios", len(df))
        col2.metric("Total ciudades", df["ciudad"].nunique())
        col3.metric("Total correos", df["email"].nunique())

elif menu == "Buscar los usuarios":
    st.header("Buscar usuario en SQLite")

    df = consultar_usuarios()

    if df.empty:
        st.warning("No hay datos guardados.")
    else:
        nombre = st.text_input("Ingrese nombre o usuario a buscar")

        if nombre:
            resultado = df[
                df["nombre"].str.contains(nombre, case=False, na=False) |
                df["usuario"].str.contains(nombre, case=False, na=False)
            ]

            if resultado.empty:
                st.error("No se encontraron coincidencias.")
            else:
                st.success("Resultado encontrado.")
                st.dataframe(resultado, use_container_width=True)

elif menu == "Eliminar los datos":
    st.header("Eliminar registros de SQLite")

    st.warning("Esta acción eliminará todos los datos almacenados.")

    if st.button("Eliminar todos los datos"):
        eliminar_datos()
        st.success("Datos eliminados correctamente.")   
    
