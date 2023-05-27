from dotenv import load_dotenv
from typing import Callable, List, Tuple, Dict
import re
import os

from langchain.vectorstores import Chroma
from langchain.text_splitter import MarkdownTextSplitter, RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.document_loaders import ReadTheDocsLoader
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

load_dotenv()


def generate_metadata(doc_content) -> str:
    """Generate metadata based off of document text."""

    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.6,
        )

    template = "You are a helpful assistant that will generate five highly accurate keywords based on the text you are given. Respond with the keywords, separated by commas. Respond only with the keywords, not with any other text."
    system_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{doc}"
    human_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_prompt, human_prompt])
    chain = LLMChain(llm=llm, prompt=chat_prompt)

    return chain.run(doc=doc_content)

def ingest_docs(subdir):
    """Parse and store given documentation in vector db."""
    path = os.path.join("docs", subdir)
    loader = ReadTheDocsLoader(path=path, encoding="utf-8")
    raw_docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
    )
    documents = text_splitter.split_documents(raw_docs)

    for document in documents:
        document.metadata['keywords'] = generate_metadata(document.page_content)

    embeddings = OpenAIEmbeddings()

    chromapath = os.path.join(path, "chroma")

    vector_store = Chroma.from_documents(
        documents,
        embeddings,
        collection_name="docs",
        persist_directory=chromapath,
    )
    try:
        vector_store.persist()
    except Exception as e:
        print(f"Error while persisting vector store: {e}")


def get_directories():
    """Get all directories in docs."""
    subdirectories = next(os.walk("docs"))[1]
    output = []

    for subdir in subdirectories:
        subdir_path = os.path.join("docs", subdir)
        has_chroma = "chroma" in next(os.walk(subdir_path))[1]

        output.append((subdir, has_chroma))

    return output

