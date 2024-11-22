import discord
import os
import datetime
import whisper
from lib.models import FileRegister, Message, User, Resume

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
        # Enregistrer le fichier audio complet pour chaque utilisateur
        file_path = os.path.join(temp_dir, f"{user_id}.wav")
        with open(file_path, "wb") as f:
            f.write(audio.file.read())

        # Transcrire l'audio avec Whisper
        result = model.transcribe(file_path, language="fr")
        
        # Ajouter les segments transcrits avec leurs horodatages
        for segment in result["segments"]:
            transcriptions.append({
                "user_id": user_id,
                "start": segment["start"],  # Début du segment (en secondes)
                "end": segment["end"],      # Fin du segment (en secondes)
                "text": segment["text"],    # Texte transcrit
            })

    # Trier les transcriptions par ordre chronologique
    transcriptions.sort(key=lambda x: x["start"])
    messages = []
    for segment in transcriptions:
        messages.append(Message(
            author_id=segment["user_id"],
            date=datetime.datetime.now(),
            duration=datetime.timedelta(seconds=segment["end"] - segment["start"]),
            content=segment["text"]
        ))
    users = []
    for user_id in sink.audio_data.keys():
        discord_tag = ctx.guild.get_member(user_id).name

        users.append(User(
            id=user_id,
            discord_tag="",
            avatar="",
            public_flags=0,
            global_name="",
            flags=0,
            locale="",
            mfa_enabled=False
        ))
    
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
    await ctx.send(f"Transcription des interventions dans l'ordre chronologique :\n```\n{final_text}\n```")
    
    # Déconnecter le client vocal après l'envoi des transcriptions
    await ctx.voice_client.disconnect()

    # Creation des object pourl la base sqlite
    
