from fastapi import HTTPException
from bs4 import BeautifulSoup as Soup
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader

from app.types.url_input import UrlInput

link_count = 0
stop_loading = False
stop_max_links = 10
stop_max_characters = 400000


def custom_extractor(html_content):
    global link_count
    global stop_loading
    global stop_max_links
    global stop_max_characters

    # XML dosyası kontrolü
    if html_content.strip().startswith('<?xml'):
        return None

    soup = Soup(html_content, "html.parser")

    if link_count == stop_max_links or len(soup.text) > stop_max_characters:
        stop_loading = True

    if stop_loading:
        return None

    link_count = link_count + 1

    return soup.text


def load_url(url_input: UrlInput):
    global stop_max_links
    global stop_max_characters

    if url_input.is_free:
        stop_max_links = 2
        stop_max_characters = 400000
    else:
        stop_max_links = float('inf')
        stop_max_characters = 11000000

    exclude_dirs = (f'{url_input.url}wp-content/', f'{url_input.url}wp-includes/',
                    f'{url_input.url}wp-json/', f'{url_input.url}comments/', f'{url_input.url}category/', f'{url_input.url}feed/')

    try:
        string_url = str(url_input.url)
        loader = RecursiveUrlLoader(
            url=string_url, max_depth=8, prevent_outside=True, use_async=True, extractor=custom_extractor,
            timeout=60, check_response_status=True, exclude_dirs=exclude_dirs
        )
        docs = loader.lazy_load()

        updated_docs = []
        total_character_count = 0

        for doc in docs:
            doc_dict = doc.__dict__

            doc_dict['page_content'] = doc_dict.get(
                'page_content', '').replace('\n', '').replace('\r', '')

            character_count = len(doc_dict.get('page_content', ''))
            total_character_count += character_count

            doc_dict['character_count'] = character_count

            updated_docs.append(doc_dict)

        print(f"Total links: {link_count}")
        return updated_docs
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
