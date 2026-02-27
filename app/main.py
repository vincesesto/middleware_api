from fastapi import FastAPI, HTTPException, Response
import httpx

app = FastAPI(title="MiddlewareNewZealand API")

XML_SOURCES = {
    "1": "https://raw.githubusercontent.com/MiddlewareNewZealand/evaluation-instructions/main/xml-api/1.xml",
    "2": "https://raw.githubusercontent.com/MiddlewareNewZealand/evaluation-instructions/main/xml-api/2.xml",
}

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/xml/{xml_id}")
async def mirror_xml(xml_id: str):
    """
    Mirror the upstream XML Response as-is
    """
    url = XML_SOURCES.get(xml_id)
    if not url:
        raise HTTPException(status_code=404, detail="XML source not found")

    timeout = httpx.Timeout(10.0, connect=5.0)

    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            resp = await client.get(url)
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Error fetching XML: {e!s}")

    if resp.status_code != 200:
        raise HTTPException(status_code=502, detail=f"Upstream returned {resp.status_code}")

    # Mirror the upstream response
    content_type = resp.headers.get("Content-Type", "application/xml")
    return Response(content=resp.content, media_type=content_type)
