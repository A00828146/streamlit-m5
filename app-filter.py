import streamlit as st
import pandas as pd

st.title('Search by range')
DATA_URL = 'dataset.csv'

# Funcion usada para llenar la lista de generos.
@st.cache
def load_data():
  data = pd.read_csv(DATA_URL)
  return data

# Funcion para filtrar en base al genero
@st.cache
def load_data_bysex(sex):
  data = pd.read_csv(DATA_URL)
  filterBySex = data[data['sex'] == sex]
  return filterBySex


# Al inicio del programa se llama a la funcion
# para el llenado de la lista. 
data = load_data()
selected_sex = st.selectbox('Select sex', data['sex'].unique())
btnSearch = st.button("Search")


if(btnSearch):
  filteredData = load_data_bysex(selected_sex)
  count_row = filteredData.shape[0]
  st.write(f"Total items: {count_row}")
  st.dataframe(filteredData)
  