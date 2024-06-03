import pandas as pd
import streamlit as st
from utils.utils import *
import datetime

st.subheader("Aggiungi un :blue[Istruttori]")
col1, col2 = st.columns(2)
def form():
    with st.form("Nuovo istruttore"):
        CF = st.text_input("CF", placeholder="Codice fiscale")
        Nome = st.text_input("Nome", placeholder="Nome")
        Cognome = st.text_input("Cognome", placeholder="Cognome")
        DataNascita = st.date_input("Data di nascita")
        Email = st.text_input("Email", placeholder="Email")
        Telefono = st.text_input("Telefono", placeholder="Telefono")

        insert_dict = {"codFisc" : CF, "Nome" : Nome, "Cognome": Cognome, "DataNascita" :DataNascita.isoformat(), "Email" : Email, "Telefono" : Telefono}
        submitted = st.form_submit_button("Invia", type = 'primary')

        if submitted:
            if insert(insert_dict):
                st.success("Hai inserito l'istruttore",icon='✅')
            else:
                st.error("Impossibile aggiungere il prodotto.",icon='⚠️')

def insert(insert_dict):
    if checkData(insert_dict):
        attributi = ", ".join(insert_dict.keys())
        valori = tuple(insert_dict.values())
        query = f"INSERT INTO Istruttore ({attributi}) VALUES {valori};"
        print(query)
        try:
            execute_query(st.session_state['connection'], query)
            st.session_state['connection'].commit()
            return True
        except:
            return False
def checkData(insert_dict):
    if insert_dict["Telefono"] == '':
        insert_dict.pop("Telefono")
    for value in insert_dict.values():
        if value == '':
            return False
    return True





if check_connection():
    form()
