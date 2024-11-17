from discord import slash_command
from lib import embed_help

@slash_command(
    name="help",
    description="All commands of the bot"
)
async def help_command(ctx):
    embed = embed_help(ctx)
    await ctx.respond(embed=embed, ephemeral=True)