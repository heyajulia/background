import os
import time
from urllib.parse import urljoin as join_url

import httpx
from fastapi import FastAPI
from fastapi.responses import FileResponse

MARKET = os.environ.get("MARKET", "en-US")
BING_HOSTNAME = "https://www.bing.com"
IMAGE_ARCHIVE_URL = join_url(
    BING_HOSTNAME, f"/HPImageArchive.aspx?format=js&idx=0&n=1&mkt={MARKET}"
)


app = FastAPI()


@app.get("/")
async def root():
    try:
        with open("/data/last-updated") as f:
            last_updated = float(f.read())
    except FileNotFoundError:
        last_updated = 0

    if time.time() - last_updated > 86_400:
        async with httpx.AsyncClient() as client:
            response = await client.get(IMAGE_ARCHIVE_URL)
            data = response.json()
            image = await client.get(join_url(BING_HOSTNAME, data["images"][0]["url"]))

            with open("/data/image.jpg", "wb+") as f:
                f.write(image.content)

            with open("/data/last-updated", "w") as f:
                f.write(str(time.time()))

    return FileResponse("/data/image.jpg")
