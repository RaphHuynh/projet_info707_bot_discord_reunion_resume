from discord import slash_command
from .bot_manager import bot_manager


@slash_command(
    name="stop_recording", description="Stop recording voice in the current channel"
)
async def stop_recording_command(ctx):
    if ctx.voice_client is None:
        return await ctx.respond("I'm not connected to a voice channel", ephemeral=True)
    if not bot_manager.recording:
        return await ctx.respond("I'm not currently recording", ephemeral=True)

    if not bot_manager.recording_sink:
        return await ctx.respond("No active recording to stop.", ephemeral=True)

    await ctx.respond("Recording stopped", ephemeral=True)
    ctx.voice_client.stop_recording()
    bot_manager.recording = False
    bot_manager.recording_sink = None