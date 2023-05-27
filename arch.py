import os
from langchain.vectorstores.chroma import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.schema import HumanMessage, AIMessage

from dotenv import load_dotenv
load_dotenv()

def make_chain(scope):
    model = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature="0.7",
        # verbose=True
    )
    embedding = OpenAIEmbeddings()

    path = os.path.join("docs", scope, "chroma")

    vector_store = Chroma(
        collection_name="docs",
        embedding_function=embedding,
        persist_directory=path,
    )

    return ConversationalRetrievalChain.from_llm(
        model,
        retriever=vector_store.as_retriever(),
        return_source_documents=False,
        # verbose=True,
    )