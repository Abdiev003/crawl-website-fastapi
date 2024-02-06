from fastapi import HTTPException

from bs4 import BeautifulSoup as Soup
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader

from app.types.url_input import UrlInput


def load_url(url_input: UrlInput):
    try:
        string_url = str(url_input.url)
        loader = RecursiveUrlLoader(
            url=string_url, max_depth=100, extractor=lambda x: Soup(x, "html.parser").text)
        docs = loader.load()
        return docs
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
