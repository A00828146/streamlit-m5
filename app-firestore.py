import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account
import json

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
# db = firestore.Client(credentials=creds, project="names-project-Christian")

db = firestore.Client.from_service_account_json("christianFirebase.json")
dbNames = db.collection("newNames")


#Crear registro
st.header("Nuevo registro")
index = st.text_input("Index: ")
name = st.text_input("Name: ")
sex = st.selectbox('Select sex', ('F','M','Other'))

submit = st.button("Crear nuevo registro")

if index and name and sex and submit:
    doc_ref = db.collection("newNames").document(name)
    doc_ref.set({
        "index": index,
        "name": name,
        "sex": sex
    })
    st.sidebar.write("Registro insertado correctamente")

#Obtener nombres
names_ref = list(db.collection(u'newNames').stream())
names_dict = list(map(lambda x: x.to_dict(), names_ref))
names_dataframe = pd.DataFrame(names_dict)
st.dataframe(names_dataframe)

#Buscar por nombre

def loadByName(name):
    names_ref = dbNames.where(u'name', u'==', name)
    currentName = None
    for myName in names_ref.stream():
        currentName = myName
    return currentName

st.sidebar.subheader("Buscar nombre")
nameSearch = st.sidebar.text_input("Nombre: ")
btnFiltrar = st.sidebar.button("Buscar")

if btnFiltrar:
    doc = loadByName(nameSearch)
    if doc is None:
        st.sidebar.write("Nombre no existe")
    else:
        st.sidebar.write(doc.to_dict())

st.sidebar.markdown("""---""")
btnEliminar = st.sidebar.button("Eliminar")

if(btnEliminar):
    deleteName = loadByName(nameSearch)
    if deleteName is None:
        st.sidebar.write(f"{nameSearch} no existe")
    else:
        dbNames.document(deleteName.id).delete()
        st.sidebar.write(f"{nameSearch} eliminado")

st.sidebar.markdown("""---""")
newname = st.sidebar.text_input("Actualizar nombre")
btnActualizar = st.sidebar.button("Actualizar")
if btnActualizar:
    updatename = loadByName(nameSearch)
    if updatename is None:
        st.sidebar.write(f"{nameSearch} no existe")
    else:
        myupdatename = dbNames.document(updatename.id)
        myupdatename.update({
          "name": newname
        })