from discord import slash_command
from discord.sinks import WaveSink
from .bot_manager import bot_manager
from events.recording import handle_finished_recording

@slash_command(
    name="play",
    description="Start recording voice"
)
async def play_command(ctx):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.respond("You must be an administrator to use this command", ephemeral=True)
    elif ctx.author.voice is None:
        return await ctx.respond("You must be in a voice channel", ephemeral=True)
    elif ctx.voice_client is None:
        return await ctx.respond("I'm not in a voice channel", ephemeral=True)
    elif bot_manager.recording:
        return await ctx.respond("Already recording!", ephemeral=True)
    else:
        bot_manager.recording_sink = WaveSink()  # Utilisez bot_manager pour stocker le WaveSink
        ctx.voice_client.start_recording(
            bot_manager.recording_sink,  # Enregistrement sur l'instance de WaveSink du bot_manager
            handle_finished_recording,    # Fonction de callback
            ctx
        )
        bot_manager.recording = True
        await ctx.respond("Started recording!", ephemeral=True)

