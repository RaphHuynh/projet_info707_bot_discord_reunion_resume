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
    await ctx.respond(embed=embed, ephemeral=True)
    
@bot.slash_command(
    name="join_channel",
    description="Join the voice channel where you are"
)
async def join_channel(ctx):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.respond("You must be an administrator to use this command", ephemeral=True)
    else :
        if ctx.author.voice is None:
            return await ctx.respond("You must be in a voice channel", ephemeral=True)
        elif ctx.voice_client is not None:
            return await ctx.respond("I'm already in a voice channel", ephemeral=True)
        else :
            await ctx.author.voice.channel.connect()
            await ctx.respond("I'm in the voice channel", ephemeral=True)
    
@bot.slash_command(
    name="leave_channel",
    description="Leave the voice channel"
)
async def leave_channel(ctx):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.respond("You must be an administrator to use this command", ephemeral=True)
    else :
        if ctx.author.voice is None:
            return await ctx.respond("You must be in a voice channel", ephemeral=True)
        elif ctx.voice_client is None:
            return await ctx.respond("I'm already disconnected", ephemeral=True)
        else :
            await ctx.voice_client.disconnect()
            await ctx.respond("I'm disconnected", ephemeral=True)
    
    
bot.run(TOKEN)