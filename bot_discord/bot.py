import discord
from config import TOKEN, ID_SERVEUR
from commands import register_commands
from events import register_events

bot = discord.Bot(debug_guilds=ID_SERVEUR)

# Charger les événements
register_events(bot)

# Charger les commandes
register_commands(bot)

# Lancer le bot
bot.run(TOKEN)