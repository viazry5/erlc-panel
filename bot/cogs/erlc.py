import os
import httpx
import discord
from discord.ext import commands

ERLC_API_KEY = os.getenv("ERLC_API_KEY")
ERLC_BASE = "https://api.policeroleplay.community/v1"

def headers():
    return {"Server-Key": ERLC_API_KEY}

class ERLC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    erlc = discord.app_commands.Group(name="erlc", description="ERLC commands")

    @erlc.command(name="info", description="Get ERLC server info")
    async def info(self, interaction: discord.Interaction):
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{ERLC_BASE}/server", headers=headers())
            r.raise_for_status()
            data = r.json()

        embed = discord.Embed(title="🚓 ERLC Server Info")
        for k, v in data.items():
            embed.add_field(name=k, value=str(v), inline=True)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(ERLC(bot))
