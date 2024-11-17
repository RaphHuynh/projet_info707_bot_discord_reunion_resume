from discord import slash_command
from .bot_manager import bot_manager

@slash_command(
    name="stop_recording",
    description="Stop recording voice in the current channel"
)
async def stop_recording_command(ctx):
    if ctx.voice_client is None:
        return await ctx.respond("I'm not connected to a voice channel", ephemeral=True)
    elif not bot_manager.recording:
        return await ctx.respond("I'm not currently recording", ephemeral=True)
    
    # Arrêter l'enregistrement si en cours
    if bot_manager.recording_sink:
        ctx.voice_client.stop_recording()  # Arrêt de l'enregistrement
        bot_manager.recording = False
        bot_manager.recording_sink = None  # Réinitialiser le WaveSink
        await ctx.respond("Stopped recording!", ephemeral=True)
    else:
        await ctx.respond("No active recording to stop.", ephemeral=True)
