from config import *
import discord
from lib import *

bot = discord.Bot(debug_guilds=[ID_SERVEUR])

@bot.event
async def on_ready():
    print("Bot is ready")
    
@bot.slash_command(
    name="help",
    description="All commands of the bot"
)
async def help(ctx):
    embed = embed_help(ctx)
    await ctx.respond(embed=embed)
    
    
bot.run(TOKEN)