from lib.models import Resume
from .tools import (
    save_to_db,
    formated_transcription,
    users_from_audio_data,
    transcribe_audio,
    messages_from_transcriptions,
    member_to_user,
    summarize,
    messages_to_text,
)


async def handle_finished_recording(sink, ctx, title):
    if len(sink.audio_data) == 0:
        await ctx.send("No audio data recorded")
        await ctx.voice_client.disconnect()
        return

    await ctx.respond("I will now disconnect and transcribe the audio", ephemeral=True)
    await ctx.voice_client.disconnect()

    transcriptions = transcribe_audio(sink)
    messages = messages_from_transcriptions(transcriptions)
    attendees = users_from_audio_data(ctx, sink.audio_data)
    author = member_to_user(ctx.guild.get_member(ctx.author.id))
    answers = formated_transcription(ctx, transcriptions)
    sum_up = summarize(messages_to_text(messages, attendees))
    
    resume = Resume(
        date=messages[0].date,
        duration=(messages[-1].date - messages[0].date).total_seconds(),
        messages=messages,
        attendees=attendees,
        title=title,
        text_sum_up=sum_up,
        admin=author,
    )

    answers = formated_transcription(ctx, transcriptions)
    await ctx.send("Transcription of the meeting:")
    text = ""
    for answer in answers:
        if len(text) + len(answer) < 1900:
            text += answer + "\n"
        else:
            await ctx.send(f"```{text}```")
            text = answer + "\n"
    await ctx.send(f"```{text}```")

    await ctx.send("Summary of the meeting:")
    await ctx.send(f"```{sum_up}```")
    save_to_db(resume)
