from discord import slash_command
from .join_channel import join_specific_channel_command
from .play import play_on_channel_command
from datetime import datetime
from .bot_manager import bot_manager
import asyncio


@slash_command(
    name="schedule",
    description="Schedule a meeting",
)
async def schedule_command(ctx, channel_id, date: str, title: str):
    """
    Schedule a meeting in the future and start recording when the time comes

    Args:
        ctx: The context of the command
        channel_id: The channel where the meeting will take place
        date: The date and time of the meeting in the format YYYY-MM-DDTHH:MM:SS
        title: The title of the meeting

    Returns:
        None
    """
    if not ctx.author.guild_permissions.administrator:
        return await ctx.respond(
            "You must be an administrator to use this command", ephemeral=True
        )

    date = check_date(date)
    if date is None:
        return await ctx.respond(
            "invalid date format, use YYYY-MM-DDTHH:MM:SS", ephemeral=True
        )

    now = datetime.now()
    if date < now:
        return await ctx.respond("The date must be in the future", ephemeral=True)

    channel_id = check_channel_id(channel_id)
    if channel_id is None:
        return await ctx.respond("Invalid format for channel", ephemeral=True)

    channel = ctx.guild.get_channel(channel_id)
    if channel is None:
        return await ctx.respond("Channel not found", ephemeral=True)

    await ctx.respond(
        f"Meeting scheduled for {date} with title {title}", ephemeral=True
    )
    await asyncio.sleep((date - now).total_seconds())

    if not await join_specific_channel_command(ctx, channel):
        return

    if not await play_on_channel_command(ctx, channel, title):
        return

    await ctx.respond("Meeting started", ephemeral=True)


def check_date(date):
    try:
        return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")

    except ValueError:
        return None


def check_channel_id(channel_id):
    if channel_id.startswith("<#") and channel_id.endswith(">"):
        return int(channel_id[2:-1])
    elif channel_id.isdigit():
        return int(channel_id)
    else:
        return None
