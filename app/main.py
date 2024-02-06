from fastapi import FastAPI

from app.api import api
from app.types.url_input import UrlInput

app = FastAPI()


@app.post("/load-url")
def load_url(url_input: UrlInput):
    return api.load_url(url_input)
