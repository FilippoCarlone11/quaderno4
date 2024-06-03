import pandas as pd
import streamlit as st
from utils.utils import *
import datetime
from random import randint

st.subheader("Elenco :blue[Istruttori]")
col1, col2 = st.columns(2)
def dataCorsi():
    #TABELLA
    with st.expander("Filtri", False):
        col3, col4 = st.columns(2)
        start = datetime.date(1970, 12,1)
        end = datetime.date(1996, 12, 31)
        dates = col4.date_input("Date di nascita", [start, end])
        if(len(dates)>1):
            dates_query = f"DataNascita >= '{dates[0].isoformat()}' AND DataNascita <= '{dates[1].isoformat()}'" if dates != '' else ''
        else:
            dates_query = f"DataNascita >= '{dates[0].isoformat()}'" if dates != '' else ''
        cognome = col3.text_input("Nome")
        cognome_query = f"Cognome = '{cognome}'" if cognome != "" else ''

        if dates_query == '' and cognome_query != '':
            totConditionQuery = f"WHERE {cognome_query}"
        if dates_query != '' and cognome_query != '' :
            totConditionQuery = f"WHERE {cognome_query} AND {dates_query}"
        if dates_query != '' and cognome_query == '':
            totConditionQuery = f"WHERE {dates_query}"

    query = f"SELECT * FROM Istruttore {totConditionQuery};"

    with st.expander("Istruttori", True):
        elencoIstruttori = execute_query(st.session_state["connection"], query)
        df_istruttori = pd.DataFrame(elencoIstruttori)
        if df_istruttori.empty:
            st.warning("Non ci sono istruttori con queste caratteristiche")
        else:
            for index, row in df_istruttori.iterrows():
                col1, col2 = st.columns(2)
                col1.subheader(f":green[{row['Nome'] + ' '+ row['Cognome']}]")
                col1.text(f"Codice Fiscale: {row['CodFisc']}")
                col1.text(f"Data di Nascita: {row['DataNascita']}")
                col1.text(f"Email: {row['Email']}")
                col1.text(f"Telefono: {row['Telefono']}")
                x = randint(1,4)
                percorso = f"images/{x}.png"
                col2.image(percorso, width=100)




if check_connection():
    dataCorsi()
