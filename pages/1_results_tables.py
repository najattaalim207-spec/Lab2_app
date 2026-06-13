import streamlit as st
from utils import search_apps

st.title("Results Table")

query = st.text_input("Search Term", "mental health ai")

if st.button("Search"):
    with st.spinner("Recherche en cours..."):
        df = search_apps(query)
        st.session_state["apps_df"] = df

if "apps_df" in st.session_state:
    st.dataframe(st.session_state["apps_df"])
else:
    st.info("Lancez une recherche pour afficher les résultats.")
