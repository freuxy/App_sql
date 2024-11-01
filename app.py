from warnings import catch_warnings

import streamlit as st
import pandas as pd
import duckdb
import io



csv = '''
beverage,price
orange juice,2.5
Expresso,2
Tea,3
'''

beverages = pd.read_csv(io.StringIO(csv))

csv2 = '''
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
'''

food_items = pd.read_csv(io.StringIO(csv2))

answer_df= """
SELECT *
FROM beverages
CROSS JOIN food_items

"""
solution_df=duckdb.sql(answer_df).df()
st.write("SQL coach vous accompagne dans la révision de vos requêtes")


query=st.text_area(label="Veuillez saisir votre requête", key="user_input")

if query:
  res = duckdb.sql(query).df()
  st.dataframe(res)

  try:
    res=res[solution_df.columns]
    st.dataframe(res.compare(solution_df))
  except KeyError:
    st.write("Les colonnes ne sont pas dans le bon ordre")


  if len(res.columns) != len(solution_df.columns):
    st.write("Votre resultat n'a pas le même nombre de colonnes que la solution souhaitée")
  if res.shape[0]!= solution_df.shape[0]:
    dif=res.shape[0] - solution_df.shape[0]
    st.write(f"Votre resultat n'a pas le même nombre de ligne que la solution souhaitée. Il vous manque {dif} lignes ")






with st.sidebar:
  option = st.selectbox(
    "Quelle notion voulez-vous apprendre?",
    ("Groupy", "CTE", "Windows functions"),
  )
  st.write("Vous avez choisi:", option)

tab2, tab3 = st.tabs(["Tables", "solution_dfs"])

with tab2:
  st.write("Table beverages")
  st.write(beverages)
  st.write("Table food_items")
  st.write(food_items)
  st.write("Expected")
  st.write(duckdb.sql(answer_df).df())

with tab3:
  st.write(answer_df)