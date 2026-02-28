from fastapi import FastAPI
from fastapi.responses import JSONResponse
import xmltodict
import httpx

app = FastAPI(title="MiddlewareNewZealand API")

XML_SOURCES = {
    1: "https://raw.githubusercontent.com/MiddlewareNewZealand/evaluation-instructions/main/xml-api/1.xml",
    2: "https://raw.githubusercontent.com/MiddlewareNewZealand/evaluation-instructions/main/xml-api/2.xml",
}

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/v1/companies/{xml_id}")
async def get_company(xml_id: int):
    """
    Fetch the XML data from the specified URL based on the provided XML ID, convert it to JSON, and return it
    """
    url = XML_SOURCES.get(xml_id)
    if not url:
        return JSONResponse(content={"error": "not_found", "error_description": "Not found"}, status_code=404)

    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            resp = await client.get(url)
    except httpx.RequestError as e:
        return JSONResponse(content={"error": "fetch_error", "error_description": str(e)}, status_code=500)

    if resp.status_code != 200:
        return JSONResponse(content={"error": "fetch_error", "error_description": f"Failed to fetch XML data from {url}"}, status_code=500)

    try:
        parsed = xmltodict.parse(resp.content)
        data = parsed.get("Data") or {}

        # Return the JSON shape you want
        return {
            "id": int(data.get("id")),
            "name": data.get("name"),
            "description": data.get("description"),
        }
    except Exception as e:
        return JSONResponse(content={"error": "invalid_xml", "error_description": f"Failed to parse upstream XML: {e!s}"}, status_code=400)
