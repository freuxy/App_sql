from warnings import catch_warnings

import streamlit as st
import pandas as pd
import duckdb


st.write("SQL coach vous accompagne dans la révision de vos requêtes")

try:
  user_input=st.text_area(label="Veuillez saisir votre requête")
  df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
  })

  res = duckdb.sql(user_input).df()
  st.write(res)
except Exception as e:
  st.write("Exception:", e)
