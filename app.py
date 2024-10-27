import streamlit as st
import pandas as pd
import duckdb

user_input=st.text_area(label="Du texte")
df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

st.write(user_input)

#query="""
#SELECT *
#FROM df
#WHERE second column=20
#
#"""
res=duckdb.sql(user_input).df()
st.write(res)