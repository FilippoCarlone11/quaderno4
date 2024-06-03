import streamlit as st
import numpy as np
import pandas as pd
from utils.utils import *

st.set_page_config(
    page_title="La mia App",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://dbdmg.polito.it/',
        'Report a bug': "https://dbdmg.polito.it/",
        'About': "# Corso di *Basi di Dati*"
    }
)

col1, col2 = st.columns([3,2])
with col1:
    col1.title(":red[#4 Quaderno]")
    col1.markdown("# Laboratorio di :blue[Streamlit]")
    col1.markdown("## *L'obiettivo é quello di creare un’applicazione multi-pagina per visualizzare le principali informazioni contenute nel database e permettere all’utente di aggiungerne di nuove*")
    col1.markdown("### :blue[Filippo Carlone] s311016")


with col2:
    st.image("images/polito_white.png")


def createHome():
    # creo il barChart, mi servono i giorni della settimana ed i count raggruppati per giorno.
    countSettimana = execute_query(st.session_state["connection"], "SELECT Giorno As 'Giorno', COUNT(*) AS 'Conteggio' FROM Programma GROUP BY Giorno;")
    count_dict = [dict(zip(countSettimana.keys(), result)) for result in countSettimana]

    giorni = []
    conteggi = []

    for giorno in count_dict:
        giorni.append(giorno['Giorno'])
        conteggi.append(giorno['Conteggio'])

    chart_data = pd.DataFrame(conteggi, giorni)
    area_data = pd.DataFrame(conteggi, giorni)

    col1, col2 = st.columns(2)
    col1.markdown("### Bar Chart")
    col1.bar_chart(chart_data)
    col2.markdown("### Area chart")
    col1.area_chart(area_data)


if "connection" not in st.session_state.keys():
    st.session_state["connection"] = False

#check_connection()

if check_connection():
    createHome()