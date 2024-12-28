import discord
import sqlite3
import os
from discord import slash_command
from lib import *

@slash_command(
    name="generate_message_pdf",
    description="Generate all message in a PDF of a specific meeting summary by title."
)
async def generate_message_pdf_command(
    ctx,
    title: str
):
    user_id = ctx.author.id
    
    try:
        sqlite_connection = sqlite3.connect("../app/db.sqlite3")
        messages = fetch_messages_by_resume_title(sqlite_connection, title)
        
        if not messages:
            await ctx.respond("No meeting message found with the provided title.")
            return
        
        output_file = f"meeting_message_{user_id}.pdf"
        generate_pdf_for_message(messages, title,output_file)
        
        await ctx.respond(file=discord.File(output_file))
        os.remove(output_file)
        
        
    except Exception as e:
        await ctx.respond(f"An error occured; {str(e)}")
    finally:
        if sqlite_connection:
            sqlite_connection.close()