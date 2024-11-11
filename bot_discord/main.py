from config import *
import discord
from lib import *
from discord.sinks import WaveSink

bot = discord.Bot(debug_guilds=[ID_SERVEUR])
recording = False  # Variable pour suivre l'état d'enregistrement

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
    elif ctx.author.voice is None:
        return await ctx.respond("You must be in a voice channel", ephemeral=True)
    elif ctx.voice_client is not None:
        return await ctx.respond("I'm already in a voice channel", ephemeral=True)
    else:
        await ctx.author.voice.channel.connect()
        await ctx.respond("I'm in the voice channel", ephemeral=True)
    
@bot.slash_command(
    name="leave_channel",
    description="Leave the voice channel"
)
async def leave_channel(ctx):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.respond("You must be an administrator to use this command", ephemeral=True)
    elif ctx.author.voice is None:
        return await ctx.respond("You must be in a voice channel", ephemeral=True)
    elif ctx.voice_client is None:
        return await ctx.respond("I'm already disconnected", ephemeral=True)
    else:
        await ctx.voice_client.disconnect()
        await ctx.respond("I'm disconnected", ephemeral=True)

@bot.slash_command(
    name="play",
    description="Start recording voice"
)
async def play(ctx):
    global recording
    if not ctx.author.guild_permissions.administrator:
        return await ctx.respond("You must be an administrator to use this command", ephemeral=True)
    elif ctx.author.voice is None:
        return await ctx.respond("You must be in a voice channel", ephemeral=True)
    elif ctx.voice_client is None:
        return await ctx.respond("I'm not in a voice channel", ephemeral=True)
    elif recording:
        return await ctx.respond("Already recording!", ephemeral=True)
    else:
        ctx.voice_client.start_recording(
            WaveSink(),  
            finished_callback,  
            ctx
        )
        recording = True
        await ctx.respond("Started recording!", ephemeral=True)

async def finished_callback(sink, ctx):
    global recording
    files = [discord.File(audio.file, f"{user_id}.wav") for user_id, audio in sink.audio_data.items()]
    await ctx.send("Here are the recorded audio files:", files=files)
    await ctx.voice_client.disconnect()
    recording = False

@bot.slash_command(
    name="stop_recording",
    description="Stop recording voice in the current channel"
)
async def stop_recording(ctx):
    global recording
    if ctx.voice_client is None:
        return await ctx.respond("I'm not connected to a voice channel", ephemeral=True)
    elif not recording:
        return await ctx.respond("I'm not currently recording", ephemeral=True)
    
    # Arrête l'enregistrement si en cours
    ctx.voice_client.stop_recording()
    recording = False
    await ctx.respond("Stopped recording", ephemeral=True)

bot.run(TOKEN)
