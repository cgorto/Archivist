from dotenv import load_dotenv
from typing import Callable, List, Tuple, Dict
import re
import os

from langchain.vectorstores import Chroma
from langchain.text_splitter import MarkdownTextSplitter, RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.document_loaders import ReadTheDocsLoader

load_dotenv()

def ingest_docs(docspage):
    """Parse and store given documentation in vector db."""

    loader = ReadTheDocsLoader(docspage)
    raw_docs = loader.load_docs()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
    )

def get_directories():
    """Get all directories in docs."""
    subdirectories = next(os.walk("docs"))[1]  # get list of subdirectories
    output = []

    for subdir in subdirectories:
        subdir_path = os.path.join("docs", subdir)
        if "chroma" in next(os.walk(subdir_path))[1]:  # check if 'chroma' subdirectory exists
            subdir += ' ✔️'  # append a check emoji if 'chroma' exists

        output.append(subdir)
    
    return output