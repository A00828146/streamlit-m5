import streamlit as st
import pandas as pd

st.title('Search by range')
DATA_URL = 'dataset.csv'

@st.cache
def load_data_byrange(startIndex, endIndex):
  data = pd.read_csv(DATA_URL)
  if(startIndex >= 0 and endIndex < data.shape[0]):
    filteredData = data[(data['index'] >= startIndex) & (data['index'] <= endIndex)]
    return filteredData
  else:
    filteredData = data[(data['index'] >= 0) & (data['index'] <= 0)]

startIndex = st.text_input('Start Index pls: ')
endIndex = st.text_input('End Index pls: ')
btnRange = st.button("Search")

if(btnRange):
  try:
    filterByRange = load_data_byrange(int(startIndex), int(endIndex))
    count_row = filterByRange.shape[0]
    st.write(f"Total items: {count_row}")
    st.dataframe(filterByRange)
  except:
    st.write("Invalid data range")
  