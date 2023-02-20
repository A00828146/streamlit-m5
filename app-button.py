import streamlit as st

myname = st.text_input("Your name: ")
if st.button('Search'):
  st.write(f"Search name: {myname}")