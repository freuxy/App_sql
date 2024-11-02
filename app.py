# pylint: disable=missing-module-docstring
# from warnings import catch_warnings

import duckdb
import pandas as pd
import ast
import streamlit as st

con = duckdb.connect(database="data/exo_sql.duckdb", read_only=False)

# beverages = con.execute("SELECT * FROM beverages").df()
# food_items = con.execute("SELECT * FROM food_items").df()
exercice = con.execute("SELECT * FROM memory_state_df").df()


st.write("SQL coach vous accompagne dans la révision de vos requêtes")


query = st.text_area(label="Veuillez saisir votre requête", key="user_input")

with st.sidebar:
    theme = st.selectbox(
        "Quelle notion voulez-vous apprendre?",
        ("cross_join", "CTE", "window_functions"),
        index=None,
        placeholder="Select a theme",
    )
    st.write("Vous avez choisi:", theme)
    choix = con.execute(f"SELECT * FROM memory_state_df WHERE theme = '{theme}' ").df()
    st.write(choix)


ANSWER = """
   SELECT *
   FROM beverages
   CROSS JOIN food_items

   """
"""
   solution_df = duckdb.sql(ANSWER).df()
   st.write(solution_df)
"""

if query:
    res = con.execute(query).df()
    st.dataframe(res)
"""
    try:
        res = res[solution_df.columns]
        st.dataframe(res.compare(solution_df))
    except KeyError:
        st.write("Les colonnes ne sont pas dans le bon ordre")

    if len(res.columns) != len(solution_df.columns):
        st.write(
            "Votre resultat n'a pas le même nombre de colonnes que la solution souhaitée"
        )
    if res.shape[0] != solution_df.shape[0]:
        dif = res.shape[0] - solution_df.shape[0]
        st.write(
            f"Votre resultat n'a pas le même nombre de ligne "
            f"que la solution souhaitée. Il vous manque {dif} lignes "
        )


"""


tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    exercises_df = choix.loc[0, "tables"]
    for elt in exercises_df:
        data = con.execute(f"SELECT * FROM {elt}")
        st.dataframe(data)

with tab3:
    st.write("Test")
