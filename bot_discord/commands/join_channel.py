from discord import slash_command


@slash_command(name="join_channel", description="Join the voice channel where you are")
async def join_channel_command(ctx):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.respond(
            "You must be an administrator to use this command", ephemeral=True
        )
    elif ctx.author.voice is None:
        return await ctx.respond("You must be in a voice channel", ephemeral=True)
    elif ctx.voice_client is not None:
        return await ctx.respond("I'm already in a voice channel", ephemeral=True)
    else:
        await ctx.author.voice.channel.connect()
        await ctx.respond("I'm in the voice channel", ephemeral=True)


async def join_specific_channel_command(ctx, channel):
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond(
            "You must be an administrator to use this command", ephemeral=True
        )
        return False
    elif ctx.voice_client is not None:
        await ctx.respond("I'm already in a voice channel", ephemeral=True)
        return False
    else:
        await channel.connect()
        await ctx.respond("I'm in the voice channel", ephemeral=True)
        return True
