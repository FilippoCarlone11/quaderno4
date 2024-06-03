import pandas as pd
import streamlit as st
from utils.utils import *

st.subheader("Elenco Agenzie")

col1,col2,col3=st.columns(3)

numberofagenzie = execute_query(st.session_state["connection"], "SELECT COUNT(*) AS 'NumeroAgenzie' FROM AGENZIA;")
numberofagenzie_dict = [dict(zip(numberofagenzie.keys(), result)) for result in numberofagenzie]

numberofcitta = execute_query(st.session_state["connection"], "SELECT COUNT( DISTINCT Citta_Indirizzo) AS 'NumeroCitta' FROM AGENZIA;")
numberofcitta_dict = [dict(zip(numberofcitta.keys(), result)) for result in numberofcitta]

query = "SELECT Citta_Indirizzo,COUNT(*) AS num FROM `AGENZIA` GROUP BY Citta_Indirizzo ORDER BY `num` DESC LIMIT 1;"
city = execute_query(st.session_state["connection"], query)

col1.metric("Numero Agenzie", f" {numberofagenzie_dict[0]['NumeroAgenzie']}")
col2.metric("Numero Citta", f" {numberofcitta_dict[0]['NumeroCitta']}")
col3.metric("Città con più agenzie",city.mappings().first()["Citta_Indirizzo"])

query="SELECT AGENZIA.Citta_Indirizzo,CITTA.Latitudine AS 'LAT', CITTA.Longitudine AS 'LON' FROM `AGENZIA`,CITTA WHERE AGENZIA.Citta_Indirizzo=CITTA.Nome;"
citygeo=execute_query(st.session_state["connection"],query)
df_map=pd.DataFrame(citygeo)
st.map(df_map)
cityName=st.text_input("Filtra per città")
if cityName=='':
    query="SELECT Citta_Indirizzo,CONCAT(Via_Indirizzo,' ',Numero_Indirizzo) AS 'Indirizzo' FROM `AGENZIA`;"
else:
    query=f"SELECT Citta_Indirizzo,CONCAT(Via_Indirizzo,' ',Numero_Indirizzo) AS 'Indirizzo' FROM `AGENZIA` WHERE Citta_Indirizzo='{cityName}'"
cityInfo=execute_query(st.session_state["connection"],query)

agenzie_info = execute_query(st.session_state["connection"], "SELECT codA AS 'Codice', SitoWeb AS 'sito', Citta_Indirizzo AS 'citta' from AGENZIA;")
agenzie_info_dict= [dict(zip(agenzie_info.keys(), result)) for result in agenzie_info]

df = pd.DataFrame(agenzie_info_dict)

st.dataframe(df,use_container_width=True)

if "connection" not in st.session_state.keys():
    st.session_state["connection"] = False

check_connection()