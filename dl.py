import requests
from bs4 import BeautifulSoup
import os

from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain


def directory_name(docspage):
    """Create a name for a directory to contain the documentation for the given docspage."""
    
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature="0.2",
    )
    prompt = PromptTemplate(
        input_variables=["docpage"],
        template="Create a name for a directory to contain the documentation for the {docpage} page. Respond only with the name of the directory. Ensure it is a valid windows directory name.",
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(docspage)


def download_docs(base_url):
    """Download the documentation from the given base URL."""
    r = requests.get(base_url)
    r.raise_for_status()

    subdir = directory_name(base_url)
    os.makedirs(os.path.join("docs", subdir), exist_ok=True)
    # Parse the HTML of the site
    soup = BeautifulSoup(r.text, 'html.parser')

    # Get all 'a' tags with 'href' containing '.html'
    links = [a['href'] for a in soup.select('a[href$=".html"]')]


    for link in links:
        # Make a request to each link
        r = requests.get(base_url + link)
        r.raise_for_status()

        # Save the HTML content as a .html file
        with open(os.path.join("docs", subdir, os.path.basename(link)), 'w', encoding='utf-8') as f:
            f.write(r.text)