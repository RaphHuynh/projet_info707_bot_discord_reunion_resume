import discord
import sqlite3
import os
from discord import slash_command
from discord.utils import basic_autocomplete
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
    name="generate_all_pdf",
    description="Generate resume and all message in a PDF of a specific meeting by title."
)
async def generate_all_pdf_command(
    ctx,
    title: discord.Option(str, "Title of the meeting", autocomplete=basic_autocomplete(autocomplete_titles))
):
    user_id = ctx.author.id
    
    try:
        sqlite_connection = sqlite3.connect("../app/db.sqlite3")
        resume = fetch_resume_by_title(sqlite_connection, user_id, title)
        messages = fetch_messages_by_resume_title(sqlite_connection, title)
        
        if not messages:
            await ctx.respond("No meeting message found with the provided title.")
            return
        
        if not resume: 
            await ctx.respond("No meeting resume found with the provided title.")
            return
        
        output_file = f"meeting_{title}_{user_id}.pdf"
        generate_pdf_for_all(messages, resume, title, output_file)
        
        await ctx.respond(file=discord.File(output_file), ephemeral=True)
        os.remove(output_file)
    
    except Exception as e:
        await ctx.respond(f"An error occured; {str(e)}")
    finally:
        if sqlite_connection:
            sqlite_connection.close()
        