import discord
import audioop
from discord.ext import commands, tasks
from discord import app_commands, Embed, ButtonStyle, ui
from discord.ui import Button, View, Select, Modal, TextInput, button
from discord.ui import Modal, TextInput, Button, View
from discord.utils import get
from discord import TextStyle
from functools import wraps
import os
from discord import app_commands, Interaction, TextChannel, Role
import io
import random
import asyncio
import time
import re
import subprocess
import sys
import math
import traceback
from keep_alive import keep_alive
from datetime import datetime, timedelta, timezone
from collections import defaultdict, deque
import pymongo
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
import psutil
import pytz
import platform
from discord.ui import Select, View
from typing import Optional
from discord import app_commands, Interaction, Embed, SelectOption
from discord.ui import View, Select
import uuid
from zoneinfo import ZoneInfo
# Matplotlib (à mettre AVANT plt)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from io import BytesIO
import matplotlib.ticker as ticker
import numpy as np

token = os.environ['ETHERYA']
VERIFICATION_CODE = os.environ['VERIFICATION_CODE']
intents = discord.Intents.all()
start_time = time.time()
client = discord.Client(intents=intents)
status_message = None  # Pour stocker le message envoyé

#Configuration du Bot:
# --- ID Owner Bot ---
ISEY_ID = 792755123587645461


def get_log_channel(guild, key):
    log_channel_id = log_channels.get(key)
    if log_channel_id:
        return guild.get_channel(log_channel_id)
    return None

# Fonction pour créer des embeds formatés
def create_embed(title, description, color=discord.Color.blue(), footer_text=""):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_footer(text=footer_text)
    return embed

# Connexion MongoDB
mongo_uri = os.getenv("MONGO_DB")  # URI de connexion à MongoDB
print("Mongo URI :", mongo_uri)  # Cela affichera l'URI de connexion (assure-toi de ne pas laisser cela en prod)
client = MongoClient(mongo_uri)
db = client['Cass-Eco2']

def load_guild_settings(guild_id):
    # Charger les données de la collection principale

    # Débogage : Afficher les données de setup
    print(f"Setup data for guild {guild_id}: {setup_data}")

    combined_data = {
    }

    return combined_data

# Fonction pour récupérer le préfixe depuis la base de données
async def get_prefix(bot, message):
    guild_data = collection.find_one({"guild_id": str(message.guild.id)})  # Récupère les données de la guilde
    return guild_data['prefix'] if guild_data and 'prefix' in guild_data else '+'

bot = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None)

# Dictionnaire pour stocker les paramètres de chaque serveur
GUILD_SETTINGS = {}

#------------------------------------------------------------------------- Code Protection:

# Événement quand le bot est prêt
@bot.event
async def on_ready():
    print(f"✅ Le bot {bot.user} est maintenant connecté ! (ID: {bot.user.id})")

    bot.add_view(InfoView())

    # Démarrer les tâches de fond
    bot.uptime = time.time()

    guild_count = len(bot.guilds)
    member_count = sum(guild.member_count for guild in bot.guilds)

    print(f"\n📊 **Statistiques du bot :**")
    print(f"➡️ **Serveurs** : {guild_count}")
    print(f"➡️ **Utilisateurs** : {member_count}")

    activity_types = [
        discord.Activity(type=discord.ActivityType.watching, name=f"{member_count} Membres"),
        discord.Activity(type=discord.ActivityType.streaming, name=f"{guild_count} Serveurs"),
        discord.Activity(type=discord.ActivityType.streaming, name="Project : Delta"),
    ]

    status_types = [discord.Status.online, discord.Status.idle, discord.Status.dnd]

    await bot.change_presence(
        activity=random.choice(activity_types),
        status=random.choice(status_types)
    )

    print(f"\n🎉 **{bot.user}** est maintenant connecté et affiche ses statistiques dynamiques avec succès !")
    print("📌 Commandes disponibles 😊")
    for command in bot.commands:
        print(f"- {command.name}")

    try:
        synced = await bot.tree.sync()
        print(f"✅ Commandes slash synchronisées : {[cmd.name for cmd in synced]}")
    except Exception as e:
        print(f"❌ Erreur de synchronisation des commandes slash : {e}")

    while True:
        for activity in activity_types:
            for status in status_types:
                await bot.change_presence(activity=activity, status=status)
                await asyncio.sleep(10)

        for guild in bot.guilds:
            GUILD_SETTINGS[guild.id] = load_guild_settings(guild.id)

@bot.event
async def on_error(event, *args, **kwargs):
    print(f"Une erreur s'est produite : {event}")
    embed = discord.Embed(
        title="❗ Erreur inattendue",
        description="Une erreur s'est produite lors de l'exécution de la commande. Veuillez réessayer plus tard.",
        color=discord.Color.red()
    )
    
    # Vérifie si args[0] est une Interaction
    if isinstance(args[0], discord.Interaction):
        await args[0].response.send_message(embed=embed)
    elif isinstance(args[0], discord.Message):
        # Si c'est un message, envoie l'embed dans le canal du message
        await args[0].channel.send(embed=embed)
    elif isinstance(args[0], discord.abc.GuildChannel):
        # Si c'est un canal de type GuildChannel, assure-toi que c'est un canal textuel
        if isinstance(args[0], discord.TextChannel):
            await args[0].send(embed=embed)
        else:
            # Si c'est un autre type de canal (comme un canal vocal), essaye de rediriger le message vers un canal textuel spécifique
            text_channel = discord.utils.get(args[0].guild.text_channels, name='ton-salon-textuel')
            if text_channel:
                await text_channel.send(embed=embed)
            else:
                print("Erreur : Aucun salon textuel trouvé pour envoyer l'embed.")
    else:
        print("Erreur : Le type de l'objet n'est pas pris en charge pour l'envoi du message.")


# Token pour démarrer le bot (à partir des secrets)
# Lancer le bot avec ton token depuis l'environnement  
keep_alive()
bot.run(token)
