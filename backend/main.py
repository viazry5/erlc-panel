import os
from dotenv import load_dotenv

load_dotenv()  # ✅ LOAD .env FIRST

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from erlc import get_server_info, get_players, get_killlogs



load_dotenv()

APP_URL = os.getenv("APP_URL", "http://localhost:5173")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[APP_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/server")
async def api_server():
    return await get_server_info()

@app.get("/api/players")
async def api_players():
    return await get_players()

@app.get("/api/kills")
async def api_kills():
    return await get_killlogs()

@app.get("/debug-key")
async def debug_key():
    import os
    k = os.getenv("ERLC_API_KEY", "")
    return {"has_key": bool(k), "len": len(k), "last4": k[-4:] if k else ""}




