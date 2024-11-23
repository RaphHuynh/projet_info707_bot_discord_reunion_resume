from discord import slash_command
from discord.sinks import WaveSink
from .bot_manager import bot_manager
from events.recording import handle_finished_recording


@slash_command(name="play", description="Start recording voice")
async def play_command(ctx, title:str):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.respond(
            "You must be an administrator to use this command", ephemeral=True
        )
    if ctx.author.voice is None:
        return await ctx.respond("You must be in a voice channel", ephemeral=True)
    if ctx.voice_client is None:
        return await ctx.respond("I'm not in a voice channel", ephemeral=True)
    if bot_manager.recording:
        return await ctx.respond("Already recording!", ephemeral=True)

    bot_manager.recording_sink = WaveSink()
    ctx.voice_client.start_recording(
        bot_manager.recording_sink,
        handle_finished_recording,
        ctx,
        title,
    )
    bot_manager.recording = True
    await ctx.respond("Started recording!", ephemeral=True)


async def play_on_channel_command(ctx, channel, title):
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond(
            "You must be an administrator to use this command", ephemeral=True
        )
        return False

    if ctx.voice_client is None:
        await ctx.respond("I'm not in a voice channel", ephemeral=True)
        return False

    if ctx.voice_client.channel != channel:
        await ctx.respond("I'm not in the correct voice channel", ephemeral=True)
        return False

    if bot_manager.recording:
        await ctx.respond("Already recording!", ephemeral=True)
        return False

    bot_manager.recording_sink = WaveSink()
    ctx.voice_client.start_recording(
        bot_manager.recording_sink,
        handle_finished_recording,
        ctx,
        title,
    )
    bot_manager.recording = True
    return True
