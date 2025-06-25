import discord
from discord.ext import commands

intents = discord.Intents.default()  # Pas besoin d'intents spéciaux si le bot ne fait rien
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")

# Remplace "TON_TOKEN_ICI" par le token réel de ton bot
bot.run("ETHERYA")
