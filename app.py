from warnings import catch_warnings

import streamlit as st
import pandas as pd
import duckdb


st.write("SQL coach vous accompagne dans la révision de vos requêtes")



option = st.selectbox(
  "Quelle notion voulez-vous apprendre?",
  ("Groupy", "CTE", "Windows functions"),
)
st.write("You selected:", option)

user_input=st.text_area(label="Veuillez saisir votre requête")
df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

try:
  res = duckdb.sql(user_input).df()
  st.write(res)
except Exception as e:
  st.write("Exception:", e)
