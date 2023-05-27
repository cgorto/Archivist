import streamlit as st

from langchain.schema import HumanMessage, AIMessage

from dl import download_docs
from db import get_directories, ingest_docs
from arch import make_chain

directories = get_directories()
chat_history = []

st.header("Archivist")

with st.sidebar:

    docspage = st.text_input('Enter the base URL of the documentation, must include https:// :')

    if docspage:
        with st.spinner('Downloading documentation...'):
            download_docs(docspage)
            e = RuntimeError('Invalid documentation URL')
            st.exception(e)
        st.success('Documentation downloaded!')
        directories = get_directories()

    # get all directories in docs
    #dropdown of all directories, append a check emoji to the end if there is a chroma directory in that directory,


    directory_dict = {f"{name} ✔️" if has_chroma else name: name for name, has_chroma in directories}

    docs_choice = st.selectbox('Select a directory:', list(directory_dict.keys()))


    clicked = st.button('Ingest docs')

    if clicked:
        with st.spinner('Ingesting docs...'):
            original_name = directory_dict[docs_choice]
            ingest_docs(original_name)
        st.success('Docs ingested!')
        directories = get_directories()


chroma_directories = [(name, has_chroma) for name, has_chroma in directories if has_chroma]
chroma_dict = {f"{name}": name for name, has_chroma in chroma_directories}

docs_scope = st.selectbox('Choose Scope:', list(chroma_dict.keys()))

def get_text():
    """Get text from user."""

    styl = f"""
    <style>
        .stTextInput {{
        position: fixed;
        bottom: 3rem;
        }}
    </style>
    """
    st.markdown(styl, unsafe_allow_html=True)

    input_text = st.text_input("Input Message: ","", key="input")
    return input_text



user_input = get_text()

if docs_scope:
    chain = make_chain(chroma_dict[docs_scope])



if user_input:
    response = chain({"question": user_input, "chat_history": chat_history})
    answer = response["answer"]
    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=answer))

    for message in chat_history:
        if isinstance(message, HumanMessage):
            st.write(f"**You:** {message.content}")
        elif isinstance(message, AIMessage):
            st.write(f"**Archivist:** {message.content}")
        st.divider()