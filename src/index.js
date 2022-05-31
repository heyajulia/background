addEventListener("fetch", (event) => {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  let image = await KV.get("image", {
    type: "arrayBuffer",
  });

  if (image) {
    return new Response(image, {
      headers: { "Content-Type": "image/jpeg" },
    });
  }

  const BING_HOSTNAME = "https://www.bing.com";
  const IMAGE_ARCHIVE_URL = `${BING_HOSTNAME}/HPImageArchive.aspx?format=js&idx=0&n=1`;

  const imageArchive = await fetch(IMAGE_ARCHIVE_URL);
  const imageArchiveJson = await imageArchive.json();
  const imageUrl = `${BING_HOSTNAME}/${imageArchiveJson.images[0].url}`;
  image = await fetch(imageUrl);

  const buf = await image.arrayBuffer();

  await KV.put("image", buf, {
    expirationTtl: 60 * 60 * 24,
  });

  return new Response(buf, {
    headers: { "Content-Type": "image/jpeg" },
  });
}
