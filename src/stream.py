import streamlit as st
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('sqlite:///../data/gold/database.db')

st.title("Análise de Vendas")

df_faturamento = pd.read_sql(
    "SELECT * FROM faturamento_diario",
    con=engine
)

st.dataframe(df_faturamento)
