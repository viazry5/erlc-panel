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


from pydantic import BaseModel
from erlc import run_command, get_server_info, get_players, get_killlogs, get_staff, get_modcalls

class AnnounceBody(BaseModel):
    message: str

class PMBody(BaseModel):
    player: str   # Roblox username
    message: str

@app.post("/api/announce")
async def api_announce(body: AnnounceBody):
    # :h = server-wide announcement
    return await run_command(f":h {body.message}")

@app.post("/api/pm")
async def api_pm(body: PMBody):
    return await run_command(f":pm {body.player} {body.message}")

