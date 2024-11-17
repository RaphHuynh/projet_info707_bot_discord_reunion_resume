import discord
from discord.sinks import WaveSink

recording = False  # Variable globale pour suivre l'état d'enregistrement

async def handle_finished_recording(sink, ctx):
    global recording
    files = [discord.File(audio.file, f"{user_id}.wav") for user_id, audio in sink.audio_data.items()]
    await ctx.send("Here are the recorded audio files:", files=files)
    await ctx.voice_client.disconnect()
    recording = False