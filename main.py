import streamlit as st
from dl import download_docs
from db import get_directories

docspage = st.text_input('Enter the base URL of the documentation:')

if docspage:
    with st.spinner('Downloading documentation...'):
        download_docs(docspage)
        e = RuntimeError('Invalid documentation URL')
        st.exception(e)
    st.success('Documentation downloaded!')

# get all directories in docs
#dropdown of all directories, append a check emoji to the end if there is a chroma directory in that directory,

docs_choice = st.selectbox('Select a directory:', get_directories())

clicked = st.button('Ingest docs')

if clicked:
    with st.spinner('Ingesting docs...'):
        ingest_docs(docs_choice)
    st.success('Docs ingested!')

