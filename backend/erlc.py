import os, httpx

ERLC_BASE = "https://api.policeroleplay.community/v1"
ERLC_KEY = os.getenv("ERLC_API_KEY", "").strip()

def _headers():
    return {
        "Server-Key": ERLC_KEY,
        "User-Agent": "ERLC-Dashboard"
    }

async def _get(path: str):
    timeout = httpx.Timeout(10.0, connect=10.0)
    url = f"{ERLC_BASE}{path}"
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.get(url, headers=_headers())
        print("REQUEST:", url)
        print("KEY last4:", ERLC_KEY[-4:])
        print("STATUS:", r.status_code)
        if r.status_code >= 400:
            print("BODY:", r.text)
        r.raise_for_status()
        return r.json()

async def get_server_info():
    return await _get("/server")

async def get_players():
    return await _get("/server/players")

async def get_killlogs():
    return await _get("/server/killlogs")

