# pylint: disable=missing-module-docstring
# from warnings import catch_warnings

import ast
import logging
import os
import subprocess

import duckdb
import streamlit as st
import datetime as date
import time

from narwhals import Boolean

from init_db import init_db


if "data" not in os.listdir():
    logging.error(os.listdir())
    logging.error("creating data repository")
    os.mkdir("data")


if "exo_sql.duckdb" not in os.listdir("data"):
    init_db()
    # exec(open("init_db.py").read())
    # logging.info("Initializing the database")
    # subprocess.run(["python", "init_db.py"])

con = duckdb.connect(database="data/exo_sql.duckdb", read_only=False)


def user_answer_checking(user_query: str) -> Boolean:
    """
    Fonction pour vérifier la réponse de l'utilisateur
    1) Vérifier la taille des lignes et des colonnes
    2) Comparer le contenu de la dataframe resultat et celle issue de la requête de l'utilisateur
    :param user_query: un string contenant la requête de l'utilisateur
    :return: Boolean
    """
    res = con.execute(user_query).df()
    ans = False
    try:
        st.dataframe(res)
    except duckdb.CatalogException:
        st.write("Erreur : La table spécifiée n'existe pas.")
    except Exception as e:
        st.write(f"Erreur de syntaxe SQL : {e}")
    try:
        res = res[solution_df.columns]
        check = res.compare(solution_df)
        if check.empty:
            ans = True
            st.balloons()
            st.dataframe(check)
            st.write("Challenge réussi")
        else:
            st.write(check)
    except (KeyError, NameError, ValueError):
        st.write("Les colonnes ne sont pas dans le bon ordre")
    if len(res.columns) != len(solution_df.columns):
        st.write(
            "Votre resultat n'a pas le même nombre de colonnes que la solution souhaitée"
        )
    if res.shape[0] != solution_df.shape[0]:
        dif = solution_df.shape[0] - res.shape[0]
        st.write(
            f"Votre resultat n'a pas le même nombre de ligne "
            f"que la solution souhaitée. Il vous manque {dif} lignes "
        )
    return ans


def update_time(user_theme: str, user_exo: str) -> None:
    """
    Fonction pour mettre à jour la date de dernière pratique de l'exercice
    :param user_theme: String
    :param user_exo: String
    :return: None
    """
    if user_answer_checking(query):
        today = date.datetime.now()
        st.write(today)
        con.execute(
            f"UPDATE memory_state_df SET last_reviewed='{today}' WHERE theme='{user_theme}' and exercice_name='{user_exo}'"
        )
        time.sleep(2)
        st.rerun()


exercice = con.execute("SELECT * FROM memory_state_df").df()


st.header("SQL coach vous accompagne dans la révision de vos requêtes")


query = st.text_area(label="Veuillez saisir votre requête", key="user_input")
list_theme_query = """
SELECT DISTINCT theme
FROM memory_state_df
"""
themes = con.execute(list_theme_query).df()


with st.sidebar:
    theme = st.selectbox(
        "Quelle notion voulez-vous apprendre?",
        themes,
        index=None,
        placeholder="Select a theme",
    )
    st.write("Vous avez choisi:", theme)

    if theme:
        select_data = f"SELECT * FROM memory_state_df WHERE theme = '{theme}' "
    else:
        select_data = f"SELECT * FROM memory_state_df"
    choix = (
        con.execute(select_data)
        .df()
        .sort_values(by="last_reviewed", ascending=True)
        .reset_index(drop=True)
    )
    st.write(choix)

    # left, right = st.rows(2)

    if st.button("Réinitialiser les dates de soumission", type="secondary"):
        con.execute("UPDATE memory_state_df SET last_reviewed='1994-04-05'")
        st.rerun()


exercises_df = choix.loc[0, "exercice_name"]
with open(f"answer/{exercises_df}.sql", "r") as f:
    answer = f.read()
solution_df = con.execute(answer).df()

# left, right = st.columns(2)
if query:
    if st.button("Soumettre ma requête", type="primary"):
        update_time(theme, exercises_df)
else:
    st.markdown(
        "<span style='color: red;'>Veuillez écrire une requête et pressez CMD+ENTRER. Assurez-vous d'avoir choisi une thématique</span>",
        unsafe_allow_html=True,
    )
    time.sleep(3)
    st.rerun()


tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    try:
        exercises_df = choix.loc[0, "tables"]
        for elt in exercises_df:
            data = con.execute(f"SELECT * FROM {elt}").df()
            st.dataframe(data)
    except KeyError:
        st.header("veuillez choisir un exercice")

with tab3:
    try:
        st.write(answer)
        st.write(solution_df)
    except NameError:
        st.header("veuillez choisir un exercice")
