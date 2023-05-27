# Archivist

Archivist is a powerful documentation parsing tool that helps you store and interact with any web-hosted documentation in a local Chroma vector database. Built on LangChain and Streamlit, Archivist allows you to chat with a ChatGPT-like assistant that can search through your documentation to help answer your specific questions.

## Features
- Parse and store documentation from any web source.
- Generate embeddings for efficient and accurate search.
- A conversational assistant interface for querying the documentation.
- Simple and user-friendly web app interface.

## Installation

Before you get started, ensure that you have Python installed on your machine.

Here are the steps to install Archivist:

1. Clone this repository:
    ```shell
    git clone https://github.com/gorto/Archivist.git
    cd archivist
    ```

2. Install the necessary Python packages:
    ```shell
    pip install streamlit langchain chromadb
    ```

## Usage

1. Start the app using the following command:
    ```shell
    streamlit run main.py
    ```

2. Paste the URL of the documentation you want to parse into the text box in the sidebar. This will download the documentation locally.

3. Once the pages are downloaded, you can choose to ingest them and create the embeddings in the local vector database.

4. After the documentation has been ingested, you can select the scope in the main dropdown and start chatting with the assistant.

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and make changes as you'd like. If you have any questions or need further guidance, feel free to open an issue.
