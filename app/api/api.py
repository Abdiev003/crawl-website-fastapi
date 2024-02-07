from fastapi import HTTPException
from copy import deepcopy
from bs4 import BeautifulSoup as Soup
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader

from app.types.url_input import UrlInput


def load_url(url_input: UrlInput):
    try:
        string_url = str(url_input.url)
        loader = RecursiveUrlLoader(
            url=string_url, max_depth=100, extractor=lambda x: Soup(x, "html.parser").text)
        docs = loader.load()

        updated_docs = []
        for doc in docs:
            doc_dict = doc.__dict__

            character_count = len(doc_dict.get('page_content', ''))
            doc_dict['character_count'] = character_count

            updated_docs.append(doc_dict)

        return updated_docs
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
