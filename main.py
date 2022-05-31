import os
from urllib.parse import urljoin as join_url

import httpx
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

MARKET = os.environ.get("MARKET", "en-US")
BING_HOSTNAME = "https://www.bing.com"
IMAGE_ARCHIVE_URL = join_url(
    BING_HOSTNAME, f"/HPImageArchive.aspx?format=js&idx=0&n=1&mkt={MARKET}"
)


app = FastAPI()


@app.get("/")
async def root(response_class=RedirectResponse):
    with httpx.AsyncClient() as client:
        response = await client.get(IMAGE_ARCHIVE_URL)
        data = response.json()
        image_url = data["images"][0]["url"]

        return join_url(BING_HOSTNAME, image_url)
