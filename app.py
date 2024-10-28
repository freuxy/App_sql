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

answer= """
SELECT *
FROM beverages
CROSS JOIN food_items

"""
st.write("SQL coach vous accompagne dans la révision de vos requêtes")


query=st.text_area(label="Veuillez saisir votre requête", key="user_input")


if query:
  res = duckdb.sql(query).df()
  st.dataframe(res)

with st.sidebar:
  option = st.selectbox(
    "Quelle notion voulez-vous apprendre?",
    ("Groupy", "CTE", "Windows functions"),
  )
  st.write("You selected:", option)

tab2, tab3 = st.tabs(["Tables", "Solutions"])

with tab2:
  st.write("Table beverages")
  st.write(beverages)
  st.write("Table food_items")
  st.write(food_items)
  st.write("Expected")
  st.write(duckdb.sql(answer).df())

with tab3:
  st.write(answer)

#try:
#  st.write(res)
#except Exception as e:
#  st.write("Exception:", e)