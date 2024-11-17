import discord
import os
import datetime
from pydub import AudioSegment, silence
from lib.models import FileRegister, Message

async def handle_finished_recording(sink, ctx):
    # Définir un répertoire temporaire pour stocker les fichiers audio
    temp_dir = "./temp_audio_files"
    os.makedirs(temp_dir, exist_ok=True)
    
    # Liste pour stocker les objets FileRegister
    files = []
    messages = []

    # Liste pour stocker l'ordre des messages basés sur les timestamps
    ordered_files = []

    # Compteur pour générer un id_message unique
    message_counter = 1

    # Liste pour garder la trace des utilisateurs qui parlent
    user_speaking_order = []

    # Enregistrer les fichiers audio et associer les timestamps
    for user_id, audio in sink.audio_data.items():
        # Enregistrer le fichier audio complet pour chaque utilisateur
        file_path = os.path.join(temp_dir, f"{user_id}.wav")
        with open(file_path, "wb") as f:
            f.write(audio.file.read())  # Sauvegarder le contenu de l'audio en tant que fichier

        # Charger le fichier audio avec pydub pour le traitement
        audio_file = AudioSegment.from_wav(file_path)

        # Détecter les périodes de silence (blancs) dans le fichier audio
        silence_chunks = silence.split_on_silence(
            audio_file, 
            min_silence_len=1000,  # Durée minimale du silence en millisecondes
            silence_thresh=-40  # Seuil de silence en dB (relatif au bruit ambiant)
        )

        # Découper l'audio en segments basés sur les silences
        for chunk in silence_chunks:
            # Créer un fichier pour chaque segment d'audio
            segment_path = os.path.join(temp_dir, f"{user_id}_{message_counter}.wav")
            chunk.export(segment_path, format="wav")

            # Créer l'objet FileRegister pour ce segment
            file_register = FileRegister(
                id=user_id,
                name=f"{user_id}_{message_counter}.wav",
                id_message=message_counter,  # Attribuer un id_message unique
                audio_file_path=segment_path,
                date=datetime.datetime.now()  # Timestamp du moment de l'enregistrement
            )
            
            # Ajouter à la liste des fichiers
            ordered_files.append(file_register)

            # Ajouter le fichier à la liste de fichiers pour Discord
            files.append(discord.File(segment_path, f"{user_id}_{message_counter}.wav"))

            # Enregistrer le message dans l'ordre des fichiers avec le nom de l'utilisateur
            user = ctx.guild.get_member(user_id)
            user_name = user.name if user else f"Utilisateur {user_id}"

            messages.append(Message(
                id=user_id,
                text=f"Message de {user_name} (ID: {user_id})",  # Inclure le nom de l'utilisateur
                numero_message=message_counter,  # Incrémenter l'index du message
                id_user=user_id  # Ajouter l'id_user ici si nécessaire
            ))

            # Garder la trace de l'ordre des utilisateurs
            user_speaking_order.append(user_id)

            # Incrémenter le compteur pour le prochain message
            message_counter += 1

    # Trier les fichiers en fonction de la date pour déterminer l'ordre de parole
    ordered_files.sort(key=lambda file: file.date)

    # Réorganiser les messages en fonction de l'ordre de parole
    ordered_messages = []
    for file in ordered_files:
        # Trouver le message correspondant à l'ID du fichier et ajouter dans l'ordre
        for msg in messages:
            if msg.id == file.id:
                ordered_messages.append(msg)

    # Générer le texte des messages dans l'ordre
    ordered_text = "\n".join([f"{msg.numero_message}: {msg.text}" for msg in ordered_messages])
    
    # Envoyer les fichiers et le texte dans l'ordre
    await ctx.send(f"Voici les messages enregistrés dans l'ordre des interventions :\n{ordered_text}", files=files)
    
    # Déconnecter le client vocal après l'envoi des fichiers
    await ctx.voice_client.disconnect()
