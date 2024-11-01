# pylint: disable=missing-module-docstring
# from warnings import catch_warnings

import io

import duckdb
import pandas as pd
import streamlit as st

from init_db import food_items

con= duckdb.connect(database="data/exo_sql.duckdb", read_only=False)

beverages = con.execute("SELECT * FROM beverages").df()
food_items = con.execute("SELECT * FROM food_items").df()

ANSWER_DF = """
SELECT *
FROM beverages
CROSS JOIN food_items

"""

solution_df = duckdb.sql(ANSWER_DF).df()
st.write("SQL coach vous accompagne dans la révision de vos requêtes")


query = st.text_area(label="Veuillez saisir votre requête", key="user_input")

with st.sidebar:
    theme = st.selectbox(
        "Quelle notion voulez-vous apprendre?",
        ("cross_join", "CTE", "Windows functions"),
    )
    st.write("Vous avez choisi:", theme)
    exercice = con.execute(f"SELECT * FROM memory_state_df WHERE theme = '{theme}' ").df()
    st.write(exercice)


if query:
    res = duckdb.sql(query).df()
    st.dataframe(res)

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




tab2, tab3 = st.tabs(["Tables", "solution_dfs"])

with tab2:
    st.write("Table beverages")
    st.write(beverages)
    st.write("Table food_items")
    st.write(food_items)
    st.write("Expected")
    st.write(duckdb.sql(ANSWER_DF).df())

with tab3:
    st.write(ANSWER_DF)


