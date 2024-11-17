from discord import slash_command

@slash_command(
    name="leave_channel",
    description="Leave the voice channel where I am"
)
async def leave_channel_command(ctx):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.respond("You must be an administrator to use this command", ephemeral=True)
    elif ctx.author.voice is None:
        return await ctx.respond("You must be in a voice channel", ephemeral=True)
    elif ctx.voice_client is None:
        return await ctx.respond("I'm already disconnected", ephemeral=True)
    else:
        await ctx.voice_client.disconnect()
        await ctx.respond("I'm disconnected", ephemeral=True)