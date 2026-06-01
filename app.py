import streamlit as st
import sqlite3
import pandas as pd

st.title("Inventario de Supermercado")

conexion = sqlite3.connect("inventario.db")

consulta = "SELECT * FROM productos"
df = pd.read_sql_query(consulta, conexion)

st.subheader("Lista de productos")
st.dataframe(df)

conexion.close()