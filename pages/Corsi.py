import pandas as pd
import streamlit as st
from utils.utils import *

st.subheader("Elenco :blue[Corsi]")
col1, col2 = st.columns(2)
def dataCorsi():

    #METRICHE
    ncorsi = execute_query(st.session_state["connection"], "SELECT COUNT(*) AS 'NumeroCorsi' FROM Corsi;")
    ncorsi_dict = [dict(zip(ncorsi.keys(), result)) for result in ncorsi]

    ntipcorsi = execute_query(st.session_state["connection"], "SELECT COUNT(DISTINCT Tipo) AS 'NumeroDistinti' FROM Corsi;")
    ntipcorsi_dict = [dict(zip(ntipcorsi.keys(), result)) for result in ntipcorsi]

    col1.metric("Numero corsi", f" {ncorsi_dict[0]['NumeroCorsi']}")
    col2.metric("Tipologie corsi", f" {ntipcorsi_dict[0]['NumeroDistinti']}")

    #TABELLA
    with st.expander("Filtri", True):
        col3, col4 = st.columns(2)
        livello_corso = col4.slider("Livello difficolta", 0, 4)
        livello_query = f"Livello = '{livello_corso}'" if livello_corso != 0 else ''

        tipologia_corso = col3.radio("Tipologia corso", ["Tutte", "Spinning", "Attivitá musicale", "Yoga", "Piscina"])
        tipo_query = f"Tipo = '{tipologia_corso}'" if tipologia_corso != "Tutte" else ''

        totConditionQuery = ''
        if livello_corso == 0:
            if tipologia_corso != "Tutte":
                totConditionQuery = f"WHERE {tipo_query}"
        else:
            if tipologia_corso != "Tutte":
                totConditionQuery = f"WHERE {tipo_query} AND {livello_query}"
            else:
                totConditionQuery = f"WHERE {livello_query}"


    query = f"SELECT * FROM Corsi {totConditionQuery};"
    elencoCorsi = execute_query(st.session_state["connection"], query)
    df_corsi = pd.DataFrame(elencoCorsi)
    if df_corsi.empty:
        st.warning("Non ci sono istruttori con queste caratteristiche")
    else:
        st.dataframe(df_corsi, use_container_width=True)


    #EXPANDER
    with st.expander("Corsi", False):
        if totConditionQuery != '':
            totConditionQuery = totConditionQuery[5:]
            totConditionQuery = 'AND ' + totConditionQuery
        query = f"SELECT C.Nome AS 'NomeCorso', C.Tipo AS 'TipoCorso', I.Nome AS 'NomeIstruttore', I.Cognome AS 'CognomeIstruttore' FROM Corsi C, Istruttore I, Programma P WHERE C.CodC = P.CodC AND P.CodFisc = I.CodFisc {totConditionQuery};"
        print(query)
        elencoCorsi = execute_query(st.session_state["connection"], query)
        df_corsi = pd.DataFrame(elencoCorsi)
        if df_corsi.empty:
            st.warning("Non ci sono istruttori con queste caratteristiche")
        else:
            for index, row in df_corsi.iterrows():
                st.subheader(f":green[{row['NomeCorso']}]")
                st.text(f"Tipologia corso: {row['TipoCorso']}")
                st.text(f"Nome dell'istruttore: {row['NomeIstruttore']}")
                st.text(f"Cognome dell'istruttore: {row['CognomeIstruttore']}")


if check_connection():
    dataCorsi()
