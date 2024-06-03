import pandas as pd
import streamlit as st
from utils.utils import *
import datetime

st.subheader("Aggiungi una :blue[lezione]")
col1, col2 = st.columns(2)
def form():
    with st.form("Nuova lezione"):
        #query per i selectbox
        query = "SELECT CodFisc FROM Istruttore;"
        elencoCF = execute_query(st.session_state["connection"], query)
        cfDataFrame = pd.DataFrame(elencoCF)
        query = "SELECT CodC FROM Corsi;"
        elencoCorsi = execute_query(st.session_state["connection"], query)
        corsiDataFrame = pd.DataFrame(elencoCorsi)


        CF = st.selectbox("CF", cfDataFrame)
        Giorno = st.selectbox("Giorno della lezione", ["Lunedì","Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"])
        OrarioInizio = st.time_input("OrarioInizio", datetime.time(8,00))
        Durata = st.slider("Minuti", 0, 60)
        CodC = st.selectbox("CodC", corsiDataFrame)
        Sala = st.text_input("Sala")

        insert_dict = {"CodFisc" : CF, "Giorno" : Giorno, "OraInizio": OrarioInizio.strftime('%H:%M:%S'), "Durata" :Durata, "Sala" : Sala, "CodC" : CodC}
        submitted = st.form_submit_button("Invia", type = 'primary')

        if submitted:
            insert(insert_dict)
def insert(insert_dict):
        attributi = ", ".join(insert_dict.keys())
        valori = tuple(insert_dict.values())
        testdata = checkData(insert_dict)
        if testdata is True:
            test1 = check_query(valori)
            if test1 is True:
                qr2 = insertquery(attributi, valori)
                if qr2 is True:
                    st.success("Operazione eseguita correttamente")
                else:
                    st.error(qr2)
            else:
                st.error(test1)
        else:
            st.error(testdata)

def check_query(valori):
    check_query = f"SELECT COUNT(*) AS 'Conteggio' FROM Programma WHERE Giorno = '{valori[1]}' AND CodC = '{valori[5]}';"
    try:
        checkcorsi = execute_query(st.session_state['connection'], check_query)
        checkdict = [dict(zip(checkcorsi.keys(), result)) for result in checkcorsi]
        if checkdict[0]['Conteggio'] == 0:
            return True
        else:
            return "é giá presente nel database una lezione per questo corso in quel giorno."
    except Exception as exp:
        return exp

def insertquery(attributi, valori):
    query = f"INSERT INTO Programma ({attributi}) VALUES {valori};"
    try:
        execute_query(st.session_state['connection'], query)
        st.session_state['connection'].commit()
        return True
    except Exception as exp:
        return exp

def checkData(insert_dict):
    if insert_dict.get("Durata") > 60:
        return "Durata troppo grande."
    if insert_dict.get("Giorno") == "Sabato" or insert_dict.get("Giorno") == "Domenica":
        return "Giorno non lavorativo."
    return True


if check_connection():
    form()
