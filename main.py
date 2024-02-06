from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import logging
from bs4 import BeautifulSoup as Soup
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
import uvicorn

class UrlInput(BaseModel):
    url: HttpUrl

app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/load-url/")
async def load_url(url_input: UrlInput):
    try:
        string_url = str(url_input.url)
        loader = RecursiveUrlLoader(
            url=string_url, max_depth=100, extractor=lambda x: Soup(x, "html.parser").text)
        docs = loader.load()
        return docs
    except Exception as e:
        logger.error(f"Error loading URL: {e}")
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    port = 8080
    uvicorn.run(app, host="0.0.0.0", port=port)
