import os
import datetime
import whisper
from lib.models import Message, User, Resume
import sqlite3


async def handle_finished_recording(sink, ctx):
    if len(sink.audio_data) == 0:
        await ctx.send("Aucune donnée audio enregistrée.")
        await ctx.voice_client.disconnect()
        return

    await ctx.respond(
        "Fin de l'enregistrement, transcription en cours...", ephemeral=True
    )
    await ctx.voice_client.disconnect()

    transcriptions = transcribe_audio(sink)
    messages = messages_from_transcriptions(transcriptions)
    attendees = users_from_audio_data(ctx, sink.audio_data)
    author = member_to_user(ctx.guild.get_member(ctx.author.id))

    resume = Resume(
        date=messages[0].date,
        duration=messages[-1].date - messages[0].date,
        messages=messages,
        attendees=attendees,
        title="Réunion",
        text_sum_up="Réunion de test",
        admin=author,
    )

    answer = formated_transcription(ctx, transcriptions)
    await ctx.send(
        f"Transcription des interventions dans l'ordre chronologique :\n```\n{answer}\n```"
    )

    save_to_db(resume)


def transcribe_audio(sink):
    temp_dir = "./temp_audio_files"
    os.makedirs(temp_dir, exist_ok=True)

    model = whisper.load_model("large-v3-turbo")

    transcriptions = []

    for user_id, audio in sink.audio_data.items():
        file_path = os.path.join(temp_dir, f"{user_id}.wav")
        with open(file_path, "wb") as f:
            f.write(audio.file.read())

        result = model.transcribe(file_path, language="fr")

        for segment in result["segments"]:
            transcriptions.append(
                {
                    "user_id": user_id,
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"],
                }
            )

    transcriptions.sort(key=lambda x: x["start"])
    return transcriptions


def messages_from_transcriptions(transcriptions):
    messages = []
    for segment in transcriptions:
        messages.append(
            Message(
                author_id=segment["user_id"],
                date=datetime.datetime.now(),
                duration=datetime.timedelta(seconds=segment["end"] - segment["start"]),
                content=segment["text"],
            )
        )
    messages.sort(key=lambda x: x.date)
    return messages


def member_to_user(member):
    if member:
        avatar = str(member.avatar).split("/")[-1].split(".png")[0]
        user = User(
            id=member.id,
            discord_tag=member.discriminator,
            avatar=avatar,
            global_name=member.global_name,
        )
    else:
        user = User(
            id=member.id,
            discord_tag="unknown",
            avatar="unknown",
            global_name="unknown",
        )
    return user


def users_from_audio_data(ctx, audio_data):
    users = []
    for user_id in audio_data.keys():
        member = ctx.guild.get_member(user_id)
        user = member_to_user(member)
        users.append(user)
    return users


def formated_transcription(ctx, transcriptions):
    transcription_text = []
    for idx, segment in enumerate(transcriptions, start=1):
        user = ctx.guild.get_member(segment["user_id"])
        if user:
            user_name = user.name
        else:
            user_name = f"Utilisateur {segment['user_id']}"

        transcription_text.append(
            f"{idx}. [{user_name}] ({segment['start']:.2f}-{segment['end']:.2f}s): {segment['text']}"
        )

    return "\n".join(transcription_text)


def save_users_to_db(sqlite_connection, users):
    users_id = []
    for user in users:
        user_exist = sqlite_connection.execute(
            f"SELECT * FROM discord_login_discorduser WHERE id = {user.id}"
        ).fetchone()
        if user_exist:
            continue
        print(f"Saving user {user.global_name}")
        sqlite_connection.execute(
            f"INSERT INTO discord_login_discorduser (id, discord_tag, avatar, global_name) VALUES ({user.id}, '{user.discord_tag}', '{user.avatar}', '{user.global_name.replace("'", "''")}')"
        )
        users_id.append(user.id)

    return users_id


def save_messages_to_db(sqlite_connection, messages):
    messages_id = []
    for message in messages:
        value = sqlite_connection.execute(
            f"INSERT INTO meeting_app_message (author_id, date, duration, content) VALUES ({message.author_id}, '{message.date}', '{message.duration}', '{message.content.replace("'", "''")}')"
        )
        messages_id.append(value.lastrowid)
    return messages_id


def save_resume_to_db(sqlite_connection, resume):
    value = sqlite_connection.execute(
        f"INSERT INTO meeting_app_resume (title, date, duration, text_sum_up, admin_id) VALUES ('{resume.title.replace("'", "''")}', '{resume.date}', '{resume.duration}', '{resume.text_sum_up.replace("'", "''")}', {resume.admin.id})"
    )
    return value.lastrowid


def save_resume_messages_to_db(sqlite_connection, resume_id, messages_id):
    for message_id in messages_id:
        sqlite_connection.execute(
            f"INSERT INTO meeting_app_resume_messages (resume_id, message_id) VALUES ({resume_id}, {message_id})"
        )


def save_resume_attendees_to_db(sqlite_connection, resume_id, attendees_id):
    for user_id in attendees_id:
        sqlite_connection.execute(
            f"INSERT INTO meeting_app_resume_attendees (resume_id, discorduser_id) VALUES ({resume_id}, {user_id})"
        )


def save_to_db(resume):
    attendees = resume.attendees
    messages = resume.messages

    sqlite_connection = sqlite3.connect("../app/db.sqlite3")

    save_users_to_db(sqlite_connection, attendees + [resume.admin])

    messages_id = save_messages_to_db(sqlite_connection, messages)
    resume_id = save_resume_to_db(sqlite_connection, resume)

    save_resume_messages_to_db(sqlite_connection, resume_id, messages_id)
    save_resume_attendees_to_db(
        sqlite_connection, resume_id, [user.id for user in attendees]
    )

    sqlite_connection.commit()
