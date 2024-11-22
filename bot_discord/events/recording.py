import discord
import os
import datetime
import whisper
from lib.models import FileRegister, Message, User, Resume
import sqlite3


async def handle_finished_recording(sink, ctx):
    # Définir un répertoire temporaire pour stocker les fichiers audio
    temp_dir = "./temp_audio_files"
    os.makedirs(temp_dir, exist_ok=True)

    # Liste pour stocker les transcriptions avec horodatages
    transcriptions = []

    # Charger le modèle Whisper (choisissez un modèle adapté)
    model = whisper.load_model("large-v3-turbo")

    # Parcourir les fichiers audio de chaque utilisateur
    for user_id, audio in sink.audio_data.items():
        user = ctx.guild.get_member(user_id)
        # Enregistrer le fichier audio complet pour chaque utilisateur
        file_path = os.path.join(temp_dir, f"{user_id}.wav")
        with open(file_path, "wb") as f:
            f.write(audio.file.read())

        # Transcrire l'audio avec Whisper
        result = model.transcribe(file_path, language="fr")

        # Ajouter les segments transcrits avec leurs horodatages
        for segment in result["segments"]:
            transcriptions.append(
                {
                    "user_id": user_id,
                    "start": segment["start"],  # Début du segment (en secondes)
                    "end": segment["end"],  # Fin du segment (en secondes)
                    "text": segment["text"],  # Texte transcrit
                }
            )

    # Trier les transcriptions par ordre chronologique
    transcriptions.sort(key=lambda x: x["start"])
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

    users = []
    for user_id in sink.audio_data.keys():
        user = ctx.guild.get_member(user_id)
        if user:
            avatar = str(user.avatar).split("/")[-1].split(".png")[0]
            users.append(
                User(
                    id=user.id,
                    discord_tag=user.discriminator,
                    avatar=avatar,
                    global_name=user.global_name,
                )
            )
        else:
            users.append(
                User(
                    id=user.id,
                    discord_tag="unknown",
                    avatar="unknown",
                    global_name="unknown",
                )
            )
    # time for first and last message
    messages.sort(key=lambda x: x.date)
    resume_duration = messages[-1].date - messages[0].date
    resume = Resume(
        date=messages[0].date,
        duration=resume_duration,
        messages=messages,
        attendees=users,
        title="Réunion",
        text_sum_up="Réunion de test",
        admin=ctx.author.id,
    )

    # Construire le texte final basé sur l'ordre des interventions
    transcription_text = []
    for idx, segment in enumerate(transcriptions, start=1):
        # Récupérer l'utilisateur associé au segment
        user = ctx.guild.get_member(segment["user_id"])
        if user:
            user_name = user.name  # Nom d'utilisateur trouvé
        else:
            user_name = f"Utilisateur {segment['user_id']}"  # Identifiant générique si non trouvé

        transcription_text.append(
            f"{idx}. [{user_name}] ({segment['start']:.2f}-{segment['end']:.2f}s): {segment['text']}"
        )

    # Générer le texte combiné des transcriptions
    final_text = "\n".join(transcription_text)

    # Envoyer le texte transcrit dans le canal Discord
    await ctx.send(
        f"Transcription des interventions dans l'ordre chronologique :\n```\n{final_text}\n```"
    )

    # Déconnecter le client vocal après l'envoi des transcriptions
    await ctx.voice_client.disconnect()

    # Creation des object pourl la base sqlite
    sqlite_connection = sqlite3.connect("../app/db.sqlite3")
    for user in users:
        print(f"Saving user {user.global_name}")
        # check if user already exist
        user_exist = sqlite_connection.execute(
            f"SELECT * FROM discord_login_discorduser WHERE id = {user.id}"
        ).fetchone()
        if user_exist:
            continue
        sqlite_connection.execute(
            f"INSERT INTO discord_login_discorduser (id, discord_tag, avatar, global_name) VALUES ({user.id}, '{user.discord_tag}', '{user.avatar}', '{user.global_name.replace("'", "''")}')"
        )

    messages_id = []
    for message in messages:
        value = sqlite_connection.execute(
            f"INSERT INTO meeting_app_message (author_id, date, duration, content) VALUES ({message.author_id}, '{message.date}', '{message.duration}', '{message.content.replace("'", "''")}')"
        )
        messages_id.append(value.lastrowid)

    value = sqlite_connection.execute(
        f"INSERT INTO meeting_app_resume (title, date, duration, text_sum_up, admin_id) VALUES ('{resume.title.replace("'", "''")}', '{resume.date}', '{resume.duration}', '{resume.text_sum_up.replace("'", "''")}', {resume.admin})"
    )

    resume_id = value.lastrowid

    for message_id in messages_id:
        sqlite_connection.execute(
            f"INSERT INTO meeting_app_resume_messages (resume_id, message_id) VALUES ({resume_id}, {message_id})"
        )

    for user in users:
        sqlite_connection.execute(
            f"INSERT INTO meeting_app_resume_attendees (resume_id, discorduser_id) VALUES ({resume_id}, {user.id})"
        )

    sqlite_connection.commit()
