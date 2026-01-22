import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DASHBOARD_URL = os.getenv("PUBLIC_DASHBOARD_URL", "http://localhost:5173")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"✅ Logged in as {bot.user} | Synced {len(synced)} commands")
    except Exception as e:
        print("❌ Sync error:", e)

@bot.tree.command(name="dashboard", description="Get the dashboard link")
async def dashboard_cmd(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📊 ERLC Dashboard",
        description=f"Open: {DASHBOARD_URL}",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

# Load cogs
bot.load_extension("cogs.erlc")

bot.run(TOKEN)
