import streamlit as st
import pandas as pd
import numpy as np

st.title('City Bike Tripdata')
st.write("A00828146 - Christian Eduardo Terron Garcia")

DATE_COLUMN = 'started_at'
DATA_URL = ('citibike-tripdata.csv')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    data.rename({'start_lat': 'lat', 'start_lng': 'lon'}, axis=1, inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Cargando informacion...')
data = load_data(1000)
data_load_state.text("Listo")



if st.sidebar.checkbox('Recorridos por hora'):
    st.subheader('Numero de recorridos por hora')

    hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
    st.bar_chart(hist_values)

if st.sidebar.checkbox('Mostrar toda la informacion'):
    st.subheader('Informacion')
    st.write(data)

hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Mapa a la hora %s:00' % hour_to_filter)
st.map(filtered_data)