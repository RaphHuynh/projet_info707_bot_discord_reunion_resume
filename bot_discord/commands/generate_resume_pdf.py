import discord
import os
from discord import slash_command
from discord.utils import basic_autocomplete
import sqlite3
from lib import *

async def autocomplete_titles(ctx):
    try:
        sqlite_connection = sqlite3.connect("../app/db.sqlite3")
        user_id = ctx.interaction.user.id
        titles = fetch_titles_by_user(sqlite_connection, user_id)
        sqlite_connection.close()

        user_input = ctx.options['title']
        suggestions = [title for title in titles if user_input.lower() in title.lower()]
        return suggestions
    except Exception as e:
        return []

@slash_command(
    name="generate_resume_pdf",
    description="Generate a PDF with resume of a specific meeting summary by title."
)
async def generate_resume_pdf_command(
    ctx,
    title: discord.Option(str, "Title of the meeting", autocomplete=basic_autocomplete(autocomplete_titles))
):
    user_id = ctx.author.id  # Récupérer l'ID Discord de l'utilisateur qui invoque la commande

    try:
        sqlite_connection = sqlite3.connect("../app/db.sqlite3")
        resume = fetch_resume_by_title(sqlite_connection, user_id, title)

        if not resume:
            await ctx.respond("No meeting summary found with the provided title.")
            return

        # Générer le fichier PDF
        output_file = f"meeting_summary_{user_id}_{resume['id']}.pdf"
        generate_pdf_for_resume(resume, output_file)

        # Envoyer le fichier PDF en réponse
        await ctx.respond(file=discord.File(output_file), ephemeral=True)
        os.remove(output_file)

    except Exception as e:
        await ctx.respond(f"An error occurred: {str(e)}")
    finally:
        if sqlite_connection:
            sqlite_connection.close()
