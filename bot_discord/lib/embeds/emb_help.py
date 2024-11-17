import discord

def embed_help(ctx):
    embed = discord.Embed(
        title="Help",
        color=discord.Colour.random()
    )
    embed.add_field(name="/help", value="Show all commands of the bot", inline=False)
    embed.add_field(name="/join_channel", value="join the voice channel where you are", inline=False)
    embed.add_field(name="/leave_channel", value="leave the voice channel", inline=False)
    embed.add_field(name="/play", value="start recording voice", inline=False)
    embed.add_field(name="/stop", value="stop recording voice", inline=False)
    embed.add_field(name="/generate_resume", value="generates a summary of the last meeting", inline=False)
    embed.set_author(name=ctx.author.name)
    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/256/7498/7498864.png")
    embed.set_footer(text="By MeetBotResume")

    return embed